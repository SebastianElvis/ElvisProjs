# -*- coding: utf-8 -*-
import scrapy


class RedditSpider(scrapy.Spider):
    name = "reddit"
    allowed_domains = ["reddit.com"]
    start_urls = (
        'http://www.reddit.com/',
    )

    def parse(self, response):
        pass
