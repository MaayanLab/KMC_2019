def main():
  import json_scripts

  hgram_info = json_scripts.load_to_dict('../harmonogram_classes/gene_classes_harmonogram.json')

  gene_types = ['KIN', 'IC', 'GPCR']

  for inst_type in gene_types:
    print(inst_type)
    print(len(hgram_info[inst_type]))
    print('\n')

main()