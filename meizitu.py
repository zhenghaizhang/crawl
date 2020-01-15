# -*- coding: utf-8
# File : meizhitu.py
# Author : baoshan
# Desc: 爬取妹纸图网站上的图片

import requests
from bs4 import BeautifulSoup
import time
import os

# headers 应该尽可能的详细，否则抓取不下来
headers = {
    "authority": "www.mzitu.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,"
              "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "cookie": "Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1579055343; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1579074763",
    "referer": "https://www.mzitu.com/mm/",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
}


def create_dir(name):
    """
    创建文件夹
    :param name: 需要创建的文件夹名称
    :return:
    """
    if not os.path.exists(name):
        os.mkdir(name)


def get_pic_list(cur_page, url):
    """
    获取每页的图片列表
    :param cur_page: 当前页码
    :param url: 列表页URL
    :return:
    """
    try:
        r = requests.get(url, headers=headers)
        html = r.text
        soup = BeautifulSoup(html, 'lxml')  # 根据lxml解析HTML文档，也可以改成html.parser
        pic_list = soup.find_all('img', class_='lazy')  # 根据img标签和class属性获取图片列表
        get_pic_info(cur_page, pic_list)
    except:
        pass


def get_pic_info(cur_page, pic_list):
    """
    获取每页的图片列表中的图片信息
    :param cur_page: 当前页码
    :param pic_list: 图片列表
    :return:
    """
    for index in pic_list:
        try:
            a_tag = index
            pic_url = a_tag.get('data-original')
            pic_text = a_tag.get('alt')
            crawl_pic_and_save(cur_page, pic_text, pic_url)
        except:
            pass


def crawl_pic_and_save(cur_page, pic_text, pic_url):
    """
    根据图片说明和图片URL获取图片并且保存
    :param cur_page: 当前页码
    :param pic_text: 图片说明
    :param pic_url: 图片地址
    :return:
    """
    try:
        r = requests.get(pic_url, headers=headers)
        suffix = pic_url.split('.')[-1]
        with open('pic/' + str(cur_page) + "/" + pic_text + suffix, 'wb') as f:
            f.write(r.content)
        print('正在下载第{}页，照片名为：{}，链接为：{}'.format(cur_page, pic_text, pic_url))
    except:
        pass
    time.sleep(2)  # 停两秒再进行，否则容易被封


def main():
    queue = [i for i in range(1, 13)]   # 要抓取的页码范围
    create_dir("pic/")
    while len(queue) > 0:
        cur_page = queue.pop(0)
        create_dir("pic/" + str(cur_page))
        url = 'https://www.mzitu.com/mm/page/{}/'.format(cur_page)
        get_pic_list(cur_page, url)


if __name__ == '__main__':
    main()
