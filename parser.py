import json
import httpx
from time import sleep
from datetime import datetime
from math import floor


class Parser():
    '''Наша рабочая лошадка'''

    def __init__(self, key):
        self.key = key
        self.avito_urls = {
            'region_id': 'https://m.avito.ru/api/1/slocations',
            'categories_id': 'https://m.avito.ru/api/2/search/main',
            'items': 'https://m.avito.ru/api/9/items',
            'avito_link': 'https://avito.ru'
        }

    def get_json_by_request(self, url, params):
        sleep(2)
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
            self.get_json_by_request(url, params)

    def _get_region_id(self, region):
        params = {
            'key':f'{self.key}',
            'q':f'{region}',
            'limit':10
        }
        url = f'{self.avito_urls["region_id"]}'
        json_content = self.get_json_by_request(url, params)
        locations = json_content['result']['locations']

        return locations[0]['id']

    def _get_category_ids(self, location_id):
        params = {
            'key':f'{self.key}',
            'locationId':f'{location_id}'
        }
        url = f'{self.avito_urls["categories_id"]}'
        categories = self.get_json_by_request(url, params)['categories']
        for category in categories:
            [category.pop(key, None) for key in []]
        # print(json_content)
        return json_content

    def get_items(self, region, category_id):
        time = floor(datetime.timestamp(datetime.now().replace(second=0, microsecond=0)))
        location_id = self._get_region_id(region)
        params = {
            'key': f'{self.key}',
            'lastStamp': f'{time}',
            'locationId': f'{location_id}',
            'categoryId': f'{category_id}',
            'page':1,
            'display':'list',
            'limit':5
        }
        url = f'{self.avito_urls["items"]}'
        json_content = self.get_json_by_request(url, params)

        if json_content is None:
            return None

        #print(json_content['result'])

        items = [ res['value'] for res in json_content['result']['items'] if res['type'] != 'snippet']
        for item in items:
            [item.pop(key, None) for key in ['callAction', 'category', 'imageList', 'images', 'geoReferences', 'coords', 'userType', 'hasVideo', 'isVerified', 'contactlessView', 'uri', 'isFavorite']]

        return items

    def search_category(self, category_name, region_id):
        categs = self._get_category_ids(region_id)

        return category

    def __repr__(self):
        return "Parser('%s')" % (self.url)

if __name__ == '__main__':
    #url = 'https://m.avito.ru/api/1/slocations?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&locationId=621540&limit=10&q='
    parser = Parser('af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir')
    #print(parser.get_region_id('Пермь')) #643700
    #print(parser.get_category_ids(643700))
    print(parser.get_items('Пермь', 98))
    #response = parser.get_json_by_request() #, headers=headers, proxies=proxies, timeout=Config.REQUEST_TIMEOUT)

    #print(response)