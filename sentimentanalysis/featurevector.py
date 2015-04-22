#!/usr/bin/python

import nltk
import nltkpreprocessor
import re
import sys

# initialize featureList and stopWords
featureList = []
stopWords = []

def printUsage():
    print "featurevector.py <inputEmailFile> <isInputFileLabeled>"
    print "e.g."
    print "featurevector.py emails.txt false"
    print "featurevector.py processedlabels.txt true"

def updateStopWordList():
    global stopWords
    stopWords = nltk.corpus.stopwords.words('english')
    # append any other stop words
    # stopWords.append('word')

def getFeatureVector(email):
    global stopWords
    featureVector = []

    # split email into words
    words = email.split()
    for w in words:
        # strip punctuation
        w = w.strip('\'"?,.')
        # check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)

        # ignore if it is a stop word or does not start with an alphabet
        if (val is None or unicode(w, 'utf-8') in stopWords):
            continue
        else:
            featureVector.append(w.lower())

    return featureVector

def getFeatures(email):
    global featureList
    features = {}

    emailWords = set(email)
    for word in featureList:
        features['contains(%s)' % word] = (word in emailWords)

    return features

def processRawEmails(inputFile):
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

def processLabeledEmails(inputFile):

    emailSentiments = []

    fr = open(inputFile, 'rU')
    line = fr.readline()
    while line:
        emailItems = line.split('\t')
        emailLine = emailItems[0]
        sentiment = emailItems[1].rstrip()

        processedEmail = nltkpreprocessor.processEmail(emailLine)
        featureVector = getFeatureVector(processedEmail)
        emailSentiments.append((featureVector, sentiment))
        global featureList
        featureList.extend(featureVector)
        line = fr.readline()

    # close file handle
    fr.close()

    # remove dupes from featureList
    featureList = list(set(featureList))

    # generate training set
    emailTrainingSet = nltk.classify.util.apply_features(getFeatures, emailSentiments)

    # train the claffifier
    classifier = nltk.NaiveBayesClassifier.train(emailTrainingSet)

    return classifier

def testClassifier(classifier):
    testEmails = ['class www.berkeley.edu link',
                  'some mailto:bear@berkeley.edu link',
                  'sample email']

    for testEmail in testEmails:
        processedEmail = nltkpreprocessor.processEmail(testEmail)
        print classifier.classify(getFeatures(getFeatureVector(processedEmail)))

    classifier.show_most_informative_features(10)

def main(argv):
    inputFile = argv[1]
    isInputLabeled = ((argv[2]).lower() == 'true')

    # update the global stopWords list
    updateStopWordList()

    if (isInputLabeled):
        classifier = processLabeledEmails(inputFile)

        # testing
        testClassifier(classifier)
    else:
        processRawEmails(inputFile)


if __name__ == "__main__":
    if (len(sys.argv) != 3):
        printUsage()
    else:
        main(sys.argv)
