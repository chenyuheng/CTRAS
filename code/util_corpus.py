#-*- coding:utf-8 -*-
import os
from variables import CORPUS_PATH, DUPLICATES_CLUSTER_PATH

# ---------------------------------------------------------------------------------------
# Description   : Report Corpus Data Processor
# ---------------------------------------------------------------------------------------

# return the list that contains all the id of the review. e.g. [1,2,]
def get_all_reports_id(app:str)->list:
	all_reports_id = []
	for report_file_name in sorted(os.listdir('/'.join([CORPUS_PATH, app]))): # report = 1111.txt 是一个文件名
		report_id = report_file_name.split('.')[0]
		all_reports_id.append(report_id)
	return all_reports_id
# return duplicate cluster id
def get_dup_groups(app):
	dup_groups = []
	for report in sorted(os.listdir('/'.join([DUPLICATES_CLUSTER_PATH, app]))):
		dup_groups.append(report)
	return dup_groups

def get_dup_reports_of_one_group(app, group_id):
	dup_reports = []
	for report in sorted(os.listdir('/'.join([DUPLICATES_CLUSTER_PATH, app, group_id]))):
		report_id = report.split('.')[0]
		if report_id !='':
			dup_reports.append(report_id)
	return dup_reports

