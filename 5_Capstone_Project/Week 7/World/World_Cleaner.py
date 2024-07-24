import sqlite3
import xlrd

def fixnumber(num):
    num = num.replace(',', '')
    try:
        num = int(num)
        return num
    except:
        return None

db = 'World_COVID.sqlite'
conn = sqlite3.connect(db)
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Data')
cur.execute('''
    CREATE TABLE Data(
        id INTEGER PRIMARY KEY,
        country TEXT UNIQUE,
        total_cases INTEGER,
        total_deaths INTEGER,
        total_recovered INTEGER,
        active_cases INTEGER
    )
''')

xl = 'World_COVID.xlsx'
wb = xlrd.open_workbook(xl)
ws = wb.sheet_by_index(0)

world_data = dict()
world_cases = dict()
for i in range(ws.nrows):
    if i == 0:
        continue
    row = ws.row_values(i)
    country = row[1]
    cases = fixnumber(row[2])
    deaths = fixnumber(row[4])
    recoveries = fixnumber(row[6])
    actives = fixnumber(row[7])
    world_cases[country] = cases
    world_data[country] = (cases, deaths, recoveries, actives)

countries = sorted(world_cases, key=world_cases.get, reverse=True)
for country in countries:
    cases, deaths, recoveries, actives = world_data[country]
    cur.execute('''INSERT INTO Data(country, total_cases, total_deaths, total_recovered, active_cases)
    VALUES(?, ?, ?, ?, ?)''', (country, cases, deaths, recoveries, actives))
print('Done, total countries', len(world_cases))
conn.commit()
conn.close()
