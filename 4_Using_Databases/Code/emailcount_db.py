import sqlite3

# create/open a database
conn = sqlite3.connect('emailcount_db.sqlite')
cur = conn.cursor()  # like file handle

# drop previous 'Counts' table
cur.execute('DROP TABLE IF EXISTS Counts')

# create new table 'Counts'
cur.execute('CREATE TABLE Counts(email TEXT, count INTEGER)')

fpath = 'mbox-short.txt'
fhand = open(fpath)
for line in fhand:
    if not line.startswith('From: '):
        continue  # skips
    pieces = line.split()
    email = pieces[1]
    # retrieve value of 'count' row for a specific 'email'
    cur.execute('SELECT count FROM Counts WHERE email=?', (email,))
    row = cur.fetchone()  # fetch the value of 'count' row
    #print(email, row)
    if row is None:  # email not found in database
        # insert a new entry with a specific 'email' and 'count' value 1
        cur.execute('INSERT INTO Counts(email, count) VALUES(?, 1)', (email,))
    else:  # email was found in database
        # update previous entry with a specific 'email' and increase 'count' value by 1
        cur.execute('UPDATE Counts SET count=count+1 WHERE email=?', (email,))
    conn.commit()

sqlstr = 'SELECT email, count FROM Counts ORDER BY count DESC LIMIT 10'
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
