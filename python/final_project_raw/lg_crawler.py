# -*- coding:utf-8 -*- 
import requests, threading, copy, time
from md_conn import md_conn
from proxy_list import proxy_list
from Queue import Queue
from random_ua import  random_ua

class lg_crawler(threading.Thread):
    url = ''
    post_data = {
        'first' : 'false', 
        'pn' : 1     
    }
    conn = None
    proxies = None
    queue = None
    headers = None
    r_ua = None
    
    def __init__(self, parsed_url, connection, proxies, queue, page, r_ua):
        threading.Thread.__init__(self)
        self.url = parsed_url
        self.post_data = copy.copy(self.post_data)
        self.page = page
        self.post_data['pn'] = self.page
        self.conn = connection
        self.proxies = proxies
        self.queue = queue
        self.r_ua = random_ua()
        self.headers = { 
            "User-Agent" : self.r_ua.get_random_ua()
        }
        
    
    def parse_page(self):
        try:
            #resp = requests.post(self.url, self.post_data, proxies=self.proxies.get_random_proxy(), timeout=3, headers=self.headers)
            resp = requests.post(self.url, self.post_data, timeout=3, headers=self.headers)
            resp_obj = resp.json()
            #print 'page : ', self.page
            #print 'proxy : ', self.proxy
            result_list = resp_obj['content']['positionResult']['result']
            self.store_list_in_md(result_list)
            print 'page : ', self.page, ' crawled!'
        except Exception:
            print 'Error occured when crawling page ', self.page
        #print result_list
    
    def store_list_in_md(self, result_list):
        self.conn.insert_many_to('lagou', 'jobs', result_list)
    
    def run(self):
        self.parse_page()
        new_crawler = lg_crawler(self.url, self.conn, self.proxies, self.queue, 
                                 self.page+self.queue.maxsize, self.r_ua)
        if self.queue.full() != True:
            self.queue.put(new_crawler)

if __name__ == '__main__':
    url = 'http://www.lagou.com/jobs/positionAjax.json'
    conn = md_conn()
    proxies = proxy_list()
    job_queue = Queue(maxsize=10)
    page = 1
    r_ua = random_ua()
    
    while job_queue.full() == False:
        job_queue.put( lg_crawler(url, conn, proxies, job_queue, page, r_ua) )
        page += 1
    
    while True:
        job_queue.get().start()
        time.sleep(1)
        
        