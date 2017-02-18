from pymongo import MongoClient
import pprint
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation


dates = []
for i in range(12,14):
	dates.append("{0:0>2}".format(i))

#MongoDB connection
client = MongoClient()
db = client.tweet_db

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

for i in range(len(dates)):
	collection = db['tweets_11_' + dates[i]]

	print("Extracting tf features for LDA...")
	t0 = time()
	sentences = [[word for word in doc['words'] if len(word) != 1 and word[0].isalnum()] for doc in collection.find()]

	n_features = 1000
	n_topics = 10
	n_top_words = 20
	print("done in %0.3fs." % (time() - t0))
	t0 = time()
	# Use tf (raw term count) features for LDA.
	print("Extracting tf features for LDA...")
	tf_vectorizer = CountVectorizer(max_df=0.80, min_df=50)

	tf = tf_vectorizer.fit_transform([' '.join(s) for s in sentences])
	print("done in %0.3fs." % (time() - t0))
	t0 = time()
	print("Fitting LDA models with tf features, "
	      "n_samples=%d and n_features=%d..."
	      % (len(sentences), n_features))
	lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
		                        learning_method='online',
		                        learning_offset=50.,
		                        random_state=0)
	lda.fit(tf)
	print("done in %0.3fs." % (time() - t0))

	print("\nTopics in LDA model:")
	tf_feature_names = tf_vectorizer.get_feature_names()
	print_top_words(lda, tf_feature_names, n_top_words)

	from sklearn.externals import joblib
	joblib.dump(lda, 'lda_11_' + dates[i] + '.pkl')
	joblib.dump(tf_vectorizer, 'tf_vectorizer_11_' + dates[i] + '.pkl')
	joblib.dump(tf, 'tf_11_' + dates[i] + '.pkl')

#lda = joblib.load('lda_11_03.pkl')
#tf_vectorizer = joblib.load('tf_vectorizer_11_03.pkl')
#tf = joblib.load('tf_11_03.pkl')



	
