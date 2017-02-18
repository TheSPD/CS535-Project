import pprint
from time import time

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.externals import joblib
from scipy.sparse import csr_matrix
import numpy as np
import random
    
def save_sparse_csr(filename,array):
    np.savez(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )

def load_sparse_csr(filename):
    loader = np.load(filename)
    return csr_matrix((  loader['data'], loader['indices'], loader['indptr']),
                         shape = loader['shape'])

start_date = 3
end_date = 13
tf_idf_vectorizer = joblib.load('/freespace/local/sp1467/NO_URLpickles/tf_idf_vectorizer_11_03.pkl')
brands = [('donald','trump'),('hillary','clinton')]

k = 10                  #Number of Topics
L = 2                   #Number of brands
g = len(tf_idf_vectorizer.vocabulary_) 
min_num = 0.0
max_num = 1.0

# Loop to initialize beta, phi, theta, z, r
for t in range(start_date, end_date):
    '''
    For each time slice set the initial params and load the known entities
    '''
    
    t0 = time()
    
    tf_idf = joblib.load('/freespace/local/sp1467/NO_URLpickles/tf_idf_11_{:0>2}.pkl'.format(t))
	
    print 'TF-IDF : ', tf_idf.shape
	
    brand_vectors = load_sparse_csr('/freespace/local/sp1467/NO_URLpickles/brands_11_{:0>2}.pkl.npz'.format(t))
	
    print 'Brand Vectors : ', brand_vectors.shape
	
    beta = np.random.uniform(min_num, max_num, (k, g-1))
    print 'Beta : ', beta.shape
    
    beta = [np.append(np.append([min_num],np.sort(beta_k)),[max_num]) for beta_k in beta]
    beta = [[beta_k[i+1] - beta_k[i] for i in range(g)] for beta_k in beta]
	
    print 'Beta : ', np.array(beta).shape
	
    phi = np.random.uniform(min_num, max_num, (k, L-1))
    print 'Phi : ', phi.shape
    
    phi = [np.append(np.append([min_num],np.sort(phi_k)),[max_num]) for phi_k in phi]
    phi = [[phi_k[l+1] - phi_k[l] for l in range(L)] for phi_k in phi]
	
    print 'Phi : ', np.array(phi).shape
	
    D = tf_idf.shape[0]

    theta_documents = []
    z_words_documents = []
    r_words_documents = []
    for d in range(D):
        theta = np.random.uniform(min_num, max_num, k)
        theta_documents.append(np.array(theta))
        z_words = []
        N = len(tf_idf[d].nonzero()[0])
        for n in range(N):
            z = np.random.uniform(min_num, max_num, k)
            z_words.append(np.array(z))
        z_words_documents.append(np.array(z_words))
        
        r_words = []
        for l in range(L):
            r = np.random.uniform(min_num, max_num, k)
            r_words.append(np.array(r))
        r_words_documents.append(np.array(r_words))

    print 'Theta :', np.array(theta_documents).shape

    print 'Z : ', np.array(z_words_documents).shape

    print 'R : ', np.array(r_words_documents).shape

    print 'Day {0} complete, time taken '.format(t), time() - t0
    
    joblib.dump(beta, '/freespace/local/sp1467/NO_URLpickles/beta_11_{:0>2}.pkl'.format(t))
    joblib.dump(phi, '/freespace/local/sp1467/NO_URLpickles/phi_11_{:0>2}.pkl'.format(t))
    joblib.dump(np.array(theta_documents), '/freespace/local/sp1467/NO_URLpickles/theta_documents_11_{:0>2}.pkl'.format(t))
    joblib.dump(np.array(z_words_documents), '/freespace/local/sp1467/NO_URLpickles/z_words_documents_11_{:0>2}.pkl'.format(t))
    joblib.dump(np.array(r_words_documents), '/freespace/local/sp1467/NO_URLpickles/r_words_documents_11_{:0>2}.pkl'.format(t))

