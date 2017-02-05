# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 21:02:34 2016

@author: elvis
"""
import random
class proxy_list:
    list = []
    def __init__(self):
        f = open('proxy.txt','r')
        lines = f.readlines()
        for line in lines:
            self.list.append({line.split('://')[0] : line[0:(len(line)-1)]})
            
    def get_random_proxy(self):
        return self.list[random.randint(0, len(self.list) )]
            
#print proxy_list().list