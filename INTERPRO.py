# -*- coding: utf-8 -*-
import requests

def get_interpro_links(uniprot_id):
    """
    Récupère les liens InterPro pour un identifiant UniProt donné.
    """
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}"
    headers = {"Accept": "application/json"}
    interpro_links = []

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Vérifie si la requête a réussi

        if response.ok:
            data = response.json()
            for ref in data.get('uniProtKBCrossReferences', []):
                if ref['database'] == 'InterPro':
                    interpro_links.append({
                        'id': ref['id'],
                        'name': ref['properties'][0]['value'] if ref['properties'] else '',
                    })
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des liens InterPro pour UniProt ID {uniprot_id}: {e}")

    return interpro_links

