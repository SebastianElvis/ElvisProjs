# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 16:12:16 2016

@author: cmri
"""

import threading, hashlib
from json import JSONEncoder

class data_processor(threading.Thread):
    
    def __init__(self, output_queue, md_conn):
        threading.Thread.__init__(self)
        self.md_conn = md_conn
        self.output_queue = output_queue
        
    def add_hash_to_result(self, single_result):
        single_result_json = JSONEncoder().encode(single_result)
        md5 = hashlib.md5(single_result_json).hexdigest()
        single_result['md5'] = md5
        return single_result
        
    def if_dup_md5(self, hashed_single_result):
        md5 = hashed_single_result['md5']
        self.md_conn.select_db('lagou')
        self.md_conn.select_collection('jobs')
        if self.md_conn.col.find({"md5":md5}) != None:
            return True
        else:
            return False
        
    def insert_one_into_db(self, single_result):
        self.md_conn.insert_one_to('lagou', 'jobs', single_result)
        
    def run(self):
        while True:
            single_result = self.output_queue.get()
            hashed_single_result = self.add_hash_to_result(single_result)
            if self.if_dup_md5(hashed_single_result) == False:        
                self.insert_one_into_db(hashed_single_result)
        