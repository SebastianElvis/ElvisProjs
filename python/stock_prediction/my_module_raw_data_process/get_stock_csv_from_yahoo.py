from module_data_access.base_dao import *
import urllib2

yahoo_finance_url = 'https://ichart.finance.yahoo.com/table.csv?d=6&e=1&f=2017&g=d&a=7&b=19&c=2004%20&ignore=.csv&s='
stockdata_dir = '../dataset/stockdata/'


def get_stock_csv_from_yahoo(code):
    csv_url = yahoo_finance_url + code
    csv_file_dir = stockdata_dir + code + '.csv'
    csv_file = open(csv_file_dir, 'w+')
    data = urllib2.urlopen(csv_url).read()
    csv_file.write(data)
    csv_file.close()


def get_all_stock_csv_from_yahoo():
    company_list = dao.get_all_processed_companies()
    for company in company_list:
        print 'Retrieving stock data of ' + company['code'] + '...'
        get_stock_csv_from_yahoo(company['code'])
        print 'Finished!'

if __name__ == '__main__':
    get_all_stock_csv_from_yahoo()
