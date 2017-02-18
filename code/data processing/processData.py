from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import json

class processData(object):
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

    def getTweets(self):
        return self.tweetText

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

                        self.tweetText.append({"words" : meaningful_words, "time" : tweets[i]['created_at'], "tweet_id" : tweets[i]['id_str']})
                        i += 1
                    except Exception as e:
                        print 'Exception : ' + str(e)
                        pass


