# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 16:02:23 2016

@author: elvis
"""

import urllib2
from bs4 import BeautifulSoup
 
# get the proxy
of = open('proxy.txt', 'w')
of.truncate()
for page in range(1,50):
    url = 'http://www.xicidaili.com/nn/%s' %page
    user_agent = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
    request = urllib2.Request(url)
    request.add_header("User-Agent", user_agent)
    content = urllib2.urlopen(request)
    soup = BeautifulSoup(content, "lxml")
    table = soup.find('table', {"id":"ip_list"})
    trs = table.findAll('tr')
    for tr in trs[1:]:
        tds = tr.findAll('td')
        ip = tds[1].text.strip()
        port = tds[2].text.strip()
        protocol = tds[5].text.strip()
        if protocol == 'HTTP' or protocol == 'HTTPS':
            of.write('%s://%s:%s\n' % (protocol.lower(), ip, port))
            print '%s://%s:%s' % (protocol.lower(), ip, port)
of.close()