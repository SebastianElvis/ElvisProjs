# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 10:25:08 2016

@author: elvis
"""
import datetime, time


class EnterpriseEntity:
    def __init__(self, code, abbr, name, keyword, subreddit):
        self.code = code
        self.abbr = abbr
        self.name = name
        self.keyword = keyword
        self.subreddit = subreddit
        self.last_crawled_day = None

    def search_by_day(self, dt):
        timestamp_tuple = EnterpriseEntity.convert_date_to_ts(dt)
        t1 = timestamp_tuple[0]
        t2 = timestamp_tuple[1]
        query = '(and timestamp:' + str(t1) + '..' + str(t2) + ' title:\"' + self.keyword + '\")'
        search_list = self.subreddit.search(query,
                              sort='hot',
                              syntax='cloudsearch',
                              time_filter='all')
        l = []
        i = 0
        for item in search_list:
            if i >= 25:
                break
            l.append(item)
            i += 1
        return l

    @classmethod
    def convert_date_to_ts(cls, dt):
        t1 = str(dt)
        t2 = str(dt - datetime.timedelta(days=-1))
        timeArray1 = time.strptime(t1, "%Y-%m-%d %H:%M:%S")
        timeArray2 = time.strptime(t2, "%Y-%m-%d %H:%M:%S")
        timeStamp1 = int(time.mktime(timeArray1))
        timeStamp2 = int(time.mktime(timeArray2))
        #print (timeStamp1, timeStamp2)
        return (timeStamp1, timeStamp2)

    @classmethod
    def get_entities_from_csv(cls, subreddit):
        entities = []
        file = open('./stockdata/chosen-stocks.csv')
        csv_content = file.readlines()
        del csv_content[0]
        for line in csv_content:
            splitted_line = line.split(',')
            entities.append( EnterpriseEntity(splitted_line[0],
                                             splitted_line[1], 
                                             splitted_line[2], 
                                             splitted_line[3],
                                             subreddit) )
        return entities
