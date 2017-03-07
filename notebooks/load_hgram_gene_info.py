def main():
  '''
  I'm working on making similarity matrices for KIN, IC, and GPCR genes based on
  data in the Hzome. Here I'm gathering my old (Hgram) gene lists with the
  latest list of the 'dark' genes from the KMC 2017 grant. I'm saving these to a
  new JSON for later use. The next step is to calculate the similarity matrices
  and visualize them in a notebook or webpage.
  '''
  import json_scripts

  hgram_info = json_scripts.load_to_dict('../harmonogram_classes/gene_classes_harmonogram.json')

  grant_poi = json_scripts.load_to_dict('../grant_pois/proteins_of_interest.json')

  gene_types = ['KIN', 'IC', 'GPCR']

  # make a new json with merged all genes and dark gene info
  gene_info = {}

  for inst_type in gene_types:

    # add any dark genes to all_genes
    dark_genes = grant_poi[inst_type]
    all_genes = hgram_info[inst_type] + dark_genes

    dark_genes = sorted(list(set(dark_genes)))
    all_genes = sorted(list(set(all_genes)))

    print(inst_type)
    print('all: ' + str(len(all_genes)))
    print('dark: ' + str(len(dark_genes)))

    print(len(list(set(dark_genes) - set(all_genes))))

    gene_info[inst_type] = {}
    gene_info[inst_type]['all'] = all_genes
    gene_info[inst_type]['dark'] = dark_genes

    print('\n\n')

  json_scripts.save_to_json(gene_info, '../grant_pois/gene_info_with_dark.json', indent='indent')

main()