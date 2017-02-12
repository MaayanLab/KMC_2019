def main():
  make_protein_dictionary()

  make_matrix_subset()

def make_matrix_subset():
  '''
  This will save a subset of the downsampled matrix using the proteins of interest
  '''
  from clustergrammer import Network
  import json_scripts

  print('-- load CCLE downsampled data')

  # load downsampled CCLE data
  net = Network()
  net.load_file('CCLE/CCLE_kmeans_ds_col_100.txt')

  df = net.export_df()

  print('dataframe shape before filtering')

  # load proteins of interest
  filename = 'proteins_of_interest/proteins_of_interest.json'
  poi = json_scripts.load_to_dict(filename)

  all_poi = []
  for inst_type in poi:
    all_poi.extend(poi[inst_type])

  # only keep pois that are found in the CCLE
  all_genes = df.index.tolist()

  found_poi = list( set(all_genes) & set(all_poi) )

  num_found_poi = len(found_poi)

  print( str(num_found_poi) + ' proteins of interest were found in the CCLE data')

  # filter dataframe using row list (transpose and transpose-back)
  ##################################################################
  df = df.transpose()
  df = df[found_poi]
  df = df.transpose()

  print('dataframe shape after fitlering for proteins_of_interest')
  print(df.shape)

  # save version without protein categories (e.g. kinase)
  df.to_csv('CCLE_kmeans_ds_col_100_poi.txt', sep='\t')


def make_protein_dictionary():
  '''
  This script makes a python dictionary from the proteins of interest lists
  and saves them as a JSON for later use.
  '''
  print('-- generate dictionary with protein names')

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