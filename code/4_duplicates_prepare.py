#-*- coding:utf-8 -*-
import os, csv
from shutil import copyfile

from variables import APPS
from variables import CORPUS_PATH, RAW_IMG_PATH, DUPLICATES_REPORT_PATH, DUPLICATES_CLUSTER_PATH, DUPLICATES_CLUSTER_IMG_PATH

# ---------------------------------------------------------------------------------------
# Description   : Function to prepare the duplicate report data
# ---------------------------------------------------------------------------------------

def prepare_txt(app):
	with open('/'.join([DUPLICATES_REPORT_PATH, app, 'duplicate_set.csv'])) as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			if len(row) == 1: # 只包含一个review的cluster
				continue

			tag = row[0] # tag 是review的id
			#print("row[0] {}".format(row[0])) #135552
			if not os.path.exists('/'.join([DUPLICATES_CLUSTER_PATH, app, str(tag)])):
				os.makedirs('/'.join([DUPLICATES_CLUSTER_PATH, app, str(tag)]))
			
			for i in range(len(row)):
				report_id = row[i]

				from_name = '/'.join([CORPUS_PATH, app, str(report_id) + '.txt'])
				to_name = '/'.join([DUPLICATES_CLUSTER_PATH, app, str(tag), str(report_id) + '.txt'])
				copyfile(from_name, to_name) # 就是把同一个cluster的review的txt文件都拷贝到了同一个文件夹下


for app in APPS:
	prepare_txt(app)
