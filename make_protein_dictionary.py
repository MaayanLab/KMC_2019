def main():
  '''
  This script makes a python dictionary from the proteins of interest lists
  and saves them as a JSON for later use.
  '''

  import json_scripts

  poi = {}

  for inst_type in ['kinase', 'gpcr', 'ion_channel']:
    inst_names = load_names(inst_type)

    poi[inst_type] = inst_names

  json_scripts.save_to_json(poi, 'proteins_of_interest/proteins_of_interest.json', indent='indent')

def load_names(protein_type):
  filename = 'proteins_of_interest/' + protein_type + 's_of_interest.txt'
  f = open(filename)
  lines = f.readlines()
  f.close()

  protein_names = []
  for inst_line in lines:
    inst_line = inst_line.strip()
    protein_names.append(inst_line)

  return protein_names

main()
