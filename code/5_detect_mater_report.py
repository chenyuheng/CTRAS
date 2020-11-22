#-*- coding:utf-8 -*-
import os, json
import numpy as np
from tqdm import tqdm

from variables import APPS
from variables import DISTANCE_BASE_PATH, DUPLICATES_CLUSTER_PATH, MASTER_REPORT_PATH

from util_corpus import get_dup_groups, get_dup_reports_of_one_group, get_all_reports_id
from util_pagerank import graphMove, firstPr, pageRank

# ---------------------------------------------------------------------------------------
# Description   : Function to detect master reports
# ---------------------------------------------------------------------------------------
## CTRAS identifies the test report having the greatest page rank score as the master report for the group.

def calculate_pr_matrix(app):
	distance_matrix = np.load('/'.join([DISTANCE_BASE_PATH, app, 'distance_txt.npy']))
	# print(distance_matrix[2][4])
	# print(distance_matrix[4][2])
	dup_groups = get_dup_groups(app)  # actually is group id
	groups_pr_matrix = [] #all group
	all_reports = get_all_reports_id(app)
	for group in tqdm(dup_groups): #tqdm进度条
		pr_matrix = [] # one group
		dup_reports = get_dup_reports_of_one_group(app, group)
		for report_a in dup_reports:
			weight_list = [] # one report in the group
			for report_b in dup_reports:
				index_a = all_reports.index(report_a)
				index_b = all_reports.index(report_b)

				distance = distance_matrix[index_a][index_b] # distance_matrix[a][b] = distance_matrix[b][a]
				weight = 1 - distance
				weight_list.append(weight)
				distance = 0
				weight = 0
			pr_matrix.append(weight_list) # n*n 一个点到他所在的group的其他所有点的距离
		groups_pr_matrix.append(pr_matrix)
	return groups_pr_matrix

def get_pagerank(app):
	groups_pr_matrix = calculate_pr_matrix(app)
	pr_list = []
	for i, pr_matrix in enumerate(groups_pr_matrix):
		a_matrix = np.array(pr_matrix) # 是一个n*n的
		M = graphMove(a_matrix)
		pr = firstPr(M)  
		p = 0.8
		re = pageRank(p,M,pr)        
		pr_list.append(re)
	return pr_list

def get_master_report(app)->list:
	pr_list = get_pagerank(app)  #all groups' pagerank矩阵 n*1
	group_master = {}
	i = 0 #这个i也没用。。。
	for group in sorted(os.listdir('/'.join([DUPLICATES_CLUSTER_PATH, app]))):
		group_id = group.split('.')[0]
		if group_id != '':
			pos = np.where(pr_list[i] == np.max(pr_list[i]))[0][0] #mater report的index
			pos = int(str(pos))
			reports = sorted(os.listdir('/'.join([DUPLICATES_CLUSTER_PATH, app, group_id]))) #sorted？你确定要sorted？是的，因为之前所有都是sorted，但感觉有点丑，有个dict会更好吧
			group_master[group_id] = reports[pos].split('.')[0]
			i = i + 1
	return group_master

def detect_master_report(app):
	master_report = get_master_report(app)

	if not os.path.exists('/'.join([MASTER_REPORT_PATH, app])):
		os.makedirs('/'.join([MASTER_REPORT_PATH, app]))

	f = open('/'.join([MASTER_REPORT_PATH, app, 'master_report.json']), 'w+')
	f.write(json.dumps(master_report))  
	f.close()

for app in APPS:
	detect_master_report(app)
	#get_pagerank(app)