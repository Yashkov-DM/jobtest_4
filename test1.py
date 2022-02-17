# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import datetime
import pyodbc
import constants

SERVER = constants.SERVER
DATABASE = constants.DATABASE
USER = constants.USER
PASSWORD = constants.PASSWORD

conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server="+SERVER+";"
                           "Database="+DATABASE+";"
                           "UID="+USER+";"
                           "PWD="+PASSWORD+";")
cursor = conn.cursor()


def get_weather(city):
    weather_tup = []
    now = datetime.date.today()
    for day in range(40, 48):
        delta = datetime.timedelta(days=day)
        from_day = now - delta
        response = requests.get(f'https://www.meteoservice.ru/archive/{str(city)}'
                                f'/{str(from_day.year)}/{str(from_day.month)}/{str(from_day.day)}')
        html_doc = BeautifulSoup(response.text, features='html.parser')
        list_of_temperature = html_doc.find_all('div', {'class': 'callout'})
        temp_pattern = re.compile(r'Температура воздуха [+]?(-?\d{1,2})…[+]?(-?\d{1,2})°C|Температура воздуха [+]?(-?\d{1,2})°C')
        match_temp = re.findall(temp_pattern, str(list_of_temperature[0]))
        try:
            res = [int(x) for x in match_temp[1] if x]
            res = sum(res)//2 if len(res) > 1 else sum(res)
            weather_tup.append(res)
        except IndexError:
            print('отсутствует значение')
    return tuple(weather_tup)


day_list = ('DayToday', 'Day1DayAgo', 'Day2DayAgo', 'Day3DayAgo', 'Day4DayAgo', 'Day5DayAgo', 'Day6DayAgo')
row = cursor.execute('SELECT CityCodName FROM cityRF4')
city_row = [x[0] for x in row]
for city in city_row:
    print(city)
    weather = get_weather(city)
    res_zip = list(zip(day_list, weather))
    for day, temper in res_zip:
        sql = "UPDATE cityRF4 SET {day}= {temper} WHERE CONVERT(NVARCHAR(MAX), CityCodName)= ?".format(day=day, temper=temper)
        cursor.execute(sql, city)
        conn.commit()

cursor.execute('SELECT * FROM cityRF4')
for row in cursor:
    print(f'температура в {row[1]} сегодня:{row[3]}, вчера:{row[4]}, 2 дня назад:{row[5]}, 3 дня назад:{row[6]},'
          f'4 дня назад:{row[7]}, 6 дней назад:{row[8]}, 7 дней назад:{row[9]},')

conn.close()

