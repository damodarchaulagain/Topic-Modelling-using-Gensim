import codecs

file=codecs.open("np_nouns.txt","r",encoding='utf-8')
file=list(file)
for data in file:
	print type(data[0:-1])