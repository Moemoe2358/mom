import pandas as pd

df1 = pd.read_csv("170522.tsv", delimiter = '\t', header = None)
df2 = pd.read_csv("170531.tsv", delimiter = '\t', header = None)

for i in range(len(df1) / 3):
	if df2[1][3 * i] == df1[1][3 * i + 1] or df2[1][3 * i + 1] == df1[1][3 * i + 1] or df2[1][3 * i + 1] == df1[1][3 * i + 1]:
		t = df1[1][3 * i + 1]
		df1.set_value(3 * i + 1, 1, df1[1][3 * i])
		df1.set_value(3 * i, 1, t)
		print i
	elif df2[1][3 * i] == df1[1][3 * i + 2] or df2[1][3 * i + 1] == df1[1][3 * i + 2] or df2[1][3 * i + 1] == df1[1][3 * i + 2]:
		t = df1[1][3 * i + 2]
		df1.set_value(3 * i + 2, 1, df1[1][3 * i + 1])
		df1.set_value(3 * i + 1, 1, t)
		print i

df1.to_csv("submit.tsv", sep = '\t', header = None, index = None)