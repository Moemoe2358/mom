# -*- coding: utf-8 -*-
import progressbar as pb
import pandas as pd
import math as m
import sys

def findThreeDisease_discr(discr, discrDic, diseaseFreDic):
	closestDisease = []
	dl = discrDic.keys()
	for discr_i in dl:
		if discr == discr_i and flag != "test":
			continue
		else:
			disease_i = discrDic[discr_i]
			distance_i = getDistance(testDic[discr], fastDic[discr_i]) + getDistance(testDic[discr], fastDiseaseDic[discr_i])
			distance_i = balance(distance_i, discr, discr_i, disease_i, diseaseFreDic)
			if len(closestDisease) < 3:
				closestDisease.append((distance_i, discr_i, disease_i))
				closestDisease.sort()
			else:
				if distance_i < closestDisease[2][0]:
					closestDisease = add(closestDisease, distance_i, discr_i, disease_i)
	return closestDisease

def balance(distance_i, discr, discr_i, disease_i, diseaseFreDic):
	distance_i -= m.sqrt(diseaseFreDic[disease_i]) / 90
	if (discr in discr_i) or (discr_i in discr):
		distance_i -= 0.1
	if (discr in disease_i) or (disease_i in discr):
		distance_i -= 0.1
	return distance_i

def add(closestDisease, distance_i, discr_i, disease_i):
	closestDisease.append((distance_i, discr_i, disease_i))
	if disease_i not in [i[2] for i in closestDisease]:
		closestDisease.pop(2)
	else:
		for i in range(len(closestDisease) - 1):
			if disease_i == closestDisease[i][2]:
				if distance_i < closestDisease[i][0]:		
					closestDisease.pop(i)
				else:
					closestDisease.pop()
				break
	closestDisease.sort()
	return closestDisease

def excludeStopWords(s):
	stopWords = ["【", "】", "（", "）", "(", ")"]
	# , "１", "２", "３", "４", "５", "６", "７", "８", "９", "０", "年", "月", "日", "才"
	for i in stopWords:
		s = s.replace(i, "")
	return s

def getDistance(s1, s2):
	n = len(s1.intersection(s2))
	m = len(s1) + len(s2) - n 
	distance = 1 - n / float(m)
	return distance

def getScore(d1, d2, d3, ans):
	if d1 == ans:
		return float(1)
	elif d2 == ans:
		return float(1)/2
	elif d3 == ans:
		return float(1)/3
	else:
		return float(0)

flag = sys.argv[1]
log = sys.argv[2]

dfIn = pd.read_csv("train.tsv", delimiter = '\t', header = None)
dfFre_in = pd.value_counts(dfIn[1]).reset_index()
dfFre_in.columns = ['disease', 'f_in']
diseaseDic = dfFre_in.set_index("disease")["f_in"].to_dict()
dfIn[2] = pd.Series("")
dfIn[3] = pd.Series("")
dfIn[4] = pd.Series("")
for i in range(len(dfIn)):
	dfIn.set_value(i, 2, excludeStopWords(dfIn[0][i]))
	dfIn.set_value(i, 3, set(list(unicode(dfIn[2][i], "utf-8"))))
	dfIn.set_value(i, 4, set(list(unicode(dfIn[1][i], "utf-8"))))
discrDic = dfIn.set_index(2)[1].to_dict()
fastDic = dfIn.set_index(2)[3].to_dict()
fastDiseaseDic = dfIn.set_index(2)[4].to_dict()

if flag == "test":
	sampleFile = "sample_test.tsv"
	dfIn = pd.read_csv("test.tsv", delimiter = '\t', header = None)
	dfIn[1] = pd.Series("")
	dfIn[2] = pd.Series("")
	for i in range(len(dfIn)):
		dfIn.set_value(i, 1, excludeStopWords(dfIn[0][i]))
		dfIn.set_value(i, 2, set(list(unicode(dfIn[1][i], "utf-8"))))
	testDic = dfIn.set_index(1)[2].to_dict()
if flag == "train":
	sampleFile = "sample_train.tsv"
	testDic = fastDic
if flag == "smoke":
	sampleFile = "sample_smoke.tsv"
	dfIn = pd.read_csv("smoke.tsv", delimiter = '\t', header = None)
	testDic = fastDic

dfResult = pd.read_csv(sampleFile, delimiter = '\t', header = None)

p = pb.ProgressBar(max_value = len(dfIn),
	redirect_stdout = True,
	widgets=[pb.Percentage(), "(", pb.SimpleProgress(), ")", pb.Bar(), pb.Timer(), " ", pb.ETA(), " "])

if flag != "test":
	sumScore = 0
	scoreFrequency = []

with p:
	for i in range(len(dfIn)):

		discription = excludeStopWords(dfIn[0][i])
		threeDisease_discr = findThreeDisease_discr(discription, discrDic, diseaseDic)
		dfResult.set_value(3 * i, 1, threeDisease_discr[0][2])
		dfResult.set_value(3 * i + 1, 1, threeDisease_discr[1][2])
		dfResult.set_value(3 * i + 2, 1, threeDisease_discr[2][2])

		if flag != "test":
			s = getScore(threeDisease_discr[0][2], threeDisease_discr[1][2], threeDisease_discr[2][2], dfIn[1][i])
			scoreFrequency.append(s)
			sumScore += s

			if log == "1" and s != 1 and diseaseDic[dfIn[1][i]] > 1:
				print i, discription, dfIn[1][i], diseaseDic[dfIn[1][i]]
				print threeDisease_discr[0][0], threeDisease_discr[0][1], threeDisease_discr[0][2]
				print threeDisease_discr[1][0], threeDisease_discr[1][1], threeDisease_discr[1][2]
				print threeDisease_discr[2][0], threeDisease_discr[2][1], threeDisease_discr[2][2]
				print "[" + str(s) + "]"
				print ""

		p.update(i)

dfResult.to_csv("submit.tsv", sep = '\t', header = None, index = None)

if flag != "test":
	print "Your score is", sumScore / len(dfIn)
	print scoreFrequency.count(1), scoreFrequency.count(0.5), scoreFrequency.count(1 / float(3)), scoreFrequency.count(0)