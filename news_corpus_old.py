# -*- coding: utf-8 -*-
import gensim
import random
from gensim import corpora
from collections import defaultdict
import sys
import os
import logging
import numpy as np
from gensim import corpora, models, similarities
from suffix_rules import *
from noun_rules import *
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import threading

reload(sys)
sys.setdefaultencoding("utf-8")

def remove_digits(news):
	file_list=[]
	with open("np_digits.txt","r") as f:
		file_list=[value.replace("\n","") for value in list(f)]
	chars_to_remove = file_list

	subj = news
	dd=dict((ord(unicode(char)), None) for char in chars_to_remove)
	subj=subj.translate(dd)
	return subj

def get_new_data():
	file1=codecs.open("testnews.txt","r",encoding="utf-8")
	file2=codecs.open("testnews1.txt","r",encoding="utf-8")
	file3=codecs.open("testnews2.txt","r",encoding="utf-8")
	file4=codecs.open("testnews4.txt","r",encoding="utf-8")
	file5=codecs.open("testnews5.txt","r",encoding="utf-8")
	file6=codecs.open("testnews6.txt","r",encoding="utf-8")
	news_list=[file1.read(),file2.read(),file3.read(),file4.read(),file5.read(),file6.read()]

	common_words=get_common_words()
	news_list= [filter(None,[(get_truncated(word.encode('utf-8'))).lstrip().rstrip() for word in balRules(remove_digits(news)).split(" ") if word not in common_words and len(word)>0]) for news in news_list]

	news_list = [[token for token in news] for news in news_list]
	return news_list

def get_common_words():
	file_list=[]
	f=codecs.open("common_words_list.txt",'r',encoding='utf-8')
	for file in f:
		file_list.append(file[:-1])
	return file_list

def gen_corpus(news_list):
	dictionary = corpora.Dictionary(news_list)
	print dictionary.token2id, #gives the token-tokenid relation of the terms

	corpus = [dictionary.doc2bow(news) for news in news_list] #gives tokenid-document_term_frequcency
	return corpus

if __name__=="__main__":
	
	news_list=get_new_data()
	dictionary = corpora.Dictionary(news_list)
	corpus=gen_corpus(news_list)
	print corpus

	ldamodel=gensim.models.ldamodel.LdaModel(corpus, num_topics=10, id2word = dictionary, passes=20)
	print ldamodel.print_topics(num_topics=4, num_words=3)

	lsimodel=gensim.models.lsimodel.LsiModel(corpus, id2word=dictionary, num_topics=10)
	print lsimodel.print_topics(num_topics=4,num_words=3)
	
	tfidf = models.tfidfmodel.TfidfModel(corpus)

	corpus_tfidf = tfidf[corpus]

	for i in corpus_tfidf:
		print i #shows the tfidf translation matrix

	# ldamodell = gensim.models.ldamodel.LdaModel(corpus_tfidf, num_topics=4, id2word = dictionary, passes=50)
	# print ldamodell.print_topics(num_topics=4, num_words=3)
	
	lsimodell =gensim.models.lsimodel.LsiModel(corpus_tfidf, num_topics=4, id2word = dictionary)
	print lsimodel.print_topics(num_topics=4,num_words=3)

	# coupuslsi=lsimodell[corpus_tfidf] #Double wrapping the corpus with the lsi model
	# lsimodell2=gensim.models.lsimodel.LsiModel(coupuslsi, num_topics=2, id2word = dictionary) 
