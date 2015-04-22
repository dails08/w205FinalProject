#!/usr/bin/python

import nltk
import nltkpreprocessor
import re
import sys

# initialize stopWords
stopWords = []

def printUsage():
    print "featurevector.py <inputEmailFile>"

def getStopWordList():
    stopWords = nltk.corpus.stopwords.words('english')
    # append any other stop words
    # stopWords.append('word')

    return stopWords

def getFeatureVector(email):
    featureVector = []

    # split email into words
    words = email.split()
    for w in words:
        # strip punctuation
        w = w.strip('\'"?,.')
        # check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        # ignore if it is a stop word or does not start with an alphabet
        if (w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())

    return featureVector

def main(argv):
    inputFile = argv[1]

    # update the global stopWords list
    stopWords = getStopWordList()

    fr = open(inputFile, 'rU')

    # read the emails and process one by one
    line = fr.readline()
    while line:
        processedEmail = nltkpreprocessor.processEmail(line)
        featureVector = getFeatureVector(processedEmail)
        print featureVector
        line = fr.readline()

    # close file handle
    fr.close()

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        printUsage()
    else:
        main(sys.argv)
