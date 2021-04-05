from db import Memory
from parser import Parser
from pprint import pprint
from datetime import datetime
from sql_constant import QUERY_PUT_ADS, QUERY_SELECT_ACTIVE_MONITOR

db = Memory()
monitors = db.select(QUERY_SELECT_ACTIVE_MONITOR)
pprint(monitors)
ads = []
# for item in parser.get_items(city_id, category_id):
#     id = item['id']
#     ad = parser.get_info(id)
#     posted = datetime.fromtimestamp(ad['time'])
#     now = datetime.now()
#     ads.append((id, ad['title'], ad['categoryId'], city_id, ad['seller']['name'], ad['description'], 
#                 ad['images'][0]['1280x960'], ad['seo']['canonicalUrl'], ad['address'], posted, now, True, 
#                 ad['stats']['views']['total'], int(ad['price']['value'].replace(' ', '')), 'avito'))
# db.insert(QUERY_PUT_ADS, ads)
# print("Добавил в базу объявления")

del db