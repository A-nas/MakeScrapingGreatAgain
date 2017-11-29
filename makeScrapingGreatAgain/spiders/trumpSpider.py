# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider
from scrapy import FormRequest
from scrapy import Selector
from scrapy.http import Request # for yelding a request
from time import sleep
from urllib import urlencode
import logging
import json
from scrapy.conf import settings

#selector must be exported to config files
class TrumpspiderSpider(Spider):
    #overrided properties
    name = 'trumpSpider'
    #class properties
    tweetAPIGetParams = None
    profileName = None
    since = None
    until = None
    query = None
    last_position = None
    params = None
    cookies = None
    keepScroll = True
    get_params = None # api get params (for fetching new lists)
    API_Cookies = {
    'personalization_id' :'v1_AxNAd+cMYAuU4SmQcsKBlw==',
    'guest_id' :'v1%3A150592161834956482',
    '_ga' :'GA1.2.1438276811.1506337821', 
    'eu_cn' :'1',
    'kdt' :'Jtqd64V6rkpRKrALlMD8S0PXa4B93rSU9idtTb0E',
    'remember_checked_on' :'1', 
    'ads_prefs' :'HBERAAA=',
    'twid' :'u=3462555082',
    'auth_token' :'f415a8976fe683be29fbbef3bbce3855b92a8c16',
    'tip_nightmode' :'true',
    'tfw_exp' :'0',
    '__utma' :'43838368.1438276811.1506337821.1508530210.1508547526.5',
    '__utmz' :'43838368.1508320207.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    '_gid' :'GA1.2.820665622.1508520108',
    '_twitter_sess' :'BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCLho0EBfAToMY3NyZl9p%250AZCIlOGYxNjQ3OTUxNzUyMjc3ZmM2ZTI2M2YyZGFjMjdlODA6B2lkIiVjYzcw%250AMDIyOTczYmQ3OWRkNjU3MzNlZTJlNTZlOGZjZQ%253D%253D--9dffee641f695f6e52d049fd90d1ebf823f57095',
    'lang' :'fr',
    'ct0' :'5eec94032ed6d21e015d80900952cb5d'
    }

    #computd properties
    start_urlsGetParams = None
        #overrided fucntion that prepare request with inner headers
    def start_requests(self):
        self.params = { 
        'Host':'twitter.com',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language':'en-US,en;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'Upgrade-Insecure-Requests':'1',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0',
        'authority' : 'twitter.com',
        }
        #careful with session auth, may be expired
        self.cookies = {
        'personalization_id':'v1_YHTV7EBksk3kG/Ywvj8gTw==',
        'guest_id':'v1%3A150773123259177115',
        'eu_cn':'1',
        'tfw_exp':'0',
        'lang':'fr',
        'ct0':'f0055d52b075c1ecab6a2cb01ee32357',
        'gt':'921462777285357568',
        '_ga':'GA1.2.2111084724.1507731254',
        '_gid':'GA1.2.2106045753.1508528820',
        '_twitter_sess':'BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCLIDUztfAToMY3NyZl9p%250AZCIlNWQ1ZDBjMDZlN2ViOGY5YzMzOGMxYzlhOThjYTg3MzI6B2lkIiU3ZjI5%250AYjNlOTVkYjJlMWUzOWQ3Y2ZlNzJhNjU2MDU5Nw%253D%253D--7ce3c5c371e0c5d6a5403a6d7292fd1700951f82',
        '__utma':'43838368.2111084724.1507731254.1508532429.1508532429.1',
        '__utmt':'1',
        '__utmb':'43838368.1.10.1508532429',
        '__utmc':'43838368',
        '__utmz':'43838368.1508532429.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'
        }
        return [Request(self.start_urls[0],headers=self.params,cookies=self.cookies)]#default callback will be parse function  

    def __init__(self, profileName, since, until):
        #setting of database name and collection
        
        #init other class properties
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
        #self.tweetAPIGetParams = ['https://twitter.com/i/profiles/show/'+self.profileName+'/timeline/tweets'] OLD
        self.tweetAPIGetParams = ['https://twitter.com/i/search/timeline']
    	self.start_urls = ['https://twitter.com/search?'+urlencode(self.start_urlsGetParams)] 	

    def parse(self, response):
        yield Request(response.url, callback=self.parse_data,dont_filter=True, headers=self.params)
        #search for next iteration (min-position)
        next_position = response.xpath('//*[@id="timeline"]/div/@data-max-position').extract_first().split('-')[1]
        last_position = response.xpath('//*[@id="timeline"]/div/@data-max-position').extract_first().split('-')[2]
        #GET parameters (no headers needed (for the moment))
        self.get_params = {
        'q' : self.query,
        'include_available_features' : '1',
        'include_entities' : '1',
        'max_position' : 'TWEET-'+next_position+'-'+last_position,
        'reset_error_state' : 'false',
        'vertical':'default'
        }

        yield Request(self.tweetAPIGetParams[0]+'?'+urlencode(self.get_params), callback=self.parse_json_tweets,dont_filter=True,cookies=self.API_Cookies,headers=self.params)


    def parse_json_tweets(self, response):
            #convert response
            data = json.loads(response.text)
            selector = Selector(text=data['items_html'], type='html')
            #extract data
            nextPosition = data['min_position'].split('-')
            nextPosition = 'TWEET-'+nextPosition[1] + '-' + nextPosition[2]
            #logging.info('next position to performe ====>  %s old position %s',nextPosition,self.get_params['max_position'])
            if(self.get_params['max_position'] != nextPosition):
                comments_react = self.stats_extractor('reply', selector)
                retweet_react = self.stats_extractor('retweet', selector)
                favorite_react = self.stats_extractor('favorite', selector)
                tweetdates = selector.xpath('.//*[contains(@class,"js-stream-item stream-item stream-item")]/div[1]/div[2]/div[1]/small/a/span[1]/text()').extract()
                #tweets = selector.xpath('.//*[contains(@class,"js-stream-item stream-item stream-item")]/div[1]/div[2]/div[2]/p/text()').extract()
                brut_tweets = selector.xpath('.//*[contains(@class,"js-stream-item stream-item stream-item")]/div[1]/div[2]/div[2]//p').extract()
                for key,value in enumerate(brut_tweets):
                    brut_tweet = Selector(text=value.encode('utf-8'),type='html')
                    current_tweet = ''.join(brut_tweet.xpath('//p//text()').extract())
                    #record data
                    yield {
                     'comment' : comments_react[key],
                     'retweet' : retweet_react[key],
                     'favorite' : favorite_react[key],
                     'teweet' : current_tweet,
                     'tweetDate' : tweetdates[key],
                    }
                #seek for the next position
                self.get_params['max_position'] = nextPosition
                self.keepScroll = data['new_latent_count']
                #call the new API with the nex parameters
                #logging.info('running url ==> %s', self.tweetAPIGetParams[0]+'?'+urlencode(self.get_params))
                #test wether condition returned same index or is not keepScroll
                if(self.keepScroll == 0):
                    return
                yield Request(self.tweetAPIGetParams[0]+'?'+urlencode(self.get_params), callback=self.parse_json_tweets,dont_filter=True,cookies=self.API_Cookies,headers=self.params)

    def parse_data(self, response):
        comments_react = self.stats_extractor('reply', response)
        retweet_react = self.stats_extractor('retweet', response)
        favorite_react = self.stats_extractor('favorite', response)
        tweetdates = response.xpath('.//*[contains(@class,"js-stream-item stream-item stream-item")]/div[1]/div[2]/div[1]/small/a/span[1]/text()').extract()
        brut_tweets = response.xpath('.//*[contains(@class,"js-stream-item stream-item stream-item")]/div[1]/div[2]/div[2]//p').extract()
        for key,value in enumerate(brut_tweets):
            brut_tweet = Selector(text=value.encode('utf-8'),type='html')
            current_tweet = ''.join(brut_tweet.xpath('//p//text()').extract())
            yield {
             'comment' : comments_react[key],
             'retweet' : retweet_react[key],
             'favorite' : favorite_react[key],
             'teweet' : current_tweet,
             'tweetDate' : tweetdates[key],
            }

    def stats_extractor(self, statsString, response):
        #make an enum for that (parameter)
        stats = response.xpath('.//*[contains(@class,"js-stream-item stream-item stream-item")]/'
        +'div[1]/div[2]/div[contains(@class,"stream-item-footer")]/'
        +'div[contains(@class,"ProfileTweet-actionCountList u-hiddenVisually")]/'
        +'span[contains(@class,"ProfileTweet-action--'+ statsString +' u-hiddenVisually")]/span[1]/@data-tweet-stat-count').extract()
        
        return stats

