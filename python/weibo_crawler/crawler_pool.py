from base_dao import *
from weibo_crawler import WeiboCrawler


class CrawlerPool:
    def __init__(self):
        '''
        httpHandler = urllib2.HTTPHandler(debuglevel=1)
        httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
        opener = urllib2.build_opener(httpHandler, httpsHandler)
        urllib2.install_opener(opener)
        '''

        ds = dao.find_all('data_source')
        ds.sort()
        self.pool = [WeiboCrawler(single_ds, dao) for single_ds in ds]
        i = 0
        for one in self.pool:
            print 'Thread ' + str(i) + ' --- ' + one.target_data_source['name']
            i += 1

    def start_crawl_all(self):
        for wc in self.pool:
            wc.sleep_interval = [j*len(self.pool) for j in wc.sleep_interval]
            wc.start()

    def start_crawl_one(self, number):
        t = self.pool[number]
        t.start()

if __name__ == '__main__':
    cp = CrawlerPool()
    cp.start_crawl_all()
