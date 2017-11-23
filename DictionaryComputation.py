import os
from gensim import corpora,models
from textblob.wordnet import Synset
from textblob import Word

documents=[]
path = os.getcwd()+'/non_stemmed_output/'
for filename in os.listdir(path):
    file1 = open(path+filename,'r')
    text1 = file1.readlines()
    for line in text1:
        line2=''  # contains the stemmed sentence 
        line_list = []
        for word in line.split():
            line_list.append(word)
        documents.append(line_list)

dictionary = corpora.Dictionary(documents)
dictionary.save('/tmp/classic_doc.dict')
corpus = [dictionary.doc2bow(text) for text in documents]

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
#for doc in corpus_tfidf:
#	print doc

#CALCULATING THE SIMILARITY USING WORDNET

file2 = open(os.getcwd()+'/Similarity_Score.txt', 'w')
for word1 in dictionary:
	word1 = str(word1)
	l = []
	l.append(word1)
	for word2 in dictionary:
		word2 = str(word2)
		l.append(word2)
		try:
			word = Word(word1)
			word = word.synsets[0]
			word = str(word)
			word = word.split("'")
			word = word[1]
			word1.Synset(word)

			word_ = Word(word2)
			word_ = word_.synsets[0]
			word_ = str(word_)
			word_ = word_.split("'")
			word_ = word_[1]
			word2.Synset(word_)

			similarity = word1.path_similarity(word2)
			l.append(similarity)
		except:
			l.append(0.0)

	file2.write(str(l))

