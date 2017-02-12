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
    write_dict = dict()
    records = dao.get_records(type=type, num=-1, sort=1)
    print records['count']
    for record in records['records_list']:
        # record['time'] = datetime.datetime.strptime(record['time'], u'%Y-%m-%d')
        date = record['time']
        record['content'] = record['content'].replace('\r', '')\
            .replace('\n', '')\
            .replace(' ', '')
        if date in write_dict.keys():
            write_dict[date] += record['content'] + ','
        else:
            write_dict[date] = record['content'] + ','
    write_dict_keys = write_dict.keys()
    print 'Before sort ---', write_dict_keys
    write_dict_keys.sort(cmp=date_string_comparator, key=lambda a: a)
    print 'After sort ---', write_dict_keys
    for key in write_dict_keys:
        line = key + ',' + write_dict[key] + '\n'
        #print line
        write_file.write(line)
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
    generate_daily_news('financial_news')
    print 'start'
    print '\n'.join([str('\n' in line) for line in open(news_dir + 'financial_news.csv').readlines()])
