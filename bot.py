from db import Memory
from parser import Parser
from pprint import pprint
from datetime import datetime
from sql_constant import QUERY_INSERT_ADS, QUERY_INSERT_CATEGORIES, QUERY_PUT_ADS, QUERY_INSERT_REGIONS

print("Доступные комнады: и - попробовать искать что-то, р - получить готовые результаты, м - посмотреть списко мониторингов.")
command = input("Введите команду:")

if(command == 'и'):
    parser = Parser('af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir')
    db = Memory()
    city = input("В каком городе ищем? ")
    ans_city = parser.get_region_id(city)
    city_id = ans_city["id"];
    if city_id > -1:
        print("Ищу в:", ans_city["name"])
        db.insert(QUERY_INSERT_REGIONS, [(city_id, ans_city["name"])])
        category = input("Какую категорию мониторим? ")
        ans_category = parser.search_category(category, city_id)
        category_id = ans_category["id"];
        if (category_id > -1):
            print("Буду искать по:", ans_category["name"], ans_category["id"])
            categs = [(ans_category["id"], ans_category["name"])]
            db.insert(QUERY_INSERT_CATEGORIES, categs)
            print("Ищу товары...")
            pprint(parser.get_items(city_id, category_id))
            monitor = input("То что надо? Запускаю мониторинг? (д/Н) ")
            if monitor == 'д' or monitor == 'Д':
                print("Мониторинг пока не готов")
                ads = []
                for item in parser.get_items(city_id, category_id):
                    id = item['id']
                    ad = parser.get_info(id)
                    posted = datetime.fromtimestamp(ad['time'])
                    now = datetime.now()
                    ads.append((id, ad['title'], ad['categoryId'], ad['seller']['name'], ad['description'], 
                                ad['images'][0]['1280x960'], ad['seo']['canonicalUrl'], ad['address'], posted, now, True, 
                                ad['stats']['views']['total'], int(ad['price']['value'].replace(' ', '')), 'avito'))
                db.insert(QUERY_PUT_ADS, ads)
                print("Добавил в базу объявления")
            else:
                print("Ну ок. Тогда запусти меня по новой!")
        else:
            print("Я не смог найти подходящую категорию. Попробуйте указать точнее")
    else:
        print("Я не смог найти подходящий город/регион. Попробуйте указать точнее")


#ad_id, ad_name, category_id, owner_name, description, img, link, address, date_posted, date_added, status, "views", price, "source"
