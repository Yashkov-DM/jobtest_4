# -*- coding: utf-8 -*-
import pyodbc
import constants

avto_constant = (('SkodaRapid2020', 55, 647), ('VolkswagenPolo2015', 55, 696), ('NissanQashqai2017', 60, 1071),
        ('HyundaiSolaris2018', 50, 562))
verified_avto = []

SERVER = constants.SERVER
DATABASE = constants.DATABASE
USER = constants.USER
PASSWORD = constants.PASSWORD


def found_last_milage(row, avto_constant):
    max_milage = None
    avto = row[0][1]
    avto_milage = row[0][3]
    for item in avto_constant:
        if item[0] == avto:
            max_milage = item[2]
            break
    if max_milage:
        avto_milage_last = avto_milage - max_milage
        return avto_milage_last


def strange_avto(avto, row, avto_constant):
    max_liter = None
    for item in avto_constant:
        if item[0] == avto:
            max_liter = item[1]
            break
    if row > max_liter:
        return True


def chouse_avto():
    for item in avto_constant:
        avto = item[0]
        if avto in verified_avto:
            continue
        else:
            return avto


conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                           "Server="+SERVER+";"
                           "Database="+DATABASE+";"
                           "UID="+USER+";"
                           "PWD="+PASSWORD+";")
cursor = conn.cursor()

while len(verified_avto) < len(avto_constant):
    avto = chouse_avto()
    cursor.execute('SELECT TOP 1 * FROM avtomilage_table WHERE AvtoName = ? ORDER BY TimeCheck DESC', avto)
    row = cursor.fetchall()
    avto = row[0][1]
    avto_data = row[0][2]
    avto_milage = found_last_milage(row, avto_constant)

    cursor.execute('SELECT TOP 1 * FROM avtomilage_table WHERE AvtoName = ? AND MilageCheck > ? '
                   'ORDER BY TimeCheck', (avto, avto_milage))
    row = cursor.fetchall()
    avto_data_last = row[0][2]

    cursor.execute('SELECT SUM(LiterCheck) FROM avtolitr_table WHERE '
                   'AvtoName = ? AND TimeCheck >= ?', (avto, avto_data_last))
    row = cursor.fetchone()
    liter_sum = row[0]

    if strange_avto(avto, liter_sum, avto_constant):
        print(f'Обнаружен перерасход топлива {avto} {liter_sum}')
        verified_avto.append(avto)
    else:
        print(f'Проверено {avto} {liter_sum}')
        verified_avto.append(avto)

conn.close()

