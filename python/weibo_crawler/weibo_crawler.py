# coding:utf-8

import threading
import urllib
import urllib2
import time
import random
from crawler_logger import logger
import pymongo

import weibo_utils
from time import sleep


class WeiboCrawler(threading.Thread):
    def __init__(self, target_data_source, mongo_dao, page_num=1):
        threading.Thread.__init__(self)
        self.target_data_source = target_data_source  # dict
        self.mongo_dao = mongo_dao  # MongoDAO
        self.sleep_interval = (0, 20)

        # counter of the failed requests
        self.failed_count = 0

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
        logger.info('Start crawl thread ' + self.target_data_source['name'] + '!')
        self.crawl()

    def crawl(self, url=None):
        page_num = self.page_num
        while self.failed_count < 5:
            logger.info('Start crawling ' + self.target_data_source['name'] + ' page ' + str(page_num))

            # url
            if url is None:
                url = self.target_data_source['url']

            # get method data and headers
            get_data = urllib.urlencode({'page': page_num, 'vt': 4})
            header_dict = weibo_utils.generate_header()

            # request obj
            req = urllib2.Request(url, data=get_data, headers=header_dict)
            resp, html = None, None
            # try to get the html
            try:
                resp = urllib2.urlopen(req, timeout=5)
                html = resp.read()
            except:
                logger.error('Exception detected when crawling page ' + str(page_num))
                logger.error('The request header is ' + str(req.headers))
                if resp is not None:
                    logger.error('The response code is ' + str(resp.getcode()))
                    logger.error('The response header is ' + str(resp.headers.dict))
                else:
                    logger.error('Response refused --- null !')

                self.failed_count += 1
                sleep(5)
                continue

            # object id obj to str
            object_id_str = str(self.target_data_source['_id'])
            # get the record list from html
            record_list = weibo_utils.get_records_from_html(html, page_num, poster_id=object_id_str)

            # insert the records into the weibo database -> record collection
            if record_list is None or len(record_list) == 0:
                logger.error('Crawl error!')
                logger.error('The request header is ' + str(req.headers))
                logger.error('Login required!')
                self.failed_count += 1
                continue
            else:
                self.mongo_dao.get_col('record').insert_many(record_list)
                logger.info('The records are inserted!')

            # clear the failed count
            self.failed_count = 0

            # crawl the next page
            page_num += 1
            logger.info('Finish')
            # sleep for some seconds to fight against the Anti-Spider System
            time.sleep(random.uniform(self.sleep_interval[0],
                                      self.sleep_interval[1]))

        if self.failed_count >= 5:
            logger.fatal('Failed too many times, crawler of %s exiting...' % self.target_data_source['name'])
