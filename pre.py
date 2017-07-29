import pandas as pd
import MeCab

def tokenize(text):
	node = mecab.parseToNode(text)
	s = ""
	while node:
		s += node.surface.lower()
		s += " "
		node = node.next
	s = s[:-1]
	return s

mecab = MeCab.Tagger("-Owakati")
df = pd.read_csv("train.tsv", delimiter = '\t', header = None)
df1 = df[[0]]
df2 = df[[0]]

for i in range(len(df)):
	df1.set_value(i, 0, df[0][i])
	df2.set_value(i, 0, df[1][i])

df1.to_csv("en.txt", header = None, index = False, encoding='utf-8')
df2.to_csv("ja.txt", header = None, index = False, encoding='utf-8')