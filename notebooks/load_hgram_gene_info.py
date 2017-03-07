def main():
  import json_scripts

  hgram_info = json_scripts.load_to_dict('../harmonogram_classes/gene_classes_harmonogram.json')

  grant_poi = json_scripts.load_to_dict('../grant_pois/proteins_of_interest.json')

  gene_types = ['KIN', 'IC', 'GPCR']

  for inst_type in gene_types:

    all_genes = hgram_info[inst_type]
    dark_genes = grant_poi[inst_type]

    print(inst_type)
    print('all: ' + str(len(all_genes)))
    print('dark: ' + str(len(dark_genes)))
    print('\n')




main()