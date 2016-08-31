# -*- coding: utf-8 -*-

import urllib
from urllib.request import urlopen
import html.parser as h
from bs4 import BeautifulSoup
import sys
import time
import io

# 创建以日期命名的txt文件, print 时加入file = file1可重写入该文件
crFile = time.strftime("%Y%m%d", time.localtime())
file1 = open("LiveNews" + crFile + ".txt", 'w')


def fetchMao():
    urlrequest = urlopen('https://site.douban.com/maosh/widget/events/1441569/?start=0')
    # html_src = urllib.urlopen(urlrequest).read()
    parser = BeautifulSoup(urlrequest, "html.parser")
    elist = parser.find('div', 'events-list-s').findAll('li', 'item')
    for event in elist:
        # with open(file1, 'wt') as f:
        print(event.findNext('a').text, file = file1)
        print(event.findNext('p').text, file = file1)
        print(event.findNext('a')['href'], file = file1)



    # 查找所有已结束节目，并打印出第一个已结束的节目，url翻页到了第二页，才有结束的节目
    url2 = urlopen('https://site.douban.com/maosh/widget/events/1441569/?start=10')
    parser2 = BeautifulSoup(url2, 'html.parser')
    firstendevent = parser2.find('div', 'events-list-s').findAll('li', 'item close')
    for firstend in firstendevent:
        print('this is the first closed itme', file = file1)
        print(firstend.find('a').text, file = file1)
        print(firstend.find('p').text, file = file1)
        print(firstend.find('a')['href'], file = file1)

    # 搜索所有翻页并打印出
    alist = parser.find('div', 'paginator').findAll('a')
    for ahref in alist:
        print('https://site.douban.com/'+ ahref.findNext('a')['href'], file = file1)


def main(argv):
    fetchMao()
# if len(argv) > 1:
# 	return 0
# else:
# 	return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))
