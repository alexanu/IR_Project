#class to parse SGML files
from __future__ import print_function
from glob import glob
import itertools
import os.path
import re
import tarfile
import time
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import rcParams
from sklearn.externals.six.moves import html_parser
from sklearn.externals.six.moves.urllib.request import urlretrieve
from sklearn.datasets import get_data_home
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import MultinomialNB

def _not_in_sphinx():
    # Hack to detect whether we are running by the sphinx builder
    return '__file__' in globals()

#SGML Parser
class ReutersParser(html_parser.HTMLParser):
    #Utility class to parse a SGML file and yield documents one at a time.

    def __init__(self, encoding='latin-1'):
        html_parser.HTMLParser.__init__(self)
        self._reset()
        self.encoding = encoding

    def handle_starttag(self, tag, attrs):
        method = 'start_' + tag
        getattr(self, method, lambda x: None)(attrs)

    def handle_endtag(self, tag):
        method = 'end_' + tag
        getattr(self, method, lambda: None)()

    def _reset(self):
        self.in_title = 0
        self.in_body = 0
        self.in_topics = 0
        self.in_topic_d = 0
        self.title = ""
        self.body = ""
        self.topics = []
        self.topic_d = ""

    def parse(self, fd):
        self.docs = []
        print(type(fd))
        for chunk in fd:
            self.feed(chunk.decode(self.encoding))
            for doc in self.docs:
                yield doc
            self.docs = []
        self.close()

    def handle_data(self, data):
        if self.in_body:
            self.body += data
        elif self.in_title:
            self.title += data
        elif self.in_topic_d:
            self.topic_d += data

    def start_reuters(self, attributes):
        pass

    def end_reuters(self):
        self.body = re.sub(r'\s+', r' ', self.body)
        self.docs.append({'title': self.title,
                          'body': self.body,
                          'topics': self.topics})
        self._reset()

    def start_title(self, attributes):
        self.in_title = 1

    def end_title(self):
        self.in_title = 0

    def start_body(self, attributes):
        self.in_body = 1

    def end_body(self):
        self.in_body = 0

    def start_topics(self, attributes):
        self.in_topics = 1

    def end_topics(self):
        self.in_topics = 0

    def start_d(self, attributes):
        self.in_topic_d = 1

    def end_d(self):
        self.in_topic_d = 0
        self.topics.append(self.topic_d)
        self.topic_d = ""

#Generator function to yield  a document in each file
def stream_reuters_documents(data_path=None):
	"""DOWNLOAD_URL = ('http://archive.ics.uci.edu/ml/machine-learning-databases/'
	               'reuters21578-mld/reuters21578.tar.gz')
	ARCHIVE_FILENAME = 'reuters21578.tar.gz'"""
	parser = ReutersParser()
	for filename in glob(os.path.join(data_path, "*.sgm")):
		for doc in parser.parse(open(filename, 'rb')):
			yield doc

os.mkdir(os.getcwd()+'/trial/')
path = os.getcwd()+'/trial/' #path where datapath would be stored
data_path="/home/surya/Desktop/IR_Project/reuters21578" #Path were datapath is present
print(os.path.join(data_path, "*.sgm"))

"""i=1
a=stream_reuters_documents(data_path)
value=next(a)
titleDict={}
bodyDict={}
topicDict={}
titleDict[i]=value['title']
bodyDict[i]=value['body']
topicDict[i]=value['topics']
print(titleDict)
print(bodyDict)
print(topicDict)"""

i=0
a=stream_reuters_documents(data_path)
titleDict={} # Dictionary to store title with a unique i as key
bodyDict={} # Dictionary to store body with a unique i as key
topicDict={}  # Dictionary to store topics with a unique i as key
for value in a:
	titleDict[i]=value['title']
	bodyDict[i]=value['body']
	if bodyDict[i]=='': # IF BODY IS NULL, as in case of news-bulletin, BODY=TITLE
		bodyDict[i]=titleDict[i]
	topicDict[i]=value['topics']
	i=i+1
    #print(value)

print(i)

fo_corpus=open("corpus.txt","w") #CORPUS FILE
fo_title=open("title.txt","w") #TITLE FILE

corpus=""
title=""
for i in range(0,21578):
    foo=path+"reuters"+str(i)+".txt"
    fo=open(foo,"w") 
    fo.write(bodyDict[i])
    fo.close()
    corpus=corpus+bodyDict[i]
    title=title+"\n"+titleDict[i]
fo_corpus.write(corpus)
fo_title.write(title)
"""file_list=[]
for i in range(0,21578):
    foo="reuters"+str(i)+".txt"
    fo=open(foo,"r")
    file_list.append(fo.read())
    fo.close()
"""
