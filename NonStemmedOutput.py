import os
import string
import shutil
import re
from gensim import corpora, models, similarities

path = os.getcwd()+'/trial/' #path to the dataset

#path to the output of stemmed data set
os.mkdir(os.getcwd()+'/non_stemmed_output/')

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
		#stemmed_word = stem(word)
		#line2+=stemmed_word+' '
		#line_list.append(stemmed_word)
		line2+=word+' '
		line_list.append(word)
	return line2, line_list

# looping over the files
for filename in os.listdir(path):
	file1 = open(path+filename,'r')
	file2 = open(os.getcwd()+'/non_stemmed_output/'+filename, 'w')
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

