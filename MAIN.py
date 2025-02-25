# -*- coding: utf-8 -*-
import json
from NCBI import obtenir_sequences
from Ensembl import isole_data
from Uniprot import get_uniprot_from_ncbi_detailed
from GO import get_go_terms
from INTERPRO import get_interpro_links
from html_report import report_html
import sys
def lire_et_formater_especes(chemin_fichier):
    """
    Lit un fichier contenant des espèces et leurs symboles, formate les noms d'espèces,
    et retourne un dictionnaire avec l'espèce formatée comme clé et le symbole comme valeur.
    Chaque ligne du fichier doit être au format "symbole,espece".
    """
    dico = {}

    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        for ligne in fichier:
            # Supprimer les espaces superflus
            ligne = ligne.strip()
            if not ligne:  # Ignorer les lignes vides
                continue
                
            # Séparer symbole et espèce
            if ',' not in ligne:
                print(f"Ligne mal formatée ignorée : {ligne}")
                continue

            symbole, esp = ligne.split(",", 1)
            symbole = symbole.strip()
            esp = esp.strip()

            # Si l'espèce n'a pas déjà des underscores, remplacer les espaces par des underscores
            if '_' not in esp:
                esp = esp.replace(" ", "_")
            
            # Mettre en minuscules
            esp = esp.lower()

            # Initialiser et remplir le dictionnaire
            if esp not in dico:
                dico[esp] = {}
            dico[esp]["Symbole"] = symbole

    return dico
def main():
    """
    Fonction principale pour lire les espèces, récupérer les données associées
    et les stocker dans un dictionnaire.
    """
    dico = lire_et_formater_especes("GeneSymbol.txt")
        
    for espece in dico.keys():
        symbole = dico[espece]['Symbole']  
        
        print(("-" * 80))
        print(f"\n{symbole} - {espece}:")
        
        # Requête Ensembl
        print("\n - Requete Ensembl ...")
        try: 
            Ensembl = isole_data(espece, symbole)
            dico[espece]['Ensembl'] = Ensembl
            print("   Request successful.")
        except Exception as e:
            print(f"   Request failed. {e}")
            dico[espece]['Ensembl'] = None
        
        # Requête NCBI
        print("\n - Requete NCBI ...")
        try:
            NCBI = obtenir_sequences(symbole, espece)
            if NCBI and isinstance(NCBI, list) and len(NCBI) > 0:
                NCBI = NCBI[0]  # Prendre le premier résultat
                dico[espece]['NCBI'] = NCBI
                gene_id = NCBI.get("Gene ID")
                print("   Request successful.")
            else:
                print("   No results found.")
                dico[espece]['NCBI'] = None
                gene_id = None
        except Exception as e:        
            print(f"   Request failed. {e}")
            dico[espece]['NCBI'] = None
            gene_id = None

        if gene_id:
            # Récupération de l'identifiant UniProt
            print("\n - Recupération identifiant UniProt ...")
            try:
                uniprot_id = get_uniprot_from_ncbi_detailed(gene_id)
                print("   Request successful.")
            except Exception as e:      
                print(f"   Request failed. {e}")
                uniprot_id = None
           
            if uniprot_id:  
                dico[espece]['Uniprot'] = uniprot_id
                
                # Obtenir les GO terms
                print("\n - Requete GO termes ...")
                try:
                    GO = get_go_terms(uniprot_id)
                    dico[espece]['GO_terms'] = GO
                    print("   Request successful.")
                except Exception as e:    
                    print(f"   Request failed. {e}")
                    dico[espece]['GO_terms'] = None         
              
                # Obtenir les liens InterPro
                print("\n - Requete interPro ...")
                try:
                    interpro_links = get_interpro_links(uniprot_id)
                    dico[espece]['interpro'] = interpro_links
                    print("   Request successful.")
                except Exception as e:    
                    print(f"   Request failed. {e}")
                    dico[espece]['interpro'] = None

            else:
                print(f"\nNo UniProt ID found for Gene {symbole}")
                dico[espece]['Uniprot'] = "Non trouvé"
                dico[espece]['GO_terms'] = None
                dico[espece]["interpro"] = None
      
    return dico

if __name__ == "__main__":
    # Vérifier si un fichier est fourni en argument
    if len(sys.argv) != 2:
        print("Usage: python MAIN.py chemin_fichier.txt")
        sys.exit(1)
        
    input_file = sys.argv[1]
    
    # Utiliser le fichier fourni en argument
    dico = lire_et_formater_especes(input_file)
    json_name = "resultat.json"
    html_name = "gene_raport.html"
    
    # Le reste du code reste identique
    dico = main()
    
    with open(json_name, "w") as json_file:
        json.dump(dico, json_file, indent=4)
    
    report_html(json_name, html_name)