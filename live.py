# -*- coding: utf-8 -*-
import urllib2
import HTMLParser
from bs4 import BeautifulSoup
import sys
from datetime import *
import re
import smtplib
from email.MIMEText import MIMEText

def sendmail(subject, content):
	email_host = 'smtp host'
	email_user = 'sender email'
	email_pwd = 'sender pwd'
	maillist = ['example@123.com']
	me = email_user
	msg = MIMEText(content, 'html', 'utf-8')
	msg['Subject'] = subject
	msg['From'] = me
	msg['To'] = ', '.join(maillist)
	try:
		smtp = smtplib.SMTP(email_host)
		smtp.login(email_user, email_pwd)
		smtp.sendmail(me, maillist, msg.as_string())
		smtp.quit()
		print 'email send success.'
	except Exception, e:
		print e
		print 'email send failed.'

livedict = {
			'MAO' : 'maosh/1441569/1', # https://site.douban.com/maosh/widget/events/1441569/
			'YYT' : 'yuyintang_h/1217192/1',
			'QSW' : '187956/11298220/1', # https://site.douban.com/187956/widget/events/11298220/
			'OST' : '176416/10189365/1',
			'JZC' : 'jzclub/1357869/1',
			'HAL' : '273062/191469274/1', # https://site.douban.com/273062/widget/events/191469274/
			'MSL' : '290170/192970720/2', # https://site.douban.com/290170/widget/events/192970720/
			'696' : 'livebar696/1381481/1', # https://site.douban.com/livebar696/widget/events/1381481/
			'YGS' : 'yugongyishan/1431074/2', # https://site.douban.com/yugongyishan/widget/events/1431074/
			'MOG' : 'moguspace/191972683/1', # https://site.douban.com/moguspace/widget/events/191972683/
			'DDC' : '237627/16619636/2' # https://site.douban.com/237627/widget/events/16619636/
			}

def fetchliveshow(livehouse):
	baseurl = 'https://site.douban.com/' + livedict[livehouse].split('/')[0] + '/widget/events/' + livedict[livehouse].split('/')[1] + '/?start='
	liststyle = int(livedict[livehouse].split('/')[2])
	pagedepth = 10
	pagecnt = 0
	urlrequest = urllib2.Request(baseurl + str(pagecnt))
	html_src = urllib2.urlopen(urlrequest).read()
	parser = BeautifulSoup(html_src, "html.parser")
	try:
		eventcnt = re.findall(r'\d+', parser.find('span', 'count').text)
	except:
		eventcnt = ['0']
	if len(eventcnt):
		pagecnt = int(eventcnt[0]) / pagedepth + 1
	print pagecnt
	text = ''
	for i in range(0, pagecnt):
		urlrequest = urllib2.Request(baseurl + str(i * pagedepth))
		html_src = urllib2.urlopen(urlrequest).read()
		parser = BeautifulSoup(html_src, "html.parser")
		# liststyle 1: 'events-list-s', 'class':'item close' and 'class':'item '
		# liststyle 2: 'events-list', 'class':'item'
		if liststyle == 1:
			elist = parser.find('div', {'class' : 'events-list-s'}).findAll('li', {'class' : 'item '})
		elif liststyle == 2:
			elist = parser.find('div', {'class' : 'events-list'}).findAll('li', {'class' : 'item'})
		else:
			elist = []
		print len(elist), i
		for event in elist:
			if event.findNext('span').text.find(u'已结束') != -1:
				elist = []
				break
			eventurl = event.findNext('a')['href']
			urlrequest = urllib2.Request(eventurl)
			html_src = urllib2.urlopen(urlrequest).read()
			parser = BeautifulSoup(html_src, "html.parser")
			title = parser.find('h1', {'itemprop' : 'summary'}).contents[0].strip()
			try:
				datetime = parser.find('li', 'calendar-str-item').text.strip()
			except AttributeError:
				datetime = next(parser.find('ul', 'calendar-strs ').findNext('li').children).strip()
			except:
				datetime = ''
			prices = parser.findAll('span', 'tickets-info-price')
			price = prices[-1].text.strip() if len(prices) else ' '
			text += '<b>' + datetime + '&nbsp;&nbsp;&nbsp;&nbsp;' + price + '</b><br>' + '<a href="' + eventurl + '">' + title + '</a><br><br>'
		if len(elist) < pagedepth:
			break
	sendmail(livehouse + ' Liveshow - ' + str(date.today()), text)

def main(argv):
	if len(argv) > 1:
		fetchliveshow(argv[1])
		return 0
	else:
		print "Please input the livehouse: MAO, YYT, QSW, OST."
		return 1

if __name__ == '__main__':
	sys.exit(main(sys.argv))
