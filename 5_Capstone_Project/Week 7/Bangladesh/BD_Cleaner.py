import sqlite3
import xlrd

def fixdate(date):
    pieces = date.split(' ')
    month = pieces[0]
    day = pieces[1]
    year = '2020'
    months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    return year+'-'+months[month]+'-'+day

def fixnumber(number):
    if number == 'null':
        return None
    else:
        return number

db = 'BD_COVID.sqlite'
conn = sqlite3.connect(db)
cur = conn.cursor()

xl = 'BD_COVID.xlsx'
wb = xlrd.open_workbook(xl)

sheets = wb.sheet_names()
for sheet in sheets:
    ws = wb.sheet_by_name(sheet)
    table = sheet.replace('-', '_')
    cur.execute('DROP TABLE IF EXISTS '+table)
    cur.execute('CREATE TABLE '+table+'(id INTEGER PRIMARY KEY, date TEXT UNIQUE, number INTEGER)')
    print('sheet:', sheet)
    for i in range(ws.nrows):
        if i == 0:
            continue
        row = ws.row_values(i)
        date = fixdate(row[0])
        number = fixnumber(row[1])
        cur.execute('INSERT INTO '+table+'(date, number) VALUES(?, ?)', (date, number))
    conn.commit()
    print()
conn.close()
