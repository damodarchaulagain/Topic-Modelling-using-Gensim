# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from bson import ObjectId
from pymongo import MongoClient
from noun_rules import *
from suffix_rules import *
from collections import defaultdict
import random

reload(sys)
sys.setdefaultencoding("utf-8")

client=MongoClient("mongodb://192.241.170.140:65000/")
db=client.all_news

def get_new_data():
	file=open("ids_list.txt","r")
	id_list=[]
	print "getting id"
	for ids in file:
		if len(ids)==25:
			id_list.append(ObjectId(ids[0:-1]))
		else:
			id_list.append(ObjectId(ids))
	np.random.shuffle(id_list)
	b=id_list[100000:100001:]
	print "getting news"
	data=db.news_collection.find({"_id":{"$in":b}})
	df=pd.DataFrame(list(data))
	print "listing news"
	news_list=list(df['news_content'])
	#newd=balRules(news_list[0].split(" "))
	print "Contents ready"

 	news_list= filter(None,[(get_truncated(word.encode('utf-8'))).lstrip().rstrip() for news in news_list for word in balRules(remove_digits(news)).split(" ") if len(word)>0])
	print "gettng word list with bibhakti"
	word_list= filter(None,np.unique([filter_bibhakti(word) for news in news_list for word in news ]))
	return word_list

def filter_bibhakti(word):
	file=codecs.open("bibhakti.txt","r",encoding='utf-8')
	bibhakti_list=[data[0:-1] for data in file]
	print type(bibhakti_list[0])
	print type(word)
	try:
		b=[word for data in bibhakti_list if data==word[-len(data):]][0]
	except IndexError:
		b=None
	return b

def remove_digits(news):
	f=codecs.open("np_digits.txt","r", encoding='utf-8')
	file_list=[value[0:-1] for value in f]
	print type(file_list[0])
	chars_to_remove = file_list
	subj = news
	dd=dict((ord(unicode(char)), None) for char in chars_to_remove)
	subj=subj.translate(dd)
	return subj

if __name__=='__main__':
	for data in get_new_data():
		print data