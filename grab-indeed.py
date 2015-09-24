#!/usr/bin/python
# -*- coding: utf8 -*-

import os
from time import sleep
import logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

import indeed_com

import ConfigParser
import codecs
SCRIPT_DIR = os.path.dirname(__file__)
config = ConfigParser.ConfigParser()
config.readfp(codecs.open(os.path.join(SCRIPT_DIR,'./config.ini'), 'r', encoding='utf-8'))
QUERY_URL_TEMPLATE = config.get('query', 'template')

# read query tgt data
from uritemplate import variables
from uritemplate import expand
query_f = codecs.open(os.path.join(SCRIPT_DIR,'./queries.txt'), 'r', encoding='utf-8')
QUERIES= []
keys = query_f.readline().split("\t")
keys = [ x.strip() for x in keys ]
qurls = []
for line in query_f:
    values = line.split("\t")
    values = [ x.strip() for x in values ]
    d = {}
    for i in range(0, len(keys)):
        d[keys[i]] = values[i]
    qurls.append(expand(QUERY_URL_TEMPLATE, d))

# query and save salaries { salary: num of jobs }
from openpyxl import Workbook
SAVE_DIR = config.get('save', 'dir')
SAVE_FILENAME = config.get('save', 'filename')
def main():
    wb = Workbook()
    ws = wb.active
    for q in qurls:
        ws.append([q])
        d = indeed_com.query(q);
        print q
        print d
        for k,v in d.items():
            ws.append([k,v])
        # write 
    wb.save(os.path.join(SAVE_DIR, SAVE_FILENAME))

if __name__ == '__main__': # not as a module
    main()

