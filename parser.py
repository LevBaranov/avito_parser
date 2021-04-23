import json
import httpx
from logger import MyLogger
from random import randint
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
        sleep(randint(2, 5))
        logger = MyLogger('parser')
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
        except Exception as ex:
            logger.exception(f'Parsing Error')

    def get_region_id(self, region):
        params = {
            'key':f'{self.key}',
            'q':f'{region}',
            'limit':10
        }
        url = f'{self.avito_urls["region_id"]}'
        json_content = self._get_json_by_request(url, params)
        locations = json_content['result']['locations']
        if(len(locations) > 0):
            return {"id" : locations[0]['id'], "name": locations[0]["names"]["1"] }
        else:
            return {"id" : -1, "name": "None" }

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

    def get_items(self, location_id, category_id, limit=5, page=1):
        time = floor(datetime.timestamp(datetime.now().replace(second=0, microsecond=0)))
        if limit > 50:
            limit = 50
        params = {
            'key': f'{self.key}',
            'lastStamp': f'{time}',
            'locationId': f'{location_id}',
            'categoryId': f'{category_id}',
            'page':f'{page}',
            'display':'list',
            'limit':f'{limit}'
        }
        url = f'{self.avito_urls["items"]}'
        json_content = self._get_json_by_request(url, params)

        if json_content is None:
            return None

        #print(json_content['result'])

        items = [ res['value'] for res in json_content['result']['items'] if res['type'] == 'item']
        # C vip что-то пока не ясно как быть
        # for res in json_content['result']['items']:
        #     if res['type'] == 'vip':
        #         for r in res['value']['list']:
        #             # pprint(r)
        #             items.append(r['value'])

        for item in items:
            [item.pop(key, None) for key in ['callAction', 'category', 'imageList', 'images', 'geoReferences', 'coords', 'userType', 'hasVideo', 'isVerified', 'contactlessView', 'uri', 'isFavorite']]

        return items

    def search_category(self, category_name, location_id):
        #location_id = self.get_region_id(region);
        categs = self._get_category_ids(location_id)
        for categ in categs:
            # pprint((categ["name"], compare(categ["name"], category_name)))
            if compare(categ["name"], category_name) >=0.15:
                return {"id": categ["id"], "name": categ["name"]} 
        return -1

    def get_info(self, add_id, debug=False):
        #time = floor(datetime.timestamp(datetime.now().replace(second=0, microsecond=0)))
        # location_id = self.get_region_id(region)
        params = {
            'key': f'{self.key}',
        }
        url = f'{self.avito_urls["info"]}{add_id}'
        json_content = self._get_json_by_request(url, params)
        if debug:
            return json_content
        for key in ['adjustParams', 'advertOptions', 'breadcrumbs', 'coords', 'deliveryC2C', 'firebaseParams', 'geoReferences', 'icebreakers', 'marketplaceRenameBadge', 'needToCheckCreditInfo', 'needToCheckSimilarItems', 'safeDeal', 'shouldShowMapPreview', 'sharing']:
            json_content.pop(key, None)
        return json_content


if __name__ == '__main__':
    #url = 'https://m.avito.ru/api/1/slocations?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&locationId=621540&limit=10&q='
    parser = Parser('af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir')
    # city = input("В каком городе ищем? ")
    # ans_city = parser.get_region_id(city)
    # city_id = ans_city["id"];
    # if city_id > -1:
    #     print("Ищу в:", ans_city["name"])
    #     category = input("Какую категорию мониторим? ")
    #     ans_category = parser.search_category(category, city_id)
    #     category_id = ans_category["id"];
    #     if (category_id > -1):
    #         print("Буду искать по:", ans_category["name"], ans_category["id"])
    #         print("Ищу товары...")
    #         pprint(parser.get_items(city_id, category_id))
    #         monitor = input("То что надо? Запускаю мониторинг? (д/Н) ")
    #         if monitor == 'д' or monitor == 'Д':
    #             print("Запускаю мониторинг")
    #         else:
    #             print("Ну ок. Тогда запусти меня по новой!")
    #     else:
    #         print("Я не смог найти подходящую категорию. Попробуйте указать точнее")
    # else:
    #     print("Я не смог найти подходящий город/регион. Попробуйте указать точнее")
    #print(parser.get_region_id('Пермь')) #643700
    #print(parser.search_category('товар', 'Пермь'))
    pprint(parser.get_items(643700, 84, 5000)) # ноут леново для теста
    # pprint(parser.get_info(2090665858)) #телефон редми
    #response = parser.get_json_by_request() #, headers=headers, proxies=proxies, timeout=Config.REQUEST_TIMEOUT)

    #print(response)
