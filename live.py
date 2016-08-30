# -*- coding: utf-8 -*-

import urllib2
import HTMLParser
from bs4 import BeautifulSoup
import sys

def fetchMao():
	urlrequest = urllib2.Request('https://site.douban.com/maosh/widget/events/1441569/?start=0')
	html_src = urllib2.urlopen(urlrequest).read()
	parser = BeautifulSoup(html_src, "html.parser")
	elist = parser.find('div', 'events-list-s').findAll('li', 'item')
	for event in elist:
		print event.findNext('a').text
		print event.findNext('a')['href']

def main(argv):
	fetchMao()
	# if len(argv) > 1:
	# 	return 0
	# else:
	# 	return 1

if __name__ == '__main__':
	sys.exit(main(sys.argv))