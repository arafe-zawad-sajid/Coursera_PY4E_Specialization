import sqlite3

db = 'World_COVID.sqlite'
conn = sqlite3.connect(db)
cur = conn.cursor()

cases = dict()
deaths = dict()
recoveries = dict()
actives = dict()
cur.execute('SELECT country, total_cases, total_deaths, total_recovered, active_cases FROM Data')
# -1 indicates NULL
for row in cur:
    if row[1] is None:
        cases[row[0]] = -1
    else:
        cases[row[0]] = row[1]
    if row[2] is None:
        deaths[row[0]] = -1
    else:
        deaths[row[0]] = row[2]
    if row[3] is None:
        recoveries[row[0]] = -1
    else:
        recoveries[row[0]] = row[3]
    if row[4] is None:
        actives[row[0]] = -1
    else:
        actives[row[0]] = row[4]

print('countries affected', len(cases))

n = int(input('How many to dump? '))

print(n, 'countries with most recorded cases')
mostcases = sorted(cases, key=cases.get, reverse=True)
mostcases = mostcases[:n]
for country in mostcases:
    print(country, cases[country])
print()

print(n, 'countries with most recorded deaths')
mostdeaths = sorted(deaths, key=deaths.get, reverse=True)
mostdeaths = mostdeaths[:n]
for country in mostdeaths:
    print(country, deaths[country])
print()

print(n, 'countries with most recorded recoveries')
mostrecoveries = sorted(recoveries, key=recoveries.get, reverse=True)
mostrecoveries = mostrecoveries[:n]
for country in mostrecoveries:
    print(country, recoveries[country])
print()

print(n, 'countries with most recorded active cases')
mostactives = sorted(actives, key=actives.get, reverse=True)
mostactives = mostactives[:n]
for country in mostactives:
    print(country, actives[country])
