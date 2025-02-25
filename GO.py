import requests

# Fonction pour récupérer les termes GO (Gene Ontology) associés à un identifiant UniProt
def get_go_terms(uniprot_id):
    # URL de l'API UniProt pour récupérer les informations sur une protéine
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}"
    # En-têtes pour spécifier que nous voulons une réponse au format JSON
    headers = {"Accept": "application/json"}
    # Effectuer une requête GET à l'API UniProt
    response = requests.get(url, headers=headers)
    go_terms = {
        'Molecular Function': {},
        'Biological Process': {},
        'Cellular Component': {},
    }

    # Vérifier si la réponse est réussie (code 200)
    if response.ok:
        # Analyser la réponse JSON
        data = response.json()
        # Parcourir les références croisées pour trouver les termes GO
        for ref in data.get('uniProtKBCrossReferences', []):
            if ref['database'] == 'GO':
                id = ref['id']
                term = ref['properties'][0]['value'] if ref['properties'] else ''

                # Ajouter l'entrée au dictionnaire correspondant
                if term.startswith('F:'):
                    go_terms['Molecular Function'][id] = term[2:]
                elif term.startswith('P:'):
                    go_terms['Biological Process'][id] = term[2:]
                elif term.startswith('C:'):
                    go_terms['Cellular Component'][id] = term[2:]

    return go_terms

