# -*- coding: utf-8 -*-
import scrapy, urlparse, re
from ttmeiju.items import OperaItem


class MjspiderSpider(scrapy.Spider):
    name = "mjspider"
    allowed_domains = ["ttmeiju.com"]
    start_urls = (
        'http://www.ttmeiju.com/summary.html',
    )
    
    def get_page(url):
        query = urlparse.urlparse(url).query
        if 'page' not in query:
            return 1
        else :
            p = re.compile('page=[0-9]{1,3}')
            page = int( p.findall(url)[0].split('=')[-1] ) 
            return page
            
    def parse(self, response):
        for url in response.xpath('//tr[@bgcolor="#ffffff"]/td/a/@href').extract():
            yield scrapy.Request(url, callback=self.parse_opera)
    
    
        
    def parse_opera(self, response):
        name = response.xpath('//h3').extract()[0].split(' ')[0]
        if u'高清电影' in name:
            for line in response.xpath('//tr[@class="Scontent"]'):
                item = OperaItem()
                tds = line.xpath('td')
                item.opera_name = tds[1]
                item.season_number = 0
                item.episode_number = 0
                item.tail = 0
                
                if len(line.xpath('td/a[@title="百度云盘下载"]/@href')) != 0:
                    item.baiduyun_link = line.xpath('td/a[@title="百度云盘下载"]/@href').extract()
                else: 
                    item.baiduyun_link = ''
                
                if len(line.xpath('td/a[@title="BT美剧片源下载"]/@href')) != 0:
                    item.bt_link = line.xpath('td/a[@title="BT美剧片源下载"]/@href').extract()
                else: 
                    item.bt_link = ''
                
                if len(line.xpath('td/a[@title="磁力链高清美剧下载"]/@href')) != 0:
                    item.magnet_link = line.xpath('td/a[@title="磁力链高清美剧下载"]/@href').extract()
                else: 
                    item.magnet_link = ''
                
                if len(line.xpath('td/a[@title="ed2k高清片源"]/@href')) != 0:
                    item.ed2k_link = line.xpath('td/a[@title="ed2k高清片源"]/@href').extract()
                else: 
                    item.ed2k_link = ''
                
                item.resolution = None
                yield item
        
        else:
            for line in response.xpath('//tr[@class="Scontent"]'):
                item = OperaItem()
                tds = line.xpath('td')
                item['opera_name'] = name
                
                session_episode_p = re.compile('S[0-9]{1,2}E[0-9]{1,2}') 
                item.season_number = int(session_episode_p.findall(tds[1].extract())[0].split('E')[0][1:])
                item.episode_number = int(session_episode_p.findall(tds[1].extract())[0].split('E')[1])
                item.tail = 0
                
                if len(line.xpath('td/a[@title="百度云盘下载"]/@href')) != 0:
                    item.baiduyun_link = line.xpath('td/a[@title="百度云盘下载"]/@href').extract()
                else: 
                    item.baiduyun_link = ''
                
                if len(line.xpath('td/a[@title="BT美剧片源下载"]/@href')) != 0:
                    item.bt_link = line.xpath('td/a[@title="BT美剧片源下载"]/@href').extract()
                else: 
                    item.bt_link = ''
                
                if len(line.xpath('td/a[@title="磁力链高清美剧下载"]/@href')) != 0:
                    item.magnet_link = line.xpath('td/a[@title="磁力链高清美剧下载"]/@href').extract()
                else: 
                    item.magnet_link = ''
                
                if len(line.xpath('td/a[@title="ed2k高清片源"]/@href')) != 0:
                    item.ed2k_link = line.xpath('td/a[@title="ed2k高清片源"]/@href').extract()
                else: 
                    item.ed2k_link = ''
                
                item.resolution = None
                yield item
        
        base_url = urlparse.urlparse(response.url)
        if len(response.xpath('tr/a[@class="next"]')) != 0:
            next_url = base_url + response.xpath('//tr/a[@class="next"]/@href').extract()
            yield scrapy.Request(next_url, callback=self.parse_opera)
        
        
        
                
                
                
            
            
        
