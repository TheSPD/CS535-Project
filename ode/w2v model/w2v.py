import gensim, logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import pandas as pd
import nltk
import json
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import os.path
import pickle
import pymongo
from pymongo import MongoClient

# Variable Initialization
tweets = []
sentences=[]
words=[]
sentence=[]
i=0
vocab=[]
#text;

stemmer = SnowballStemmer("english")
tknzr = TweetTokenizer()
stops = set(stopwords.words('english'))

class word2vec():

	def __init__(self, dirname,modelFileName):
		self.dirname = dirname
		self.fname=[]
		self.modelFileName=os.path.join(self.dirname, modelFileName)
        

	def textToWords(self, text):
		return tknzr.tokenize(text)

	def removeStopWords(self, words):
		return [w for w in words if not w in stops]

	def stemWords(self, words):
		return [stemmer.stem(w) for w in words]

	# read the entire file into a python array
	
	def preprocess(self):
		
						
		client = MongoClient()
		db = client.local
		collection = db.tweets_11_12
		sentences=([[word for word in doc['words'] if len(word) != 1 and word[0].isalnum()] for doc in collection.find()])
		print(sentences)

		self.model = gensim.models.Word2Vec(sentences, min_count=50,size=200,sg=1) 

		vocab_dict={}
		w2v_doc_matrix= [[0 for col in range(200)] for row in range(0,len(self.model.vocab))]
		count=0
		for i in self.model.vocab:
			print(i,self.model[i])
			vocab_dict[count]=i
			w2v_doc_matrix[count]=self.model[i]
			count=count+1


		pickle.dump(vocab_dict, open("tweets_11_12_vocab.txt", "wb" ))
		pickle.dump(w2v_doc_matrix, open("tweets_11_12.txt", "wb" ))



	def process(self):
		#Checks if a word vector file is created
		# yes: loadsthe existing model and trains with more sentence.
		# no: fits the model,and saves the model.
		#self.getFile(self.dirname)
		#print self.fname

		self.preprocess()
			
	

w2v = word2vec("","")
w2v.process()
