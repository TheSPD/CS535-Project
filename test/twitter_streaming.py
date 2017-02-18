

import tweepy
# from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import re
from collections import Counter


#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
	# vectorizer = CountVectorizer(min_df=1)
	tknzr = TweetTokenizer()
	stops = set(stopwords.words('english'))
	stemmer = SnowballStemmer("english")

	def textToWords(self, text):
		return self.tknzr.tokenize(text)

	def removeStopWords(self, words):
		return [w for w in words if not w in self.stops]

	def stemWords(self, words):
		return [self.stemmer.stem(w) for w in words]

	def on_status(self, status):

		#Plain text
		text = status.text

		#Tokenize text 
		words = self.textToWords(text)

		#Text only
		# letters_only = [re.sub("[^a-zA-Z0-9]", " ", word) for word in word]

		#Remove stop words
		meaningful_words = self.removeStopWords(words)

		#Stem words		
		stemmed_words = self.stemWords(meaningful_words)

		print text, words, meaningful_words, stemmed_words
		print Counter(stemmed_words)
		#TODO -- Bag of Words
		
		# X = self.vectorizer.fit_transform([status.text])
		# print status.text
		# analyze = self.vectorizer.build_analyzer()
		# print analyze
		# print self.vectorizer.get_feature_names()
		

	def on_error(self, status_code):
		if status_code == 420:
			#returning False in on_data disconnects the stream
			return False

#Credentials 
consumer_key = "HDJNJYmgnkecU87UvAWSwNDdK"
consumer_secret = "ADpOXeHvuh6uiG0xieweuCXEQD2a7UQqLEAuov1QTrwDhtRNkI"

access_token = "215905178-burCGOJ9LhFAIL4Um3DXB1luN4fYYMtMWPyIr5MM"
access_token_secret = "4lSni5fHILbZspY056rzhZSTWkgcCIglpuhlwuNKUQ3DH"


#Using the credentials for tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Start the streaming
api = tweepy.API(auth)
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())

#filter
myStream.filter(languages = ["en"], track=['trump'])


# from nltk.twitter import Twitter
# tw = Twitter()
# tw.tweets(keywords='love, hate', limit=10) #sample from the public stream