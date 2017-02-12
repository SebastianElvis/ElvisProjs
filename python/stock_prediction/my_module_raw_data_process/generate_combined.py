from generate_trend_csv import *
from daily_news_mongo_to_csv import *
from module_data_access.base_dao import *
import utils

combined_dir = '../dataset/combined/'


def generate_combined_csv(filename):
    print 'Generating combined data of ' + filename.split('.')[0]
    trend_dict = trend_csv_to_dict(filename)
    news_file = open(news_dir + 'financial_news.csv', 'r')
    combined_file = open(combined_dir + 'Combined_News_' + filename.split('.')[0] + '.csv', 'w+')
    for news_line in news_file.readlines():
        splitted_news_lines = news_line.split(',')
        if splitted_news_lines[0] is not None \
                and splitted_news_lines[0] != '' \
                and splitted_news_lines[0] in trend_dict.keys():
            print 'Date %s found in trend_dict !' % splitted_news_lines[0]
            combined_line = splitted_news_lines[0] + ',' \
                            + str(trend_dict[splitted_news_lines[0]]) + ','\
                            + ','.join(splitted_news_lines[1:-1]) + '\n'
            combined_file.write(combined_line)
        else:
            continue
    news_file.close()
    combined_file.close()
    print 'Finished!'
    print utils.line

if __name__ == '__main__':
    company_list = dao.get_all_processed_companies()
    for company in company_list:
        generate_combined_csv(company['code'])
