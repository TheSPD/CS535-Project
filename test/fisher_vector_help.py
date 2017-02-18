

#def main():
#    # Short demo.
#    K = 64
#    N = 1000
#
#    file = open("tweets_11_04.txt",'rb')
#    data = pickle.load(file)
#
#    #xx, _ = make_classification(n_samples=N)
#    #xx_tr, xx_te = xx[: -100], xx[-100: ]
#
#    gmm = GMM(n_components=K, covariance_type='diag')
#    gmm.fit(data)#xx_tr




#    for i in range(0,len(sentences)):
#        fv[i) = fisher_vector(data(i), gmm)








import numpy as np
import pickle
from sklearn.mixture import GMM


data = pickle.load(open("tweets_11_12.txt",'rb'))
K = 20
gmm = GMM(n_components=K, covariance_type='diag')
gmm.fit(data)#xx_tr
fv = {}
for i in range(0,len(data)):
    #fv[i] = fisher_vector(data(i), gmm)
    
    xx = data[i]
    
    xx = np.atleast_2d(xx)
    N = xx.shape[0]
    
    # Compute posterior probabilities.
    Q = gmm.predict_proba(xx)  # NxK
    
    # Compute the sufficient statistics of descriptors.
    Q_sum = np.sum(Q, 0)[:, np.newaxis] / N
    Q_xx = np.dot(Q.T, xx) / N
    Q_xx_2 = np.dot(Q.T, xx ** 2) / N
    
    # Compute derivatives with respect to mixing weights, means and variances.
    d_pi = Q_sum.squeeze() - gmm.weights_
    d_mu = Q_xx - Q_sum * gmm.means_
    d_sigma = (
        - Q_xx_2
        - Q_sum * gmm.means_ ** 2
        + Q_sum * gmm.covars_
        + 2 * Q_xx * gmm.means_)
    
        # Merge derivatives into a vector.
        #return np.hstack((d_pi, d_mu.flatten(), d_sigma.flatten()))
    fv[i] = np.hstack((d_pi, d_mu.flatten(), d_sigma.flatten()))
pickle.dump(fv, open("fishers_11_12.txt", "wb" ))
