from generate_trend_csv import *
from daily_news_mongo_to_csv import *
from module_data_access.base_dao import *
import utils
import sys

reload(sys)
sys.setdefaultencoding('utf8')

combined_dir = '../dataset/combined/'

def list_to_dict(l):
    d = dict()
    for line in l:
        d[line[0:10]] = line[11:-1]
    return d


def generate_assembled_combined():
    print 'Generating the assembled combined file'
    assembled_combined_file = open(combined_dir + 'assembled_combined.csv', 'w+')
    assembled_trend_file = open(trends_dir + 'assembled_trend.csv', 'r')
    financial_news_file = open(news_dir + 'financial_news.csv', 'r')
    tech_news_file = open(news_dir + 'tech_news.csv', 'r')

    print 'Reading the file...'
    assembled_trend_list = assembled_trend_file.readlines()
    financial_news_list = financial_news_file.readlines()
    tech_news_list = tech_news_file.readlines()

    max_news = 50

    print 'Converting lists to dictioinaries...'
    assembled_trend_dict = list_to_dict(assembled_trend_list)
    financial_news_dict = list_to_dict(financial_news_list)
    tech_news_dict = list_to_dict(tech_news_list)
    # date range
    date_start = datetime.datetime.strptime("2004-01-01", '%Y-%m-%d')
    date_end = datetime.datetime.strptime("2017-03-01", '%Y-%m-%d')
    date_range = (date_end - date_start).days

    line = assembled_trend_list[0].strip('\n') + ',News' + ','*max_news + '\n'
    assembled_combined_file.write(line)

    for day in range(date_range+1):
        pin_date = date_start + datetime.timedelta(days=day)
        pin_date = pin_date.date()
        pin_date = str(pin_date)
        line = ''
        line += pin_date + ',' + assembled_trend_dict[pin_date].strip('\n') + ','

        # get the news list
        news_list = []
        today_financial_news_list = []
        today_tech_news_list = []
        if pin_date in financial_news_dict.keys():
            today_financial_news_list = financial_news_dict[pin_date].strip('\n').strip(',').split(',')
        if pin_date in tech_news_dict.keys():
            today_tech_news_list = tech_news_dict[pin_date].strip('\n').strip(',').split(',')

        news_list += today_financial_news_list
        news_list += today_tech_news_list

        # cut it to the max_news long
        if len(news_list) < max_news:
            for i in range(max_news-len(news_list)):
                news_list.append('')
        else:
            news_list = news_list[0:max_news]

        # delete , in the weibo
        for news in news_list:
            news.replace(',', '-')

        line += ','.join(news_list)
        line += '\n'
        print len(line.split(','))
        assembled_combined_file.write(line)
        # print line

    assembled_combined_file.close()
    assembled_trend_file.close()
    financial_news_file.close()
    tech_news_file.close()


# generate the combined news of a specific company
def generate_combined_csv(code):
    print 'Generating combined data of ' + code
    trend_dict = trend_csv_to_dict(code)
    news_file = open(news_dir + 'financial_news.csv', 'r')
    combined_file = open(combined_dir + 'Combined_News_' + code + '.csv', 'w+')
    combined_file.write("Date,Label,News\n")
    for news_line in news_file.readlines():
        splitted_news_lines = news_line.split(',')
        if splitted_news_lines[0] is not None \
                and splitted_news_lines[0] != '' \
                and splitted_news_lines[0] in trend_dict.keys():
            print 'Date %s found in trend_dict !' % splitted_news_lines[0]
            combined_line = splitted_news_lines[0] + ',' \
                            + str(trend_dict[splitted_news_lines[0]]) + ','\
                            + ' '.join(splitted_news_lines[1:-1]) + '\n'
            combined_file.write(combined_line)
        else:
            continue
    news_file.close()
    combined_file.close()
    print 'Finished!'
    print utils.line

if __name__ == '__main__':
    '''
    # companies = ['BABA', 'BIDU', 'CHA', 'CHL', 'CHU', 'DJIA', 'JMEI', 'NTES', 'SINA', 'SOHU', 'TCTZF']
    company_list = dao.get_all_processed_companies()
    for company in company_list:
        generate_combined_csv(company['code'])
    '''
    generate_assembled_combined()
