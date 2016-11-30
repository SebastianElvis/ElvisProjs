# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 09:29:50 2016

@author: elvis
"""
import Queue
import datetime
import praw
from enterprise_entity import EnterpriseEntity
from threading import Thread


class RedditCrawler(Thread):
    my_user_agent = 'android:com.example.myredditapp:v1.2.3 (by /u/kemitche)'
    my_client_id = 'BjEAsPzwChScuQ'
    my_client_secret = 'KGiTfb7KgAfat1Yp4YUjyuX_dz4'
    my_username = 'elvisage'
    my_password = 'hrc941102'
    queue = Queue.Queue(maxsize=20)
    datetime_period = (datetime.datetime(2008, 8, 8, 0, 0, 0), datetime.datetime(2016, 7, 1, 0, 0, 0))

    def __init__(self, entity):
        Thread.__init__(self)
        self.reddit = praw.Reddit(user_agent=RedditCrawler.my_user_agent,
                     client_id=RedditCrawler.my_client_id,
                     client_secret=RedditCrawler.my_client_secret)
        self.subreddit = self.reddit.subreddit('news')
        self.entity = entity

    def run(self):
        start = RedditCrawler.datetime_period[0]
        end = RedditCrawler.datetime_period[1]
        l = start
        res_dict = dict()
        while l + datetime.timedelta(days=1) < end:
            l = l + datetime.timedelta(days=1)
            res = [x.title for x in self.entity.search_by_day(l, self.subreddit)]
            res_dict[str(l)] = res
            print res

if __name__ == '__main__':
    '''
    rc = RedditCrawler(1)
    entities = EnterpriseEntity.get_entities_from_csv(rc.subreddit)
    for entity in entities:
        res = entity.search_by_day(datetime.datetime(2008, 4, 6, 0, 0, 0))
        print [s.title for s in res]
    '''
    entities = EnterpriseEntity.get_entities_from_csv()
    RedditCrawler(entities[0]).start()
