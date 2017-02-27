# -*- coding: utf-8 -*-
import scrapy
from ipcrawler.items import IpAddrItem
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class YqieSpider(scrapy.Spider):
    name = "yqie"
    allowed_domains = ["yqie.com"]
    start_urls = ['http://ip.yqie.com/china.aspx']

    def parse(self, response):
        licitynavgraycity_list = response.xpath('//li[@class="licitynavgraycity"]')
        print 'Length of the li list --- ', len(licitynavgraycity_list)
        for licitynavgraycity in licitynavgraycity_list:
            province = licitynavgraycity.xpath('../../preceding-sibling::a/text()').extract()[0] + '省'
            city = licitynavgraycity.xpath('./a/text()').extract()[0]
            city_link = 'http://ip.yqie.com' + licitynavgraycity.xpath('./a/@href').extract()[0]
            yield scrapy.http.Request(city_link,
                                      headers={'city': city, 'province': province},
                                      callback=self.parse_city_link)

    def parse_city_link(self, response):
        tr_list = response.xpath('//tr')[1:]
        print 'Length of the tr list --- ', len(tr_list)
        for tr in tr_list:
            single_ip_addr_item = IpAddrItem()
            td_list = tr.xpath('./td/text()').extract()
            single_ip_addr_item['ip_start'] = td_list[1]
            single_ip_addr_item['ip_end'] = td_list[2]
            single_ip_addr_item['city'] = response.request.headers['city']
            single_ip_addr_item['province'] = response.request.headers['province']

            # judge if there is something more detailed
            position_detail = td_list[3].split(' ')
            if len(position_detail) >= 2:
                single_ip_addr_item['isp'] = position_detail[1]

            if(position_detail[0].find('市') != -1 and
                (position_detail[0].find('区') != -1 or position_detail[0].find('县') != -1) ):
                single_ip_addr_item['district'] = position_detail[0].split('市')[-1]

            yield single_ip_addr_item





