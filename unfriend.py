import csv
import requests
from configparser import ConfigParser
import json

config = ConfigParser(interpolation=None)
config.read('masterData.ini')
configSection = config['FACEBOOK']

header = json.loads(configSection['Headers'])
cookies = json.loads(configSection['Cookies'])
datas = json.loads(configSection['Datas'])
datas.update({'doc_id':'3226051994092510'}) #important (type of request)

with open('out.csv',newline='',encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(spamreader)
    for row in spamreader:
        datas.update({'variables':'{"input":{"cancelled_friend_requestee_id":"'+row[0]+'","source":"manage_outgoing_requests","actor_id":"100000946033663","client_mutation_id":"4"},"scale":1.5}'})
        response = requests.post('https://www.facebook.com/api/graphql/',headers=header,data=datas,cookies=cookies)
        print(response.url + '  ' + str(response.status_code) )
        #print(', '.join(row))
