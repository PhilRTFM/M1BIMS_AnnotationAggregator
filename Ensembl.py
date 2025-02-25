# -*- coding: utf-8 -*-
"""
Ce script lit un fichier de noms d'espèces et de symboles, interroge l'API Ensembl
pour récupérer des informations sur les gènes associés (transcripts, protéines, etc.)
puis génère un rapport HTML.
"""

import requests
import sys 


def requete_division(espece):
    """
    Récupère la division d'une espèce pour construire le lien HTML.

    """
    server = "https://rest.ensembl.org"
    url = f"{server}/info/genomes/{espece}?content-type=application/json"

    try:
        reponse = requests.get(url, headers={"Content-Type": "application/json"})
        reponse.raise_for_status()  
        data = reponse.json()
        division = data.get("division", None)
        # Vérifie qu'il y a un résultat dans division et qu'il commence bien par Ensembl
        if division and division.startswith("Ensembl"):
            # Retirer "Ensembl" du début pour avoir juste la partie "Vertebrates." par ex.
            return (division[len("Ensembl"):] + ".").strip()
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de la division pour {espece}: {e}")
        return None


def requete_data(espece, symbole):
    """
    Réalise pour une espèce et un symbole une recherche dans l'API Ensembl
    afin de récupérer les informations liées (Gene, Transcripts, etc.).
    """
    server = "https://rest.ensembl.org"
    ext = f"/lookup/symbol/{espece}/{symbole}?expand=1"
    url = server + ext

    try:
        r = requests.get(url, headers={"Content-Type": "application/json"})
        r.raise_for_status() 
        return r.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de données pour {espece}, {symbole}: {e}")
        return None


def isole_data(espece, symbole):
    """
    Isole les données depuis la requête API et les stocke dans un dictionnaire.
    """
    # Récupérer la division, utile pour la création de liens
    division = requete_division(espece)

    # Récupérer les données du gène via l'API
    dico_API = requete_data(espece, symbole)
    if not dico_API:
        # Si la requête renvoie None (erreur).
        dico = {
            "gene_acces_number": "",
            "RNA_acces_number": {} ,
            "proteine": {}
        }
        return dico

    # Isolation des données à partir de la réponse
    gene_acces_number = dico_API.get("id", "N/A")

    dico_prot = {}
    dico_RNA = {}

    # Vérifier si la clé "Transcript" existe et n'est pas vide
    if "Transcript" in dico_API and dico_API["Transcript"]:
        for transcript in dico_API["Transcript"]:
            # On récupère le display_name
            display_name = transcript.get("display_name", "undefined")

            # On récupère l'id du transcript
            rna_id = transcript.get("id", "N/A")
            dico_RNA[display_name] = rna_id

            # Vérifier l'existence de "Translation" avant de récupérer l'id de protéine
            if "Translation" in transcript and transcript["Translation"]:
                ensp = transcript["Translation"].get("id", "N/A")
            else:
                ensp = "N/A"
            dico_prot[display_name] = ensp

    # Stockage des infos dans le dictionnaire principal
    dico = {
        "division": division,
        "gene_acces_number": gene_acces_number,
        "RNA_acces_number": dico_RNA,
        "proteine": dico_prot
    }

    return dico