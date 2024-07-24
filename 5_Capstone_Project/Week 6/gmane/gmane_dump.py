import sqlite3

conn = sqlite3.connect('content2.sqlite')
cur = conn.cursor()

cur.execute('SELECT id, email, sent_at, subject FROM Messages ORDER BY sent_at')
for row in cur:
    print(row)
print('the end')
