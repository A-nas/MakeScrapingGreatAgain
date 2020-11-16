import scrapy
#from scrapy.http import Request
import requests
import logging
from scrapy.http import FormRequest
import json
from configparser import ConfigParser

#scrapy crawl FacebookPendingRequestSpider -a user="" -a pwd="" -a datr=""
class FacebookpendingrequestspiderSpider(scrapy.Spider):
    name = 'FacebookPendingRequestSpider'
    allowed_domains = ['facebook.com']
    start_urls = ['http://facebook.com/']
    

    params = None
    cookies = None
    data = None
    user = None
    pwd = None
    _datr = None


    def __init__(self, user, pwd, datr):
        #INSTRUCTOR
        self.allowed_domains = ['facebook.com']
        self.start_urls = ['https://www.facebook.com/api/graphql/','https://www.facebook.com/login/']
        self.user = user
        self.pwd = pwd
        self._datr = datr


    
    def start_requests(self):
        #GET HIDEN INPUT DATA FROM LOGIN FORM
        return [FormRequest(self.start_urls[1],
                    method='GET',
                    cookies = {'datr':self._datr},
                    callback = self.extract_cookies)]

    def extract_cookies(self, response):
        #PARSING HIDEN DATA REQUIRED TO SEND A LOGIN REQUEST
        lsd = response.xpath('//*[@name="lsd"]/@value').extract_first()
        return [FormRequest(self.start_urls[1],
                    method='POST',
                    formdata={'email': self.user, 'pass': self.pwd, 'lsd': lsd},
                    cookies = {'datr':self._datr},
                    meta = {'cookiejar': 1, 'dont_redirect': True,'handle_httpstatus_list': [302]},
                    callback = self.after_login)]

    def after_login(self, response):
        cookies = {}
        for item in response.headers.getlist('Set-Cookie'):
            cookies.update(self.parse_cookies(item.decode(),'; ', '='))
        #Get manual config
        config = ConfigParser(interpolation=None)
        config.read('masterData.ini')
        configSection = config['FACEBOOK']
        #Fill data
        self.cookies = cookies
            #form data to send via POST
        self.data = json.loads(configSection['Datas'])
        return [FormRequest(self.start_urls[0],
                            #headers=self.params,
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

    def parse_cookies(self, raw_cookies, delimiter, equaloperator):
        cookies = {}
        for cookie in raw_cookies.split(delimiter):
            try:
                key = cookie.split(equaloperator)[0]
                val = cookie.split(equaloperator)[1]
                cookies[key] = val
            except:
                pass
            break
        return cookies