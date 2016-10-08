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
	msg['To'] = ','.join(maillist)
	try:
		smtp = smtplib.SMTP(email_host)
		smtp.login(email_user, email_pwd)
		smtp.sendmail(me, maillist, msg.as_string())
		smtp.quit()
		print 'email send success.'
	except Exception, e:
		print e
		print 'email send failed.'

def fetchMao():
	baseurl = 'https://site.douban.com/maosh/widget/events/1441569/?start='
	pagedepth = 10
	pagecnt = 0
	urlrequest = urllib2.Request(baseurl + str(pagecnt))
	html_src = urllib2.urlopen(urlrequest).read()
	parser = BeautifulSoup(html_src, "html.parser")
	eventcnt = re.findall(r'\d+', parser.find('span', 'count').text)
	if len(eventcnt):
		pagecnt = int(eventcnt[0]) / pagedepth + 1
	print pagecnt
	text = ''
	for i in range(0, pagecnt):
		urlrequest = urllib2.Request(baseurl + str(i * pagedepth))
		html_src = urllib2.urlopen(urlrequest).read()
		parser = BeautifulSoup(html_src, "html.parser")
		elist = parser.find('div', 'events-list-s').findAll('li', 'item ')
		print len(elist), i
		if len(elist) < pagedepth:
			break
		for event in elist:
			eventurl = event.findNext('a')['href']
			urlrequest = urllib2.Request(eventurl)
			html_src = urllib2.urlopen(urlrequest).read()
			parser = BeautifulSoup(html_src, "html.parser")
			title = parser.find('h1', {'itemprop' : "summary"}).contents[0].strip()
			datetime = parser.find('li', 'calendar-str-item').text.strip()
			prices = parser.findAll('span', 'tickets-info-price')
			price = prices[-1].text.strip() if len(prices) else ' '
			text += '<b>' + datetime + '&nbsp;&nbsp;&nbsp;&nbsp;' + price + '</b><br>' + '<a href="' + eventurl + '">' + title + '</a><br><br>'
	sendmail('Mao Liveshow - ' + str(date.today()), text)

def main(argv):
	fetchMao()

if __name__ == '__main__':
	sys.exit(main(sys.argv))