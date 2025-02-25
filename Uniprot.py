# -*- coding: utf-8 -*-
import requests


#fonctionne avec gene id du ncbi 
def get_uniprot_from_ncbi_detailed(ncbi_id):
    """
    Permet de recuper l'identifiant uniportkb
    """
    
    queries = [
        f"xref:GeneID:{ncbi_id}",
        f"database:GeneID {ncbi_id}",
        f"gene_id:{ncbi_id}"
    ]
    
    for query in queries:
        url = f"https://rest.uniprot.org/uniprotkb/search?query={query}"
        headers = {"Accept": "application/json"}
        
        response = requests.get(url, headers=headers)
        if response.ok:
            data = response.json()
            if data.get('results'):
                return data['results'][0]['primaryAccession']
    return None