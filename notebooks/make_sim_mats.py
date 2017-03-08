from clustergrammer import Network
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
import hzome_to_df
from copy import deepcopy

def main():

  net = Network()

  # load genes of interest
  gene_info = net.load_json_to_dict('../grant_pois/gene_info_with_dark.json')

  # ENCODE, GTEx, etc
  # hzome_names = ['my_CCLE_exp.txt', 'ENCODE_TF_targets.txt', 'ChEA_TF_targets.txt']
  # hzome_names = ['my_gtex_Moshe_2017_exp.txt']
  hzome_names = ['my_CCLE_exp.txt']

  # define separate sim_cutoffs for different files
  cutoffs = {}
  cutoffs['my_CCLE_exp.txt'] = 0.15
  cutoffs['ENCODE_TF_targets.txt'] = 0.6
  cutoffs['ChEA_TF_targets.txt'] = 0.2
  cutoffs['my_gtex_Moshe_2017_exp.txt'] = 0.2

  genes_of_class = gene_info['KIN']['all']

  for hzome_name in hzome_names:

    hzome_filename = '../hzome_data/' + hzome_name

    # load hzome data
    ####################
    if 'my_' in hzome_name:
      # if I am providing the data, then load in normal way
      net.load_file(hzome_filename)
      hzome_data = net.export_df()
    else:
      # load data in hzome format
      hzome_data = deepcopy(hzome_to_df.load_matrix(hzome_filename))

    for gene_class in gene_info:
      calc_gene_sim_mat(hzome_data, net, gene_info, gene_class, hzome_name, cutoffs)

def calc_gene_sim_mat(hzome_data, net, gene_info, gene_class, hzome_name, cutoffs):
  '''
  Calculate a similarity matrix of a subset of genes using a hzome dataset
  (specified by filename). The files will be saved and clustered similarity
  matrices will be calculated next.
  '''

  # convert to normal names
  class_titles = {}
  class_titles['KIN'] = 'Kinases'
  class_titles['IC'] = 'Ion Channels'
  class_titles['GPCR'] = 'GPCRs'


  sim_cutoff = cutoffs[hzome_name]


  genes_of_class = gene_info[gene_class]['all']

  print('hzome_name: ' + hzome_name)
  print('gene_class: ' + gene_class)
  print('number of genes: ' + str(len(genes_of_class)))


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

  ################################################
  # must have different rules for each data type
  ################################################
  if '_exp' in hzome_name:
    # z-score normalize expression data to highlight correlations in gene
    # expression rather than absolute expression
    net.normalize(axis='row', norm_type='zscore', keep_orig=False)
    print('** normalize rows')

  hzome_data = net.export_df()

  # Calc similarity matrix
  ##########################
  if '_targets' in hzome_name:
    # targets means binary data
    inst_metric = 'jaccard'
  elif '_exp' in hzome_name:
    # expression data is real valued, so use cosine distance
    inst_metric = 'cosine'

  print('inst_metric: '+ inst_metric)

  inst_dm = pdist(hzome_data, metric=inst_metric)
  inst_dm = squareform(inst_dm)
  # convert cosine distance to similarity
  inst_dm = 1 - inst_dm
  # cutoff values below 0.25
  inst_dm[ abs(inst_dm) < sim_cutoff] = 0

  gene_title = class_titles[gene_class]

  # add categories to found genes
  ################################
  found_genes_cat = []
  for inst_gene in found_genes:

    inst_tuple = ()

    inst_name = gene_title + ': ' + inst_gene

    if inst_gene in gene_info[gene_class]['dark']:
      inst_cat = 'Dark Gene: true'
    else:
      inst_cat = 'Dark Gene: false'

    inst_tuple = (inst_name, inst_cat)
    found_genes_cat.append( inst_tuple )

  df_dm = pd.DataFrame(data=inst_dm, columns=found_genes_cat, index=found_genes_cat)

  net.load_df(df_dm)

  # always use default parameters to cluster distance matrix since the values
  # a real numbers
  net.make_clust(views=[])

  viz_filename = '../json/' + hzome_name.split('.txt')[0] + '_' + gene_class + \
                 '.json'

  net.write_json_to_file('viz', viz_filename, 'no-indent')

  print('-------------------------\n\n')

main()
