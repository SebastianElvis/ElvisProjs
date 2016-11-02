import urllib, urllib2, json

class StockData:
    """docstring for StockData"""
    def __init__(self):
        self.juhe_stock_query_appkey = '9b8aef021e82ff6b65ad7fa3efddb1f9'
        self.juhe_stock_query_url = 'http://op.juhe.cn/onebox/stock/query'
        self.juhe_stock_data_appkey = 'f505169826d5540b1a7108a0af0bceab'
        self.juhe_stock_data_url = 'http://web.juhe.cn:8080/finance/stock/usa'
        self.baidu_apikey = '596fe855925b9355e516ae327f4528ca'
        self.baidu_djia_url = 'http://apis.baidu.com/apistore/stockservice/usastock'
        self.stock_list = {
            'AMZN' : 'Amazon',
            'BIDU' : 'Baidu',
            'MSFT' : 'Microsoft',
            'GOOG' : 'Google',
            'ADBE' : 'Adobe',
            'RHT' : 'RedHat',
            'HPQ' : 'HP',
            'NOK' : 'Nokia',
            'YHOO' : 'Yahoo',
            'AAPL' : 'Apple',
            'ORCL' : 'Oracle',
            'BABA' : 'Alibaba',
            'ERIC' : 'Ericsson',
            'CHL' : 'China Mobile',
            'T' : 'AT&T'        
        }

    def getJSON(self, url, data):
        encoded_data = urllib.urlencode(data)
        print encoded_data
        req = urllib2.Request(self.baidu_djia_url, encoded_data)
        res_data = json.loads(urllib2.urlopen(req).read())
        return res_data
    
    def getDJIA(self):
        data = {'apikey' : self.baidu_apikey , 'stockid' : 'bidu', 'list' : 1}
        return self.getJSON(self.baidu_djia_url, data)
        
    def query_stock(self, stock_id):
        data = {'gid' : stock_id, 'key' : self.juhe_stock_data_appkey}
        return self.getJSON(self.juhe_stock_data_url, data)

    def query_all_stock(self):
        all_stock_data = []
        for id in self.stock_list.keys():
            all_stock_data.append(self.query_stock(id))
        return all_stock_data
		
print StockData().query_all_stock()