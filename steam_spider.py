# -*- coding:utf-8 -*-
from __future__ import print_function

import sys
if sys.version < '3':
    reload(sys)
    sys.setdefaultencoding('utf-8')

import requests
import re
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup as Soup

from time import sleep
from timeout_decorator import timeout

import getopt
import csv

base_url = 'https://store.steampowered.com/'

cookie = {}
cookie['mature_content'] = '1'
cookie['birthtime'] = '-157795199'
cookie['lastagecheckage'] = '1-January-1965'
cookie['Steam_Language'] = 'english'
cookie['bShouldUseHTML5'] = '1'

steam_category = {}
steam_category['game'] = '998'
steam_category['software'] = '994'
steam_category['video'] = '992'
steam_category['dlc'] = '21'
steam_category['demo'] = '10'
steam_category['mod'] = '997'
steam_category['hardware'] = '993'
steam_category['trailer'] = '999'
steam_category['bundle'] = '996'
steam_category['all'] = ''


@timeout(15, use_signals=False)
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
            message['id'] = content['data-ds-packageid']
            message['type'] = 'sub'
        elif content.has_attr('data-ds-bundleid'):
            message['id'] = content['data-ds-bundleid']
            message['type'] = 'bundle'
        else:
            message['id'] = content['data-ds-appid']
            message['type'] = 'app'

        message['title'] = content.find('span', 'title').string
        message['release_date'] = content.find('div', 'col search_released responsive_secondrow').string

        discount_span = content.find('div', 'col search_discount responsive_secondrow').find('span')
        is_discount = (discount_span != None)
        if is_discount:
            message['discount'] = discount_span.string

            price_div = content.find('div', 'col search_price discounted responsive_secondrow')
            message['original_price'] = price_div.find('strike').string
            message['current_price'] = price_div.contents[len(price_div.contents)-1].replace('\t', '')
        else:
            message['discount'] = ''
            message['current_price'] = content.find('div', 'col search_price responsive_secondrow').string.replace('\t', '').replace('\n', '').replace('\r', '')
            message['original_price'] = message['current_price']

        content_messages.append(message)
    return content_messages

def steam_read_page(page, category, cookie):
    param = {'category1':category, 'page':str(page)}
    try:
        response = safe_get_request(base_url + 'search/', param, cookie)
        messages = steam_read_page_content(Soup(response.text, 'lxml'))

        print ('Read Page {page} Success'.format(page=page))
        return messages
    except Exception as exp:
        print ('Read Page {page} Error, Retry in 3s'.format(page=page, type=category), file=sys.stderr)
        sleep(3)
        return steam_read_page(page, category, cookie)

def steam_read_all_multithread(category, cookie, threads, output_file):
    param = {'category1':category}
    pages = []

    try:
        response = safe_get_request(base_url + 'search/', param, cookie)
        page_num = steam_read_page_num(Soup(response.text, 'lxml'))
        pages = range(1, page_num + 1)
    except Exception as exp:
        return steam_read_all_multithread(category, cookie, threads)

    pool = ThreadPool(threads)
    steam_messages = pool.map(lambda p: steam_read_page(p, category, cookie), pages)

    pool.close()
    pool.join()

    print ('Waitting for write in csv')

    headers = ['id', 'type', 'title', 'release_date', 'discount', 'original_price', 'current_price']
    with open(output_file, 'w') as f:
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()

    for message in steam_messages:
        with open(output_file, 'a') as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writerows(message)


if __name__ == '__main__':

    threads = 1
    category = 'All'
    output_file = 'steam_message.csv'

    categorys = ['game', 'software', 'video', 'dlc', 'demo', 'mod', 'hardware', 'trailer', 'bundle', 'all']
    languages = ['bulgarian', 'czech', 'danish', 'dutch', 'english', 'finnish', 'french', 'greek', 'german',
            'hungarian', 'italian', 'japanese', 'koreana', 'norwegian', 'polish', 'portuguese', 'brazilian',
            'russian', 'romanian', 'spanish', 'swedish', 'schinese', 'tchinese', 'thai', 'turkish', 'ukrainian']

    opts, args = getopt.getopt(sys.argv[1:], 'j:c:o:l:')
    for o, a in opts:
        if o == '-j':
            threads = int(a)
        elif o == '-c':
            if a.lower() not in categorys:
                print ('Category Not Supported')
                exit()
            else:
                category = a.lower()
        elif o == '-o':
            output_file = a
        elif o == '-l':
            if a.lower() not in languages:
                print ('Language Not Supported')
                exit()
            else:
                cookie['Steam_Language'] = a.lower()

    steam_read_all_multithread(steam_category[category], cookie, threads, output_file)
