import sqlite3

conn = sqlite3.connect('Assignment_15a.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Ages')

cur.execute('CREATE TABLE Ages(name VARCHAR(128), age INTEGER)')

cur.execute('DELETE FROM Ages')

cur.execute("INSERT INTO Ages(name, age) VALUES('Aryian', 35)")
cur.execute("INSERT INTO Ages(name, age) VALUES('Nyree', 38)")
cur.execute("INSERT INTO Ages(name, age) VALUES('Abbie', 38)")
cur.execute("INSERT INTO Ages(name, age) VALUES('Nyomi', 17)")
cur.execute("INSERT INTO Ages(name, age) VALUES('Johnson', 29)")
cur.execute("INSERT INTO Ages(name, age) VALUES('Amey', 13)")
conn.commit()

cur.execute('SELECT hex(name || age) AS X FROM Ages ORDER BY X')
print(cur.fetchone())
