import gensim, logging
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

		pickle.dump(sentences, open("affinity_11_12.txt", "wb" ))



	def process(self):
		#Checks if a word vector file is created
		# yes: loadsthe existing model and trains with more sentence.
		# no: fits the model,and saves the model.
		#self.getFile(self.dirname)
		#print self.fname

		self.preprocess()


w2v = word2vec("","")
w2v.process()


#import pickle
#from sklearn.cluster import AffinityPropagation
#X = pickle.load(open("fishers_11_04.txt",'rb'))
#af = AffinityPropagation().fit(list(X.values()))
#exemplars = af.cluster_centers_indices_


#import pickle
#from sklearn.cluster import AffinityPropagation
#X = pickle.load(open("tweets_11_04.txt",'rb'))
#af = AffinityPropagation(preference=-50).fit(list(X.values()))
#exemplars = af.cluster_centers_indices_


#import pickle
#twits      = pickle.load(open("affinity_11_04.txt",'rb'))
#twit_cnt = len(twits)
#
#kill twits
#
#dictionary = pickle.load(open("tweets_11_04_vocab.txt",'rb'))
#dict_cnt = len(dictionary.keys())
#
#affinity_matrix= [[0 for col in range(twit_cnt)] for row in range(twit_cnt)]
#for i in range(0,len(twits)):
#    for k in range(0,len(twits)):
#        cost = 0
#        twiti = twits[i]
#        twitk = twits[k]
#        leni = len(twiti)
#        lenk = len(twitk)
#        for w in range(0,leni):
#            for z in range(0,lenk):
#                wordw = twiti[w]
#                wordz = twitk[z]
#                if wordi in wordk or wordk in wordi:
#                    cost = cost - math.log(lenk)
#                else:
#                    cost = cost + math.log(dict_cnt)
#        affinity_matrix[i,k] = cost
