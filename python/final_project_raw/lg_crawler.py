# -*- coding:utf-8 -*- 
import requests, threading, copy, time, random
from md_conn import md_conn
from proxy_list import proxy_list

class lg_crawler(threading.Thread):
    url = ''
    post_data = {
        'first' : 'false', 
        'pn' : 1     
    }
    conn = None
    proxy = {}
    
    def __init__(self, parsed_url, connection, page, proxy):
        threading.Thread.__init__(self)
        self.url = parsed_url
        self.post_data = copy.copy(self.post_data)
        self.post_data['pn'] = page
        self.conn = connection
        self.proxy = proxy
    
    def parse_page(self):
        page = self.post_data['pn']
        #data = urllib.urlencode(self.post_data)
        #req = urllib2.Request(self.url, data)
        #resp = urllib2.urlopen(req)
        #resp_obj = json.loads(resp.read())
        
        try:
            resp = requests.post(self.url, self.post_data, proxies=self.proxy)
            resp_obj = resp.json()
            print 'page : ', page
            print 'proxy : ', self.proxy
            result_list = resp_obj['content']['positionResult']['result']
        except Exception:
            print resp.read()
        #print result_list
        self.store_list_in_md(result_list)
    
    def store_list_in_md(self, result_list):
        self.conn.select_db('lagou')
        self.conn.select_collection('jobs')
        self.conn.col.insert_many(result_list)
    
    def run(self):
        self.parse_page()

if __name__ == '__main__':
    url = 'http://www.lagou.com/jobs/positionAjax.json'
    thread_pool = []
    thread_num = 10
    proxy_list = proxy_list().list
    conn = md_conn('localhost', 27017)
    i = 1
    for i in range(1, thread_num+1):
        print 'i : ', i
        thread_pool.append( lg_crawler(url, conn, i, proxy_list[random.randint(0,len(proxy_list))]) )
    
    for j in range(100):
        for th in thread_pool:
            if th.is_alive() == False:
                i += 1
                th = lg_crawler(url, conn, i, proxy_list[random.randint(0,len(proxy_list))])
            th.start()
        time.sleep(1)