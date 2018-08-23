# pip install summa
from summa.keywords import keywords
from sets import Set
import sys
import os.path

numLineReadEachExtraction = 20
extractedText = ""
dataset = sys.argv[1]
f = open(dataset, "r")
line = f.readline()
termDict = {}
while line:
	for i in range(0, numLineReadEachExtraction):
		if (line):
			extractedText += line
			line = f.readline()
		else: break
	termScoreList = keywords(extractedText, scores=True)
	extractedText = ""
	for termTuple in termScoreList:
		score = termTuple[1]
		term = termTuple[0]
		if term in termDict:
			if (score > termDict[term]):
				termDict[term] = score
		else:
			termDict[term] = score
f.close()

termFile = open(dataset + "_textrank_term.txt", "w")
for term, score in termDict.iteritems():
	termFile.write(term)
	termFile.write("\t")
	termFile.write(str(score))
	termFile.write("\n")
termFile.close()
