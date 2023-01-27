import os
import string
import numpy as np

from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.tokenize import word_tokenize
from sklearn.metrics import silhouette_score
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from afinn import Afinn
import matplotlib.pyplot as plt

afinn = Afinn()

# extract the texts from the html files
file_list = os.listdir("testData")
documents = []
file_list = [file for file in file_list]
for file in file_list:
    with open("testData/" + file, "r", encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        text = soup.get_text()
        documents.append(text)


# a custom tokenizer for handling with stemming, lowercase, punctuation and stop_words
def my_tokenizer(text):
    ps = PorterStemmer()
    stop_words = stopwords.words('english')
    text_lower = text.lower()
    tokens = word_tokenize(text_lower)
    tokens = list(filter(lambda token: token not in string.punctuation, tokens))
    words = [ps.stem(token) for token in tokens if token not in stop_words]
    return words


# use scrikit learn to cluster the resulting document collection
vec = TfidfVectorizer(tokenizer=my_tokenizer)
X = vec.fit_transform(documents)
print(f"n_samples: {X.shape[0]}, n_features: {X.shape[1]}")

# # uses silhouette coefficient to measure the quality of the clusters
# sil_avg = []
# range_n_clusters = [2, 3, 4, 5, 6, 7, 8]
#
# for k in range_n_clusters:
#     kmeans = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=5).fit(X)
#     labels = kmeans.labels_
#     sil_avg.append(silhouette_score(X, labels, metric='euclidean'))
#
# plt.plot(range_n_clusters, sil_avg, 'bx-')
# plt.xlabel('Values of K')
# plt.ylabel('Silhouette score')
# plt.title('Silhouette analysis For Optimal k')
# plt.show()

num_of_clusters = 5
model = KMeans(n_clusters=num_of_clusters, init='k-means++', max_iter=100, n_init=5)
model.fit(X)
mydict = {i: np.where(model.labels_ == i)[0] for i in range(model.n_clusters)}

# print out 20 index terms for each cluster which are most informative
print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vec.get_feature_names_out()
for i in range(num_of_clusters):
    top_ten_words = [terms[ind] for ind in order_centroids[i, :20]]
    print("Cluster {}: {}".format(i, ' '.join(top_ten_words)))


# derive cluster sentiment scores
def calculate_afinn_score(docs, index_list):
    total_afinn_score = 0
    average_afinn_score = 0
    afinn_scores = []
    for index in index_list:
        afinn_score = afinn.score(docs[index])
        total_afinn_score = total_afinn_score + afinn_score
        afinn_scores.append(afinn_score)
        average_afinn_score = total_afinn_score / len(index_list)
    return total_afinn_score, average_afinn_score, afinn_scores


# print out the sentiment scores details of each cluster
def print_afinn_score(docs, dict_cluster):
    for dict_info in dict_cluster:
        print(calculate_afinn_score(docs, dict_cluster[dict_info]))


print_afinn_score(documents, mydict)
