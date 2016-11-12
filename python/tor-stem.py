# -*- coding: utf-8 -*-
"""
Created on Sun Aug  7 11:32:55 2016

@author: elvis
"""

import time
import socket
import socks
import requests
from stem import Signal
from stem.control import Controller
controller = Controller.from_port(port=9051)
def connectTor():
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5 , "127.0.0.1", 9050, True)
    socket.socket = socks.socksocket
def renew_tor():
    controller.authenticate(password='1122')
    controller.signal(Signal.NEWNYM)
def showmyip():
    r = requests.get('hhttp://ifconfig.me/ip')
    ip_address = r.text.strip()
    print(ip_address)
    
renew_tor() 
connectTor()
#controller.authenticate(password='1122')
'''   
for i in range(10):
    renew_tor()
    connectTor()
    showmyip()
    time.sleep(10)
'''