# coding:utf-8

from base_dao import BaseDAO
from poster import Poster
import weibo_utils
import sys
import bs4
import re
import urllib2
import time

reload(sys)
sys.setdefaultencoding('utf-8')


keywords = {
    'financial_news': ['财经', '金融', '证券', '财富', '投资', '理财'],
    'tech_news': ['科技', '互联网', '创新', 'IT', '创投']
}


def get_seed_posters():
    dao = BaseDAO()
    poster_list = dao.find_all('data_source')
    poster_obj_list = []
    for poster_dict in poster_list:
        poster = Poster()
        poster.id = str(poster_dict['_id'])
        poster.name = poster_dict['name']
        poster.url = poster_dict['url']
        poster.type = poster_dict['type']
        poster_obj_list.append(poster)
    return poster_obj_list


def get_followings_from_html(html):
    poster_list = []
    parsed_html = bs4.BeautifulSoup(html, 'lxml')
    poster_table_list = parsed_html.find_all('table')
    for poster_table in poster_table_list:
        key_td = poster_table.find_all('td')[1]
        poster = Poster()
        poster.name = key_td.find_all('a')[0].get_text()
        poster.url = key_td.find_all('a')[0]['href']

        # get the number of fans
        follower_num_pattern = re.compile(u'粉丝([0-9]+)人')
        pattern_search = follower_num_pattern.search(key_td.get_text())
        if pattern_search is not None:
            poster.follower_num = int(pattern_search.group(1))

        # get details of the poster
        hp_resp = None
        while hp_resp is None:
            try:
                hp_req = urllib2.Request(poster.url, headers=weibo_utils.generate_header())
                hp_resp = urllib2.urlopen(hp_req, timeout=5)
            except:
                print 'urlopen error! url is ' + poster.url
                hp_resp = None
            finally:
                time.sleep(3)
        hp_html = hp_resp.read()
        poster_info = get_info_from_homepage_html(hp_html)
        poster.description = poster_info['description']
        poster.fans_url = poster_info['fans_url']
        poster.auth = poster_info['auth']
        poster_list.append(poster)
        print poster
    return poster_list


def get_info_from_homepage_html(html):
    poster_info = {}
    parsed_html = bs4.BeautifulSoup(html, 'lxml')
    # print parsed_html
    div_ut = parsed_html.find_all('table')[0].tr.find_all('td')[1]
    poster_info['auth'] = div_ut.find_all('span', {'class': 'ctt'})[1].get_text()[3:]
    poster_info['description'] = div_ut.find_all('span', {'class': 'ctt'})[2].get_text()
    poster_info['fans_url'] = 'http://weibo.cn' \
                              + parsed_html.find_all('div', {'class': 'tip2'})[0].find_all('a')[1].get('href')
    return poster_info


def judge_poster(poster):
    if poster.follower_num < 50000:
        return 'fail'
    else:
        for financial_word in keywords['financial_news']:
            if financial_word in ' '.join([poster.name, poster.description, poster.auth]):
                print 'Hit financial word ----' + financial_word
                return 'financial_news'
        for tech_word in keywords['tech_news']:
            if tech_word in ' '.join([poster.name, poster.description, poster.auth]):
                print 'Hit tech word ----' + tech_word
                return 'tech_news'
        return 'fail'


if __name__ == '__main__':
    req = urllib2.Request('http://weibo.cn/1638782947/follow', headers=weibo_utils.generate_header())
    print req.headers
    resp = urllib2.urlopen(req, timeout=5)
    html = resp.read()
    followings = get_followings_from_html(html)
    print len(followings)
    for following in followings:
        if judge_poster(following) == 'fail':
            followings.remove(following)
        else:
            following.type = judge_poster(following)
    print len(followings)
    print followings

