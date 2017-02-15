# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OperaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    opera_name = scrapy.Field()
    season_number = scrapy.Field()    
    episode_number = scrapy.Field()
    tail = scrapy.Field()
    baiduyun_link = scrapy.Field()
    bt_link = scrapy.Field()
    magnet_link = scrapy.Field()
    ed2k_link = scrapy.Field()
    resolution = scrapy.Field()
    pass
