from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import json
from collections import Counter

class bagOfWords():
	"""docstring for bagOfWords"""
	tknzr = TweetTokenizer()
	stops = set(stopwords.words('english'))
	stemmer = SnowballStemmer("english")

	
	def __init__(self, fileName):
		self.fileName = fileName
		self.tweetText = []
		# self.train_data_features = []
		
	
	def textToWords(self, text):
		return self.tknzr.tokenize(text)

	def removeStopWords(self, words):
		return [w for w in words if not w in self.stops]

	def stemWords(self, words):
		return [self.stemmer.stem(w) for w in words]

	def process(self):
		count = 0
		
		with open(self.fileName) as f:
			i = 0
			tweets = []
			for line in f:
				if(line != '\n'):
					tweets.append(json.loads(line))
					text = tweets[i]['text']

					#Tokenize text 
					words = self.textToWords(text)

					#Text only
					# letters_only = [re.sub("[^a-zA-Z0-9]", " ", word) for word in word]

					#Stem words		
					stemmed_words = self.stemWords(words)

					#Remove stop words
					meaningful_words = self.removeStopWords(stemmed_words)

					self.tweetText.append(' '.join(meaningful_words))

					# print text, words, meaningful_words, stemmed_words
					# print Counter(meaningful_words)
					i +=1
	def createBOW(self):
		from sklearn.feature_extraction.text import CountVectorizer
		vectorizer = CountVectorizer(analyzer = "word",   
                             tokenizer = None,    
                             preprocessor = None, 
                             stop_words = None,   
                             max_features = 5000) 
		self.train_data_features = vectorizer.fit_transform(self.tweetText)
		# self.train_data_features = train_data_features.toarray()
		print self.train_data_features.toarray()

		return


BOW = bagOfWords('../streaming_data/Twitter.Elections.Data.20161101-012808.json')

BOW.process()

BOW.createBOW()
