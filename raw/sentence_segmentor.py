#!/usr/bin/env python
# encoding: utf-8

import csv
import nltk.data

count = 0
rf = open("report_DDGS.csv", "w")
csv_writer = csv.writer(rf)
with open("report_DDG.csv", "r") as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        text = row[1]
        sent_detector = nltk.data.load("tokenizers/punkt/english.pickle")
        sents = sent_detector.tokenize(text.strip())
        for sent in sents:
            csv_writer.writerow([count, sent])
            count += 1
rf.close()



