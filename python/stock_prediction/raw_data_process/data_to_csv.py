import csv
import pymongo

class DataToCsv:
    def __init__(self, dao):
        self.dao = dao

    def record_to_csv(self, file_dir):
        news_list = self.dao.get_col('record').find_all().sort({'time', pymongo.ASCENDING})
        csv_writer = csv.writer( open(file_dir, 'w') )
        date_pin = None
        joined_daily_news = ''
        for news in news_list:
            cur_date = news['time']
            if date_pin is None:
                date_pin = cur_date
                joined_daily_news = ' '.join((item['content'] for item in news_list if item['']))

