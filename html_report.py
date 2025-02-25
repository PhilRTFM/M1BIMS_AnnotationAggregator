import json

def report_html(resultat_path, output_path):
    with open(resultat_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Gene Information</title>
                <!-- Inclusion des feuilles de style et des scripts nécessaires pour DataTables -->
                <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
                <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
                <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
                <style>
                    /* Styles de base pour le HTML et le corps */
                    html, body {
                        height: 100%;
                        margin: 0;
                        padding: 0;
                    }
            
                    body {
                        display: flex;
                        flex-direction: column;
                    }
            
                    /* Style pour le titre principal */
                    h1 {
                        margin: 0;
                        padding: 20px;
                        background-color: #f1f1f1;
                        text-align: center;
                    }
            
                    /* Styles pour l'enveloppe DataTables */
                    .dataTables_wrapper {
                        flex: 1;
                        display: flex;
                        flex-direction: column;
                    }
            
                    .dataTables_scrollBody {
                        flex: 1;
                        overflow: auto;
                    }
            
                    /* Style pour la ligne d'en-tête */
                    tr.entete {
                        background-color: rgb(79, 104, 241);
                        color: rgb(255, 255, 255);
                    }
            
                    /* Style pour la ligne de la banque de données */
                    tr.databank-header {
                        background-color: rgb(17, 37, 150); /* bleu plus foncé */
                        color: rgb(255, 255, 255);
                        font-size: 1.5em; /* Texte plus gros */
                        text-align: center;
                        height: 50px; /* Ligne plus grosse */
                    }
            
                    /* Style général pour la table */
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        overflow: hidden;
                    }
            
                    /* Bordures pour la table et ses éléments */
                    table, thead, tbody, th, td, tr {
                        border: 1px solid black;
                    }
            
                    th, td {
                        text-align: left;
                        padding: 8px;
                    }
            
                    /* Définir la hauteur des lignes */
                    tr {
                        max-width: 400px;
                        min-width: 200px;
                        max-height: 200px;
                        overflow: hidden; /* Gérer le débordement */
                    }
            
                    /* Alternance des couleurs pour les lignes */
                    #table_id tbody tr:nth-of-type(odd) {
                        background-color: rgb(255, 255, 255) !important;
                        color: rgb(0, 0, 0);
                    }
            
                    #table_id tbody tr:nth-of-type(even) {
                        background-color: rgb(238, 238, 238) !important;
                        color: rgb(0, 0, 0);
                    }
            
                    /* Effet de survol pour les lignes */
                    #table_id.dataTable tbody tr:hover {
                        background-color: rgb(230, 244, 248) !important;
                        cursor: pointer;
                    }
            
                    /* Zone défilable pour les cellules */
                    .scrollable {
                        max-height: 200px;
                        width: 100%; /* Utiliser toute la largeur de la cellule */
                        overflow-y: auto;
                        overflow-x: auto;
                        padding: 5px;
                        font-family: Arial, sans-serif;
                    }
            
                    td {
                        max-width: 400px;
                        min-width: 200px;
                        max-height: 200px;
                        overflow: hidden; /* Gérer le débordement */
                        padding: 0; /* Supprimer le padding pour que le div scrollable prenne toute la place */
                        box-sizing: border-box; /* Inclure les bordures et le padding dans la largeur et la hauteur */
                    }
                </style>
                <script>
                    $(document).ready(function () {
                        // Initialisation de DataTables avec des options spécifiques
                        var table = $('#table_id').DataTable({
                            'scrollX': true,
                            'lengthMenu': [6, 10, 15, 20, 'All'],
                            fixedColumns: {
                                leftColumns: 1
                            }
                        });
            
                        // Fonction pour ajuster la longueur de la page en fonction de la hauteur de la fenêtre
                        function adjustPageLength() {
                            var windowHeight = $(window).height();
                            var headerHeight = $('thead').height();
                            var rowHeight = $('tbody tr').height();
                            var availableHeight = windowHeight - headerHeight - 100; // Ajuster 100 pour le padding/margin
                            var pageLength = Math.floor(availableHeight / rowHeight);
            
                            table.page.len(pageLength).draw();
                        }
            
                        // Ajuster la longueur de la page lors du redimensionnement de la fenêtre
                        $(window).on('resize', function () {
                            adjustPageLength();
                        });
            
                        // Ajuster la longueur de la page au chargement initial
                        adjustPageLength();
                    });
                </script>
            </head>
            
            <body>
                <h1>Gene report</h1>
                <table id='table_id' class='display nowrap cell-border' style='width:100%'>
                    <thead>
                        <tr class="databank-header">
                            <th>INPUT</th>
                            <th colspan='4'>NCBI</th>
                            <th colspan='3'>ENSEMBL</th>
                            <th>UNIPROT</th>
                            <th colspan='3'>GO</th>
                            <th>INTERPRO</th>
                        </tr>
                        <tr class="entete">
                            <!-- input -->
                            <th>Gene and Organism</th>
            
                            <!-- NCBI -->
                            <th>Official full name</th>
                            <th>Gene ID</th>
                            <th>Transcript ID(s)</th>
                            <th>Protein ID(s)</th>
            
                            <!-- Ensembl-->
                            <th>Gene ID</th>
                            <th>Transcript ID(s)</th>
                            <th>Protein ID(s)</th>
            
                            <!-- Uniprot -->
                            <th>UniProt ID</th>
            
                            <!-- GO -->
                            <th>Molecular Function</th>
                            <th>Biological Process</th>
                            <th>Cellular Component</th>
            
                            <!-- Interpro -->
                            <th>InterPro Domains</th>
                        </tr>
                    </thead>
                    <tbody>
                """

    for species, details in data.items():
        # INPUT
        symbol = details.get("Symbole") if details.get("Symbole") is not None else None
        symbol = symbol if symbol else "N/A"
    
        # NCBI
        ncbi = details.get("NCBI") if details.get("NCBI") is not None else {}
        name = ncbi.get("Description") if ncbi.get("Description") is not None else None
        name = name if name else "N/A"
        
        gene_id = ncbi.get("Gene ID") if ncbi.get("Gene ID") is not None else None
        gene_id = gene_id if gene_id else "N/A"
        if gene_id != "N/A":
            gene_id_link = f"""
         <a href="https://www.ncbi.nlm.nih.gov/gene/{gene_id}">
             {gene_id}
         </a>
         """
        else:
            gene_id_link = "N/A"
    
     
    
        transcripts = ncbi.get("Transcrits")
        if transcripts and isinstance(transcripts, list) and any(transcripts):
            transcripts_id = "<br>".join([
                f"<a href='https://www.ncbi.nlm.nih.gov/nuccore/{rna}'>{rna}</a>" 
                for rna in transcripts if rna
            ])
        else:
            transcripts_id = "N/A"
    
        proteins = ncbi.get("Protéines") or ncbi.get("Protéine")  
        if proteins:
            if type(proteins) == list:  
                proteins_id = "<br>".join([
                    f"<a href='https://www.ncbi.nlm.nih.gov/protein/{prot}'>{prot}</a>" 
                    for prot in proteins if prot
                ])
            else:  
                proteins_id = f"<a href='https://www.ncbi.nlm.nih.gov/protein/{proteins}'>{proteins}</a>"
        else:
            proteins_id = "N/A"
    
        # Ensembl
        ensembl = details.get("Ensembl") if details.get("Ensembl") is not None else {}
        ensembl_div = ensembl.get("division") if ensembl.get("division") is not None else None
        if ensembl_div == "Vertebrates.":
            ensembl_div = ""
        ensembl_div = ensembl_div if ensembl_div and ensembl_div != "N/A" else ""
    
        ensembl_gene = ensembl.get("gene_acces_number") if ensembl.get("gene_acces_number") is not None else None
        ensembl_gene = ensembl_gene if ensembl_gene else "N/A"
        if ensembl_gene != "N/A":
            ensembl_gene_link =  f"""
         <a href="https://{ensembl_div}ensembl.org/{species}/Gene/Summary?db=core;g={ensembl_gene};">
             {ensembl_gene}
         </a>
         """
        else:
            ensembl_gene_link = "N/A"
    
        rna_dict = ensembl.get("RNA_acces_number") if isinstance(ensembl.get("RNA_acces_number"), dict) else {}
        if rna_dict:
            ensembl_rna = "<br>".join([
                f"<a href='https://{ensembl_div}ensembl.org/{species}/Transcript/Summary?db=core;g={ensembl_gene};t={rna_acc};'>{rna_name}: {rna_acc}</a>"
                for rna_name, rna_acc in rna_dict.items() if rna_name and rna_acc
            ])
        else:
            ensembl_rna = "N/A"
    
        prot_dict = ensembl.get("proteine") if isinstance(ensembl.get("proteine"), dict) else {}
        if prot_dict:
            ensembl_prot = "<br>".join([
                f"<a href='https://{ensembl_div}ensembl.org/{species}/Transcript/ProteinSummary?db=core;g={ensembl_gene};t={prot_acc};'>{prot_name}: {prot_acc}</a>"
                for prot_name, prot_acc in prot_dict.items() if prot_name and prot_acc
            ])
        else:
            ensembl_prot = "N/A"
      
        # Uniprot
        uniprot_id = details.get("Uniprot") if details.get("Uniprot") is not None else None
        uniprot_id = uniprot_id if uniprot_id else "N/A"
        if uniprot_id != "N/A":
            uniprot_id_link =  f"""
         <a href="https://www.uniprot.org/uniprotkb/{uniprot_id}">
             {uniprot_id}
         </a>
         """
        else:
            uniprot_id_link = "N/A"
    
        # GO
        go = details.get("GO_terms") if details.get("GO_terms") is not None else {}
    
        mf = go.get("Molecular Function") if go.get("Molecular Function") is not None else {}
        if mf:
            go_mf = "<br>".join([
                f"<a href='https://amigo.geneontology.org/amigo/term/{acc}'> {acc}: {name} </a>" 
                for acc, name in mf.items() if acc and name
            ])
        else:
            go_mf = "N/A"
    
        bp = go.get("Biological Process") if go.get("Biological Process") is not None else {}
        if bp:
            go_bp = "<br>".join([
                f"<a href='https://amigo.geneontology.org/amigo/term/{acc}'> {acc}: {name} </a>"
                for acc, name in bp.items() if acc and name
            ])
        else:
            go_bp = "N/A"
    
        cc = go.get("Cellular Component") if go.get("Cellular Component") is not None else {}
        if cc:
            go_cc = "<br>".join([
                f"<a href='https://amigo.geneontology.org/amigo/term/{acc}'> {acc}: {name} </a>"
                for acc, name in cc.items() if acc and name
            ])
        else:
            go_cc = "N/A"
        
        # Interpro
        interpro_list = details.get("interpro") if details.get("interpro") is not None else []
        if interpro_list and isinstance(interpro_list, list):
            interpro_domains = "<br>".join([
                f"<a href='https://www.ebi.ac.uk/interpro/entry/InterPro/{dico.get('id', '')}/'> {dico.get('id', '')}: {dico.get('name', '')} </a>" 
                for dico in interpro_list if dico.get("id") and dico.get("name")
            ])
            if not interpro_domains:
                interpro_domains = "N/A"
        else:
            interpro_domains = "N/A"
        
        html += f"""
        <tr>
            <!-- input -->
            <td><div class="scrollable">
                    {symbol}<br><i>{species.replace('_', ' ').title()}</i>
            </div></td>
                
            
            <!-- NCBI -->
            <td><div class="scrollable">
                    {name}
            </div></td>
                    
            <td><div class="scrollable">
                    {gene_id_link}
            </div></td>
                    
            <td><div class="scrollable">
                    {transcripts_id}
            </div></td>
                    
            <td><div class="scrollable">
                    {proteins_id}
            </div></td>
                
            
            <!-- Ensembl -->
            <td><div class="scrollable">
                    {ensembl_gene_link}
            </div></td>
                    
            <td><div class="scrollable">
                    {ensembl_rna}
            </div></td>
                    
            <td><div class="scrollable">
                    {ensembl_prot}
            </div></td>
                   
   
            <!-- Uniprot -->
            <td><div class="scrollable">
                    {uniprot_id_link}
            </div></td>
                 
            <!-- GO -->
            <td><div class="scrollable">
                    {go_mf}
            </div></td>
                    
            <td><div class="scrollable">
                    {go_bp}
            </div></td>
                    
            <td><div class="scrollable">
                    {go_cc}
            </div></td>
                    
            <!-- Interpro -->
            <td><div class="scrollable">
                    {interpro_domains}
            </div></td>
                    
        </tr>
        """

    html += """
    </tbody>
    </table>
    </body>
    </html>
    """

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"\n HTML report successfully generated at {output_path}")