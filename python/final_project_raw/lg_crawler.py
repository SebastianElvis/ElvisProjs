# -*- coding:utf-8 -*- 
import requests, threading, copy, time
from md_conn import md_conn
from data_processor import data_processor
from proxy_list import proxy_list
from Queue import Queue
from random_ua import  random_ua

class lg_crawler(threading.Thread):
    post_data = {
        'first' : 'false', 
        'pn' : 1     
    }
    
    def __init__(self, proxies, job_queue, output_queue, r_ua):
        threading.Thread.__init__(self)
        self.url = 'http://www.lagou.com/jobs/positionAjax.json'
        self.job_queue = job_queue
        self.output_queue = output_queue
        self.post_data = copy.copy(self.post_data)
        self.proxies = proxies
        self.r_ua = random_ua()
        self.headers = { 
            "User-Agent" : self.r_ua.get_random_ua()
        }

    def parse_new_page(self):
        time.sleep(1)
        self.page = self.job_queue.get()
        self.post_data['pn'] = self.page
        try:
            #resp = requests.post(self.url, self.post_data, proxies=self.proxies.get_random_proxy(), timeout=3, headers=self.headers)
            resp = requests.post(self.url, self.post_data, timeout=3, headers=self.headers)
            resp_obj = resp.json()
            #print 'page : ', self.page
            #print 'proxy : ', self.proxy
            result_list = resp_obj['content']['positionResult']['result']
            self.push_list_into_output_queue(result_list)
            print 'page : ', self.page, ' crawled!'
        except Exception:
            print 'Error occured when crawling page ', self.page
        finally:
            return result_list
        #print result_list
    
    #def store_list_in_md(self, result_list):
    #    self.conn.insert_many_to('lagou', 'jobs', result_list)
    
    def push_list_into_output_queue(self, result_list):
        for result in result_list:
            self.output_queue.put(result)
        return True
    
    def run(self):
        while True:
            result_list = self.parse_new_page()
            push_result = self.push_list_into_output_queue(result_list)
            if push_result == True:
                self.job_queue.put( self.page+self.job_queue.maxsize )





if __name__ == '__main__':
    #url = 'http://www.lagou.com/jobs/positionAjax.json'
    md_conn = md_conn()
    proxies = proxy_list()
    job_queue = Queue(maxsize=10)
    output_queue = Queue(maxsize=100)
    page = 1
    r_ua = random_ua()
    
    #initialize the thread pool of jobs and data_processors
    job_thread_pool = []
    dp_thread_pool = []
    jtp_size = 10
    dtp_size = 10
    
    #initialize the job queue
    for i in range(10):
        job_queue.put(i)
    
    #put the crawler into the job queue
    while job_queue.full() == False:
        job_queue.put(page)
        page += 1
    
    #start the crawlers in the job thread pool
    for i in range(0, jtp_size):
        job_thread_pool.append( lg_crawler(proxies, job_queue, output_queue, r_ua) ) 
        job_thread_pool[i].start()
    
    #start the data processors in the dp thread pool
    for i in range(0, dtp_size):
        dp_thread_pool.append( data_processor(output_queue, md_conn) )
        dp_thread_pool[i].start()
        