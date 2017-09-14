# -*- coding:utf-8 -*-
import ConfigParser
import urllib
import urllib2
import socket
import re
from bs4 import BeautifulSoup
import codecs
import os
import datetime


class ShowStart(object):
    city = {}
    live_house = {}
    time_range = ''
    target_city_and_live_house = {}
    crawler_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'Host': 'www.showstart.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }
    host = 'http://www.showstart.com/event/list'

    def __init__(self):
        self.init()
        self.set_time_range()
        self.get_config()

    def get_config(self):
        cf = ConfigParser.ConfigParser()
        cf.readfp(codecs.open(os.path.abspath(os.path.dirname(__file__)) + '/settings.ini', 'r', 'utf-8'))
        # cf.read(os.path.abspath(os.path.dirname(__file__)) + '/settings.ini', 'utf-8')
        city = cf.get('common', 'city')
        target_city = city.split(',')
        for city in target_city:
            try:
                self.target_city_and_live_house[city] = cf.get('live_house', city).split(',')
            except ConfigParser.Error as e:
                self.target_city_and_live_house[city] = ['全部']
        for city, live_houses in self.target_city_and_live_house.items():
            city_live_house_map = dict()
            city_live_house_map[city] = []
            for live_house in live_houses:
                live = dict()
                live_house_id = self.live_house.get(live_house, None)
                if live_house_id is None:
                    live[live_house] = None
                else:
                    # url ?showTime=0&cityId=21&siteId=4249&isList=1&timeRange=2017-08-03_2017-08-25
                    url_query = [('cityId', self.city[city]), ('siteId', live_house_id), ('timeRange', self.time_range)]
                    if live_house_id != 0:
                        url_query.append(('isList', 1))
                    live[live_house] = self.host + '?' + urllib.urlencode(url_query)
                city_live_house_map[city].append(live)
            self.crawler_list.append(city_live_house_map)

    def init(self):
        req = urllib2.Request(url=self.host + '?cityId=0&siteId=0', headers=self.headers)
        try:
            html = urllib2.urlopen(req).read()
            soup = BeautifulSoup(html, 'html.parser')
            cities = soup.find('div', {'class': 'list-city-content'}).select('a')
            for city in cities:
                href = city.get('href')
                pattern = re.compile('cityId=(\d*)')
                match = pattern.search(href)
                value = match.group(1)
                key = city.get_text()
                self.city[key] = value
            live_houses = soup.find('div', {'class': 'list-livehouse-content'}).select('a')
            for live_house in live_houses:
                key = live_house.get_text()
                href = live_house.get('href')
                pattern = re.compile('siteId=(\d*)')
                match = pattern.search(href)
                value = match.group(1)
                self.live_house[key] = value
        except urllib2.error as e:
            print(e)

    def set_time_range(self):
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(weeks=2)
        self.time_range = start_time.strftime('%Y-%m-%d') + '_' + end_time.strftime('%Y-%m-%d')

    def get_live_info(self):
        f = open(os.path.abspath(os.path.dirname(__file__)) + '/liveshow-info.html', 'w+')
        print >>f, '<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>'
        for crawler in self.crawler_list:
            for city, v in crawler.items():
                print(city)
                print >>f, ('<br />' + city).encode('utf-8')
                for live_house_info in v:
                    for live_house, url in live_house_info.items():
                        if url is None:
                            print(live_house + ' is None')
                            break
                        print(live_house)
                        print >>f, ('<br />' + live_house).encode('utf-8')
                        self.parse_html(f, url)
        f.close()

    def parse_html(self, f, url):
        try:
            req = urllib2.Request(url=url, headers=self.headers)
            html = urllib2.urlopen(req).read()
            soup = BeautifulSoup(html, 'html.parser')
            lives = soup.find('ul', {'class': 'g-list-wrap'})
            if lives:
                lives = lives.select('a')
                for live in lives:
                    url = live.get('href')
                    img = live.find('img')
                    title = live.get('title')
                    artist = live.find('p', {'class': 'performerName'}).string
                    price = live.find('p', {'class': 'g-price'}).get_text()
                    times = live.find('p', {'class': 'g-time'}).get_text()
                    place = live.find('p', {'class': 'g-place'}).get_text()
                    ostr = '''
                    <div class="item">
                    <div class="title">
                        <br /><br /><span class="title"><font color="#ff6f27" size="+1"><b>%s</b></font></span><br />
                    </div>
                    <div class="pic">
                        <img src=%s />
                    </div>
                    <div class="info">
                        <span class="info">
                        <br /><span><font size="-1">%s</font></span>
                        <br /><span><font size="-1">%s</font></span>
                        <br /><span><font size="-1">%s</font></span>
                        <br /><span><font size="-1">%s</font></span>
                        </span>
                    </div>
                    </div>
                    '''%(title, img.get('original'), times.strip(), price, artist.replace('\t', '').replace('\n', ''), url)
                    print >>f, ostr.encode('utf-8')
                    # print(url)
                    # print(img.get('original'))
                    # print(title)
                    # print(artist.replace('\t', '').replace('\n', ''))
                    # print(price)
                    # print(times.strip())
                    # print(place)
            else:
                print('No live house')
        except urllib2.error as e:
            print(e)

    def run(self):
        self.get_live_info()


if __name__ == '__main__':
    socket.timeout = 10
    show = ShowStart()
    show.run()
