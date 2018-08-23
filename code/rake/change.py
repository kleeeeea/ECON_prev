from sets import Set
import sys
import os

dataset = sys.argv[1]
f = open(dataset + "_rake_term.txt", "r")
ff = open(dataset + "_rake_term0.txt", "w")
line = f.readline()
while line:
	termPair = line.split("\t")
	term = termPair[0]
	score = termPair[1]
	score = str(float(score) / 100)
	if (len(score) > 6): score = score[:6]
	ff.write(term + "\t" + score + "\n")
	line = f.readline()
f.close()
ff.close()
