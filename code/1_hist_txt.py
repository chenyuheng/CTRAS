#-*- coding:utf-8 -*-
import os, csv, json
from scipy.sparse import save_npz
from sklearn.feature_extraction.text import TfidfVectorizer
from variables import POS_TAGS, APPS
from variables import CORPUS_PATH, HIST_TXT_PATH

# ---------------------------------------------------------------------------------------
# Description   : Function to calculate textual features of reports
# ---------------------------------------------------------------------------------------

def parse_corpus(_corpus):
	for tag in POS_TAGS:
		_corpus = _corpus.replace(tag, '') # 把posttag又去掉了
	_corpus = _corpus.replace('_n', '') # 这里为什么是_n??????????????????????????????????
	return _corpus

def load_corpus(app):
	corpus = [] # 装入所有的review
	for name in sorted(os.listdir('/'.join([CORPUS_PATH, app]))):
		_corpus_file = open('/'.join([CORPUS_PATH, app, name]), 'r')
		_corpus = _corpus_file.read().replace('\n','') # 一个review
		corpus.append(parse_corpus(_corpus))
	print(len(corpus)) #1000
	return corpus

def generate_hist(app):
	corpus = load_corpus(app)
	vectorizer = TfidfVectorizer(norm=u'l1', max_features=200)
	X = vectorizer.fit_transform(corpus)
	# 生成一个 tfidf 函数 tf-idf(t, d, D) 表格，对于每一个篇文档的特定词（features），得到tfidf的值。
	i = 0
	# print(f"""
	# corpus length: {len(corpus)}
	# X width: {len(X.toarray()[0])}
	# X height: {len(X.toarray())}
	# """)
	# for x, y in zip(X, corpus):
	# 	print(y)
	# 	print(x)
	# 	print("=====")
	# for x in (zip(vectorizer.get_feature_names(), range(len(vectorizer.get_feature_names())))):
	# 	print(x, end=", ")
	save_npz('/'.join([HIST_TXT_PATH, app+'.npz']), X) # save text hist


for app in APPS:
	generate_hist(app) # for each group, generate its text hist