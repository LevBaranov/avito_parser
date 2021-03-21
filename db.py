import psycopg2
from psycopg2 import sql
# import httpx
# from time import sleep
# from datetime import datetime
# from math import floor
# from utils import compare
from pprint import pprint


class Memory():
    ''' Класс через который добавляем и обновляем записи в БД '''

    def __init__(self, key):
        conn = psycopg2.connect(dbname='database', user='db_user', 
                        password='mypassword', host='localhost')
        self.cursor = conn.cursor()
    def __repr__(self):
        return "Memory('%s')" % ()

    def put():
        pass

    def insert():
        with conn.cursor() as cursor:
            conn.autocommit = True
            values = [
                ('ALA', 'Almaty', 'Kazakhstan'),
                ('TSE', 'Astana', 'Kazakhstan'),
                ('PDX', 'Portland', 'USA'),
            ]
            insert = sql.SQL('INSERT INTO city (code, name, country_name) VALUES {}').format(
                sql.SQL(',').join(map(sql.Literal, values))
            )
            cursor.execute(insert)

    def update():
        pass

    def select():
        cursor.execute('SELECT * FROM airport LIMIT 10')
        records = cursor.fetchall()
        ...
        cursor.close()
        conn.close()

