from base_dao import BaseDAO
from weibo_crawler import WeiboCrawler
import urllib2
import weibo_utils

class CrawlerPool:
    def __init__(self):
        '''
        httpHandler = urllib2.HTTPHandler(debuglevel=1)
        httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        opener = urllib2.build_opener(httpHandler, httpsHandler)
        urllib2.install_opener(opener)
        '''

        dao = BaseDAO()
        ds = dao.find_all('data_source')
        ds.sort()
        self.pool = [WeiboCrawler(single_ds, dao) for single_ds in ds]
        i = 0
        for one in self.pool:
            print 'Thread ' + str(i) + ' --- ' + one.target_data_source['name']
            i += 1

    def start_crawl_all(self):
        for wc in self.pool:
            wc.start()

    def start_crawl_one(self, number):
        t = self.pool[number]
        t.start()

if __name__ == '__main__':
    cp = CrawlerPool()
    cp.start_crawl_one(0)