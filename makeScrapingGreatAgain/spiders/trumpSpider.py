# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import FormRequest
from scrapy.http import Request # for yelding a request
import logging


class TrumpspiderSpider(Spider):
    name = 'trumpSpider'
    allowed_domains = ['https://twitter.com/realDonaldTrump']


    def __init__(self, profileName, since, until): # date should be formated as follow yyyy-mm-dd
    	self.start_urls = ['https://twitter.com/search?l=&q=from:'+profileName+
                           ' since:'+ since +
                           ' until:'+ until +'&src=typd']

    #URL headers
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
        comments_react = self.stats_extractor('reply', response)
        retweet_react = self.stats_extractor('retweet', response)
        favorite_react = self.stats_extractor('favorite', response)
        tweets = response.xpath('.//*[contains(@class,"js-stream-item stream-item stream-item")]/div[1]/div[2]/div[2]/p/text()').extract()
        tweetdates = response.xpath('.//*[contains(@class,"js-stream-item stream-item stream-item")]/div[1]/div[2]/div[1]/small/a/span[1]/text()').extract();
        #maxPosition = response.xpath();
        yield {
         'comments' : comments_react,
         'retweets' : retweet_react,
         'favorites' : favorite_react,
         'teweets' : tweets,
         'tweetDates' : tweetdates,
        }
        #search for next position
        params = { 
        "action": "search",
        "description": "My search here",
        "e_author": ""
        }
        yield Request(response.url, callback=self.parse_tweets)

    def stats_extractor(self, statsString, response):
        #make an enum for that (parameter)
        stats = response.xpath('.//*[contains(@class,"js-stream-item stream-item stream-item")]/'
        +'div[1]/div[2]/div[contains(@class,"stream-item-footer")]/'
        +'div[contains(@class,"ProfileTweet-actionCountList u-hiddenVisually")]/'
        +'span[contains(@class,"ProfileTweet-action--'+ statsString +' u-hiddenVisually")]/span[1]/@data-tweet-stat-count').extract()
        
        return stats

