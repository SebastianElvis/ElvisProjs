import urllib, urllib2, json

class StockData:
	"""docstring for StockData"""
	def __init__(self):
		self.apikey = '596fe855925b9355e516ae327f4528ca'

	def getDJIA(self):
		url = 'http://apis.baidu.com/apistore/stockservice/usastock?stockid=bidu&list=1'
		data = {'apikey':self.apikey}
		encoded_data = urllib.urlencode(data)
		req = urllib2.Request(url, encoded_data)
		res_data = json.loads(urllib2.urlopen(req).read())
		print res_data
		