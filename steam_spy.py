# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import requests
import re
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup as Soup

from time import sleep
from functimeout.timeout import timeout

base_url = 'https://store.steampowered.com/'

cookie = {}
cookie['mature_content'] = '1'
cookie['birthtime'] = '-157795199'
cookie['lastagecheckage'] = '1-January-1965'
cookie['Steam_Language'] = 'schinese'
cookie['bShouldUseHTML5'] = '1'

steam_category = {}
steam_category['Game'] = '998'
steam_category['Software'] = '994'
steam_category['Video'] = '992'
steam_category['DLC'] = '21'
steam_category['Demo'] = '10'
steam_category['Mod'] = '997'
steam_category['Hardware'] = '993'
steam_category['Trailer'] = '999'
steam_category['All'] = ''

steam_search_url = base_url + 'search/?category1='

@timeout(30)
def safe_get_request(url, param, cookie):
    return requests.get(url, allow_redirects = False, params = param, cookies = cookie, timeout = 30)

def steam_read_page_num(soup):
    tag = soup.find('div', 'search_pagination_right')
    links = tag.find_all('a')
    link_num = len(links)
    if link_num == 0:
        return 1
    else:
        return int(links[link_num - 2].string)

def steam_read_page_content(soup):
    content_messages = []
    contents = soup.find('div', id = 'search_result_container').find('div', '').find_all('a')
    for content in contents:
        message = {}
        if content.has_attr('data-ds-packageid'):
            message['packageid'] = content['data-ds-packageid']
        message['appid'] = content['data-ds-appid']
        message['title'] = content.find('span', 'title').string
        message['release_date'] = content.find('div', 'col search_released responsive_secondrow').string
        content_messages.append(message)
    return content_messages

def steam_read_dlc(page):
    param = {'category1':steam_category['DLC'], 'page':str(page)}
    try:
        response = safe_get_request(base_url + 'search/', param, cookie)
        messages = steam_read_page_content(Soup(response.text, 'lxml'))
        for message in messages:
            if message.has_key('packageid'):
                print ('Subid: {id}\t\tTitle: {title}'.format(id=message['packageid'], title=message['title']))
            else:
                print ('Appid: {id}\t\tTitle: {title}'.format(id=message['appid'], title=message['title']))
    except:
        steam_read_dlc(page)

def steam_read_demo(page):
    param = {'category1':steam_category['Demo'], 'page':str(page)}
    try:
        response = safe_get_request(base_url + 'search/', param, cookie)
        messages = steam_read_page_content(Soup(response.text, 'lxml'))
        for message in messages:
            if message.has_key('packageid'):
                print ('Subid: {id}\t\tTitle: {title}'.format(id=message['packageid'], title=message['title']))
            else:
                print ('Appid: {id}\t\tTitle: {title}'.format(id=message['appid'], title=message['title']))
    except:
        steam_read_demo(page)

def steam_read_game(page):
    param = {'category1':steam_category['Game'], 'page':str(page)}
    try:
        response = safe_get_request(base_url + 'search/', param, cookie)
        messages = steam_read_page_content(Soup(response.text, 'lxml'))
        for message in messages:
            if message.has_key('packageid'):
                print ('Subid: {id}\t\tTitle: {title}'.format(id=message['packageid'], title=message['title']))
            else:
                print ('Appid: {id}\t\tTitle: {title}'.format(id=message['appid'], title=message['title']))
    except:
        steam_read_demo(page)

param = {'category1':steam_category['Game']}
response = safe_get_request(base_url + 'search/', param, cookie)
page_num = steam_read_page_num(Soup(response.text, 'lxml'))
pages = range(1, page_num + 1)

pool = ThreadPool(16)
pool.map(steam_read_game, pages)

pool.close()
pool.join()
