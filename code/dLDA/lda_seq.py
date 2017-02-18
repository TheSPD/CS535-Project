from gensim import corpora
from gensim.models.ldaseqmodel import LdaSeqModel
from gensim.models.ldamodel import LdaModel
from pymongo import MongoClient
from sklearn.externals import joblib
from time import time
import itertools

dates = []
for i in range(3,13):
	dates.append("{0:0>2}".format(i))

#MongoDB connection
client = MongoClient()
db = client.tweet_db

sentences = []
sentences_len = []

vocab_words = joblib.load('/freespace/local/sp1467/pickles/vocab_stc.pkl')

K = 10

for w in vocab_words:
    if w[:5] != 'https' and w != '': # Removing links
        sentences.append([w])
dictionary = corpora.Dictionary(sentences)
print len(sentences)
        
print("Dumping Dictionary for LDA...")
t0 = time()	
dictionary.save('/freespace/local/sp1467/NO_URLgensimDumps/vocab_lda.dict')  # store the dictionary, for future reference
print("done in %0.3fs." % (time() - t0))

corpus = []
for i in range(len(dates)):
	collection = db['tweets_11_' + dates[i]]
	
	print("Converting Day {0} to gensims BleiCorpus and saving for LDA...".format(dates[i]))
	t0 = time()
	sentences_time = [[word for word in doc['words'] if len(word) != 1 and word[0].isalnum()] for doc in collection.find()]
	corpus_time = [dictionary.doc2bow(s) for s in sentences_time]
	corpora.BleiCorpus.save_corpus('/freespace/local/sp1467/NO_URLgensimDumps/corpora_lda_{:0>2}.lda-c'.format(dates[i]), corpus_time)
		
	print("done in %0.3fs." % (time() - t0))


print("Appending corpora and calculaing lengths for each corpus...")
t0 = time()
corpus = corpora.BleiCorpus('/freespace/local/sp1467/NO_URLgensimDumps/corpora_lda_{:0>2}.lda-c'.format(3))
sentences_len.append(len(list(corpus))) 

print("done in %0.3fs." % (time() - t0))
for i in range(len(dates[1:])):
    t0 = time()
    corpus_time = corpora.BleiCorpus('/freespace/local/sp1467/NO_URLgensimDumps/corpora_lda_{:0>2}.lda-c'.format(dates[1:][i]))
    sentences_len.append(len(list(corpus_time)))
    corpus = itertools.chain(corpus, corpus_time)
    print("done in %0.3fs." % (time() - t0))

t0 = time()
print 'Fitting LDA'
ldaseq = LdaSeqModel(corpus=corpus, time_slice= sentences_len, num_topics=K, initialize='gensim', sstats=None, lda_model=None, obs_variance=0.5, chain_variance=0.005, passes=10, random_state=None, lda_inference_max_iter=25, em_min_iter=6, em_max_iter=20, chunksize=100)
ldaseq.save("/freespace/local/sp1467/NO_URLgensimDumps/ldaseq")
print("done in %0.3fs." % (time() - t0))

dictionary = corpora.Dictionary.load('/freespace/local/sp1467/NO_URLgensimDumps/vocab_lda.dict')
ldaseq = LdaSeqModel.load('/freespace/local/sp1467/NO_URLgensimDumps/ldaseq')
for t in range(len(dates)):
    print [[dictionary[int(word)] for word, freq in topic] for topic in ldaseq.print_topics(time=t, top_terms=20)]
    
