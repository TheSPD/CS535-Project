from sklearn.externals import joblib

start_date = 3
end_date = 13
K = 10

tf_idf_vectorizer = joblib.load('/freespace/local/sp1467/NO_URLpickles/tf_idf_vectorizer_11_03.pkl')
inv_map = {v: k for k, v in tf_idf_vectorizer.vocabulary_.iteritems()}

for t in range(start_date, end_date):
    print 'Day {:0>2}'.format(t)
    beta = joblib.load('/freespace/local/sp1467/NO_URLpickles_5_iter/beta_trained_11_{0:0>2}.pkl'.format(t))
    phi = joblib.load('/freespace/local/sp1467/NO_URLpickles_5_iter/phi_trained_11_{0:0>2}.pkl'.format(t))
    for k in range(K):
        print 'Topic #{0}'.format(k)
        print 'Trump : {0}, Clinton : {1}'.format(phi[k][0],phi[k][1])
        print ' '.join([inv_map[i] for i in beta[k].argsort()[-20:][::-1]])
