import pickle
import collections
from sklearn.cluster import AffinityPropagation
from sklearn.decomposition import PCA

# load fishers
X = pickle.load(open("fishers_11_12.txt",'rb'))

#PCA
pca = PCA(n_components=8000)
pca.fit(list(X.values()))
result = pca.explained_variance_ratio_
curr_sum = 0
index = 0
while curr_sum < 0.9:
    curr_sum+=result[index]
    index = index + 1

pca = PCA(n_components=index)
reduced_X = PCA(n_components=index).fit_transform(list(X.values()))

# affinity
af = AffinityPropagation(preference=-300).fit(reduced_X)
exemplars = af.cluster_centers_indices_
labels = af.labels_

# load dictionary
vocab = pickle.load(open("tweets_11_12_vocab.txt",'rb'))

# making sure things look good
exemplar_words = {}
for i in range(0,len(exemplars)):
    exemplar_words[i] = vocab[exemplars[i]]
    print(labels[exemplars[i]])
    exemplar_words[i]


# PRINTING TO FILES

# affinity labels for the clusters
pickle.dump(labels, open("RESULTS_11_12_cluster_labels.txt", "wb" ))


# printing exemplars
all_exemplars = ''
for i in range(0,len(exemplars)):
    all_exemplars = all_exemplars + '\n' + vocab[exemplars[i]]

text_file = open('RESULTS_11_12_cluster_exemplars.txt', "w")
text_file.write(all_exemplars[1:len(all_exemplars)])
text_file.close()


# print exemplars and all the words in the cluster
for ex in range(0,len(exemplars)):
    total = 0
    for lbl in range(0,len(labels)):
        if labels[lbl] == ex:
            total = total + 1;
    # Write the cluster exemplar
    text_file = open('RESULTS_11_12_cluster_'+str(ex)+'_total_'+str(total)+'.txt', "w")
    text_file.write(vocab[exemplars[ex]]+'\n')
    text_file.write("-----------------------------------\n")
    # Write the cluster words
    for lbl in range(0,len(labels)):
        if labels[lbl] == ex:
            text_file.write(vocab[lbl]+'\n')
    text_file.close()
