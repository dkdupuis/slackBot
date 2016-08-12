from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
import pysolr
import datetime
import pandas as pd
from solrQuery import *

vectorizer = CountVectorizer(min_df=1)
#vectorizer                     
#CountVectorizer(analyzer=...'word', binary=False, decode_error=...'strict',
#    dtype=<... 'numpy.int64'>, encoding=...'utf-8', input=...'content',
#    lowercase=True, max_df=1.0, max_features=None, min_df=1,
#    ngram_range=(1, 1), preprocessor=None, stop_words=None,
#    strip_accents=None, token_pattern=...'(?u)\\b\\w\\w+\\b',
#    tokenizer=None, vocabulary=None)


#corpus = [
#     'This is the first document.',
#     'This is the second second document.',
#     'And the third one.',
#     'Is this the first document?',
#]



times = getTimes()
f = findArt('Content Marketing', times[0], times[1])
f.searchOpinions()
ops = f.getOpinions()
corpus = ops['sentenceText'].tolist()

X = vectorizer.fit_transform(corpus)
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(X)


from sklearn.cluster import KMeans
num_clusters = 5
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf)

from sklearn.metrics import pairwise_distances_argmin_min
clusExamp, _ = pairwise_distances_argmin_min(km.cluster_centers_, tfidf)

for i in range(len(clusExamp)):
    examp = corpus[clusExamp[i]]
    print('Cluster {}: '.format(i).encode('utf-8') + examp)
        

order_centroids = km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(num_clusters):
    print("Cluster %d:" % i, end='')
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind], end='')
    print()    



#-------------
import nltk
stopwords = nltk.corpus.stopwords.words('english') + ['https', 'co', 'rt']
#corpClean = []
#for sent in corpus:
#    corpClean.append(' '.join([word for word in sent.lower().split() if word not in stopwords]))

#### can do stop_words='english'; https, rt still an issue
vectorizer = CountVectorizer(min_df=1, stop_words=stopwords)
X = vectorizer.fit_transform(corpClean)
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(X)




#-------------
#Mention Extraction (AWS Lambda of PEZ function)
#import json
#import requests
#headers = {'X-Api-Key':'***'}
#data = {'text':'The quick brown fox jumped over the lazy dog.'}
#url = '***'
#r = requests.post(url, headers=headers, data=json.dumps(data))
#r.text
#--------------

