from urllib.request import urlopen
import ssl
from bs4 import BeautifulSoup
import sqlite3

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

sample_url = 'http://py4e-data.dr-chuck.net/known_by_'  # Fikret

db_name = 'knownby_spider_db.sqlite'
conn = sqlite3.connect(db_name)
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS Link(name TEXT, retrieved BOOLEAN, friendcount INTEGER, friendlist TEXT)')

while True:
    name = input("Enter a name in Link or, enter 'r' to choose randomly or, enter 'q' to quit: ")
    if name == 'q':
        break
    elif name == 'r':  # select unretrieved Link
        cur.execute('SELECT name, friendlist FROM Link WHERE retrieved = 0 LIMIT 1')
        try:
            name, friendlist = cur.fetchone()  # fetchone() returns a tuple
            retrieved = 0
            newname = False
            print(name, 'picked randomly')
        except:
            print('No unretrieved Link found')
            continue
    else:  # entered name
        cur.execute('SELECT retrieved, friendlist FROM Link WHERE name = ?', (name,))
        try:  # name exists in database
            retrieved, friendlist = cur.fetchone()
            print(name, "exists in the database")
            newname = False
        except:  # new name
            print(name, "doesn't exist in the database, inserting new row")
            retrieved = 0
            friendlist = ''
            newname = True

    if retrieved == 1:
        print(name + "'s friends have already been retrieved")
        continue
    elif retrieved == 0:  # unretrieved till now
        print(name + "'s friends are being retrieved")

    # newly retrieved name
    link = sample_url + name + '.html'
    uhand = urlopen(link, context=ctx)

    soup = BeautifulSoup(uhand, 'html.parser')
    tags = soup('a')
    users = [tag.text for tag in tags[:5]]  # friends of name

    if newname:
        friendlist = ', '.join(users)
        cur.execute('INSERT INTO Link(name, retrieved, friendcount, friendlist) VALUES(?, 1, 5, ?)', (name, friendlist))
    elif not newname:
        friendlist = friendlist + ', ' + ', '.join(users)
        cur.execute('UPDATE Link SET retrieved = 1, friendcount = friendcount+5, friendlist = ? WHERE name = ?', (friendlist, name))

    countnew = 0
    countold = 0
    for user in users:
        friend = user
        print(friend)
        cur.execute('SELECT friendcount, friendlist FROM Link WHERE name = ? LIMIT 1', (friend,))
        try:  # friend already in database
            friendcount, friendlist = cur.fetchone()
            friendlist = friendlist + ', ' + name
            cur.execute('UPDATE Link SET friendcount = ?, friendlist = ? WHERE name = ?', (friendcount+1, friendlist, friend))  # bug
            countold += 1
        except:  # friend not in database
            cur.execute('INSERT INTO Link(name, retrieved, friendcount, friendlist) VALUES(?, 0, 1, ?)', (friend, name))
            countnew += 1
    print('New accounts=', countnew, ' revisited=', countold)
    conn.commit()
cur.close()
