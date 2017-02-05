# coding:utf-8

from base_dao import BaseDAO
from poster import Poster
import weibo_utils
import sys
import bs4
import re
import urllib2

reload(sys)
sys.setdefaultencoding('utf-8')


keywords = {
    'financial': ['财经', '金融', '证券', '财富', '投资', '理财'],
    'tech': ['科技', '互联网', '创新', 'IT', '创投']
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
        key_td = poster_table.tbody.tr.td[1]
        poster = Poster()
        poster.name = key_td.a[0].get_text()
        poster.url = key_td.a[0]['href']
        # get the number of followers
        follower_num_pattern = re.compile(u'粉丝([0-9]+)人')
        pattern_search = follower_num_pattern.search(key_td.get_text())
        if pattern_search is not None:
            poster.follower_num = pattern_search.group(1)
        print poster.__dict__
    pass


if __name__ == '__main__':
    req = urllib2.Request('http://weibo.cn', headers=weibo_utils.generate_header())
    print req.headers
    resp = urllib2.urlopen(req, timeout=5)
    html = resp.read()
    #get_followings_from_html(html)

