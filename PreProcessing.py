import os
import string
import shutil
import re
from stemming.porter2 import stem
from gensim import corpora, models, similarities

path = os.getcwd()+'/trial/' #path to the dataset

#path to the output of stemmed data set
os.mkdir(os.getcwd()+'/stemmed_output/')

documents = [] # contains lists of sentences, each list of words
stoplist = [] # contains the list of stopwords
f=open('stopwords.txt')

for line in f:
    line = line[:-2] # the line is like "the\r\n"
    stoplist.append(line)
f.close()

def preprocess(line):
	line = line.strip()
	line = line.lower()
	line=re.sub("<.*?>","",line)
	for c in string.punctuation:
		line=line.replace(c,' ')
	line2=''  # contains the stemmed sentence 
	line_list = []
	for word in line.split():
		if word in stoplist:
			continue
		if len(word) < 3:
			continue
		stemmed_word = stem(word)
		line2+=stemmed_word+' '
		line_list.append(stemmed_word)
	return line2, line_list


# looping over the files
for filename in os.listdir(path):
	file1 = open(path+filename,'r')
	file2 = open(os.getcwd()+'/stemmed_output/'+filename, 'w')
	text1 = file1.readlines()
	for line in text1:
		# preprocessing the text
		line2, line_list = preprocess(line)
		file2.write(line2)
		documents.append(line_list)
				
dictionary = corpora.Dictionary(documents)
dictionary.save('/tmp/classic_doc.dict')
corpus = [dictionary.doc2bow(text) for text in documents]
#print (corpus)

#TF_IDF Calculation

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
#for doc in corpus_tfidf:
#	print doc
	
index = similarities.MatrixSimilarity(corpus_tfidf)
query = "Preliminary Report Proposal"
q, ql = preprocess(query)
vec_bow = dictionary.doc2bow(q.lower().split())
vec_tfidf = tfidf[vec_bow] # convert the query to LSI space
#print("\n\nThe TF-IDF vector of query:\n")
#print(vec_tfidf)
sims = index[vec_tfidf]
#print("\n\nThe results of cosine similarity calculations with the corpus:\n")
sorted(enumerate(sims), key=lambda item: -item[1])
#print(sims)	
