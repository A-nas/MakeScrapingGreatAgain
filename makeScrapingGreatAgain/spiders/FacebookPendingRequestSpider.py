import scrapy
from scrapy.http import Request
import logging
from scrapy.http import FormRequest
import json


class FacebookpendingrequestspiderSpider(scrapy.Spider):
    name = 'FacebookPendingRequestSpider'
    allowed_domains = ['facebook.com']
    start_urls = ['http://facebook.com/']

    params = None
    cookies = None
    data = None

    def start_requests(self):
        self.params = { 
        'authority':'www.facebook.com',
        'method':'POST',
        'path':'/api/graphql/',
        'scheme':'https',
        'origin':'https://www.facebook.com',
        'sec-fetch-dest':'empty',
        'sec-fetch-mode':'cors',
        'sec-fetch-site:':'same-origin',
        'referer':'https://www.facebook.com/friends',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
        'content-type':'application/x-www-form-urlencoded',
        'Accept':'*/*',
        'Accept-Language':'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'accept-encoding': 'gzip, deflate, br'
        }
        #careful with session auth, may be expired
        self.cookies = {
        'datr':'FodeXdJu6iOTnr_-qX5dvkKc',
        'sb':'IodeXdO2zjSiVe6onpYrrvmI',
        'c_user':'100000946033663',
        'dpr':'1.100000023841858',
        'spin':'r.1002918994_b.trunk_t.1604387633_s.1_v.2_',
        'xs':'31%3AWg8itQHvPhOhbA%3A2%3A1602545394%3A12670%3A6976%3A%3AAcU0MyFulAlAlb4XoRCseVcC0YAIT3qgqtS047WpxjZx', 
        'fr':'20RlVxEc3CUg0oHJo.AWVTdHtRde75b-q9WHDjMScfgcI.BdXoci.6Y.F-M.0.0.BfogoT.AWVJwXVeFOI',
        'wd':'1165x661',
        'presence':'C%7B%22t3%22%3A%5B%7B%22i%22%3A%22u.100013589642648%22%7D%2C%7B%22i%22%3A%22u.100002123225278%22%7D%2C%7B%22i%22%3A%22u.1431583426%22%7D%2C%7B%22i%22%3A%22u.100014284686565%22%7D%2C%7B%22i%22%3A%22u.100001515357200%22%7D%2C%7B%22i%22%3A%22u.100004078822829%22%7D%2C%7B%22i%22%3A%22u.100007372480026%22%7D%2C%7B%22i%22%3A%22u.100009481263870%22%7D%2C%7B%22i%22%3A%22u.100002336901919%22%7D%2C%7B%22i%22%3A%22u.1190418754%22%7D%2C%7B%22i%22%3A%22u.100014817197562%22%7D%2C%7B%22i%22%3A%22u.100056090225976%22%7D%2C%7B%22i%22%3A%22u.100002359090644%22%7D%2C%7B%22i%22%3A%22u.100001442425862%22%7D%2C%7B%22i%22%3A%22u.1183870551%22%7D%2C%7B%22i%22%3A%22u.100006782493370%22%7D%5D%2C%22utc3%22%3A1604548008408%2C%22v%22%3A1%7D'
        }
        #form data to send via POST
        self.data = {
            'av':'100000946033663',
            '__user':'100000946033663',
            '__a':'1',
            '__dyn':'7AzHJ16U9k9wxxt0BwRyaG5UjBWo2nDwAxu13w8CewSwAyU8EW3K1uwJyEiwp8O2S1DwUx60xU8E1J9EtwMw65xOfwwwto88hwKx-8wgolzUO0-E4a3aUS2G2Caw9m8wnolwBgK7qxS18wc61axe3e9xy48aU8od8-UqwsUkxe2GewGwkUtxGm2SUbElxm3y2K2DUjDw-wAw8idG5EaU',
            '__csr':'gRqO2qainVmOQeRAL46uiqGGqXSCFkQJ2xboyZp4hXCml7hEhhIipYy84FUx8Cqld94CrycVliAyVeaQbc65UCiiQiV6SWLiaF9S9yWWtlQ4oEB6O9XIH949qAh7yqUwp_ObHKBpzkFQeBh54xnDGvaJyrUC8yiFCPDGGlepV59ohHyQ4oxVogEAhcKagnu8yaIDzQeykaz-UzyGoyco-bgBrzQdgJ6yVEswLQapXrHKVdxmh7eWO7DLK56SBzkXccy8eopBJ7iGPeh4h9OAUOqK5axWaxa9yx9EuhojNHPaiuaDl7Dx2a4Akyxe329y4QXxOuCGw8qm19Awxyu1yQ2OK4rgG-4psVooAm8ACrQae2eVEij84EkxzyEG33KcKVGoS2Bd2U-UaUpWB79AAK7u7iyAUhV8-4GxN0Ixp5zQzt5DgN6BeV4iaDyahS8y6ay18koUfHxl2oyFEWeDjCK5t11pUV1539A2ueK5AeYw5qbzszzUIxo8-1czbx2262-2OmEG2HG6EabTJ2YIwxiGFoC4pAl0Lwzg14ECui2C5p8Ba18g2xwa-6UO0Ro6S0xo2Qw2v8fe8CzUcU6q4e2m79pFm0EHz89UbQ14mE0Aq940ee3uaBJKEK1R40NxOm88O0d10bi0ayx619gcNa8qe8E0CrUtCAgfE2Rwso2Kw1FubVYzwd602copsb0',
            '__req':'45',
            '__beoa':'0',
            '__pc':'EXP3:comet_pkg',
            'dpr':'1.5',
            '__ccg':'EXCELLENT',
            '__rev':'1002925151',
            '__s':'9x1e1i:u5g0yu:wijdpl',
            '__hsi':'6891481306573093469-0',
            '__comet_req':'1',
            'fb_dtsg':'AQEQ798a_Mr4:AQHlwdg8S2ur',
            'jazoest':'22025',
            '__spin_r':'1002925151',
            '__spin_b':'trunk',
            '__spin_t':'1604548028',
            'fb_api_caller_class':'RelayModern',
            'fb_api_req_friendly_name':'FriendingCometOutgoingRequestsDialogPaginationQuery',
            'variables':'{"count":10,"cursor":"636816498","scale":1.5}',
            'server_timestamps':'true',
            'doc_id':'3032982086830073'
        }

        return [FormRequest(self.start_urls[0],
                            headers=self.params,
                            method='POST',
                            formdata=self.data,
                            cookies=self.cookies)]#default callback will be parse function  


    def __init__(self):
        #overrided
        self.allowed_domains = ['https://twitter.com/']
        self.start_urls = ['https://www.facebook.com/api/graphql/']


    def parse(self, response):
        #logging.DEBUG()
        logging.warning(response.text)
        pass
