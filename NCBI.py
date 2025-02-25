# -*- coding: utf-8 -*-

from Bio import Entrez
import re

def lire_fichier(nom_fichier):

    resultats = []
    with open(nom_fichier, 'r') as f:
        for ligne in f:
            if ligne.strip():  # Ignore les lignes vides
                gene, organisme = ligne.strip().split(',')
                resultats.append((gene.strip(), organisme.strip()))
    return resultats

def extraire_description(gene_content, est_bacterie):
   
    description = "Description non disponible"
    
    # Chercher d'abord le format "Name:"
    for ligne in gene_content.split('\n'):
        if 'Name:' in ligne:
            description = ligne.split('Name:')[1].split('[')[0].strip()
            return description
    
    # Si pas trouvé, chercher le format "1. Gene\ndescription"
    lignes = gene_content.split('\n')
    for i, ligne in enumerate(lignes):
        if ligne.startswith('1.') and i + 1 < len(lignes):
            description = lignes[i + 1].split('[')[0].strip()
            return description
            
    return description

def espece_name(espece):
 
    espece_split = espece.split("_")
    if len(espece_split) > 2:
        return "_".join(espece_split[:2])
    else:
        return espece

def extraire_accessions_bacterie(gene_content, prot_content):
 
    gene_id = None
    # Extraire l'identifiant du gène à partir du contenu du gène
    for ligne in gene_content.split('\n'):
        if 'ID:' in ligne:
            gene_id = ligne.split('ID:')[1].strip()
            break

    # Motifs regex pour identifier les accession des transcrits et protéines
    transcript_pattern = re.compile(r'RefSeq:([A-Z]M_\S+)')
    protein_pattern = re.compile(r'RefSeq:([A-Z]P_\S+)')

    transcript = None
    protein = None

    # Extraire l'accession du transcrit
    for ligne in gene_content.split('\n'):
        match = transcript_pattern.search(ligne)
        if match:
            transcript = match.group(1)
            break

    # Extraire l'accession de la protéine
    for ligne in prot_content.split('\n'):
        match = protein_pattern.search(ligne)
        if match:
            protein = match.group(1)
            break

    return gene_id, transcript, protein

def extraire_accessions_eucaryote(handle):
   
    record = Entrez.read(handle)[0]
    gene_id = record['Entrezgene_track-info']['Gene-track']['Gene-track_geneid']
    rna_accs = []
    protein_accs = []

    # Motifs regex pour identifier les accession des ARN et protéines
    rna_pattern = re.compile(r'[A-Z]M_')
    protein_pattern = re.compile(r'[A-Z]P_')

    # Extraire les accession des ARN et protéines
    if 'Entrezgene_locus' in record:
        for product in record['Entrezgene_locus']:
            if 'Gene-commentary_products' in product:
                for p in product['Gene-commentary_products']:
                    acc = p.get('Gene-commentary_accession', '')
                    if rna_pattern.match(acc):
                        rna_accs.append(acc)
                    if 'Gene-commentary_products' in p:
                        for subp in p['Gene-commentary_products']:
                            acc = subp.get('Gene-commentary_accession', '')
                            if protein_pattern.match(acc):
                                protein_accs.append(acc)

    return gene_id, rna_accs, protein_accs

def obtenir_sequences(gene, organisme):
   
    organisme = espece_name(organisme)
    results = []  # Liste pour stocker tous les résultats
    
    Entrez.email = "mathieu.cartier@univ-rouen.fr"

    est_bacterie = False
    # Rechercher l'organisme dans la base de données taxonomique
    handle = Entrez.esearch(db="taxonomy", term=organisme)
    tax = Entrez.read(handle)
    if tax['IdList']:
        tax_info = Entrez.efetch(db="taxonomy", id=tax['IdList'][0], retmode="xml")
        est_bacterie = 'Bacteria' in Entrez.read(tax_info)[0]['Lineage']
        tax_info.close()
    handle.close()

    # Rechercher le gène dans la base de données des gènes
    gene_handle = Entrez.esearch(db="gene", term=f"{gene}[Gene Name] AND {organisme}[Organism]")
    gene_records = Entrez.read(gene_handle)
    gene_handle.close()

    if gene_records['IdList']:
        if est_bacterie:
            # Traitement pour les bactéries
            handle = Entrez.efetch(db="gene", id=gene_records['IdList'][0], rettype="gb", retmode="text")
            gene_content = handle.read()
            handle.close()

            prot_handle = Entrez.esearch(db="protein", term=f"{gene}[Gene Name] AND {organisme}[Organism]")
            prot_records = Entrez.read(prot_handle)
            prot_handle.close()

            if prot_records['IdList']:
                handle = Entrez.efetch(db="protein", id=prot_records['IdList'][0], rettype="gp", retmode="text")
                prot_content = handle.read()
                handle.close()
                gene_id, _, protein = extraire_accessions_bacterie(gene_content, prot_content)
                description = extraire_description(gene_content, est_bacterie)

                result = {
                    "Gene": gene,
                    "Gene ID": gene_id,
                    "Description": description,
                    "Transcrit": None,
                    "Protéine": protein if protein else None
                }
                results.append(result)
        else:
            # Traitement pour les eucaryotes
            handle = Entrez.efetch(db="gene", id=gene_records['IdList'][0], rettype="gb", retmode="text")
            gene_content = handle.read()
            description = extraire_description(gene_content, est_bacterie)
            handle.close()
            
            handle = Entrez.efetch(db="gene", id=gene_records['IdList'][0], retmode="xml")
            gene_id, transcrits, proteines = extraire_accessions_eucaryote(handle)
            handle.close()

            result = {
                "Gene": gene,
                "Gene ID": gene_id,
                "Description": description,
                "Transcrits": transcrits if transcrits else None,
                "Protéines": proteines if proteines else None
            }
            results.append(result)

    return results

if __name__ == "__main__":
    tous_resultats = {}  # Dictionnaire pour stocker tous les résultats
    genes_organismes = lire_fichier("GeneSymbol_NCBI.txt")
    for gene, organisme in genes_organismes:
        resultats = obtenir_sequences(gene, organisme)
        if resultats:  # Si des résultats ont été trouvés
            tous_resultats[gene] = resultats[0]  # Stocke le résultat avec le gène comme clé
    
    # Pour afficher tous les résultats
    for gene, resultat in tous_resultats.items():
        print(resultat)
            
            