import scrapy
#from scrapy.http import Request
import requests
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
    #login_url = 'https://www.facebook.com/login/'
    user = None
    pwd = None
    _datr = None

    def start_requests(self):
        #LOGIN AFTER START ANY REQUEST
        return [FormRequest(self.start_urls[1],
                    method='GET',
                    cookies = {'datr':self._datr},
                    callback = self.extract_cookies)]

    def extract_cookies(self, response):
        lsd = response.xpath('//*[@name="lsd"]/@value').extract_first()
        return [FormRequest(self.start_urls[1],
                    method='POST',
                    formdata={'email': self.user, 'pass': self.pwd, 'lsd': lsd},
                    cookies = {'datr':self._datr},
                    meta = {'cookiejar': 1, 'dont_redirect': True,'handle_httpstatus_list': [302]},
                    callback = self.after_login)]


    def __init__(self, user, pwd, datr):
        #overrided
        self.allowed_domains = ['facebook.com']
        self.start_urls = ['https://www.facebook.com/api/graphql/','https://www.facebook.com/login/']
        self.user = user
        self.pwd = pwd
        self._datr = datr

    def after_login(self, response):
        #check login
        #print(response.text.encode())
        print(response.headers)
        print(response.url)
        return

        #Get manual config
        config = ConfigParser(interpolation=None)
        config.read('masterData.ini')
        configSection = config['FACEBOOK']
        #Fill data
        self.params = json.loads(configSection['Headers'])
        self.cookies = json.loads(configSection['Cookies'])
            #form data to send via POST
        self.data = json.loads(configSection['Datas'])
        return [FormRequest(self.start_urls[0],
                            headers=self.params,
                            method='POST',
                            formdata=self.data,
                            cookies=self.cookies,
                            callback=self.parse)]#default callback will be parse function



    def parse(self, response):
        keepScroll = None
        #parse json
        apiResponse = None
        try:
            apiResponse = json.loads(response.text)
        except ValueError:
            print(response.text)
        #iterate on json and yield datas (list of 10)
        for key,value in enumerate(apiResponse['data']
        ['viewer']
        ['outgoing_friend_requests_connection']
        ['edges']):
            yield {
             'id' : value['node']['id'],
             'url' : value['node']['url'],
             'name' : value['node']['name']
            }
        #get stop iterator
        keepScroll = apiResponse['data']['viewer']['outgoing_friend_requests_connection']['page_info']['has_next_page']
        #if its done (json flag) retun
        if (keepScroll == False):
            return
    #get the last cursor position #else yield request with next position (update form data only and post)
        nextCursor = apiResponse['data']['viewer']['outgoing_friend_requests_connection']['page_info']['end_cursor']
        self.data.update({'variables':'{"count":10,"cursor":"'+nextCursor+'","scale":1.5}'})
        yield FormRequest(self.start_urls[0],
                           headers=self.params,
                           method='POST',
                           formdata=self.data,
                           cookies=self.cookies)


    def close(self, reason):
        print("spider closed for ", reason)