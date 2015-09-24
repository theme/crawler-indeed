import random
import urllib2

import ConfigParser
import codecs,os
SCRIPT_DIR = os.path.dirname(__file__)
config = ConfigParser.ConfigParser()
config.readfp(codecs.open(os.path.join(SCRIPT_DIR,'./config.ini'), 'r', encoding='utf-8'))

# proxy dict for urllib2
def build_opener():
    proxy_dict ={ 'http':config.get('proxy', 'http') , 'https':config.get('proxy', 'https') }
    p = urllib2.ProxyHandler(proxy_dict)
    h = urllib2.HTTPHandler(debuglevel = 0)
    useproxy = config.get('proxy', 'useproxy')
    if 'yes' == useproxy:
        opener = urllib2.build_opener(p, h)
    else:
        opener = urllib2.build_opener()
    return opener

def randomize_user_agent():
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17',
        'Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))',
        'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)'
    ]
    return random.choice(user_agents)

def urlopen(url, data = None, headers = None):
    headers = headers or {}
    headers['User-Agent'] = randomize_user_agent()
    request = urllib2.Request(url, data, headers)
    opener = build_opener()
    return opener.open(request)

def read(url, data = None, headers = None):
    req = urlopen(url, data, headers)
    return req.read()
