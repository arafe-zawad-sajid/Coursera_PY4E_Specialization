import sqlite3

db = 'BD_COVID.sqlite'
conn = sqlite3.connect(db)
cur = conn.cursor()

cases = dict()
cur.execute('SELECT date, number FROM graph_cases_daily WHERE number IS NOT NULL')
for row in cur:
    cases[row[0]] = row[1]

deaths = dict()
cur.execute('SELECT date, number FROM graph_deaths_daily WHERE number IS NOT NULL')
for row in cur:
    deaths[row[0]] = row[1]

print('cases not null', len(cases), ', deaths not null', len(deaths))

many = int(input('How many to dump? '))

print(many, 'dates with the highest cases')

x = sorted(cases, key=cases.get, reverse=True)
for k in x[:many]:
    print(k, cases[k])
print()
print(many, 'dates with the highest deaths')

x = sorted(deaths, key=deaths.get, reverse=True)
for k in x[:many]:
    print(k, deaths[k])
