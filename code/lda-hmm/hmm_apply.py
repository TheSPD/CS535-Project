from pymongo import MongoClient
import pprint
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.externals import joblib
from hmmlearn.hmm import MultinomialHMM
import numpy as np

n_top_words = 21
start_date = 3
end_date = 10 #13

def top_words(model, feature_names, n_top_words):
	topics = []
	for topic_idx, topic in enumerate(model.components_):
		
		print("Topic #%d:" % topic_idx)
		try:
			print([i for i in topic.argsort()[:-n_top_words - 1:-1]])
			topics.append(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]).replace("rt ",""))
		except:
			pass
		print()
	return topics
  

lda = []
tf_vectorizer = []
tf = []

for i in range(start_date, end_date):
	lda.append(joblib.load('/freespace/local/sp1467/pickles/lda_11_{:0>2}.pkl'.format(i)))
	tf_vectorizer.append(joblib.load('/freespace/local/sp1467/pickles/tf_vectorizer_11_{:0>2}.pkl'.format(i)))
	tf.append(joblib.load('/freespace/local/sp1467/pickles/tf_11_{:0>2}.pkl'.format(i)))

print("\nTopics in LDA model:")

day_topics = []
for i in range(len(lda)):
	tf_feature_names = tf_vectorizer[i].get_feature_names()
	day_topics.append(top_words(lda[i], tf_feature_names, n_top_words))

overall_tf_vectorizer = CountVectorizer()
overall_tf_vectorizer.fit([topic for day in day_topics for topic in day])
tf = [overall_tf_vectorizer.transform(day) for day in day_topics]
	
MultinomialHMModel = []
for i in range(len(overall_tf_vectorizer.get_feature_names())):
	X = [[topic.toarray()[0][i] for topic in day] for day in tf]
	MultinomialHMModel.append(MultinomialHMM(n_components=1))
	print overall_tf_vectorizer.get_feature_names()[i]
	MultinomialHMModel[i].fit(np.array(X))




