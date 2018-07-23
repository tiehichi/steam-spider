# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import re
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup as Soup

base_url = 'https://store.steampowered.com/app/'
appids = range(0, 10000)
cookie = {}

cookie['mature_content'] = '1'
cookie['birthtime'] = '-157795199'
cookie['lastagecheckage'] = '1-January-1965'
cookie['Steam_Language'] = 'schinese'
cookie['bShouldUseHTML5'] = '1'

def check_appid(appid):
    r = requests.get(base_url + str(appid), allow_redirects = False, cookies = cookie, timeout = 30)
    if r.status_code == 302:
        if re.search(base_url + str(appid), r.headers['Location']) != None:
            r = requests.get(r.headers['Location'], allow_redirects = False, cookies = cookie, timeout = 30)
            soup = Soup(r.text, 'lxml')
            appname = soup.find_all("div", "apphub_AppName")[0].string
            print ('Appid: {id}\t\tName: {name}'.format(id=str(appid), name=appname))
            return base_url + str(appid)
    elif r.status_code == 200:
        soup = Soup(r.text, 'lxml')
        targets = soup.find_all("div", "apphub_AppName")
        if len(targets) != 0:
            appname = targets[0].string
            print ('Appid: {id}\t\tName: {name}'.format(id=str(appid), name=appname))
            return base_url + str(appid)
        else:
            return ''
    else:
        print ('Error in {id}'.format(id=str(appid)))
        print ('Status Code {status}'.format(status=str(r.status_code)))
        return ''

pool = ThreadPool(8)
results = pool.map(check_appid, appids)

pool.close()
pool.join()
