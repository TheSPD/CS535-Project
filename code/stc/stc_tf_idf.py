from pymongo import MongoClient
import pprint
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.externals import joblib
import random

dates = []
for i in range(3,13):
	dates.append("{0:0>2}".format(i))

#MongoDB connection
client = MongoClient()
db = client.tweet_db

'''
#Fetch corpora from DB 
sentences_day = []
for i in range(len(dates)):
	collection = db['tweets_11_' + dates[i]]

	print("Reading data from DB...")
	t0 = time()
	sentences = [[word for word in doc['words'] if len(word) != 1 and word[0].isalnum() and word[:5] != 'https'] for doc in collection.find()]

	print("done in %0.3fs." % (time() - t0))
	
	sentences_day.append([' '.join(s) for s in sentences])

#Create Vocabulary
vocab = {}
for sentences in sentences_day:
    for s in sentences:
        for w in s.split(' '):
            if w in vocab:
                vocab[w] += 1
            else:
                vocab[w] = 1

#Refine Vocabulary(Frequency < 50 removed)
i = 0
vocab_words = {}
for w in vocab:
    if vocab[w] > 50:
        vocab_words[w] = i
        i += 1

# Save Vocabulary
joblib.dump(vocab_words, '/freespace/local/sp1467/NO_URLpickles/vocab_stc.pkl') 
'''
#Load Vocabulary
vocab_words = joblib.load('/freespace/local/sp1467/NO_URLpickles/vocab_stc.pkl')        

print("Extracting tf-idf features for STC...")
tf_idf_vectorizer = TfidfVectorizer(vocabulary=vocab_words)


for i in range(len(dates)):
    print("Extracting from DB...")
    t0 = time()
    collection = db['tweets_11_' + dates[i]]
    
    # Removing tweets without the mention of either brands(Hillary or Trump)
    sentences = [[word for word in doc['words'] if len(word) != 1 and word[0].isalnum()] for doc in collection.find() if 'donald' in doc['words'] or 'trump' in doc['words'] or 'hillary' in doc['words'] or 'clinton' in doc['words']]
    
    # Random sample
    numDocs = len(sentences)
    randSample = random.sample(range(numDocs), 10000)
    sentences = [sentences[r] for r in randSample]
    # Random sample
    
    tf_idf = tf_idf_vectorizer.fit_transform([' '.join(s) for s in sentences])
    print("done in %0.3fs." % (time() - t0))
    print("Saving model to file...")
    t0 = time()

    joblib.dump(tf_idf_vectorizer, '/freespace/local/sp1467/NO_URLpickles/tf_idf_vectorizer_11_' + dates[i] + '.pkl')
    joblib.dump(tf_idf, '/freespace/local/sp1467/NO_URLpickles/tf_idf_11_' + dates[i] + '.pkl')
    print("done in %0.3fs." % (time() - t0))

#lda = joblib.load('lda_11_03.pkl')
#tf_vectorizer = joblib.load('tf_vectorizer_11_03.pkl')
#tf = joblib.load('tf_11_03.pkl')



	
