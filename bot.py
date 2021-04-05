from db import Memory
from parser import Parser
from pprint import pprint
from sql_constant import QUERY_INSERT_CATEGORIES, QUERY_PUT_REGIONS, QUERY_PUT_MONITOR

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
        db.insert(QUERY_PUT_REGIONS, [(city_id, ans_city["name"])])
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
                db.insert(QUERY_PUT_MONITOR, [(category_id, city_id)])
                print(f'Добавил мониторинг по параметрам %s %s. Данные начнут появлятся в течении часа.', ans_city["name"], ans_category["name"])
            else:
                print("Ну ок. Тогда запусти меня по новой!")
        else:
            print("Я не смог найти подходящую категорию. Попробуйте указать точнее")
    else:
        print("Я не смог найти подходящий город/регион. Попробуйте указать точнее")
 del db

#ad_id, ad_name, category_id, owner_name, description, img, link, address, date_posted, date_added, status, "views", price, "source"
