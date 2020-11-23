#-*- coding:utf-8 -*-
import os
from scipy.io import loadmat
from scipy.sparse import load_npz
from variables import POS_TAGS
from variables import CORPUS_PATH, RAW_IMG_PATH, DUPLICATES_CLUSTER_PATH
from variables import HIST_TXT_PATH, HIST_IMG_PATH
from variables import HIST_IMG_DICT_SIZE, HIST_IMG_LAYER_NUM

# ---------------------------------------------------------------------------------------
# Description   : Textual/Image Feature Hist Processor
# ---------------------------------------------------------------------------------------

def read_hist_txt(app):
	hist_txt = load_npz('/'.join([HIST_TXT_PATH, app + '.npz']))
	return hist_txt # [n_samples, n_features]

def read_hist_img(app):
	img_mat = loadmat('/'.join([HIST_IMG_PATH, app, 
		'pyramids_all_' + str(HIST_IMG_DICT_SIZE) + '_' + str(HIST_IMG_LAYER_NUM) + '.mat']))
	hist_img = img_mat['pyramid_all'] # [n_samples, 4200]
	return hist_img

def get_hist_txt(app, hist_txt, report_id)->list:
	# get the text hist according to report_id
	reports = sorted(os.listdir('/'.join([CORPUS_PATH, app])))
	reports = [x.split('.')[0] for x in reports]
	return hist_txt[reports.index(report_id)].todense().tolist()[0]

def get_hist_img(app, hist_img, report_id):
	# get the image hist according to report_id, it may contain multiple images
	imgs = sorted(os.listdir('/'.join([RAW_IMG_PATH, app])))
	indices = [i for i,x in enumerate(imgs) if x.split('-')[0] == report_id]
	return [hist_img[i] for i in indices]

def get_hist_img_by_img_name(app, hist_img, img_name):
	imgs = sorted(os.listdir('/'.join([RAW_IMG_PATH, app]))) # may contain multiple images
	index = [i for i,x in enumerate(imgs) if x == img_name.encode('utf-8')]
	return [hist_img[i] for i in index][0]

def get_img_pos(img_name):
	index = 0
	for img in sorted(os.listdir('/'.join([RAW_IMG_PATH, app]))):
		if img_name == img:
			return index
		index = index + 1
	return -1

def preprocess_line(line):
	# print("POS_TAGS:")
	# print(POS_TAGS)
	# print("--------------------------------------------------")
	for tag in POS_TAGS:
		line = line.replace(tag, tag+' ') #pos_tag 后加一个空格??? 我觉得如果没有用到，去除pos tag或者更新库
	line = line.replace('  ', ' ').replace('__','-_').replace('\n','') #很奇怪啊？？？？
	return line

def parse_words(sentence):
	sentence = preprocess_line(sentence)
	words = [x.split('_')[0] for x in sentence.split(' ')]
	return words

def processing(app, group_id, report_id): # read file content
	# print("group_id {} , report_id {}".format(group_id, report_id))
	f = open('/'.join([DUPLICATES_CLUSTER_PATH, app, group_id, report_id+'.txt']), 'r')
	line_list = [] # read one report into the list. A sentence is a list of words. A report is a list of sentence.
	for line in f.readlines():
		if line == '':
			break	
		line = preprocess_line(line)
		words = [x.split('_')[0] for x in line.split(' ')]  # x.split('_')[0]是为了 app_NN -> app
		print(words)
		exit()
		line_list.append(words) #就是只得到了原report中的单词（应该是这样）
	f.close()
	return line_list