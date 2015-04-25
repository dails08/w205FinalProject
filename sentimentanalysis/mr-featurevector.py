import nltk
import re
from mrjob.job import MRJob

class MRFeatureVector(MRJob):

    def mapper(self, _, line):
        featureVector = []
        stopWords = nltk.corpus.stopwords.words('english')

        # convert [InternetShortcut] URL=www.*, http://* to PERSONALURL
        line = re.sub('((URL=www\.[^\s]+)|(URL=http://[^\s]+))','PERSONALURL',line)

        # convert [InternetShortcut] URL=mailto to BUSINESSURL
        line = re.sub('URL=mailto:[^\s]+','BUSINESSURL',line)

        # remove email addresses
        line = re.sub('[^\s]+@[^\s]+','',line)

        # remove strings that start with </
        line = re.sub('</[^\s]+','',line)

        # remove numbers
        line = re.sub('\S*\d\S*','', line)

        # remove white spaces
        line = re.sub('[\s]+', ' ', line)

        # replace #word with word
        line = re.sub(r'#([^\s]+)', r'\1', line)

        # convert to lower case
        line = line.lower()

        # trim
        line = line.strip('\'"')

        # split input into words
        words = line.split()
        for word in words:
            # strip punctuation
            word = word.strip('\'"?,.')

            # ignore if word is a stop word or is not alpha-numeric
            if (re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", word) is None or word in stopWords):
                continue
            else:
                featureVector.append(word.lower())

        # remove proper nouns (NNP, NNPS), personal pronouns (PRP), and possessive pronouns (PRP$)
        excludeTags = ['NNP', 'NNPS', 'PRP', 'PRP$']
        wordTags = nltk.pos_tag(featureVector)
        featureVector = [word[0] for word in wordTags if word[1] not in excludeTags]
        for feature in featureVector:
            yield (feature.lower(), 1)

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == '__main__':
    MRFeatureVector.run()
