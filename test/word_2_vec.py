from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import json
from collections import Counter

class bagOfWords(object):
    """docstring for bagOfWords"""
    tknzr = TweetTokenizer()
    stops = set(stopwords.words('english'))
    stemmer = SnowballStemmer("english")

    def __init__(self, fileName):
        self.fileName = fileName
        self.tweetText = []
        # self.train_data_features = []
    """
    "textToWords
    "tokenizes text into separate words
    "@params 
    "text - Input text
    "@returns 
    "words - tokenized words
    """
    def textToWords(self, text):
        return self.tknzr.tokenize(text)

    def removeStopWords(self, words):
        return [w for w in words if w not in self.stops]

    def stemWords(self, words):
        return [self.stemmer.stem(w) for w in words]

    def process(self):
        with open(self.fileName) as f:
            i = 0
            tweets = []
            for line in f:
                if(line != '\n'):
                    try:
                        tweets.append(json.loads(line))
                        text = tweets[i]['text']

                        words = self.textToWords(text)

                        stemmed_words = self.stemWords(words)

                        meaningful_words = self.removeStopWords(stemmed_words)

                        self.tweetText.append(' '.join(meaningful_words))
                        i += 1
                    except Exception as e:
                        print "Except at : " + i + "\n" + e
                        pass

    """
    "createBOW
    "@params:
    ""
    """
    def createBOW(self):
        from sklearn.feature_extraction.text import CountVectorizer
        vectorizer = CountVectorizer(analyzer="word",
                                     tokenizer=None,
                                     preprocessor=None,
                                     stop_words=None,
                                     max_features=5000)
        self.train_data_features = vectorizer.fit_transform(self.tweetText)
        # self.train_data_features = train_data_features.toarray()
        print self.train_data_features.toarray()

        return



BOW = bagOfWords('../streaming_data/test.json')

BOW.process()

BOW.createBOW()