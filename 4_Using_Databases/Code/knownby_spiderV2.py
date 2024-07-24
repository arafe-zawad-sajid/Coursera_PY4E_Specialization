from urllib.request import urlopen  # for opening url
import ssl  # for ignoring ssl certificates
from bs4 import BeautifulSoup  # for parsing html
import sqlite3  # for databasing

# prepare the database
db_name = 'knownby_spiderV2.sqlite'
# create new or use existing database and connect to it
conn = sqlite3.connect(db_name)
# create cursor for the above database to perform actions via the cursor on the database
cur = conn.cursor()
# restartable process: tables will not refresh everytime program runs
cur.executescript('''
    CREATE TABLE IF NOT EXISTS People(
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE,
        retrieved INTEGER
    );
    CREATE TABLE IF NOT EXISTS Follows(
        from_id INTEGER,
        to_id,
        UNIQUE(from_id, to_id)
    );
''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# using this url to get an account's friendlist
main_url = 'http://py4e-data.dr-chuck.net/known_by_'  # start with Fikret

friendscount = 10  # limit the number of friends to retrieve from an account
while True:
    # enters an account name, or is picked in random, or quit program
    account_name = input("Enter an account name or, enter 'r' to choose randomly or, enter 'q' to quit:\n")
    if account_name == 'q':  # quit
        print('Program stopped by user.')
        break
    if account_name == 'r':  # select random 'id' and 'name'
        # try to check if any unretrieved entry exists
        cur.execute('SELECT id, name FROM People WHERE retrieved = 0 LIMIT 1')
        try:
            (account_id, account_name) = cur.fetchone()  # works if any unretrieved account is found, account's 'id' and 'name' fetched
            print(str(account_id) + ', ' + account_name + ' picked randomly from database.')
        except:
            print('No unretrieved account found.')
            continue
    else:  # use entered account 'name'
        # try to check if account 'name' already exists
        cur.execute('SELECT id FROM People WHERE name = ? LIMIT 1', (account_name,))
        try:
            account_id = cur.fetchone()[0]  # works if account 'name' already exists, 'id' will be fetched
            print(str(account_id) + ', ' + account_name + ' already exists in database.')
        except:  # if account 'name' doesn't exist, insert it
            cur.execute('INSERT OR IGNORE INTO People(name, retrieved) VALUES(?, 0)', (account_name,))  # insert account 'name' since it doesn't exist
            conn.commit()  # save changes
            # check if row was inserted correctly, 1 means ok
            if cur.rowcount != 1:   # error when inserting
                print('Error inserting account:', account_name)
                continue
            account_id = cur.lastrowid
            print(str(account_id) + ', ' + account_name + ' inserted now.')

    link = main_url + account_name + '.html'
    # try to check if url works
    try:
        uhand = urlopen(link, context=ctx)
    except Exception as err:  # if url doesn't work
        print('Error:', err)
        break

    data = uhand.read().decode()
    # print limit from header
    headers = dict(uhand.getheaders())
    print(headers['Set-Cookie'].split(';')[1].lstrip())

    # try to parse the html
    try:
        soup = BeautifulSoup(data, 'html.parser')
    except:  # if html has syntax error
        print('Unable to parse HTML')
        print(data)
        break

    # check if 'a' tag is in soup
    if not soup.find('a'):  # if 'a' tag not in soup
        print('Incorrect HTML received, no links.')
        continue

    # generating a list of names of account's friends
    tags = soup('a')
    users = [tag.text for tag in tags[:friendscount]]

    # update retrieved of account to 1
    cur.execute('UPDATE People SET retrieved = 1 WHERE name = ?', (account_name,))
    print('Retrieving friends of', account_name)

    countnew = 0
    countold = 0
    for user in users:
        friend_name = user
        print(friend_name)

        # try to check if friend already exists
        cur.execute('SELECT id FROM People WHERE name = ? LIMIT 1', (friend_name,))
        try:
            friend_id = cur.fetchone()[0]  # works if friend's 'name' already exists, friend's 'id' will be fetched
            countold += 1
        except:
            cur.execute('INSERT OR IGNORE INTO People(name, retrieved) VALUES(?, 0)', (friend_name,))  # insert friend's 'name' since it doesn't exist
            conn.commit()
            if cur.rowcount !=1:
                print('Error inserting friend:', friend_name)
                continue
            friend_id = cur.lastrowid
            countnew += 1

        cur.execute('INSERT OR IGNORE INTO Follows(from_id, to_id) VALUES(?, ?)', (account_id, friend_id))
    print('New accounts=', countnew, ' revisited=', countold)
    conn.commit()

cur.close()
conn.close()
