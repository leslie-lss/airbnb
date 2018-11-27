# -*- coding: utf-8 -*-
#https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&allow_override%5B%5D=&map_toggle=false&s_tag=Yz8-d_Fe&section_offset=5&items_offset=18
#https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&allow_override%5B%5D=&map_toggle=false&s_tag=Yz8-d_Fe&section_offset=5&items_offset=36
#获取源码
import re
import sys
import urllib
import requests
import random
import time
from lxml import etree
from pymongo import MongoClient
from selenium import webdriver

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
url_base = 'https://zh.airbnb.com'
def get_url():
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&allow_override%5B%5D=&map_toggle=false&s_tag=Yz8-d_Fe&section_offset=5&items_offset=18'
    #北京
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E5%8C%97%E4%BA%AC&allow_override%5B%5D=&s_tag=S-UAuJhA&section_offset=7&items_offset=18'
    #上海
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E4%B8%8A%E6%B5%B7&allow_override%5B%5D=&s_tag=Htrl1TZ8&section_offset=7&items_offset=18'
    #重庆
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E9%87%8D%E5%BA%86&allow_override%5B%5D=&s_tag=ZHiMVrjc&section_offset=4&items_offset=18'
    #成都
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E6%88%90%E9%83%BD&allow_override%5B%5D=&s_tag=U3tDiHd-&section_offset=7&items_offset=18'
    #杭州
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E6%9D%AD%E5%B7%9E&allow_override%5B%5D=&s_tag=493ksQNV&section_offset=6&items_offset=18'
    #厦门
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E5%8E%A6%E9%97%A8&allow_override%5B%5D=&s_tag=TqLblGBq&section_offset=4&items_offset=18'
    #西安
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E8%A5%BF%E5%AE%89&allow_override%5B%5D=&s_tag=GPAsj4ZQ&section_offset=6&items_offset=18'
    #广州
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E5%B9%BF%E5%B7%9E&allow_override%5B%5D=&s_tag=M37cFsWM&section_offset=6&items_offset=18'
    # 深圳
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E6%B7%B1%E5%9C%B3&allow_override%5B%5D=&s_tag=l2VT1T5g&section_offset=4&items_offset=18'
    # 香港
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E9%A6%99%E6%B8%AF&allow_override%5B%5D=&s_tag=NWKn0wnI&section_offset=4&items_offset=18'
    # 三亚
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E4%B8%89%E4%BA%9A&allow_override%5B%5D=&s_tag=PztLN_ci&section_offset=4&items_offset=18'
    # 哈尔滨
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E5%93%88%E5%B0%94%E6%BB%A8&allow_override%5B%5D=&s_tag=zkjTW5XW&section_offset=4&items_offset=18'
    # 武汉
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E6%AD%A6%E6%B1%89&allow_override%5B%5D=&s_tag=m4eR-tFz&section_offset=4&items_offset=18'
    # 长沙
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E9%95%BF%E6%B2%99&allow_override%5B%5D=&s_tag=fP1MIZUY&section_offset=6&items_offset=18'
    # 天津
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E5%A4%A9%E6%B4%A5&allow_override%5B%5D=&s_tag=nsVY-Syd&section_offset=4&items_offset=18'
    # 南京
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E5%8D%97%E4%BA%AC&allow_override%5B%5D=&s_tag=LyTQdQV4&section_offset=6&items_offset=18'
    # 苏州
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E8%8B%8F%E5%B7%9E&allow_override%5B%5D=&s_tag=rIHKk-cM&section_offset=6&items_offset=18'
    # 昆明
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E6%98%86%E6%98%8E&allow_override%5B%5D=&s_tag=0ApYku19&section_offset=4&items_offset=18'
    # 青岛
    # url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E9%9D%92%E5%B2%9B&allow_override%5B%5D=&s_tag=nvZlgG5s&section_offset=6&items_offset=18'
    # 澳门
    url = 'https://zh.airbnb.com/s/homes?refinement_paths%5B%5D=%2Fhomes&query=%E6%BE%B3%E9%97%A8&allow_override%5B%5D=&s_tag=vAzvUOHf&section_offset=4&items_offset=18'
    while url != '':
        print(url)
        dict_list = []
        retry = 3
        while retry > 0:
            try:
                myDriver = webdriver.PhantomJS(r'D:\python\phantomjs-2.1.1-windows\bin\phantomjs.exe')
                myDriver.set_page_load_timeout(15)  # 设置网页加载超时时间为10秒
                myDriver.get(url)
                time.sleep(5)
                page_source = myDriver.page_source
                # page_source = requests.get(url, headers=headers, timeout=10).content
                # print(page_source)
                myDriver.close()
                myDriver.quit()
                retry = 0
            except:
                print("@@@@@@@@@@@@@@@@sleep@@@@@@@@@@@@@@")
                time.sleep(10)
                print("retry:"+ " "+str(retry))
                retry = retry - 1
                if retry == 0:
                    myDriver.quit()
                    sys.exit(0)
        html = etree.HTML(page_source)
        url_list = html.xpath("//div[@class='_14csrlku']/div/div/div/div/div[1]/div[2]/div/div/div/a/@href")
        next_url = html.xpath("//*[@id='site-content']/div/div/div[2]/div/div/div/div/div/div[1]/nav/span/div/ul/li[7]/a/@href")
        if len(next_url) > 0:
            url = url_base + next_url[0]
        else:
            url = ''
        for content in url_list:
            id = re.sub("\D", "", content)
            dict = {'_id': id,
                    'room_url': url_base + content,
                    'crawl_id_time': time.time()}
            print(dict)
            dict_list.append(dict)
        save_mongo(dict_list)
        time.sleep(2)

def save_mongo(dict_list):
    conn = MongoClient('127.0.0.1', 27017)
    db = conn.airbnb
    my_set = db.list_1126
    try:
        my_set.insert_many(dict_list)
        print('******************insert database success!*************************')
    except:
        for dict in dict_list:
            try:
                my_set.insert(dict)
            except:
                print('###################insert database fail!!#######################')
        print('******************insert database success!*************************')
if __name__ == '__main__':
    get_url()