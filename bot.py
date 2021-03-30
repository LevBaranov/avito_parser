from db import Memory
from parser import Parser

command = input("Доступные комнады: и - попробовать искать что-то, р - получить готовые результаты, м - посмотреть списко мониторингов. Введите команду:")

if(command == 'и'):
    parser = Parser('af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir')
    city = input("В каком городе ищем? ")
    ans_city = parser.get_region_id(city)
    city_id = ans_city["id"];
    if city_id > -1:
        print("Ищу в:", ans_city["name"])
        category = input("Какую категорию мониторим? ")
        ans_category = parser.search_category(category, city_id)
        category_id = ans_category["id"];
        if (category_id > -1):
            print("Буду искать по:", ans_category["name"], ans_category["id"])
            print("Ищу товары...")
            pprint(parser.get_items(city_id, category_id))
            monitor = input("То что надо? Запускаю мониторинг? (д/Н) ")
            if monitor == 'д' or monitor == 'Д':
                print("Мониторинг пока не готов")
            else:
                print("Ну ок. Тогда запусти меня по новой!")
        else:
            print("Я не смог найти подходящую категорию. Попробуйте указать точнее")
    else:
        print("Я не смог найти подходящий город/регион. Попробуйте указать точнее")