# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request # for yelding a request 


class TrumpspiderSpider(Spider):
    name = 'trumpSpider'
    allowed_domains = ['https://twitter.com/realDonaldTrump']


    def __init__(self, profileName, since, until): # date should be formated as follow yyyy-mm-dd
    	self.start_urls = ['https://twitter.com/search?l=&q=from:'+profileName+
                           ' since:'+ since +
                           ' until:'+ until +'&src=typd']	   	

    def parse(self, response):
        # must scrap tweet date
        comments_react = self.stats_extractor('reply', response)
        retweet_react = self.stats_extractor('retweet', response)
        favorite_react = self.stats_extractor('favorite', response)

        tweets = response.xpath('.//*[contains(@class,"js-stream-item stream-item stream-item")]/div[1]/div[2]/div[2]/p/text()').extract()
        tweetdates = response.xpath('.//*[contains(@class,"js-stream-item stream-item stream-item")]/div[1]/div[2]/div[1]/small/a/span[1]/text()').extract();
        
        #search for next url and run callback
        
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

