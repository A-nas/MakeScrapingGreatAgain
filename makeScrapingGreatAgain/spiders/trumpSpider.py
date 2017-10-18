# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import FormRequest
from scrapy import Selector
from scrapy.http import Request # for yelding a request
from time import sleep
from urllib import urlencode
import logging
import json


class TrumpspiderSpider(Spider):
    #overrided properties
    name = 'trumpSpider'
    #class properties
    tweetAPIGetParams = None
    profileName = None
    since = None
    until = None
    query = None
    #computd properties
    start_urlsGetParams = None

    def __init__(self, profileName, since, until):
        self.profileName = profileName
        self.since = since
        self.until = until
        self.query = 'from:'+self.profileName+' since:'+ self.since +' until:'+ self.until +'&src=typd'
        self.start_urlsGetParams = {
        'l':'',
        'q':self.query
        }
        #overrided
        self.allowed_domains = ['https://twitter.com/'+self.profileName]
        self.tweetAPIGetParams = ['https://twitter.com/i/profiles/show/'+self.profileName+'/timeline/tweets']

    	self.start_urls = ['https://twitter.com/search?'+urlencode(self.start_urlsGetParams)]
        logging.info('warning call %s',self.start_urls[0])

    #overrided fucntion that prepare request with inner headers
    def start_requests(self):
        params = { 
        'Host':'twitter.com',
        'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linu…) Gecko/20100101 Firefox/56.0',
        'Accept':'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
        'Accept-Language':'en-US,en;q=0.5',
        'Accept-Encoding':'gzip, deflate, br',
        'Upgrade-Insecure-Requests':'1',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0'
        }
        return [FormRequest(self.start_urls[0],headers=params)]#default callback will be parse function   	

    def parse(self, response):
        self.parse_data(response)
        #search for next iteration (min-position)
        next_position = response.xpath('//*[@id="timeline"]/div/@data-min-position').extract()[0].split('-')[1]
        logging.info('Next Position ====> %s',next_position)
        #GET parameters (no headers needed (for the moment))
        get_params = {
        'q' : self.query,
        'include_available_features' : '1',
        'include_entities' : '1',
        'max_position' : next_position,
        'reset_error_state' : 'false',
        'src':'typd',
        'vertical':'default'
        }
        sleep(10)
        yield Request(self.tweetAPIGetParams[0]+'?'+urlencode(get_params), callback=self.parse_json_tweets,dont_filter=True)


    def parse_json_tweets(self, response):
        data = json.loads(response.text)
        selector = Selector(text=data['items_html'], type='html')
        self.parse_data(reponse = selector)

    def parse_data(self, response):
        logging.info(' EXTRACTIONNN ====> %s',response.url)
        comments_react = self.stats_extractor('reply', response)
        retweet_react = self.stats_extractor('retweet', response)
        favorite_react = self.stats_extractor('favorite', response)
        tweets = response.xpath('.//*[contains(@class,"js-stream-item stream-item stream-item")]/div[1]/div[2]/div[2]/p/text()').extract()
        tweetdates = response.xpath('.//*[contains(@class,"js-stream-item stream-item stream-item")]/div[1]/div[2]/div[1]/small/a/span[1]/text()').extract();
        yield {
         'comments' : comments_react,
         'retweets' : retweet_react,
         'favorites' : favorite_react,
         'teweets' : tweets,
         'tweetDates' : tweetdates,
        }

    def stats_extractor(self, statsString, response):
        #make an enum for that (parameter)
        stats = response.xpath('.//*[contains(@class,"js-stream-item stream-item stream-item")]/'
        +'div[1]/div[2]/div[contains(@class,"stream-item-footer")]/'
        +'div[contains(@class,"ProfileTweet-actionCountList u-hiddenVisually")]/'
        +'span[contains(@class,"ProfileTweet-action--'+ statsString +' u-hiddenVisually")]/span[1]/@data-tweet-stat-count').extract()
        
        return stats

