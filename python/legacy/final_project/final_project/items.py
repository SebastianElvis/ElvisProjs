# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PositionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    company_id = scrapy.Field()
    work_year = scrapy.Field()
    education = scrapy.Field()
    job_nature = scrapy.Field()
    position_name = scrapy.Field()
    company_logo = scrapy.Field()
    industry_field = scrapy.Field()
    finance_stage = scrapy.Field()
    city = scrapy.Field()
    salary = scrapy.Field()
    position_id = scrapy.Field()
    company_short_name = scrapy.Field()
    position_advantage = scrapy.Field()
    create_time = scrapy.Field()
    district = scrapy.Field()
    company_label_list = scrapy.Field()
    approve = scrapy.Field()
    company_size = scrapy.Field()
    score = scrapy.Field()
    company_full_name = scrapy.Field()
    format_create_time = scrapy.Field()
    im_state = scrapy.Field()
    publisher_id = scrapy.Field()
    pass
