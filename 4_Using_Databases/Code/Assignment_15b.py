# count the number of messages per domain name of the email address using a database
import sqlite3

conn = sqlite3.connect('Assignment_15b.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Counts')

cur.execute('CREATE TABLE Counts(org TEXT, count INTEGER)')

fpath = 'mbox.txt'
fhand = open(fpath)
for line in fhand:
    if not line.startswith('From: '):
        continue  # skip
    pieces = line.rstrip().split('@')
    domain = pieces[1]
    cur.execute('SELECT count FROM Counts WHERE org=?', (domain,))
    row = cur.fetchone()
    print(domain, row)
    if row is None:
        cur.execute('INSERT INTO Counts(org, count) VALUES(?, 1)', (domain,))
    else:
        cur.execute('UPDATE Counts SET count=count+1 WHERE org=?', (domain,))
    conn.commit()

retrieve_cmd = 'SELECT * FROM Counts ORDER BY count DESC LIMIT 10'
for row in cur.execute(retrieve_cmd):
    print(row[0], row[1])

cur.close()
