# -*- coding: utf-8 -*-
'''
0831开始加入备注：
实现dict存储url、时间；
实现sorted 倒序排列，并指定key键；
'''


import urllib
from urllib.request import urlopen
import html.parser as h
from bs4 import BeautifulSoup
import sys
import time
import io


# 创建以日期命名的txt文件, print 时加入file = file1可重写入该文件
# crFile = time.strftime("%Y%m%d", time.localtime())
# file1 = open("LiveNews" + crFile + ".txt", 'a')


def fetchMao():
    urlrequest = urlopen('https://site.douban.com/maosh/widget/events/1441569/?start=0')
    # html_src = urllib.urlopen(urlrequest).read()
    parser = BeautifulSoup(urlrequest, "html.parser")
    elist = parser.find('div', 'events-list-s').findAll('li', 'item')
    for event in elist:
        with open("livebeta.txt", 'a') as f:    # 使用with，可以自动关闭文件，参数a（add），表示追加内容
            print(event.findNext('a').text, file = f)
            print(event.findNext('p').text, file = f)
            urlevent = event.findNext('a')['href']
            print(urlevent, file = f)
            with open("timedesc.txt", 'a') as t:
                print (event.findNext('a')['href'][29:], file = t)
                urltime = event.findNext('span','time').text[:2]+event.findNext('span','time').text[3:5]
                print(urltime, file = t)
                dict = (urlevent,urltime)     # 实现字典
                with open("newresult.txt", 'a') as sexy:
                    print(sorted(dict,key=lambda d: d[1]), file = sexy)  #sorted倒序排列输出

    # for dati in elist:
    #     with open("timedesc.txt", 'a') as t:
    #         print (event.findNext('span', 'time').text, file = t)



    # 查找所有已结束节目，并打印出第一个已结束的节目，url翻页到了第二页，才有结束的节目
    url2 = urlopen('https://site.douban.com/maosh/widget/events/1441569/?start=10')
    parser2 = BeautifulSoup(url2, 'html.parser')
    firstendevent = parser2.find('div', 'events-list-s').findAll('li', 'item close')
    for firstend in firstendevent:
        with open("livebeta.txt", 'a') as f:
            print('this is the first closed itme', file = f)
            print(firstend.find('a').text, file = f)
            print(firstend.find('p').text, file = f)
            print(firstend.find('a')['href'], file = f)

    # 搜索所有翻页并打印出
    alist = parser.find('div', 'paginator').findAll('a')
    for ahref in alist:
         with open("livebeta.txt", 'a') as f:
            print('https://site.douban.com/'+ ahref.findNext('a')['href'], file = f)


def main(argv):
    fetchMao()
# if len(argv) > 1:
# 	return 0
# else:
# 	return 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))
