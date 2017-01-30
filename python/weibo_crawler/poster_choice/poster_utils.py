# coding:utf-8

from base_dao import BaseDAO
from poster import Poster
import sys

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


def get_followers_from_html(html):
    pass


if __name__ == '__main__':
    pass
