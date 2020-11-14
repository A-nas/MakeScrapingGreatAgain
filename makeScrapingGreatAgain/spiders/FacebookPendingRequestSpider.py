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
            # unfriendDatas = self.data
            # unfriendDatas.update({'variables':'{"input":{"cancelled_friend_requestee_id":"'+value['node']['id']+'","source":"manage_outgoing_requests","actor_id":"100000946033663","client_mutation_id":"4"},"scale":1.5}'})
            # unfriendDatas.update({'doc_id':'3226051994092510'}) #important (type of request)
            # requests.post(self.start_urls[0],headers=self.params,data=unfriendDatas,cookies=self.cookies)
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
