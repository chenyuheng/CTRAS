#-*- coding:utf-8 -*-
import os,csv
import numpy as np
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
	
	all_reports = get_all_reports(app)
	hist_txt = read_hist_txt(app)

	distance_matrix_txt = [([0] * len(all_reports)) for i in range(len(all_reports))]

	for i in tqdm(range(len(all_reports))):
		for j in range(len(all_reports)):
			report_a = all_reports[i]
			report_b = all_reports[j]

			hist_txt_a = get_hist_txt(app, hist_txt, report_a)
			hist_txt_b = get_hist_txt(app, hist_txt, report_b)

			distance_txt = distance_txt_jaccard(hist_txt_a, hist_txt_b)

			distance_matrix_txt[i][j] = distance_txt
	
	# save all distance
	np.save('/'.join([DISTANCE_BASE_PATH, app, 'distance_txt.npy']), distance_matrix_txt)

for app in APPS:
	calculate_distance(app) # calculate and save hybrid distance between reports