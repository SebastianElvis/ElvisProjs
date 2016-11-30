# -*- coding: utf-8 -*-
import urllib2, pymongo, bs4, re, datetime, json, sys, hashlib
from record import Record

reload(sys)
sys.setdefaultencoding('utf-8')

cookie_str = '''
                _T_WM=eb005c7d02bf6d595bb3d6c428d22d99; gsid_CTandWM=4upp399e1JDZGUibPwrfs9Fhy8e; ALF=1482738005; SCF=Au-8Lmr7NmWTYYGK6VBbp3NX61FI963-ucAjAUhPoT-bFxb-UZbrGF7l9blggRg8V3aPEncD3KpDU1IV5Bsnbfw.; SUB=_2A251PU5hDeTxGeRN61EX9CrJyjyIHXVW3lIprDV6PUJbktAKLXbukW0KQDG7B3I_ScmdERLQzXg4q8mZHA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh3LNHVkce-0__UlEggblno5JpX5o2p5NHD95QEe050SoBXSK27Ws4Dqcj.i--4iKLsi-24i--4iKLsi-24i--ci-zci-2ci--Ri-zciKnf; SUHB=0KAg41Om5Sfqw_; SSOLoginState=1480146481
             '''
header_dict = {"cookie": cookie_str,
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36'}


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def get_records_from_html(html, page_num, poster_id=''):
    record_list = []
    parsed_html = bs4.BeautifulSoup(html, 'lxml')
    record_div_list = parsed_html.find_all(id=re.compile('M_.*'))  # list of the microblog records
    for record_div in record_div_list:
        record = Record()
        # get the poster_id
        record.poster_id = poster_id
        # a record conists of two child div, the first contains contents and the second contains time, reposts and so on
        record_child_div = []
        for tmp in record_div.children:
            record_child_div.append(tmp)
        # get the content
        record.content = record_child_div[0].select('[class="ctt"]')[0].get_text()

        # get the time
        raw_record_time = record_child_div[-1].find_all("span", recursive=False)[-1].get_text()
        time_index = raw_record_time.find(u'来自')
        raw_record_time = raw_record_time[0:(time_index - 1)]
        if u'前' in raw_record_time or u'今天' in raw_record_time:  # 今天
            record.time = datetime.date.today()
        elif u'月' in raw_record_time and u'日' in raw_record_time:  # 今年中的某一天
            record_time = datetime.datetime.strptime(raw_record_time, u'%m月%d日 %H:%M')
            record_time = record_time.replace(year=2016)
            record.time = record_time.date()
        else:  # 前面的年份
            record_time = datetime.datetime.strptime(raw_record_time, '%Y-%m-%d %H:%M:%S')
            record.time = record_time.date()
        record.time = str(record.time)
        record.hash = hashlib.sha1(str(record)).hexdigest()
        record.page_num = page_num
        record_list.append(record.__dict__)

    return record_list


if __name__ == '__main__':
    url = 'http://weibo.cn/importnew?page=200'
    req = urllib2.Request(url, headers=header_dict)
    r = urllib2.urlopen(req)
    print get_records_from_html(r.read())
