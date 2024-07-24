import sqlite3

db_name = 'knownby_spider_db.sqlite'
conn = sqlite3.connect(db_name)
cur = conn.cursor()

name = 'Aniqa'
cur.execute('''SELECT retrieved, friendlist FROM Link WHERE name = ?''', (name,))

retrieved, friendlist = cur.fetchone()  # fetchone() returns a tuple
print(retrieved)
print(friendlist)
