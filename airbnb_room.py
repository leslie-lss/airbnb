# -*- coding: utf-8 -*-
#https://zh.airbnb.com/rooms/443684
#获取文章正文内容

import sys
import redis
import requests
import random
import time
from lxml import etree
from pymongo import MongoClient


my_headers = [    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
                  "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
                  'Opera/9.25 (Windows NT 5.1; U; en)',
                  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                  'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
                  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
                  'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
                  "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
                  "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36']
headers = {
    'user-agent': random.choice(my_headers),
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Enocding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'origin': 'https://zh.airbnb.com',
    'connection': 'keep-alive'
}


def get_article(id):
    url = 'https://zh.airbnb.com/api/v2/pdp_listing_details/{0}?' \
          '_format=for_rooms_show&request_url=https%3A%2F%2Fzh.airbnb.com%2Frooms%2F{1}' \
          '&&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&'.format(id, id)
    print(url)
    retry = 3
    while retry > 0:
        try:
            page_source = requests.get(url, headers=headers, timeout=10).json(encoding='utf-8')
            retry = 0
        except:
            print("@@@@@@@@@@@@@@@@sleep@@@@@@@@@@@@@@")
            time.sleep(60)
            print("retry:" + " " + str(retry))
            retry = retry - 1
            if retry == 0:
                sys.exit(0)
    main_info = page_source['pdp_listing_detail']
    info = {
        '_id': id,
        'name': main_info['name'],
        'localized_city': main_info['localized_city'],
        'primary_host': main_info['primary_host'],
        'review_details_interface': main_info['review_details_interface'],
        'visible_review_count': main_info['visible_review_count'],
        'user': main_info['user']
    }

    return info

def get_comment(id, count):
    comment_page = 0
    flag = True
    comment_info = []
    while flag:
        time.sleep(2)
        comment_url = 'https://zh.airbnb.com/api/v2/reviews?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=CNY&locale=zh&listing_id={0}' \
                      '&role=guest&_format=for_p3&_limit=7&_offset={1}&_order=language_country'.format(id, str(comment_page * 7))
        print(comment_url)
        retry = 3
        while retry > 0:
            try:
                page_source = requests.get(comment_url, headers=headers, timeout=10).json(encoding='utf-8')
                retry = 0
            except:
                print("@@@@@@@@@@@@@@@@sleep@@@@@@@@@@@@@@")
                time.sleep(60)
                print("retry:" + " " + str(retry))
                retry = retry - 1
                if retry == 0:
                    sys.exit(0)
        comment_info.extend(page_source['reviews'])
        comment_page = comment_page + 1
        if comment_page * 7 >= count:
            flag = False
    return comment_info

def save_mongo(dict):
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.airbnb
    my_set = db.room_1126_1747
    try:
        my_set.insert(dict)
        print('******************insert database success!*************************')
    except:
        print('###################insert database fail!!#######################')


def get_url_from_redis(url_list):
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.airbnb
    my_set = db.room_1126_1747
    while r.llen(url_list) > 0:
        print('----------------------------------------------------------------------------------------------------')
        x = r.lpop(url_list)
        if my_set.find({'_id': x}).count() > 0:
            continue
        info = get_article(x)
        info['comment_info'] = get_comment(x, int(info['visible_review_count']))
        save_mongo(info)
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

if __name__ == '__main__':
    url_list = 'url'
    get_url_from_redis(url_list)

    # conn = MongoClient('127.0.0.1', 27017)
    # db = conn.airbnb
    # my_set = db.room_1126_1747
    # new_set = db.room_1127
    # for x in my_set.find():
    #     if new_set.find({'_id': x['_id']}).count() > 0:
    #         continue
    #     if x.has_key('user'):
    #         print("********************************")
    #         new_set.insert(x)
    #     else:
    #         try:
    #             info = get_article(x['_id'])
    #             x['user'] = info['user']
    #             print("###############################")
    #         except:
    #             print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    #         new_set.insert(x)