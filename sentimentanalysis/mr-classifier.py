import nltk
import pickle
import re
import os.path
from mrjob.job import MRJob
from mrjob.step import MRStep

# initialize stopWords
stopWords = nltk.corpus.stopwords.words('english')

# load the classifier
classifierPickle = open('email_classifier.pickle')
classifier = pickle.load(classifierPickle)

# initialize feature list
featureList = []

# get features from the feature list file
featureFile = open('reprocessed_mr_featurevector.txt', 'r')
feature = featureFile.readline()
while feature:
    featureList.append(feature.split('\t')[0])
    feature = featureFile.readline()

# close the feature list file
featureFile.close()


def processEmail(email):
    # convert [InternetShortcut] URL=www.* or http://* to PERSONALURL
    email = re.sub('((URL=www\.[^\s]+)|(URL=http://[^\s]+))','PERSONALURL',email)
    # convert [InternetShortcut] URL=mailto to BUSINESSURL
    email = re.sub('URL=mailto:[^\s]+','BUSINESSURL',email)
    # remove email addresses
    email = re.sub('[^\s]+@[^\s]+','',email)
    # remove strings that start with </
    email = re.sub('</[^\s]+','',email)
    # remove numbers
    email = re.sub('\S*\d\S*','', email)
    # remove additional white spaces
    email = re.sub('[\s]+', ' ', email)
    # replace #word with word
    email = re.sub(r'#([^\s]+)', r'\1', email)
    # convert to lower case
    email = email.lower()
    # trim
    email = email.strip('\'"')

    return email


def getFeatureVector(email):

    # split email into words
    words = email.split()

    # initialize feature vector list
    featureVector = []

    for w in words:
        # strip punctuation
        w = w.strip('\'"?,.')

        # check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)

        # ignore if it is a stop word or does not start with an alphabet
        if (val is None or w in stopWords):
            continue
        else:
            featureVector.append(w.lower())

    # remove proper nouns (NNP, NNPS), personal pronouns (PRP), possessive pronouns (PRP$)
    excludeTags = ['NNP', 'NNPS', 'PRP', 'PRP$']
    wordTags = nltk.pos_tag(featureVector)
    featureVector = [word[0] for word in wordTags if word[1] not in excludeTags]

    return featureVector

def getFeatures(email):
    # initialize email features
    features = {}

    # initialize unique email elements
    email = set(email)

    # extract features
    for word in featureList:
        features['contains(%s)' % word] = (word in email)

    return features





class MREmailClassifier(MRJob):


    def mapper(self, _, line):
        if line is None or len(line)==0:
            yield (None, None)

        # process input to get features
        processedEmail = processEmail(line)
        featureVector = getFeatureVector(processedEmail)
        features = getFeatures(featureVector)

        # classify the input
        sentiment = classifier.classify(features)

        # format the output
        #output = line + "\t" + sentiment
        #output = "{}\t{}".format(line, sentiment)
        yield (sentiment, 1)

    def reducer(self, key, values):
        yield key, sum(values)


    #def steps(self):
        #return [MRStep(mapper_init=self.get_helper_files,
                #mapper=self.mapper,
                #reducer=self.reducer)]



if __name__ == '__main__':
    MREmailClassifier.run()
