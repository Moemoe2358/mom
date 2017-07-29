import pandas as pd

dfIn = pd.read_csv("train.tsv", delimiter = '\t', header = None)
dfFre_in = pd.value_counts(dfIn[1]).reset_index()
dfFre_in.columns = ['disease', 'f_in']

dfFre_in.to_csv("ftrain.tsv", sep = '\t', header = None, index = None)