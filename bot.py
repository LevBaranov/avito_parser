import shutil
from openpyxl import Workbook
from db import Memory
from parser import Parser
from pprint import pprint
from datetime import datetime
from sql_constant import QUERY_INSERT_CATEGORIES, QUERY_PUT_REGIONS, QUERY_PUT_MONITOR, \
                         QUERY_SELECT_NAME_ACTIVE_MONITOR, QUERY_SELECT_RESULTS_MONITOR

print("Доступные комнады: и - попробовать искать что-то, р - получить готовые результаты, м - посмотреть список мониторингов.")
command = input("Введите команду:")
db = Memory()

if(command == 'и'):
    parser = Parser('af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir')
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
                print(f'Добавил мониторинг по параметрам {ans_city["name"]}, {ans_category["name"]}. Данные начнут появлятся в течении часа.')
            else:
                print("Ну ок. Тогда запусти меня по новой!")
        else:
            print("Я не смог найти подходящую категорию. Попробуйте указать точнее")
    else:
        print("Я не смог найти подходящий город/регион. Попробуйте указать точнее")
    
if(command == 'м'):
    mon_list = db.select(QUERY_SELECT_NAME_ACTIVE_MONITOR)
    pprint(mon_list)

if(command == 'р'):
    mon_list = db.select(QUERY_SELECT_NAME_ACTIVE_MONITOR)
    pprint(mon_list)
    id = input("Введите id мониторинга по которому нужны результаты:")
    res = db.select_val(QUERY_SELECT_RESULTS_MONITOR, [id])
    wb = Workbook()
    sheet = wb.create_sheet(title = 'Результаты', index = 0)
    sheet.append(['ID объявления', 'Категория', 'Регион', 'Название', 'Автор', 
                'Описание', 'Картинка', 'Ссылка', 'Адресс', 'Дата парсинга', 
                'Дата создания', 'Дата обновления', 'Просмотры', 'Цена'])
    for item in res:
        sheet.append(list(item))
    file_name = datetime.now().strftime("%Y%m%d%H%M%S")+'.xlsx'
    wb.save(file_name)
    shutil.move(file_name, '/var/logs/results/'+file_name)
    print(f'Я скачал файл {file_name} в /var/logs/results/')
del db
#ad_id, ad_name, category_id, owner_name, description, img, link, address, date_posted, date_added, status, "views", price, "source"
