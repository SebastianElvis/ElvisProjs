from module_data_access.base_dao import *
import json
import os
import datetime

stock_data_dir = '../dataset/stockdata/'
trends_dir = '../dataset/trends/'


# read the stock data json file and convert it to trend csv file
def stock_json_to_trend(filename):
    data = json.loads(''.join(open(stock_data_dir + filename).readlines()))
    trends_file = open(trends_dir + filename.split('.')[0] + '.csv', 'w+')
    for line in data:
        date = line[0]
        trend = 0 if (line[1]-line[2]) > 0 else 1  # open-close
        trends_file.write(date + ',' + str(trend) + '\n')
    trends_file.close()


# read the trend csv file and convert it to the dictonary
def trend_csv_to_dict(code):
    trend_dict = {}
    trends_file = open(trends_dir + code.split('.')[0] + '.csv', 'r')
    for line in trends_file.readlines():
        splitted_line = line.split(',')
        trend_dict[splitted_line[0]] = int(splitted_line[1][:-1])
    trends_file.close()
    return trend_dict


# assemble all stock trends
def assemble_all_trends():
    assembled_trend_file = open(trends_dir + 'assembled_trend.csv', 'w+')

    # get all trend filename
    trends_filelist = os.listdir(trends_dir)
    for f in trends_filelist:
        if f.endswith('csv') is False or f == 'assembled_trend.csv':
            trends_filelist.remove(f)

    # write the first line
    first_line = 'Date,' + ','.join([filename.split('.')[0] for filename in trends_filelist]) + '\n'
    assembled_trend_file.write(first_line)

    # convert them to dict
    trends_dict_list = []
    for fname in trends_filelist:
        trends_dict_list.append(trend_csv_to_dict(fname))

    # date range
    date_start = datetime.datetime.strptime("2004-01-01", '%Y-%m-%d')
    date_end = datetime.datetime.strptime("2017-03-01", '%Y-%m-%d')
    date_range = (date_end - date_start).days
    for day in range(date_range+1):
        pin_date = date_start + datetime.timedelta(days=day)
        pin_date = pin_date.date()
        line = str(pin_date)
        for trends_dict in trends_dict_list:
            trend = trends_dict[str(pin_date)] if str(pin_date) in trends_dict.keys() else ''
            line = line + ',' + str(trend)
            print line
        line += '\n'
        assembled_trend_file.write(line)

    assembled_trend_file.close()


# read all json files in the directory and convert them to the trend csv file
def all_stock_json_to_trend():
    stock_dir_filelist = os.listdir(stock_data_dir)
    for line in stock_dir_filelist:
        if line.endswith('json') is False:
            stock_dir_filelist.remove(line)
    print stock_dir_filelist
    for filename in stock_dir_filelist:
        stock_json_to_trend(filename)


if __name__ == '__main__':
    '''
    stock_dir_filelist = os.listdir(stock_data_dir)
    for line in stock_dir_filelist:
        if line.endswith('json') is False:
            stock_dir_filelist.remove(line)
    print stock_dir_filelist
    for filename in stock_dir_filelist:
        stock_json_to_trend(filename)
    '''
    assemble_all_trends()
