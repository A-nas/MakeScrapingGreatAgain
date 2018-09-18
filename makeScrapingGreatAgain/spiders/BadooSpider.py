# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request # for yelding a request must be removed *
import logging
from scrapy.http import FormRequest
import json


class BadoospiderSpider(scrapy.Spider):
	name = 'BadooSpider'
	allowed_domains = ['badoo.com']
	#start_urls = ['http://badoo.com/']
	params = None
	cookies = None
	postRequest = None

	def __init__(self):
        #overrided
		logging.info('=========> start request')
		self.params = { 
		'Accept':'*/*',
		'Accept-Language':'en-US,en;q=0.5',
		'Connection':'keep-alive',
		'Referer':'https://badoo.com/encounters',
		'Content-Type':'json',
		'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
		'X-Desktop-web':'1',
		'X-Message-type':'104',
		'X-Session-id':'t2704df0f43b34636990a28e4abff9d3f',
		'X-User-id':'513426692',
		}
        #careful with session auth, may be expired
		self.cookies = {
		'_ga' : 'GA1.2.1654638883.1537058208',
		'_gid' : 'GA1.2.253655045.1537058208',
		'_parsely_visitor' : '{"id":"pid=03f1f4406b4ea8d75830498674b5417e","session_count":1,"last_session_ts":1537058205936}',
		'aid' :	'513426692',
		'cpc' :	'{"c":0,"e":1539649049778,"d":"badoo.com","u":"513426692"}',
		'device_id' : '11bbe928-e928-2875-757b-7b432abcfa26',
		'fbm_107433747809' : 'base_domain=.badoo.com',
		'fbsr_107433747809' : 'bYHpNH_SOQs_FK3E673iUc_LlBlo7VqCV8YP9i0jtVg.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUF3bUpfX0xqdG5RVXZQQ2N6U0hQLW5EcnRfLTlyejZBVHF3TnltZ0ZRV1lEa3JrXzhXUG9qYlFfUHp5RUlKS2pGeV9temhGVTNBRkRSN1FlZEZoeVQ1Zm9lMmZQbzg1V05LMlhmVDFWeG81Q01uRGJ2MDI1RE1rUy1sRWRocHBPYUxZTjFrcGswNjNfMHRrQk1RbE44N01hQzdrRGJlTVltNE91V3dMLWxFV2lmZXlrSXZjQVRGNVVmZ0JoNGdMNDdvd0FrWlBYMjFEMFZrY1l4OXhpbTBtWk03T2FERHZSRGN6djdadWIybm1DSkI4UFcyMUEwTWFnSDNxT3lvMlV1U2duLWtHR2RMNi0zMVEwckNkR1dsT2pxbHBRc0xMY084T1NLQjNlSWNhWkJVTkZYMFp0MllTd0lMaTd6UTk0dm14UDZSejJOUFp6SDRxa3FtSDEtVCIsImlzc3VlZF9hdCI6MTUzNzMxMDk4MSwidXNlcl9pZCI6IjcwNjAzOTUwMjc3MDkxMSJ9',
		'has_secure_session' : '1',
		'pid' : '1',
		's1' : 'te5832b5b657046da936486cca30e2543',
		}
		self.start_urls = ['https://badoo.com/bmaapi.phtml?SERVER_SEND_CHAT_MESSAGE']
		self.postRequest = {"version":"1",
							"message_type":"104",
							"message_id":"18",
							"body":"[{'message_type':'104','chat_message':{'mssg':'HelloThere!TheIngelFromMyNightmare','message_type':'1','uid':'1537220104538','from_person_id':'513426692','to_person_id':'309354356','read':'false'}}]",
							"is_background":"false"}
		#with open('/home/anas/Desktop/makeScrapingGreatAgain/makeScrapingGreatAgain/spiders/DataForm.txt') as handle:
		#	self.postRequest = json.loads(handle.read())
	def parse(self, response):
		logging.info('=========> parsing')
		logging.info('preaparing to send requets to %s with parameters %s',self.start_urls[0],self.postRequest)
		yield FormRequest(url=response.url  , formdata=self.postRequest , callback=self.parse_data,dont_filter=True, headers=self.params, cookies=self.cookies)

	def parse_data(self, response):
		logging.info('=========> sub parsing data %s',response.text)
		pass
