import logging
import threading
import urllib
import urllib2

import pymongo

import weibo_utils
from base_dao import BaseDAO

logging.basicConfig(format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s",
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='weibo_crawler.log',
                    filemode='w')


class WeiboCrawler(threading.Thread):
    def __init__(self, target_data_source, mongo_dao, page_num=1):
        threading.Thread.__init__(self)
        self.target_data_source = target_data_source  # dict
        self.mongo_dao = mongo_dao  # MongoDAO

        # find the last page
        current_object_id = str(target_data_source['_id'])
        ds_tmp_query = mongo_dao.get_col('record').find({'poster_id': current_object_id}).sort('time',
                                                                                               pymongo.ASCENDING)
        if ds_tmp_query.count() == 0:  # no records
            self.page_num = page_num
        else:  # has records
            res = ds_tmp_query.next()
            if res.has_key('page_num'):
                self.page_num = res['page_num']
            else:
                self.page_num = page_num

    def run(self):
        self.crawl(page_num=self.page_num)

    def crawl(self, url=None, page_num=1):
        print 'start crawl page ' + str(page_num)

        # url
        if url == None:
            url = self.target_data_source['url']
            print  'crawl url ' + url

            # get data
        get_data = urllib.urlencode({'page': page_num})

        # request obj
        req = urllib2.Request(url, data=get_data, headers=weibo_utils.header_dict)
        resp, html = None, None

        # try to get the html
        try:
            resp = urllib2.urlopen(req)
            html = resp.read()
        except:
            print  'Exception detected when crawling page ' + str(page_num)
            print 'the resp is ' + str(resp)
            print 'The html is ' + str(html)
            return None

        # object id obj to str
        object_id_str = str(self.target_data_source['_id'])
        # get the record list from html
        record_list = weibo_utils.get_records_from_html(html, page_num, poster_id=object_id_str)
        # insert the records into the weibo database -> record collection
        if len(record_list) == 0:
            print 'Crawl error!'
            print 'The response html is ' + str(html)
            return
        else:
            self.mongo_dao.get_col('record').insert_many(record_list)

        # crawl the next page
        self.page_num += 1
        print  'finish crawl page ' + str(page_num)
        return self.crawl(page_num=self.page_num)


if __name__ == '__main__':
    dao = BaseDAO()
    ds = dao.find_all('data_source')[0]
    t = WeiboCrawler(ds, dao)
    t.start()
    print "Thread start!"
