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

df = pd.read_csv("test.tsv", delimiter = '\t', header = None)

for i in range(len(df)):
    df.set_value(i, 0, df[0][i])

df.to_csv("en-test.txt", header = None, index = False, encoding = "utf-8")