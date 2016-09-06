# -*- coding: utf-8 -*-

import urllib
from urllib.request import urlopen
import html.parser as h
from bs4 import BeautifulSoup
import sys
import time
import io
import  re
import string

reg =re.compile(r'\d+')
list = ['0', '10', '20']
for s in list:
    url = ('https://site.douban.com/maosh/widget/events/1441569/?start='+s)
    urlrequest = urlopen(url)
    parser = BeautifulSoup(urlrequest, "html.parser")
    elist = parser.find('div', 'events-list-s').findAll('li', 'item')
    for event in elist:
        urlevent = event.findNext('a')['href']
        detailrequest = urlopen(urlevent)
        Detailparser = BeautifulSoup(detailrequest, 'html.parser')
        DetailInfolist = Detailparser.find('div', 'event-info')
        x = DetailInfolist.contents[1]
        x1 = DetailInfolist.findAll('div', 'event-detail')
        s1 = DetailInfolist.findNext('h1').text.strip()
        s2 = "已结束"
        s3 = s1.find(s2)
        print(urlevent)
        print(s1)
        print(DetailInfolist.findNext('li','calendar-str-item ').text)
        print(x1[2].text.replace('\t','').replace('\n','').replace(' ','').replace('\xa0','').split('\n'))
        print('\n')
        if s3 >0:
            print(urlevent+s1)
            print('game is over !')
            break;

print('see u !')
