#-*- coding:utf-8 -*-
import os, json
from scipy.spatial import distance

from variables import POS_TAGS, APPS
from variables import RAW_IMG_PATH, DUPLICATES_CLUSTER_PATH, DUPLICATES_CLUSTER_IMG_PATH, MASTER_REPORT_PATH
from variables import img_similar_threshold, T_THRESHOLD

from util_corpus import get_dup_groups
from util_db import insert_diff_sentence_into_sql, insert_diff_img_into_sql
from util_hist import read_hist_img, get_img_pos
from util_hist import processing, preprocess_line

# ---------------------------------------------------------------------------------------
# Description   : Function to detect textual and image difference item candidates
# ---------------------------------------------------------------------------------------

# return {group_id_1 : master_report_id, group_id_2 : master_report_id ....}
def read_master_reports(app):
	with open('/'.join([MASTER_REPORT_PATH, app, 'master_report.json']), 'r') as load_f:
		load_dict = json.load(load_f)
		return load_dict
# sentence_b  在 master report中有没有相似的句子，如果有就返回true
def is_same_report_sentence(master_words, sentence_b):
	for sentence_a in master_words:
		if is_same_sentence(sentence_a, sentence_b):
			return True
	return False

def is_same_sentence(sentence_a,sentence_b):
	if len(sentence_b) == 1 and sentence_b[0] == '': ## 这是要干啥？？？？？大概结束句是空格？所以单独处理一下？
		return True
	inter = 0
	union = 0
	for word_a in sentence_a:
		for word_b in sentence_b:
			if word_a == word_b:
				inter = inter + 1
	union = len(sentence_a) + len(sentence_b) - inter
	distance = 1 - (inter*1.0) / (union*1.0)
	if distance <= T_THRESHOLD:
		return True
	return False

def get_sentence(app, group_id, report_id, index):
	f = open('/'.join([DUPLICATES_CLUSTER_PATH, app, group_id, report_id+'.txt']), 'r')
	i = 0
	for line in f.readlines():
		if i == index:
			sentence = line.replace('\n', '')
			return sentence
		i = i + 1
	f.close()
	return None

def detect_diff_txt(app):
	saved_list = {}
	dup_groups = get_dup_groups(app) # all the group id
	master_reports = read_master_reports(app) # dict
	for group_id in dup_groups: #每一个group
		master_id = master_reports[str(group_id)]
		master_words = processing(app, group_id, master_id)
		for report in sorted(os.listdir('/'.join([DUPLICATES_CLUSTER_PATH, app, group_id]))):  #这个group中的每一个report
			report_id = report.split('.')[0]
			if report_id == master_id:
				continue

			report_words = processing(app, group_id, report_id)
			diff_sentence_index = 0
			for sentence_b in report_words: #这个report中的每一个sentence
				if not is_same_report_sentence(master_words, sentence_b): # 这是一句不同的sentence.
					sentense_b_initial = get_sentence(app, group_id, report_id, diff_sentence_index) #获取initial sentence (区别就是没有做奇怪的processing那一套)
					flag = str(report_id) + str(diff_sentence_index) #
					if flag not in saved_list.keys() or saved_list[flag] != group_id: #为什么要加这个判断？ 这个判断条件有点奇怪？ 一个report会被分到不同的组吗？
						insert_diff_sentence_into_sql(app, (group_id), sentense_b_initial, diff_sentence_index, (report_id))
						saved_list[flag] = group_id # 这句话是哪个组的
				diff_sentence_index += 1

# def processing_master_imgs(app, group_id, master_id):
# 	imgs = []
# 	for name in os.listdir('/'.join([DUPLICATES_CLUSTER_IMG_PATH, app, group_id])):
# 		report_id = name.split('-')[0]
# 		if report_id == master_id:
# 			imgs.append(name)
# 	return imgs

# def processing_non_master_imgs(app, group_id, master_id):
# 	imgs = []
# 	for name in os.listdir('/'.join([DUPLICATES_CLUSTER_IMG_PATH, app, group_id])):
# 		report_id = name.split('-')[0]
# 		if report_id != master_id:
# 			imgs.append(name)
# 	return imgs

# def is_same_report_img(master_imgs, img_b):
# 	for img_a in master_imgs:
# 		if is_same_img(app, img_a, img_b):
# 			return True
# 	return False

# def is_same_img(app, img_name_a, img_name_b):
# 	hist_img = read_hist_img(app)

# 	index_a = get_img_pos(img_name_a)
# 	index_b = get_img_pos(img_name_b)

# 	img_a = hist_img[index_a]
# 	img_b = hist_img[index_b]
# 	dis = distance.euclidean(img_a, img_b)
# 	if dis <= img_similar_threshold:
# 		return True
# 	return False

# def detect_diff_img(app):
# 	saved_list = {}
# 	dup_groups = get_dup_groups(app)
# 	master_reports = read_master_reports(app)
# 	for group_id in dup_groups:
# 		master_id = master_reports[str(group_id)]
# 		master_imgs = processing_master_imgs(app, group_id, master_id)
# 		non_master_imgs = processing_non_master_imgs(app, group_id, master_id)

# 		for img_b in non_master_imgs:
# 			if not is_same_report_img(master_imgs, img_b):
# 				if img_b not in saved_list.keys() or saved_list[img_b] != dup_groups:
# 					insert_diff_img_into_sql(app, (group_id), img_b, (img_b.split('-')[0]))
# 					saved_list[img_b] = dup_groups

for app in APPS:
	detect_diff_txt(app)
	#detect_diff_img(app)
