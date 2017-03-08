import pandas as pd

def load_matrix(filename):

  hzome = pd.read_csv(filename, sep='\t')

  # set the index (row names) to the first column
  hzome = hzome.set_index('#')

  orig_cols = hzome.columns.tolist()

  # drop the two other columns
  hzome = hzome.drop(orig_cols[0], 1)
  hzome = hzome.drop(orig_cols[1], 1)

  # drop two row indexes
  hzome = hzome.drop( hzome.index[[0,1]] )

  # make new dataframe from the pieces
  rows = hzome.index.tolist()
  cols = hzome.columns.tolist()
  mat = hzome.as_matrix()
  mat = mat.astype(float)

  df = pd.DataFrame(data=mat, columns=cols, index=rows)

  return df

# # how to run
# #############
# # filename = '../hzome_data/small_encode.txt'
# filename = '../hzome_data/ENCODE_TF_targets.txt'
# df = main(filename)
# print(df)
