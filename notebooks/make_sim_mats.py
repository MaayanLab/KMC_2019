from clustergrammer import Network
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

def main():

  net = Network()

  # load genes of interest
  gene_info = net.load_json_to_dict('../grant_pois/gene_info_with_dark.json')

  hzome_filename = '../CCLE/CCLE.txt'

  genes_of_class = gene_info['KIN']['all']

  calc_gene_sim_mat(net, genes_of_class, hzome_filename)

def calc_gene_sim_mat(net, genes_of_class, hzome_filename):
  '''
  Calculate a similarity matrix of a subset of genes using a hzome dataset
  (specified by filename). The files will be saved and clustered similarity
  matrices will be calculated next.
  '''

  print('number of genes: ' + str(len(genes_of_class)))

  # load hzome data
  ####################
  net.load_file(hzome_filename)
  hzome_data = net.export_df()

  # get subset of dataset
  #######################
  hzome_data = hzome_data.transpose()

  all_genes = hzome_data.columns.tolist()
  found_genes = sorted(list(set(all_genes).intersection(genes_of_class)))

  print('number of found genes: ' + str(len(found_genes)))
  hzome_data = hzome_data[found_genes]
  hzome_data = hzome_data.transpose()
  print(hzome_data.shape)

  # Z-score normalize data
  #########################
  net.load_df(hzome_data)
  net.normalize(axis='row', norm_type='zscore', keep_orig=False)

  hzome_data = net.export_df()

  # Calc similarity matrix
  ##########################
  inst_dm = pdist(hzome_data, metric='cosine')
  inst_dm = squareform(inst_dm)
  # convert cosine distance to similarity
  inst_dm = 1 - inst_dm
  # cutoff values below 0.25
  inst_dm[ abs(inst_dm) < 0.25] = 0

  df_dm = pd.DataFrame(data=inst_dm, columns=found_genes, index=found_genes)

  net.load_df(df_dm)
  net.make_clust(views=[])

  net.write_json_to_file('viz', '../json/mult_view.json', 'no-indent')


main()
