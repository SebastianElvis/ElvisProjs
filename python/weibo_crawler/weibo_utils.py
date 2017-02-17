# -*- coding: utf-8 -*-
import urllib2, bs4, re, datetime, json, hashlib
from record import Record
from random_list import RandomList
from base_dao import BaseDAO
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

line = '-------------------------------------------------------'

referers = BaseDAO().get_all_referers()


def generate_header():
    r_list = RandomList()
    header_dict = {}

    # cookie
    cookie_str = '''
_T_WM=05cc869bb2fca61fcd71553a8d18331e; ALF=1489832056; SCF=AsAX-nl6za_tqmlP7Wc4KZBfnM5lvn6m2-lc1hztSI7k5yDhHYEs74LtXw3_XszehtkW2JVeKDv235bd8Sqh6nU.; SUB=_2A251oQsuDeRxGeRN61EX9CrJyjyIHXVXbZVmrDV6PUJbktBeLVnEkW1NveA1EY7_Cfq_lvDrfzCXECY2Hg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh3LNHVkce-0__UlEggblno5JpX5o2p5NHD95QEe050SoBXSK27Ws4Dqcj.i--4iKLsi-24i--4iKLsi-24i--ci-zci-2ci--Ri-zciKnf; SUHB=0N2EF4D-dx1jDu; SSOLoginState=1487240062
                 '''.strip()
    header_dict['Cookie'] = cookie_str
    header_dict['Accept-Language'] = 'zh-CN,zh;q=0.8'
    header_dict['User-Agent'] = r_list.get_random_ua()
    header_dict['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    #header_dict['Accept-Encoding'] = 'gzip, deflate, sdch'
    header_dict['Cache-Control'] = 'max-age=0'
    header_dict['Connection'] = 'keep-alive'
    header_dict['Host'] =  'weibo.cn'
    header_dict['Referer'] = 'weibo.cn/2303644510/info' # r_list.get_random(referers)
    header_dict['Upgrade-Insecure-Requests'] = '1'
    return header_dict


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
        print 'raw_record_time :' + raw_record_time
        if u'前' in raw_record_time or u'今天' in raw_record_time:  # 今天
            record.time = datetime.date.today()
        elif u'月' in raw_record_time and u'日' in raw_record_time:  # 今年中的某一天
            # datetime不支持闰年
            if u'02月29日' in raw_record_time:
                print '02.29 Detected !'
                raw_record_time = raw_record_time.replace('29', '28')
                print 'Already replaced by 02.28 !'
            try:
                record_time = datetime.datetime.strptime(raw_record_time , u'%m月%d日 %H:%M')
            except:
                print 'Strptime Error this year ! ---- raw_record_time is: ', raw_record_time
                return
            record_time = record_time.replace(year=2017)
            record.time = record_time.date()
        else:  # 前面的年份
            try:
                record_time = datetime.datetime.strptime(raw_record_time, '%Y-%m-%d %H:%M:%S')
            except:
                print 'Strptime Error previous year ! ---- raw_record_time is: ', raw_record_time
                return
            record.time = record_time.date()
        record.time = str(record.time)
        record.hash = hashlib.sha1(str(record)).hexdigest()
        record.page_num = page_num
        record_list.append(record.__dict__)

    return record_list


class RedirctHandler(urllib2.HTTPRedirectHandler):
    """docstring for RedirctHandler"""
    def http_error_301(self, req, fp, code, msg, headers):
        pass
    
    def http_error_302(self, req, fp, code, msg, headers):
        pass

if __name__ == '__main__':
    url = 'http://weibo.cn/importnew?page=200'
    req = urllib2.Request(url, headers=generate_header())
    r = urllib2.urlopen(req)
    print get_records_from_html(r.read())
