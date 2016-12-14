import pickle
import collections
from sklearn.cluster import AffinityPropagation
from sklearn.decomposition import PCA

#load fishers
X = pickle.load(open("fishers_11_03.txt",'rb'))

#compute affinity
af = AffinityPropagation(preference=-250).fit(list(X.values()))
#affinity labels
labels = af.labels_
#load dictionary
vocab = pickle.load(open("tweets_11_03_vocab.txt",'rb'))
exemplars = af.cluster_centers_indices_


pickle.dump(exemplars, open("affinity_11_03_exemplars.txt", "wb" ))
pickle.dump(labels,    open("affinity_11_03_labels.txt", "wb" ))



exemplar_words = {}
for i in range(0,len(exemplars)):
    exemplar_words[i] = vocab[exemplars[i]]

pickle.dump(exemplar_words, open("affinity_11_03_exemplar_words.txt", "wb" ))
print(exemplar_words)
