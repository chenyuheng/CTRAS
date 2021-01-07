#-*- coding:utf-8 -*-
import json
import os, csv
import numpy as np
import scipy.cluster.hierarchy as sch
from sklearn.feature_extraction.text import TfidfVectorizer

from variables import APPS
from variables import DISTANCE_BASE_PATH, DUPLICATES_REPORT_PATH, MASTER_REPORT_PATH
from variables import CORPUS_PATH
from variables import T_THRESHOLD

from util_corpus import get_all_reports_id
from variables import POS_TAGS, APPS
from variables import CORPUS_PATH, HIST_TXT_PATH



def parse_corpus(_corpus:str)->str:
	for tag in POS_TAGS:
		_corpus = _corpus.replace(tag, '') # 把posttag又去掉了
	_corpus = _corpus.replace('_n', '') # 这里为什么是_n??????????????????????????????????
	return _corpus

def load_corpus(app:str)->list:
	corpus = [] # 装入所有的review
	for name in sorted(os.listdir('/'.join([CORPUS_PATH, app])), key=lambda x: int(x[:-4])):
		_corpus_file = open('/'.join([CORPUS_PATH, app, name]), 'r')
		_corpus = _corpus_file.read().replace('\n','') # 一个review
		corpus.append(parse_corpus(_corpus))
	print(len(corpus)) #1000
	return corpus


# ---------------------------------------------------------------------------------------
# Description   : Function to aggregate the reports into groups
# ---------------------------------------------------------------------------------------

def cluster(app):
	all_reports_id = get_all_reports_id(app)
	distance_matrix = np.load('/'.join([DISTANCE_BASE_PATH, app, 'distance_txt.npy']))
	distArray = distance_matrix[np.triu_indices(len(distance_matrix), 1)] # 返回上三角，不包括对角线

	Z = sch.linkage(distArray, method = 'single')  # Perform hierarchical/agglomerative clustering. Single distance
	clusters = sch.fcluster(Z, T_THRESHOLD, criterion = 'distance') # # Form flat clusters from the hierarchical clustering defined by the given linkage matrix.
	# The cophenetic distance between two objects is the height of the dendrogram where the two branches that include the two objects merge into a single branch.
	# Forms flat clusters so that the original observations in each flat cluster have no greater a cophenetic distance than t.
	# print(type(Z)) #<class 'numpy.ndarray'>
	# print(type(clusters))#<class 'numpy.ndarray'>
	# print(Z.shape) # (999, 4)
	# print(clusters.shape) # (1000,) ?
	# print(type(clusters[0])) # <class 'numpy.int32'>
	duplicate_set = {} # 这个名字其实取得不太恰当
	for i, cluster_id in enumerate(clusters): # 这就是clusters的内容
		report_id = all_reports_id[i]
		if cluster_id not in duplicate_set.keys():
			duplicate_set[cluster_id] = [report_id]
		else:
			duplicate_set[cluster_id].append(report_id)
	# print(len(duplicate_set)) # 955 效果不是很好？

	if not os.path.exists('/'.join([DUPLICATES_REPORT_PATH, app])):
		os.makedirs('/'.join([DUPLICATES_REPORT_PATH, app]))

	# save duplicate_set
	out = open('/'.join([DUPLICATES_REPORT_PATH, app, 'duplicate_set.csv']), 'w+')
	writer = csv.writer(out)
	for k in sorted(list(duplicate_set.keys()), key=lambda y: min(list(map(int, duplicate_set[y])))): # sort by the min rank in a duplication set
		records = duplicate_set[k]
		print(records)
		writer.writerow(records)
	out.close()
	# yuheng add---------------------------------------------------------------------
	corpus = load_corpus(app)
	#print(corpus)
	vectorizer = TfidfVectorizer(norm=u'l1', max_features=25, ngram_range=(1,1))
	X = vectorizer.fit_transform(corpus)
	#print(vectorizer.get_feature_names())
	master_report_dict = {}
	try: # 如果已经探测 master report，则在打印中标记
		master_report_dict_file = open('/'.join([MASTER_REPORT_PATH, app, "master_report.json"]), "r")
		master_report_dict_str = master_report_dict_file.read()
		master_report_dict = json.loads(master_report_dict_str)
		master_report_dict_file.close()
	except:
		pass
	group_count = 0
	review_count = 0
	for key in sorted(list(duplicate_set.keys()), key=lambda y: min(list(map(int, duplicate_set[y])))):
		if len(duplicate_set[key]) > 1:
			group_count  += 1
			ds = duplicate_set[key]
			master_id = -1
			for num in ds:
				if num in master_report_dict:
					master_id = master_report_dict[num]
					break
			for num in ds:
				review_count += 1
				repo_file = open('/'.join([CORPUS_PATH, app +"original", num]) + ".txt", "r")
				repo_con = repo_file.read()
				print(repo_con)
				#print(corpus[int(num)])
				#print(vectorizer.get_feature_names())
				repo_file.close()
				print(f"-----end of report {num} {'MASTER' if num == master_id else ''}")
			print(f"============ end of one review of {app}, group_count: {group_count}, total_review_count: {review_count}")


	# yuheng add---------------------------------------------------------------------

for app in APPS:
	cluster(app)
