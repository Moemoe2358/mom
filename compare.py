import pandas as pd
import sys

df1 = pd.read_csv(sys.argv[1], delimiter = '\t', header = None)
df2 = pd.read_csv(sys.argv[2], delimiter = '\t', header = None)
log = sys.argv[3]

s, n = 0, 0
for i in range(len(df1)):
	if df1[1][i] != df2[1][i]:
		if i % 3 == 0:
			q = 1
		elif i % 3 == 1:
			q = 0.5
		else:
			q = 1 / float(3)
		if log == "1":
			print i, df1[0][i], df1[1][i], df2[1][i], q
		s += q
		n += 1

print s / len(df1) * 3, n