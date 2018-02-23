# -*- coding: utf-8-*-

import os, os.path
import codecs

def balRules(text):
	#text=text.replace(" ","")
	###Rule removal of all other chars after Haru
	suffix_words=list(file("suffix_words.txt","r"))
	for i, j in enumerate(text):
		loc = j.find(u'हरू')
		if loc != -1 and len(j[loc+len(u'हरू'):]) != 0:
			text[i] = j.replace(j[loc+len(u'हरू'):], "")

	###Rule to remove Lai
	for i, j in enumerate(text):
		if u'लाई' in j:
			if ord(j[-3]) == 2354 and (ord(j[-2]) == 2366 and ord(j[-1]) == 2312) : 
				text[i] = j.replace(j[-3:],"")

	###Rule to remove plural
	for i, j in enumerate(text):
		if u'हरू' in j or u"हरु" in j:
			#print ord(j[-1])
			if u'हरू' in j:
				loc=j.find(u'हरू')
			else:
				loc=j.find(u"हरु")
			if loc!=len(j):
				if j[loc+len("हरु"):] in suffix_words:
						text[i] = j.replace(j[loc:], "")
			else:
				if ord(j[-3]) == 2361 and (ord(j[-2]) == 2352 and (ord(j[-1]) == 2370 or ord(j[-1])==2369)): 
					text[i] = j.replace(j[-3:],"")

	###Rule no 4 ..removing े,ो
		"""
		if unichr(2375) in j:
			if ord(j[-1]) == 2375:
				if j in expectionData:
					text[i] = j[:-1] + unichr(2379)
				else:
					text[i] = j[:-1]
		"""
	###Rule no 3
		if u'ाइ' in j:
			if ord(j[-2]) == 2366 and ord(j[-1]) == 2311:	
				if ord(j[0]) >= 2309 and ord(j[0]) <= 2324: ###vowel condition check. Replace a+aakar with aa
					text[i] = j[0] + unichr(2366) + j[1:]
					text[i] = text[i].replace(j[-2:], "")
					text[i] = text[i] + unichr(2381)
				elif ord(j[-3]) == 2357:
					text[i] = j.replace(j[-3:], "")
					text[i] = text[i] + unichr(2366)
				else: 
					text[i] = j.replace(j[-2:], "")
					text[i] = text[i] + unichr(2381)	
	###Rule no 2
		if u'ीय' in j:
			if ord(j[-2]) == 2368 and ord(j[-1]) == 2351:
				text[i] = j.replace(j[-2:], "")
			if ord(j[-2]) == 2351 and ord(j[-1]) == 2366:
				text[i] = j.replace(j[-2:], "")
	###Rule no 1
		"""
		if unichr(2368) in j:
			if ord(j[-1]) == 2368:
				text[i] = j.replace(j[-1], "")#unichr(2312))
		"""
		#ी,िक
	
	return text

#print unichr(2351), unichr(2368)