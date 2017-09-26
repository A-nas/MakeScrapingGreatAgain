# -*- coding: utf-8 -*-
import scrapy


class TrumpspiderSpider(scrapy.Spider):
    name = 'trumpSpider'
    allowed_domains = ['https://twitter.com/realDonaldTrump']
    start_urls = [
    'https://twitter.com/search?l=&q=from:realDonaldTrump since:2016-09-01 until:2017-09-26&src=typd'
    ]
    

    def parse(self, response):
        # must scrap tweet date
        comments_react = self.stats_extractor('reply', response)
        retweet_react = self.stats_extractor('retweet', response)
        favorite_react = self.stats_extractor('favorite', response)

        yield {
         'comments' : comments_react,
         'retweet' : retweet_react,
         'favorite' : favorite_react,
        }

    def stats_extractor(self, statsString, response):
        #make an enum for that (parameter)
        stats = response.xpath('.//*[contains(@class,"js-stream-item stream-item stream-item")]/'
        +'div[1]/div[2]/div[contains(@class,"stream-item-footer")]/'
        +'div[contains(@class,"ProfileTweet-actionCountList u-hiddenVisually")]/'
        +'span[contains(@class,"ProfileTweet-action--'+statsString+' u-hiddenVisually")]/span[1]/@data-tweet-stat-count').extract()
        return stats

