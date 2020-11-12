#-*- coding:utf-8 -*-
import os

APPS = [ "DD"] # names of all apps
CTRAS_root_path = "/home/yiwu/inno3/CTRAS/"
HEADER = {
    'id': 0,
    'create_time_millis': 1,
    'bug_category': 2,
    'description': 3,
    'img_url': 4,
    'severity': 5,
    'recurrent': 6
} # raw report csv file header

# '_n',
POS_TAGS = ["_CC", "_CD", "_DT", "_EX", "_FW", "_IN", "_JJ", "_JJR", "_JJS",
"_LS", "_MD", "_NN", "_NNS", "_NNP", "_NNPS", "_PDT", "_POS", "_PRP", "_PRP$",
 "_RB", "_RBR", "_RBS", "_RP", "_SYM", "__TO", "__UH", "__VB", "_VBD", "_VBG",
 "_VBN", "_VBP", "_VBZ", "_WDT", "_WP", "_WP$", "_WRB"]
# ['_a', '_b', '_c', '_d', '_e',
#     '_g', '_h', '_i', '_j', '_k', '_m',
#     '_nd', '_nh', '_ni', '_nl', '_ns', '_nt', '_nz',
#     '_o', '_p', '_q', '_r', '_u', '_v', '_wp', '_ws', '_x']

LTP_DATA_DIR = '/home/student/ltp-data-v3.4.0' # LTP path
cws_model_path = '/home/student/ltp_data_v3.4.0/cws.model'
pos_model_path = '/home/student/ltp_data_v3.4.0/pos.model'

STOP_WORDS_PATH = CTRAS_root_path+'stopwords.txt'
SYNONYM_WORDS_PATH = CTRAS_root_path+'cilin_ex.txt'

RAW_PATH = CTRAS_root_path+'raw' # raw report path
RAW_IMG_PATH = '' # raw report images path
CORPUS_PATH = CTRAS_root_path+'corpus' # preprocessed report path
HIST_TXT_PATH = CTRAS_root_path+'hist' # text hist path
HIST_IMG_PATH = '' # image hist path
DISTANCE_BASE_PATH = CTRAS_root_path+'dist_base' # hybrid distance path
DUPLICATES_REPORT_PATH = CTRAS_root_path+'duplicate_report' # duplicate groups path
DUPLICATES_CLUSTER_PATH = CTRAS_root_path+'duplicate_cluster' # duplicate report group
DUPLICATES_CLUSTER_IMG_PATH = '' # duplicate report images group
MASTER_REPORT_PATH = CTRAS_root_path+'master_report' # master report path

K = 0.25 # summary compression ratio

######## PARAMETERS ########
HIST_IMG_DICT_SIZE = 200    # default
HIST_IMG_LAYER_NUM = 3      # default

T_THRESHOLD = 0.6               # default
img_similar_threshold = 0.01    # default
LINK_THRESHOLD = 0.2

alpha = 0.75    # default
beta = 5
######## PARAMETERS ########
