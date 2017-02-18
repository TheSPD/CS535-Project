import pprint
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.externals import joblib
from scipy.sparse import csr_matrix
import numpy as np

dates = []
for i in range(7,13):
	dates.append("{0:0>2}".format(i))

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()
    
def save_sparse_csr(filename,array):
    np.savez(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )

def load_sparse_csr(filename):
    loader = np.load(filename)
    return csr_matrix((  loader['data'], loader['indices'], loader['indptr']),
                         shape = loader['shape'])

tf_idf_vectorizer = []
tf_idf = []
brands = [('donald','trump'),('hillary','clinton')]

start_date = 3
end_date = 13

# Create Brand tf-idf vectors
for i in range(start_date, end_date):
	t = time()
	print 'Converting to Brands...'
	brand_vectors = []
	tf_idf_vectorizer.append(joblib.load('/freespace/local/sp1467/NO_URLpickles/tf_idf_vectorizer_11_{:0>2}.pkl'.format(i)))
	tf_idf.append(joblib.load('/freespace/local/sp1467/NO_URLpickles/tf_idf_11_{:0>2}.pkl'.format(i)))
	t0, t1 = brands[0]
	c0, c1 = brands[1]
	
	for d in tf_idf[i-start_date]:
	    brand_vector = [0, 0]
	    if(d.toarray()[0][tf_idf_vectorizer[i-start_date].vocabulary_[t0]] > 0 or d.toarray()[0][tf_idf_vectorizer[i-start_date].vocabulary_[t1]] > 0):
	        brand_vector[0] = 1
	    if(d.toarray()[0][tf_idf_vectorizer[i-start_date].vocabulary_[c0]] > 0 or d.toarray()[0][tf_idf_vectorizer[i-start_date].vocabulary_[c1]] > 0):
	        brand_vector[1] = 1
	    brand_vectors.append([float(b)/sum(brand_vector) for b in brand_vector])
	
	save_sparse_csr('/freespace/local/sp1467/NO_URLpickles/brands_11_{:0>2}.pkl'.format(i), csr_matrix(brand_vectors))
	print("done in %0.3f s." % (time() - t))



	
