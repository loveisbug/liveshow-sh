# -*- coding: utf-8 -*-

import urllib
from urllib.request import urlopen
import html.parser as h
from bs4 import BeautifulSoup
import sys
import time
import io

list = ['0', '10', '20']
for s in list:
    url = ('https://site.douban.com/maosh/widget/events/1441569/?start='+s)
    urlrequest = urlopen(url)
    parser = BeautifulSoup(urlrequest, "html.parser")
    elist = parser.find('div', 'events-list-s').findAll('li', 'item')
    for event in elist:
        urlevent = event.findNext('a')['href']
        with open('aaa.txt', 'a', encoding='utf-8') as detail:
            print(urlevent, file=detail)
            detailrequest = urlopen(urlevent)
            Detailparser = BeautifulSoup(detailrequest, 'html.parser')
            DetailInfolist = Detailparser.find('div', 'event-info')
            print (DetailInfolist.findNext('h1'). text.strip(),file=detail)
            print (DetailInfolist.findNext('li','calendar-str-item ').text,file=detail)

            # 本句打印价格，语法错误，会导致其他程序正常运行；
            print (DetailInfolist.findNext('span', 'tickets-info-price').text.split(' ')[1]+'\n',file=detail)