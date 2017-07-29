# -*- coding: utf-8 -*-
from Translator import Translator
import pandas as pd

en_lines = open('en-test.txt').read().split('\n')

df = pd.read_csv("sample_test.tsv", delimiter = '\t', header = None)

epoch_num = 12
count = 0

for epoch in reversed(range(epoch_num)):
	model = Translator()
	model.load_model("en2ja-" + str(epoch) + ".model")
	for i in range(len(en_lines)):
		try:
			en_words = en_lines[i].split()
			ja_words = model.test(en_words)[:-1]
			s = ''.join(ja_words)
			if s == "":
				continue
			if df[1][3 * i] == "予測１":
				df.set_value(3 * i, 1, s)
			elif df[1][3 * i + 1] == "予測２":
				if s != df[1][3 * i]:
					df.set_value(3 * i + 1, 1, s)
			elif df[1][3 * i + 2] == "予測３":
				if s != df[1][3 * i] and s != df[1][3 * i + 1]:
			 		df.set_value(3 * i + 2, 1, s)
		 			continue
		except:
			count += 1
			print epoch, i			

print count

# for i in range(len(en_lines)):
# 	en_words = en_lines[i].split()
# 	try:
# 		l = []
# 		for epoch in reversed(range(epoch_num)):
# 			model = Translator()
# 			model.load_model("en2ja-" + str(epoch) + ".model")
# 			ja_words = model.test(en_words)[:-1]
# 			s = ''.join(ja_words)
# 			if s != "" and s not in l:
# 				l.append(s)
# 				if len(l) == 1:
# 					df.set_value(3 * i, 1, s)
# 				elif len(l) == 2:
# 					df.set_value(3 * i + 1, 1, s)
# 				elif len(l) == 3:
# 					df.set_value(3 * i + 2, 1, s)
# 					break
# 	except:
# 		print i

df.to_csv("submit.tsv", sep = '\t', header = None, index = None)