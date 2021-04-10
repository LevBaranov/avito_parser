import os
import psycopg2
from datetime import datetime
from psycopg2 import sql
from pprint import pprint
from sql_constant import QUERY_INSERT_ADS, QUERY_INSERT_CATEGORIES, QUERY_PUT_ADS


class Memory():
    ''' Класс через который добавляем и обновляем записи в БД '''

    def __init__(self):
        POSTGRES_DB = os.getenv('POSTGRES_DB')
        POSTGRES_USER = os.getenv('POSTGRES_USER')
        POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
        self.conn = psycopg2.connect(dbname=POSTGRES_DB, user=POSTGRES_USER, 
                        password=POSTGRES_PASSWORD, host='db')
        self.conn.autocommit = True
    def __repr__(self):
        return "Memory('%s')" % ()
    def __del__(self):
        self.conn.close()       

    def put():
        pass

    def insert(self, query, values):
        with self.conn.cursor() as cursor:
            insert = sql.SQL(query).format(
                sql.SQL(',').join(map(sql.Literal, values))
            )
            cursor.execute(insert)

    def update(self, query, values):
        with self.conn.cursor() as cursor:
            self.conn.autocommit = True
            insert = sql.SQL(query).format(
                sql.SQL(',').join(map(sql.Literal, values))
            )
            cursor.execute(insert)

    def select(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        return records

    def select_val(self, query, values):
        cursor = self.conn.cursor()
        cursor.execute(query, values)
        records = cursor.fetchall()
        return records

if __name__ == '__main__':
    
    mem = Memory()
    # mem.select('select * from pg_catalog.pg_user')
    now = datetime.now()
    values = [       
        (2058464898, 'Lenovo yoga 11s или обменяю на xiaomi redmi note 7', 98, 'Алексей', 'Lenovo yoga 11s или обменяю на\xa0xiaomi redmi note', 
        'https://63.img.avito.st/image/1/Lk18EbaygqRKpgCpLG1_Q4CygqLcsIA', 
        'https://www.avito.ru/perm/noutbuki/lenovo_yoga_11s_ili_obmenyayu_na_xiaomi_redmi_note_7_2058464898',
        'Пермский край, Пермь, 1-я Красноармейская ул.',
        '12/12/2020 12:12:12',
        now,
        True,
        980,
        13500,
        'avito')]
    categs = [
    (98, 'Ноутбуки'),
    (84, 'Телефоны')
    ]

    # mem.insert(QUERY_INSERT_CATEGORIES, categs)
    # mem.insert(QUERY_PUT_ADS, values)
    values = [(2058464898, 'Lenovo yoga 11s или обменяю на xiaomi redmi note 7', 98, 'Алексей', 'Lenovo yoga 11s или обменяю на\xa0xiaomi redmi note', 
        'https://63.img.avito.st/image/1/Lk18EbaygqRKpgCpLG1_Q4CygqLcsIA', 
        'https://www.avito.ru/perm/noutbuki/lenovo_yoga_11s_ili_obmenyayu_na_xiaomi_redmi_note_7_2058464898',
        'Пермский край, Пермь, 1-я Красноармейская ул.',
        '12/12/2020 12:12:12',
        now,
        True,
        1980,
        12500,
        'avito'),
        (2090665858, 'Redmi 9C 3/64gb NFC Ростест 5000 mAh Новые', 84, 'ХОЧУ Пылесос', 'Redmi 9C 3/64gb NFC Ростест 5000 mAh Новые:', 
        'https://81.img.avito.st/image/1/wKqRb7aybEOn2O5OnSiv_WjMbEUxzm4', 
        'https://www.avito.ru/perm/telefony/redmi_9c_364gb_nfc_rostest_5000_mah_novye_2090665858',
        'Пермский край, Пермь, ул. Василия Татищева, 6',
        '12/12/2020 12:12:12',
        now,
        True,
        740,
        9500,
        'avito'
        )]
    mem.insert(QUERY_PUT_ADS, values)
    del mem