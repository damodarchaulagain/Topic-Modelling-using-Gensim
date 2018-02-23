# -*- coding: utf-8 -*-
import sys
import codecs

def get_truncated(word):
	f=codecs.open("np_nouns.txt","r",encoding='utf-8')
	nouns_list= [data[:-1] for data in f]
	try:
		b=[data for data in nouns_list if data in word][0]
	except IndexError:
		b=word
	return b