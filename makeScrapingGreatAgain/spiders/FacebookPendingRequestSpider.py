import scrapy
from scrapy.http import Request
import logging
from scrapy.http import FormRequest
import json
from configparser import ConfigParser


class FacebookpendingrequestspiderSpider(scrapy.Spider):
    name = 'FacebookPendingRequestSpider'
    allowed_domains = ['facebook.com']
    start_urls = ['http://facebook.com/']

    params = None
    cookies = None
    data = None

    def start_requests(self):
        #Get manual config
        config = ConfigParser(interpolation=None)
        config.read('masterData.ini')
        configSection = config['FACEBOOK']
        #Fill data
        self.params = json.loads(configSection['Headers'])
        self.cookies = json.loads(configSection['Cookies'])
            #form data to send via POST
        self.data = json.loads(configSection['Datas'])
        self.data.update({'variables':'{"count":1000,"cursor":"502492655","scale":1.5}'})


        return [FormRequest(self.start_urls[0],
                            headers=self.params,
                            method='POST',
                            formdata=self.data,
                            cookies=self.cookies)]#default callback will be parse function  


    def __init__(self):
        #overrided
        self.allowed_domains = ['facebook.com']
        self.start_urls = ['https://www.facebook.com/api/graphql/']


    def parse(self, response):
        #logging.DEBUG()
        #logging.warning(response.text)
        yield {
             'JSON' : response.text
            }
        pass
