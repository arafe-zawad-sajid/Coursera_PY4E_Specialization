import sqlite3

# connect to index.sqlite database
db = 'BD_COVID.sqlite'
conn = sqlite3.connect(db)
cur = conn.cursor()

# generate cases
cases = dict()
cur.execute('SELECT date, number FROM coronavirus_cases_linear WHERE number IS NOT NULL')
for row in cur:
    cases[row[0]] = row[1]
print('total cases not null', len(cases))

js = 'BD_cases.js'
fhand = open(js, 'w')  # write permission
fhand.write("gline = [\n['Date', 'Total Cases']")

for date in cases:
    fhand.write(",\n['"+date+"', "+str(cases[date])+"]")
fhand.write('\n];')
fhand.close()

print("\nOutput written to", js)
print("Open BD_cases.htm to visualize the data")

# generate deaths
deaths = dict()
cur.execute('SELECT date, number FROM coronavirus_deaths_linear WHERE number IS NOT NULL')
for row in cur:
    deaths[row[0]] = row[1]
print('total deaths not null', len(deaths))

js = 'BD_deaths.js'
fhand = open(js, 'w')  # write permission
fhand.write("gline = [\n['Date', 'Total Deaths']")

for date in deaths:
    fhand.write(",\n['"+date+"', "+str(deaths[date])+"]")
fhand.write('\n];')
fhand.close()

print("\nOutput written to", js)
print("Open BD_deaths.htm to visualize the data")
