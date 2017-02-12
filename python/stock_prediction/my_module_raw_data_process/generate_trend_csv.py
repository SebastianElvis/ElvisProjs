from module_data_access.base_dao import *
import json
import os

stock_data_dir = '../dataset/stockdata/'
trends_dir = '../dataset/trends/'


def stock_json_to_trend(filename):
    data = json.loads(''.join(open(stock_data_dir + filename).readlines()))
    trends_file = open(trends_dir + filename.split('.')[0] + '.csv', 'w+')
    for line in data:
        date = line[0]
        trend = 0 if (line[1]-line[2]) > 0 else 1  # open-close
        trends_file.write(date + ',' + str(trend) + '\n')
    trends_file.close()


def trend_csv_to_dict(filename):
    trend_dict = {}
    trends_file = open(trends_dir + filename.split('.')[0] + '.csv', 'r')
    for line in trends_file.readlines():
        splitted_line = line.split(',')
        trend_dict[splitted_line[0]] = int(splitted_line[1][:-1])
    trends_file.close()
    return trend_dict


def all_stock_json_to_trend():
    stock_dir_filelist = os.listdir(stock_data_dir)
    for line in stock_dir_filelist:
        if line.endswith('json') is False:
            stock_dir_filelist.remove(line)
    print stock_dir_filelist
    for filename in stock_dir_filelist:
        stock_json_to_trend(filename)


if __name__ == '__main__':
    stock_dir_filelist = os.listdir(stock_data_dir)
    for line in stock_dir_filelist:
        if line.endswith('json') is False:
            stock_dir_filelist.remove(line)
    print stock_dir_filelist
    for filename in stock_dir_filelist:
        stock_json_to_trend(filename)
