# -*- coding: utf-8 -*-
import MeCab
from gensim import corpora, matutils
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.naive_bayes import GaussianNB

def tokenize(text):
    node = mecab.parseToNode(text)
    l = []
    while node:
        # if node.feature.split(',')[0] == '名詞':
        l.append(node.surface.lower())
        node = node.next
    return l

mecab = MeCab.Tagger('mecabrc')
d = []
allData = []
allLabel = []

fi = open('train.tsv', 'r')
next(fi)

for line in fi:
    words = tokenize(line.split("\t")[0])
    d.append(words)
    if line.split("\t")[1][:-2] == '無し':
        allLabel.append(1)
    else:
        allLabel.append(0)

s = 0
for i in allLabel:
    if i == 1:
        s += 1
print s

dictionary = corpora.Dictionary(d)
for i in d:
    vec = dictionary.doc2bow(i)
    # print vec
    allData.append(list(matutils.corpus2dense([vec], num_terms = len(dictionary)).T[0]))

trainData = allData[:8000]
trainLabel = allLabel[:8000]
testData = allData[8000:]
testLabel = allLabel[8000:]

estimator = RandomForestClassifier()
estimator = DecisionTreeClassifier()
estimator = svm.SVC(kernel='rbf', C=1, gamma=0.1)
estimator = svm.LinearSVC(C=1)
estimator = GaussianNB()

estimator.fit(trainData, trainLabel)
testPredict = estimator.predict(testData)

tp, fp, fn, tn = 0, 0, 0, 0
for i in range(len(testPredict)):
    if testLabel[i] == 1 and testPredict[i] == 1:
        tp += 1
    if testLabel[i] == 0 and testPredict[i] == 1:
        fn += 1
    if testLabel[i] == 1 and testPredict[i] == 0:
        fp += 1
    if testLabel[i] == 0 and testPredict[i] == 0:
        tn += 1
print tp, fn
print fp, tn
print (tp + tn) / float(len(testPredict))
print tp / float(tp + fp)

