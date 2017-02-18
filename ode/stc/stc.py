
from time import time
t0 = time()
import pprint
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.externals import joblib
from scipy.sparse import csr_matrix
import numpy as np
from scipy import optimize

print 'Time taken to load libraries : ', time()-t0
    
def save_sparse_csr(filename,array):
    np.savez(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )

def load_sparse_csr(filename):
    loader = np.load(filename)
    return csr_matrix((  loader['data'], loader['indices'], loader['indptr']),
                         shape = loader['shape'])

def proj_unit_simplex(y):
    u = np.sort(y)
    u = u[::-1]
    rho_vec = [j for j in range(len(u)) if ((u[j] + float(1 - np.sum(u[0:j+1]))/(j+1)) > 0)]
    rho = rho_vec[len(rho_vec)-1]
    lam = float(1-np.sum(u[0:rho+1]))/(rho+1)
    return [y_i + lam if y_i + lam > 0 else 0 for y_i in y]

start_date = 3
end_date = 13
tf_idf_vectorizer = joblib.load('/freespace/local/sp1467/NO_URLpickles/tf_idf_vectorizer_11_03.pkl')
brands = [('donald','trump'),('hillary','clinton')]

K = 10                  #Number of Topics
L = 2                   #Number of brands
G = len(tf_idf_vectorizer.vocabulary_) 
min_num = 0.0
max_num = 10.0 ** 6
iterations_inner = 2 #Coordinate descent iterations
iterations_outer = 2 #E-M Algorithms

#Hyperparameters
rho_1 = 1.0
sigma_1 = 1.0
rho_2 = 1.0
sigma_2 = 1.0
delta_1 = 1.0
pi_1 = 1.0
delta_2 = 1.0
pi_2 = 1.0
tau_0 = 5.0
tau = 10.0
epsilon = 1.0 
M = 1000

for t in range(start_date, end_date):
    '''
    For each time slice
    '''
    t0 = time()
    w = joblib.load('/freespace/local/sp1467/NO_URLpickles/tf_idf_11_{:0>2}.pkl'.format(t))
    g = load_sparse_csr('/freespace/local/sp1467/NO_URLpickles/brands_11_{:0>2}.pkl.npz'.format(t))
    beta = np.array(joblib.load('/freespace/local/sp1467/NO_URLpickles/beta_11_{0:0>2}.pkl'.format(t)))
    phi = np.array(joblib.load('/freespace/local/sp1467/NO_URLpickles/phi_11_{0:0>2}.pkl'.format(t)))
    if t != start_date:
        beta_prev = joblib.load('/freespace/local/sp1467/NO_URLpickles_5_iter/beta_trained_11_{0:0>2}.pkl'.format(t-1))
        phi_prev = joblib.load('/freespace/local/sp1467/NO_URLpickles_5_iter/phi_trained_11_{0:0>2}.pkl'.format(t-1))
    theta = joblib.load('/freespace/local/sp1467/NO_URLpickles/theta_documents_11_{0:0>2}.pkl'.format(t))
    z = joblib.load('/freespace/local/sp1467/NO_URLpickles/z_words_documents_11_{0:0>2}.pkl'.format(t))
    r = joblib.load('/freespace/local/sp1467/NO_URLpickles/r_words_documents_11_{0:0>2}.pkl'.format(t))
    
    print 'Time taken to load parameters : ', time()-t0
    t0 = time()
    D = w.shape[0]
    
    print 'Coordinate Descent : '

    for i_outer in range(iterations_outer):
        
        t2 = time()
        
        # Step 1
        # Fix beta & phi and optimize theta, z and r        
        for i_inner in range(iterations_inner):
            
            # Step 1.a
            # Fix theta and optimize z and r
            print 'Day :', t, ' OI : ', i_outer ,' of ', iterations_outer, ' II :', i_inner, ' of ', iterations_inner, ' Step 1.a'
            for d in range(D):
                N = len(w[d].nonzero()[0])
                for n in range(N):
                    nz_n = np.sort(w[d].nonzero()[1])[n]
                    for k in range(K):
                        z[d][n][k] = max(0, (w[d].toarray()[0][nz_n]*beta[k][nz_n] + theta[d][k] - beta[k][nz_n] * sum([z[d][n][j]*beta[j][nz_n] for j in range(K) if j != k]) - (rho_1/2))/((beta[k][nz_n] ** 2) + sigma_1))
                for l in range(L):
                    for k in range(K):
                        r[d][l][k] = max(0, (g[d].toarray()[0][l]*phi[k][l] + theta[d][k] - phi[k][l] * sum([r[d][l][j]*phi[j][l] for j in range(K) if j != k]) - (rho_2/2))/((phi[k][l] ** 2) + sigma_2))
    
            
            # Step 1.b
            # Fix z & r and optimize theta
            # lambda = gamma
            print 'Day :', t, ' OI : ', i_outer ,' of ', iterations_outer, ' II :', i_inner, ' of ', iterations_inner, ' Step 1.b'
            for d in range(D):
                #print 'Day :', t, ' OI : ', i_outer ,' of ', iterations_outer, ' II :', i_inner, ' of ', iterations_inner, ' : Document ', d, ' of ', D, ' Step 1.b'
                N = len(w[d].nonzero()[0])
                for k in range(K):
                    theta[d][k] = 1.0/(1+N) * sum([z[d][n][k] for n in range(N)])
        
        # Step 2
        # Fix theta, z & r and optimize beta and phi
        
        '''
        #def log_poisson_online(optimizer, delta, pi):
        #    optimizer = optimizer.reshape(K, G)
        #    logPoisson = 0
        #    for d in range(D):
        #        N = len(w[d].nonzero()[0])
        #        for n in range(N):
        #            nz_n = np.sort(w[d].nonzero()[1])[n]
        #            logPoisson += delta * np.linalg.norm(w[d].toarray()[0][nz_n] - (z[d][n].T.dot(optimizer[:,nz_n])))
        #    
        #    if t == start_date:
        #        return logPoisson
        #    else:
        #        return logPoisson + pi * ((beta - beta_prev) ** 2).sum()

        #flat_beta = beta.flatten()
        #flat_beta = optimize.fmin_cg(log_poisson_online, flat_beta, args=(delta_1, pi_1), epsilon=0.5, maxiter= 1)
        #beta = flat_beta.reshape(K, G)
        '''
        
        alpha = tau_0/(i_outer + tau)
        
        for d_batch in range(D/M):
            beta_gradient = np.array([[0.0 for g_i in range(G)] for k in range(K)])
            phi_gradient = np.array([[0.0 for l in range(L)] for k in range(K)])

            print 'Day :', t, ' OI : ', i_outer ,' of ', iterations_outer, ' : Document batch ', d_batch, ' of ', D/M, ' Step 2.a'
            for d  in range(M):
                N = len(w[d_batch + d].nonzero()[0])
                for n in range(N):
                    nz_n = np.sort(w[d_batch + d].nonzero()[1])[n]
                    beta_gradient[:,nz_n] = (1 - (w[d_batch + d].toarray()[0][nz_n]/(z[d_batch + d][n].T.dot(beta[:,nz_n]) + epsilon))) * z[d_batch + d][n]
                for l in range(L):
                    phi_gradient[:,l] = (1 - (g[d_batch + d].toarray()[0][l]/(r[d_batch + d][l].T.dot(phi[:, l]) + epsilon))) * r[d_batch + d][l]                    
            
            
            beta -= alpha/M * beta_gradient
            #print phi
            phi -= alpha/M * phi_gradient
            beta = np.array([proj_unit_simplex(beta[k]) for k in range(K)])
            #print phi
            phi = np.array([proj_unit_simplex(phi[k]) for k in range(K)])
            #print phi
        
        if t != start_date:
            print 'Day :', t, ' OI : ', i_outer ,' of ', iterations_outer, ' Step 2.b'
            beta_gradient = np.array([[0.0 for g_i in range(G)] for k in range(K)])
            phi_gradient = np.array([[0.0 for l in range(L)] for k in range(K)])
            
            beta_gradient = alpha * (beta - beta_prev)
            phi_gradient = alpha * (phi - phi_prev)
            
            beta -= beta_gradient
            phi -= phi_gradient
            
            beta = np.array([proj_unit_simplex(beta[k]) for k in range(K)])
            phi = np.array([proj_unit_simplex(phi[k]) for k in range(K)])
        print 'Time taken to for this iteration : ', time()-t2    
    t1 = time()
    print 'Dumping...'
    joblib.dump(beta, '/freespace/local/sp1467/NO_URLpickles_5_iter/beta_trained_11_{0:0>2}.pkl'.format(t))
    joblib.dump(phi, '/freespace/local/sp1467/NO_URLpickles_5_iter/phi_trained_11_{0:0>2}.pkl'.format(t))
    joblib.dump(theta, '/freespace/local/sp1467/NO_URLpickles_5_iter/theta_documents_trained_11_{0:0>2}.pkl'.format(t))
    joblib.dump(z, '/freespace/local/sp1467/NO_URLpickles_5_iter/z_words_documents_trained_11_{0:0>2}.pkl'.format(t))
    joblib.dump(r, '/freespace/local/sp1467/NO_URLpickles_5_iter/r_words_documents__trained_11_{0:0>2}.pkl'.format(t))    
    print 'Time taken to dump parameters : ', time()-t1
    
    print 'Time taken to for this time slice : ', time()-t0
