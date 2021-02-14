import json
import httpx
from time import sleep

class Parser():
    '''Наша рабочая лошадка'''

    def __init__(self, key):
        self.key = key
        self.avito_urls = {
            'region_id': f'https://m.avito.ru/api/1/slocations',
            'categories_id': f'https://m.avito.ru/api/2/search/main?&locationId=',
            'avito_link': 'https://avito.ru'
        }

    def get_json_by_request(self, url, params):
        try:
            resp = httpx.get(url, params=params)
            json_content = resp.json()
            if 'status' in json_content.keys():
                if json_content['status'] == 'internal-error':
                    print('internal-error')
                    self.get_json_by_request(url, params)
            return json_content
        except httpx.exceptions.ProxyError:
            sleep(0.001)
            self.get_json_by_request(url,params)

    def get_region_id(self, region):
        params = {
            'key':f'{self.key}',
            'q':f'{region}',
            'limit':10
        }
        url = f'{self.avito_urls["region_id"]}'
        json_content = self.get_json_by_request(url, params)
        locations = json_content['result']['locations']

        return locations[0]['id']

    def get_category_ids(self, location_id):
        sleep(2)
        params = {
            'key':f'{self.key}',
            'locationId':f'{location_id}'
        }
        url = f'{self.avito_urls["categories_id"]}'
        json_content = self.get_json_by_request(url, params)
        locations = json_content['result']['categories']

        return locations[0]['id']

    def __repr__(self):
        return "Parser('%s')" % (self.url)

if __name__ == '__main__':
    #url = 'https://m.avito.ru/api/1/slocations?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&locationId=621540&limit=10&q='
    parser = Parser('af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir')
    print(parser.get_region_id('Пермь'))
    #response = parser.get_json_by_request() #, headers=headers, proxies=proxies, timeout=Config.REQUEST_TIMEOUT)

    #print(response)