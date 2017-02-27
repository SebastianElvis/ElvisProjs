# -*- coding: utf-8 -*-
from module_data_access.base_dao import *
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf8')

data_sources = dao.get_all_data_sources()

news_dir = '../dataset/news/'


def generate_daily_news(type):
    write_file = open(news_dir + type + '.csv', 'w+')
    records = dao.get_records(type=type, num=-1, sort=1)
    print records['count']
    kv = [None, None] # date, content
    for record in records['records_list']:
        # record['time'] = datetime.datetime.strptime(record['time'], u'%Y-%m-%d')
        date = record['time']
        record['content'] = record['content'].replace('\r', '')\
            .replace('\n', '')\
            .replace(' ', '')
        if kv[0] is None:
            kv[0] = date
            kv[1] = record['content'] + ','
        elif kv[0] == date:
            kv[1] += record['content'] + ','
        else:
            line = kv[0] + ',' + kv[1] + '\n'
            print line
            write_file.write(line)
            kv[0] = date
            kv[1] = record['content'] + ','
    write_file.close()


def date_string_comparator(a, b):
    a_date = datetime.datetime.strptime(a, u'%Y-%m-%d')
    b_date = datetime.datetime.strptime(b, u'%Y-%m-%d')
    # print a_date, b_date
    if a_date == b_date:
        return 0
    elif a_date > b_date:
        return 1
    else:
        return -1

if __name__ == '__main__':
    print 'start'
    generate_daily_news('financial_news')
    print 'finished'
