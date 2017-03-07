from clustergrammer import Network
import pandas as pd
import numpy as np

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
  net.load_file(hzome_filename)
  hzome_data = net.export_df()

  all_genes = hzome_data.columns.tolist()

  found_genes = sorted(list(set(all_genes).intersection(genes_of_class)))

  print('number of found genes: ' + str(len(found_genes)))

main()
