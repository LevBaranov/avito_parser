import json
import httpx
from time import sleep
from datetime import datetime
from math import floor
from utils import compare
from pprint import pprint

class Parser():
    '''Наша рабочая лошадка'''

    def __init__(self, key):
        self.key = key
        self.avito_urls = {
            'region_id': 'https://m.avito.ru/api/1/slocations',
            'categories_id': 'https://m.avito.ru/api/2/search/main',
            'items': 'https://m.avito.ru/api/9/items',
            'info': 'https://m.avito.ru/api/14/items/',
            'avito_link': 'https://avito.ru'
        }

    def __repr__(self):
        return "Parser('%s')" % (self.key)
    
    def _get_json_by_request(self, url, params):
        sleep(2)
        try:
            resp = httpx.get(url, params=params)
            json_content = resp.json()
            if 'status' in json_content.keys():
                if json_content['status'] == 'internal-error':
                    print('internal-error')
                    self._get_json_by_request(url, params)
            return json_content
        except httpx.exceptions.ProxyError:
            sleep(0.001)
            self._get_json_by_request(url, params)

    def get_region_id(self, region):
        params = {
            'key':f'{self.key}',
            'q':f'{region}',
            'limit':10
        }
        url = f'{self.avito_urls["region_id"]}'
        json_content = self._get_json_by_request(url, params)
        locations = json_content['result']['locations']

        return locations[0]['id']

    def _get_category_ids(self, location_id):
        params = {
            'key':f'{self.key}',
            'locationId':f'{location_id}'
        }
        url = f'{self.avito_urls["categories_id"]}'
        categories = self._get_json_by_request(url, params)['categories']
        results = []
        for category in categories:
            if 'children' in category.keys():
                for child in category['children']:
                    if 'id' in child.keys():
                        results.append({'id':child['id'], 'name': child['name']})
            results.append({'id':category['id'], 'name': category['name']})
        #print(json_content)
        return results

    def get_items(self, location_id, category_id):
        time = floor(datetime.timestamp(datetime.now().replace(second=0, microsecond=0)))
        # location_id = self.get_region_id(region)
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
        json_content = self._get_json_by_request(url, params)

        if json_content is None:
            return None

        #print(json_content['result'])

        items = [ res['value'] for res in json_content['result']['items'] if res['type'] != 'snippet']
        for item in items:
            [item.pop(key, None) for key in ['callAction', 'category', 'imageList', 'images', 'geoReferences', 'coords', 'userType', 'hasVideo', 'isVerified', 'contactlessView', 'uri', 'isFavorite']]

        return items

    def search_category(self, category_name, location_id):
        #location_id = self.get_region_id(region);
        categs = self._get_category_ids(location_id)
        for categ in categs:
            # pprint((categ["name"], compare(categ["name"], category_name)))
            if compare(categ["name"], category_name) >=0.15:
                return categ["id"] 
        return -1

    def get_info(self, add_id):
        #time = floor(datetime.timestamp(datetime.now().replace(second=0, microsecond=0)))
        # location_id = self.get_region_id(region)
        params = {
            'key': f'{self.key}',
        }
        url = f'{self.avito_urls["info"]}{add_id}'
        json_content = self._get_json_by_request(url, params)
        for key in ['adjustParams', 'advertOptions', 'breadcrumbs', 'coords', 'deliveryC2C', 'firebaseParams', 'geoReferences', 'icebreakers', 'marketplaceRenameBadge', 'needToCheckCreditInfo', 'needToCheckSimilarItems', 'safeDeal', 'seo', 'shouldShowMapPreview', 'sharing']:
            json_content.pop(key, None)
        return json_content


if __name__ == '__main__':
    #url = 'https://m.avito.ru/api/1/slocations?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&locationId=621540&limit=10&q='
    parser = Parser('af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir')
    # city = input("В каком городе ищем? ")
    # city_id = parser.get_region_id(city)
    # print("Указан город: ", city)
    # category = input("Какую категорию мониторим? ")
    # category_id = parser.search_category(category, city_id)
    # if (category_id > -1):
    #     print("Буду искать по: ", category)
    #     print("Ищу товары...")
    #     pprint(parser.get_items(city_id, category_id))
    # else:
    #     print("Я не смог найти подходящую категорию. Попробуйте указать точнее")
    #print(parser.get_region_id('Пермь')) #643700
    #print(parser.search_category('товар', 'Пермь'))
    #print(parser.get_items('Пермь', 98))
    pprint(parser.get_info(2058464898))
    #response = parser.get_json_by_request() #, headers=headers, proxies=proxies, timeout=Config.REQUEST_TIMEOUT)

    #print(response)