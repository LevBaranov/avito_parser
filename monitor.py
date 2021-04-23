import logging
from db import Memory
from parser import Parser
from pprint import pprint
from datetime import datetime
from sql_constant import QUERY_PUT_ADS, QUERY_SELECT_ACTIVE_MONITOR

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.info('Monitoring is active')
while(True):
    db = Memory()
    parser = Parser('af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir')
    monitors = db.select(QUERY_SELECT_ACTIVE_MONITOR)
    # pprint(monitors)
    
    for mon in monitors:
        for i in [1,2,3,4,5,6,7,8,9,10]:
            ads = []
            for item in parser.get_items(mon[0], mon[1], 50, i):
            # for item in parser.get_items(mon[0], mon[1]):
                # pprint(item)
                try:
                    id = item['id']
                    ad = parser.get_info(id)
                    posted = datetime.fromtimestamp(ad['time'])
                    now = datetime.now()
                    price = ''.join([i for i in ad['price']['value'] if i.isdigit()])
                    if len(price) > 0:
                        price = int(price)
                    else:
                        price = 0
                    pprint(ad)
                    db.insert(QUERY_PUT_ADS, (id, ad['title'], ad['categoryId'], mon[0], ad['seller']['name'], ad['description'], 
                                 ad['images'][0]['1280x960'], ad['seo']['canonicalUrl'], ad['address'], posted, now, True, 
                                 ad['stats']['views']['total'], price, 'avito'))
                except Exception as e:
                    logging.exception("Exception occurred")
                # ads.append((id, ad['title'], ad['categoryId'], mon[0], ad['seller']['name'], ad['description'], 
                #             ad['images'][0]['1280x960'], ad['seo']['canonicalUrl'], ad['address'], posted, now, True, 
                #             ad['stats']['views']['total'], price, 'avito'))
            pprint(ads)
            db.insert(QUERY_PUT_ADS, ads)
            print("Добавил в базу объявления")
    del db
