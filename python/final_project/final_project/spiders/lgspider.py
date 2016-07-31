import scrapy, json

class Lgspider(scrapy.Spider):
    name = 'lgspider'
    start_urls = [
        'http://www.lagou.com/jobs/positionAjax.json'    
    ]

    def parse(self, response):
        for i in range(1,10):
            yield scrapy.FormRequest(
                response,
                #formdata={'first' : 'false', 'pn' : i },
                callback=self.crawl_next
            )
            i += 1
    
    def crawl_next(self, response):
        response_obj = json.loads(response.body)
        result_list = response_obj.content.positionResult.result
        for j in len(result_list):
            print result_list[j]
            j += 1
