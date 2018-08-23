# pip install rake-nltk
from rake_nltk import Rake
from sets import Set
import sys
numLineReadEachExtraction = 100
extractedText = ""
dataset = sys.argv[1]
r = Rake()
f = open(dataset, "r")
line = f.readline()
termDict = {}
while line:
	for i in range(0, numLineReadEachExtraction):
		if (line):
			extractedText += line
			line = f.readline()
		else: break
	r.extract_keywords_from_text(extractedText)
	extractedText = ""
	termScoreList = r.get_ranked_phrases_with_scores()
	for termTuple in termScoreList:
		score = termTuple[0]
		term = termTuple[1]
		if term in termDict:
			if (score > termDict[term]):
				termDict[term] = score
		else:
			termDict[term] = score
f.close()

termFile = open(dataset + "_rake_term.txt", "w")
for term, score in termDict.iteritems():
	termFile.write(term)
	termFile.write("\t")
	termFile.write(str(score))
	termFile.write("\n")
termFile.close()