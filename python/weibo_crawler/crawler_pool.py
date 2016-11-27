from base_dao import BaseDAO
from weibo_crawler import WeiboCrawler

class CrawlerPool:
    def __init__(self):
        dao = BaseDAO()
        ds = dao.find_all('data_source')
        self.pool = [WeiboCrawler(single_ds, dao) for single_ds in ds]

    def start_crawl(self):
        for wc in self.pool:
            wc.start()


if __name__ == '__main__':
    CrawlerPool().start_crawl()
