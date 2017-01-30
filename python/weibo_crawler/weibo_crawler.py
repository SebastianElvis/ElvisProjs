import threading
import urllib
import urllib2
import time
import random

import pymongo

import weibo_utils
from base_dao import BaseDAO


class WeiboCrawler(threading.Thread):
    def __init__(self, target_data_source, mongo_dao, page_num=1):
        threading.Thread.__init__(self)
        self.target_data_source = target_data_source  # dict
        self.mongo_dao = mongo_dao  # MongoDAO
        self.sleep_interval = (3, 7)

        # find the last page of the data source
        current_object_id = str(target_data_source['_id'])
        ds_tmp_query = mongo_dao.get_col('record')\
                                .find({'poster_id': current_object_id})\
                                .sort('page_num', pymongo.DESCENDING)

        #print 'ds_tmp_query ---------------', ds_tmp_query.count()
        if ds_tmp_query.count() == 0:  # no records
            self.page_num = page_num
        else:  # has records
            res = ds_tmp_query.next()
            if res.has_key('page_num'):
                self.page_num = res['page_num']
            else:
                self.page_num = page_num

    def run(self):
        print 'Start crawl thread ' + self.target_data_source['name'] + '!'
        self.crawl(self.crawl, page_num=self.page_num)

    def crawl(self, callback, url=None, page_num=1, ):
        print 'Start crawling ' + self.target_data_source['name'] + ' page ' + str(page_num)

        # url
        if url is None:
            url = self.target_data_source['url']

        # get method data and headers
        get_data = urllib.urlencode({'page': page_num, 'vt': 4})
        header_dict = weibo_utils.generate_header()

        # request obj
        req = urllib2.Request(url, data=get_data, headers=header_dict )
        resp, html = None, None
        # try to get the html
        try:
            resp = urllib2.urlopen(req, timeout=5)
            html = resp.read()
        except:
            print  'Exception detected when crawling page ' + str(page_num)
            print 'The request header is ' + str(req.headers)
            if resp is not None:
                print 'The response code is ' + str( resp.getcode() )
                print 'The response header is ' + str(resp.headers.dict)
            else:
                print 'Response refused --- null !'
                callback(self.crawl, page_num=self.page_num)
            return None

        # object id obj to str
        object_id_str = str(self.target_data_source['_id'])
        # get the record list from html
        record_list = weibo_utils.get_records_from_html(html, page_num, poster_id=object_id_str)

        # insert the records into the weibo database -> record collection
        if record_list is None or len(record_list) == 0:
            print 'Crawl error!'
            print 'The request header is ' + str(req.headers)
            print 'Login required!'
            callback(self.crawl, page_num=self.page_num)
        else:
            self.mongo_dao.get_col('record').insert_many(record_list)

        # crawl the next page
        self.page_num += 1
        print  'Finish'
        print weibo_utils.line

        # sleep for some seconds to fight against the Anti-Spider System
        time.sleep(random.uniform(self.sleep_interval[0],
                                  self.sleep_interval[1]) )
        try:
            callback(self.crawl, page_num=self.page_num)
        except:
            return self.page_num


if __name__ == '__main__':
    dao = BaseDAO()
    ds = dao.find_all('data_source')[0]
    t = WeiboCrawler(ds, dao)
    t.start()
    while t.is_alive is not True:
        t = WeiboCrawler(ds, dao)
        t.start()

    print "Thread start!"
