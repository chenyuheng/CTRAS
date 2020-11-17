#-*- coding:utf-8 -*-
import os,csv
import numpy as np
import time
from scipy.spatial import distance
from itertools import combinations, product
from tqdm import tqdm

from variables import APPS
from variables import DISTANCE_BASE_PATH
from variables import img_similar_threshold, alpha, beta

from util_corpus import get_all_reports
from util_hist import read_hist_txt, read_hist_img, get_hist_txt, get_hist_img

# ---------------------------------------------------------------------------------------
# Description   : Function to calculate distance between reports
# ---------------------------------------------------------------------------------------

def distance_txt_jaccard(hist_a, hist_b):
	inter = 0
	union = 0
	for i in range(len(hist_a)):
		if hist_a[i] > 0 and hist_b[i] > 0:
			inter += 1
			union += 1
		elif hist_a[i] > 0 or hist_b[i] > 0:
			union += 1
	if union == 0.0:
		return 1.0
	return 1.0 - (inter*1.0)/(union*1.0)

def distance_report_harmonic(DT, DS, hist_img_a, hist_img_b):
	if DT == 0.0:
		return 0.0
	if DS == 0.0:
		return alpha*DT
	return (1+beta*beta)*(DS*DT)/(beta*beta*DS+DT)

def calculate_distance(app):
	if not os.path.exists('/'.join([DISTANCE_BASE_PATH, app])):
		os.makedirs('/'.join([DISTANCE_BASE_PATH, app]))
	
	all_reports_id = get_all_reports(app)
	# print("len(all_reports_id) : {}".format(len(all_reports_id))) # len(all_reports_id) : 1000
	hist_txt = read_hist_txt(app) # 之前计算的 idf矩阵
	#print("type(hist_txt) : {}",format(type(hist_txt))) # {} <class 'scipy.sparse.csr.csr_matrix'>
	#print("hist_txt.shape {}".format(len(hist_txt.todense().tolist()[0]))) # hist_txt.shape (1000, 200) ->  1000 条 ， 每条 200
	#exit()
	distance_matrix_txt = [([0] * len(all_reports_id)) for i in range(len(all_reports_id))] # 1000 * 1000
	hist_txt_dict = {}
	for i in range(len(all_reports_id)):
		reports_id = all_reports_id[i]
		hist_txt_dict[reports_id] = get_hist_txt(app, hist_txt, reports_id)

	for i in tqdm(range(len(all_reports_id))):
		for j in range(len(all_reports_id)):
			t0 = time.time()
			report_a = all_reports_id[i]
			report_b = all_reports_id[j]
			hist_txt_a = hist_txt_dict[report_a]
			hist_txt_b = hist_txt_dict[report_b]
			distance_txt = distance_txt_jaccard(hist_txt_a, hist_txt_b)
			distance_matrix_txt[i][j] = distance_txt
			#print(f"1: {str(time.time() - t0)}")
	
	# save all distance
	np.save('/'.join([DISTANCE_BASE_PATH, app, 'distance_txt.npy']), distance_matrix_txt)

for app in APPS:
	calculate_distance(app) # calculate and save hybrid distance between reports