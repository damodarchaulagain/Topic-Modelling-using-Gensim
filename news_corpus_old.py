# -*- coding: utf-8 -*-
import gensim
from pymongo import MongoClient
import random
import pandas as pd
from gensim import corpora
from collections import defaultdict
import sys
import os
import logging
from bson import ObjectId
import numpy as np
from gensim import corpora, models, similarities
from suffix_rules import *
from noun_rules import *
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import threading

reload(sys)
sys.setdefaultencoding("utf-8")

client=MongoClient("mongodb://192.241.170.140:65000/")
db=client.all_news
data=[]
"""
class extractNews (threading.Thread):
   
   	def __init__(self, id_list,data):
		threading.Thread.__init__(self)
		self.id_list = id_list
		self.data=data

   	def run(self):
		self.get_news(self.id_list,self.data)
		
   	def get_news(id_list,data):
   		pass
"""


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
	file=open("ids_list.txt","r")
	id_list=[]
	print "getting id"
	for ids in file:
		if len(ids)==25:
			id_list.append(ObjectId(ids[0:-1]))
		else:
			id_list.append(ObjectId(ids))
	#np.random.shuffle(id_list)
	print "getting news"
	cursor1=db.news_collection.find({"_id":{"$in":id_list[0:500]}})
	cursor2=db.news_collection.find({"_id":{"$in":id_list[0:500]}})
	thread_1=extractNews(cursor1,data)
	thread_2=extractNews(cursor2,data)
	
	df=pd.DataFrame(data)
	print "listing news"
	news_list=list(df['news_content'])
	#newd=balRules(news_list[0].split(" "))
	print "Contents ready"
	
	common_words=get_common_words()
	
 	news_list= [filter(None,[(get_truncated(word.encode('utf-8'))).lstrip().rstrip() for word in balRules(remove_digits(news)).split(" ") if word not in common_words and len(word)>0]) for news in news_list]
	print "Stemming completed"
	frequency = defaultdict(int)
	for news in news_list:
		for token in news:
			frequency[token] += 1
	news_list = [[token for token in news] for news in news_list]
	max_value=[]
	max_dict={"value":0}
	for key in frequency:
		print key
		if frequency[key]>100:
			max_dict={"key":key,"value":frequency[key]}
			max_value.append(max_dict)
	for data in max_value:
		print data['key'],data['value']
	return news_list

def get_common_words():
	file_list=[]
	f=codecs.open("common_words_list.txt",'r',encoding='utf-8')
	for file in f:
		file_list.append(file[:-1])
	return file_list

def gen_corpus(news_list):
	print "getting corpus"
	dictionary = corpora.Dictionary(news_list)
	dictionary.save('tmp/news_new.dict')
	corpus = [dictionary.doc2bow(news) for news in news_list]
	corpora.MmCorpus.serialize('tmp/news_new.mm', corpus)

if __name__=="__main__":
	
	news_list=get_new_data()

	#gen_corpus(news_list)
	
	"""
	from gensim import corpora, models, similarities
	if (os.path.exists("tmp/news_new.dict")):
		dictionary = corpora.Dictionary.load('tmp/news_new.dict')
		corpus = corpora.MmCorpus('tmp/news_new.mm')
		print("Used files generated from first tutorial")
	else:
		print("Please run first tutorial to generate data set")
	
	tfidf = models.tfidfmodel.TfidfModel(corpus)
	corpus_tfidf = tfidf[corpus]

	lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=10)
	lsi.print_topics(10)
	#corpus_lsi = lsi[corpus_tfidf]
	lsi.save('/tmp/model.lsi')
	#lsi.print_topics(2)
	#for doc in corpus_lsi:
	#print doc
	#lsi = models.LsiModel.load('/tmp/model.lsi')
	#index = similarities.MatrixSimilarity(lsi[corpus_tfidf])
	#index.save('tmp/news_new.index')
	#data=db.news_collection.find({"source":"Kantipur"}).limit(3)
	#doc = list(data)[2]["news_content"]
	#vec_bow = dictionary.doc2bow(doc.lower().split())
	#vec_lsi = lsi[vec_bow] # convert the query to LSI space
	#index = similarities.MatrixSimilarity.load('tmp/news.index')
	#sims = index[vec_lsi]
	#print(list(enumerate(sims)))
	#lda = models.ldamodel.LdaModel(corpus,id2word=dictionary, num_topics=10,passes=10)
	#lda.save('newsgroups_lda.model')
	#lda.print_topics(10)
	#hdp.print_topics(10)
	#lda.save('newsgroups_50_lda.model')
	
	lda=models.ldamodel.LdaModel.load('newsgroups_lda.model')
	lda.print_topics(10)
	pyLDAvis.enable_notebook()
	pyLDAvis.gensim.prepare(lda, corpus, dictionary)


	doc = u"वैशाख २५, २०७४- विस्फोटक र दस्तावेजसहित प्रहरीले आइतबार नेपाल कम्युनिस्ट पार्टी (विप्लव) का ३ जना कार्यकर्ता पक्राउ गरेको छ । जनकपुर ब्युरो सदस्य मोहमद आदन राइन, कार्यालय सदस्य तिलक भनिने प्रानकुमार लामा र मिथिला चौहान पक्राउ परेका हुन् ।\
इलाका प्रहरीका डीएसपी शालिकराम शर्माको कमान्डमा गएको टोलीले उनीहरूलाई बर्दिवास नगरपालिका–३ गौरीडाँडास्थित ज्ञानप्रसाद पौडेलको घरबाट पक्राउ गरेको हो । उनको घर भाडामा लिएर केही समयदेखि पार्टी गतिविधि सञ्चालन गर्दै आएको प्रहरीले जनायो ।\
‘स्थानीय निर्वाचन खारेजी गर’ लेखिएका २ सय थान पर्चा र पोस्टर बरामद भएका छन् । टाइम बम बनाउने तार र २ थान भित्ते घडी, ६ थान डिटोनेटर, टेस्टर, २ बोतल तेजाव र ३ सय ग्राम बारुद बनाउने धूलो फेला परेका छ । यस्तै सोल्डिङ तार, आइरन, कुकर बम बनाउने सामग्री, २ किलो गन्धक, आल्मुनियम फस्फेट, बम पड्काउने योजनासहितका पेन्सिलले स्केच गरिएका नक्सा पनि फेला परेको प्रहरीले जनायो । \
२ थान ल्यापटप, ६ सेट मोबाइल, कांग्रेसको रूख छाप भएका टिसर्ट, वाम साहित्य र पार्टी नवीकरणका फाइललगायत सामग्री पनि बरामद भएका छन् । ती सबै सामग्री प्रहरीले पत्रकार सम्मेलनमार्फत सार्वजनिक गरेको छ । जिल्ला प्रहरी प्रमुख एसपी राजकुमार लम्सालले आसन्न निर्वाचनलाई बिथोल्ने नियतले गौरिवासमा सेल्टर स्थापना गरी गतिविधि सञ्चालन गर्दै आएको बुझिएको बताए । १७ वटा कार्यालयलाई लक्षित गरी विस्फोट गराउने योजनासहितका गतिविधि सञ्चालन गरिएको प्रहरीको आशंका छ । बरामद नक्साका आधारमा प्रहरीले त्यस्तो आशंका गरेको हो ।\
‘रूख छापका टिसर्ट लगाएपछि कांग्रेस कार्यकर्ता भएको भान पर्ने र कार्यालय वा सार्वजनिक कार्यक्रममा सहज प्रवेश हुने भएकाले अवांक्षित गतिविधि गरेर सुरक्षित फर्कने रणनीतिअन्तर्गत त्यस्ता टीसर्ट संकलन गरिएको हुनुपर्छ,’ एसपी लम्सालले भने । अल्मुनियम फस्फेट घातक विषादी हो । लम्सालले भने, ‘मिलिटेन्टहरू पक्राउ पर्न थालेपछि सुसाइटका लागि यस्ता विषादी सेवन गर्छन् । उनीहरूले केको प्रयोजनका लागि राखेका हुन त्यसबारेमा बुझने काम भइरहेको छ ।’\
बर्दिवासस्थित इलाका प्रहरीका डीएसपी शालिकराम शर्माका अनुसार प्रहरीले केही समयदेखि ज्ञानप्रसादको घरको गतिविधि नियाल्दै आएको थियो । सिन्धुलीमा विप्लव समूहका केही नेता, कार्यकर्ता पक्राउ परे । उनीहरूको सेल्टर पनि गौरीवासस्थित ज्ञानप्रसादकै घरमा रहेको बुझेपछि छापा मारिएको हो ।\
सडक सञ्जालका कारण आवागमनमा सुविधा रहेको गौरीवासलाई विप्लव समूहले प्रान्तीय केन्द्रको रूपमा सञचालन गरेको जिल्ला प्रहरीका अर्का डीएसपी दीपक पोखरेलले बताए । बरामद दस्तावेजको आधारमा पार्टी संगठन बढाउन र सिन्धुली लगायत २ नं प्रदेशमा निर्वाचनविरोधी गतिविधि सञ्चालन गर्न गौरीवासको भौगोलिक अवस्थितिलाई प्रयोग गर्दै आएको स्रोतको भनाइ छ ।"

	vec_bow = dictionary.doc2bow(doc.lower().split())
	#vec_hdp = hdp[vec_bow]
	vec_lda=lda[vec_bow]
	print dir(vec_lda)
	#index = similarities.MatrixSimilarity(hdp[corpus])
	#hdp.print_topics(20)
	#sims=index[vec_hdp]
	#sims = sorted(enumerate(sims), key=lambda item: -item[1])
	#keys=[]
	#print sims

	for key,value in sims:
		if value>0.90:
			keys.append(key)
	for key,value in corpus[85]:
		print dictionary[key]
	for key in keys:
		print corpus[key]

	#print corpus.docbyoffset(256)
	
	#print dictionary[num]
	#vis_data = gensimvis.prepare(lda, corpus, dictionary)
	#pyLDAvis.display(vis_data)
	#print(vec_lsi)
	#index = similarities.MatrixSimilarity(lsi[corpus])
	#sims = index[vec_lsi]
	#sims = sorted(enumerate(sims), key=lambda item: -item[1])
	#check= sims[0:5]
	#print sims
	dict_list=dictionary.id2token
	for ids in check:
		print dict_list[ids[0]]
	"""