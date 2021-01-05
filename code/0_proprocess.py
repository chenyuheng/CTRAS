#-*- coding:utf-8 -*-
import os, csv, sys, re
# from pyltp import Segmentor
# from pyltp import Postagger
# from pyltp import SentenceSplitter
import nltk
from nltk.corpus import stopwords
from zhconv import convert
from variables import APPS, HEADER
from variables import RAW_PATH, CORPUS_PATH, STOP_WORDS_PATH, SYNONYM_WORDS_PATH
from variables import cws_model_path, pos_model_path

# ---------------------------------------------------------------------------------------
# Description   : Function to preprocess the raw reports
# ---------------------------------------------------------------------------------------

def read_stop_words():
	# stop_words = []
	# f = open(STOP_WORDS_PATH, 'r')
	# for line in f.readlines():
	# 	stop_words.append(line.replace('\n','').replace('\r',''))
	# f.close()
	# print(stop_words)
	return stopwords.words('english')

def read_synonym_words(): # 返回一个字典，但是看不出来是一对一的字典还是一对多的字典，疑似一对一
	# synonym_words = {}
	# f = open(SYNONYM_WORDS_PATH, 'r')
	# for line in f.readlines():
	# 	syn = line.replace('\n','').replace('\r','').split(' ')
	# 	for word in syn:
	# 		if word != syn[1]:
	# 			synonym_words[word] = syn[1]

	# f.close()
	return {}

def preprocess(app):
	# segmentor = Segmentor()
	# segmentor.load(cws_model_path)
	# postagger = Postagger()
	# postagger.load(pos_model_path)

	stop_words = read_stop_words() # 列表
	synonym_words = read_synonym_words() # 字典

	with open('/'.join([RAW_PATH, 'report_'+app+'.csv'])) as csv_file:
		reader = csv.reader(csv_file, delimiter=',')
		for row in reader:
			_id = row[0]
			_description = row[1]
			_description = _description.replace('\n','').replace('\r','').strip()

			file_path = '/'.join([CORPUS_PATH, app])
			if not os.path.exists(file_path):os.makedirs(file_path)
			if not os.path.exists(file_path+"original"):os.makedirs(file_path+"original")
			if True: # not os.path.isfile('/'.join([CORPUS_PATH, app, _id+'.txt'])): # 每个应用的每个评论对应一个语料文件
				sents = nltk.sent_tokenize(_description) # 分成一句一句
				content = []
				for sent in sents:
					words = [w for w in nltk.word_tokenize(sent) if w not in stop_words] # 去除 stopwords
					words = [synonym_words[w] if w in synonym_words.keys() else w for w in words] # 替换同义词

					postags = nltk.pos_tag(words) #打标签
					items = ['_'.join(x) for x in postags] #打标签 [ "I_tag1", "am_tag2" ..]
					content.append(' '.join(items)) # 合成一句话 [ "I_tag1 am_tag2" ..]
				content = '\n'.join(content) #content 是一个sentence的列表

				f_out = open('/'.join([CORPUS_PATH, app, _id+'.txt']), 'w') #存储处理完的reciew
				f_out.write(content)
				f_out.close()
				f_out = open('/'.join([CORPUS_PATH, app +"original", _id+'.txt']), 'w') #存储处理之前的review
				f_out.write(row[1])
				f_out.close()
	# segmentor.release()
	# postagger.release()

for app in APPS:
	preprocess(app)
