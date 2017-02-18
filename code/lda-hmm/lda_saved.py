from pymongo import MongoClient
import pprint
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.externals import joblib
from hmmlearn.hmm import MultinomialHMM

n_top_words = 20
start_date = 3
end_date = 13

def top_words(model, feature_names, n_top_words):
	topics = []
	for topic_idx, topic in enumerate(model.components_):
		
		print("Topic #%d:" % topic_idx)
		try:
			print([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
			topics.append([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
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

for i in range(len(lda)):
	tf_feature_names = tf_vectorizer[i].get_feature_names()
	print(top_words(lda[i], tf_feature_names, n_top_words))
	print('Day : ' + str(i))
