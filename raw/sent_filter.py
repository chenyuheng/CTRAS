import csv
import re

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer

keyword_dict = {}
stopWords = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")

with open("new_keywords.csv", "r") as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        keyword_dict[row[0]] = float(row[1])

def nlp_process(content: str) -> list:
    words_filtered = []
    tokenizer = RegexpTokenizer(r'\w+')
    result = tokenizer.tokenize(content)
    for w in result:
        w = w.lower()
        if w not in stopWords:
            if re.fullmatch("([A-Za-z0-9-'])\\w+", w) is not None:
                words_filtered.append(w)
    result = []
    for w in words_filtered:
        result.append(stemmer.stem(w))
    return result

def get_sent_score(sent: str) -> float:
    sent_list = nlp_process(sent)
    score = 0
    for item in sent_list:
        if item in keyword_dict.keys():
            score += keyword_dict[item]
    return score

rf = open("report_ONSF.csv", "w")
csv_writer = csv.writer(rf)

with open("report_ONS.csv", "r") as f:
    csv_reader = csv.reader(f)
    sents = []
    for row in csv_reader:
        score = get_sent_score(row[1])
        if score > 5:
            sents.append(row[1])
    count = 0
    for sent in sents:
        csv_writer.writerow([count, sent])
        count += 1
rf.close()