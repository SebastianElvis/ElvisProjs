from module_data_access.base_dao import *
import json
import os

dir = '../dataset/stockdata/'

def stock_json_to_mongodb(filename):
    stockdata_col = dao.get_col('stockdata')
    data = json.loads(''.join(open(dir + filename).readlines()))
    for line in data:
        stockdata_col.insert({
            'code': filename.split('.')[0],
            'date': line[0],
            'open': line[1],
            'close': line[2],
            'lowest': line[3],
            'highest': line[4],
            'volume': line[5],
        })

if __name__ == '__main__':
    dir_filelist = os.listdir(dir)
    for line in dir_filelist:
        if line.endswith('json') is False:
            dir_filelist.remove(line)
    print dir_filelist
    for line in dir_filelist:
        print 'Start to store ' + line
        stock_json_to_mongodb(line)
        print 'Finished\n----------------------------------------'