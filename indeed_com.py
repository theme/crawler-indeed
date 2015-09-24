#!/usr/bin/python
# -*- coding: utf8 -*-

## www.indeed.com is a job info site
# div id="SALARY_rbo" class="rbsrbo"
#   ul class="rbList"
#       li onmousedown="rbptk('rb', 'salest', '1');"
#           <a title="$60,000+ (236)" href = >$60,000+</a>
#       li onmousedown="rbptk('rb', 'salest', '1');"
#       li onmousedown="rbptk('rb', 'salest', '1');"
#       li ...

import urllib2
import re
import datetime
from urlparse import urlparse
from urlparse import urljoin

from bs4 import BeautifulSoup
import urlproxy as urlp

import logging
# logging.basicConfig(level = logging.INFO)
logging.basicConfig(level = logging.DEBUG)
logger = logging.getLogger(__name__)

import ConfigParser
import codecs,os
SCRIPT_DIR = os.path.dirname(__file__)
config = ConfigParser.ConfigParser()
config.readfp(codecs.open(os.path.join(SCRIPT_DIR,'./config.ini'), 'r', encoding='utf-8'))
SITE_COOKIE = config.get('site', 'cookie')
logger.info('[site] cookie=%s' % SITE_COOKIE)

class Page:
    url = ''
    html = ''
    soup = None
    def __init__(self, url):
        urlp = urlparse(url, 'http')
        self.url = urlp.geturl()
    def getHtml(self):
        if self.html:
            return self.html
        else:
            self.html = urlp.read(self.url,
                            headers = {'Cookie':SITE_COOKIE})
        return self.html
    def getSoup(self):
        if self.soup:
            return self.soup
        else:
            page_html = self.html or self.getHtml()
            self.soup = BeautifulSoup(page_html)
        return self.soup


class QueryPage(Page):
    def __init__(self, url, num = 1):
        Page.__init__(self, url)
    def salaryDiv(self):
        # div id="SALARY_rbo" class="rbsrbo"
        return self.getSoup().find(id='SALARY_rbo')
    def salaries(self):
        '''return a dict of li in salary div'''
#   ul class="rbList"
#       li onmousedown="rbptk('rb', 'salest', '1');"
#           <a title="$60,000+ (236)" href = >$60,000+</a>
        d = {}
        for a in self.salaryDiv().find('ul', class_ = 'rbList').find_all('a'):
            s = a['title'].replace(',','')
            m = re.match(r"\$(\d+)\+\ \((\d+)\)$", s)
            d[m.group(1)] = m.group(2)
        return d

def query(url):
    return QueryPage(url).salaries()

