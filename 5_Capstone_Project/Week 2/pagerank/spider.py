from urllib.request import urlopen  # to open a url
from urllib.parse import urlparse  # to parse a url
from urllib.parse import urljoin  # to join a url
import ssl  # to ignore SSL certificate errors
from bs4 import BeautifulSoup  # to parse html
import sqlite3  # to connect to the database

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# connect with database
conn = sqlite3.connect('spider1.sqlite')
cur = conn.cursor()
# restartable process
cur.executescript('''
    CREATE TABLE IF NOT EXISTS Pages(
        id INTEGER PRIMARY KEY,
        url TEXT UNIQUE,
        html TEXT,
        error INTEGER,
        old_rank REAL,
        new_rank REAL
    );

    CREATE TABLE IF NOT EXISTS Links(
        from_id INTEGER,
        to_id INTEGER,
        UNIQUE(from_id, to_id)
    );

    CREATE TABLE IF NOT EXISTS Websites(
        url TEXT UNIQUE
    );
''')
# check to see if we have any unretrieved urls
cur.execute('SELECT id, url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
row = cur.fetchone()
if row is not None:  # if cursor returns something then we have unretrieved links
    print("Restarting existing crawl. Remove 'spider.sqlite' to start a fresh crawl.")
else:  # otherwise we do not have any unretrieved links, start a new crawl
    starturl = input("Enter a web url to crawl or, 'd' for default, or 'q' to quit program:\n")
    if starturl == 'q':  # quit
        print('Quitting Program.')
        quit()
    elif starturl == 'd':  # default link
        starturl = 'http://www.dr-chuck.com/'
        exit = input('Crawling:'+starturl+".Enter 'y' to continue or 'n' to quit program: ")
        if exit == 'n':
            print('Quitting Program.')
            quit()
    # chop off extensions
    if starturl.endswith('/'):
        starturl = starturl[:-1]
    web = starturl
    if starturl.endswith('.htm') or starturl.endswith('.html'):
        pos = starturl.rfind('/')
        web = starturl[:pos]
    # insert to db
    if len(web) > 1:
        cur.execute('INSERT OR IGNORE INTO Websites(url) values(?)', (web,))
        cur.execute('INSERT OR IGNORE INTO Pages(url, html, new_rank) VALUES(?, NULL, 1.0)', (starturl,))
        conn.commit()

# get the current urls from Websites table
cur.execute('SELECT url FROM Websites')
webs = list()
for row in cur:
    webs.append(str(row[0]))
print(webs)  # show the websites that will be crawled

many = 0
while True:
    if many < 1:
        sval = input('How many pages: ')
        if len(sval) < 1:  # on enter key
            break
        many = int(sval)
    many -= 1
    print('many:', many)
    # select an unretrieved page to crawl
    cur.execute('SELECT id, url FROM Pages WHERE html is NULL and error is NULL ORDER BY RANDOM() LIMIT 1')
    try:
        row = cur.fetchone()
        fromid = row[0]
        url = row[1]
    except:
        print('No unretrieved HTML pages remaining')
        many = 0
        break
    print(fromid, url, end=' ')

    # if we are just retrieving this page then there shouldn't be any links from it
    cur.execute('DELETE FROM Links WHERE from_id=?', (fromid,))
    # retrieve this page
    try:
        doc = urlopen(url, context=ctx)
        html = doc.read()
        # check if error code is OK (200)
        if doc.getcode() != 200:
            print('Error on page:', doc.getcode())
            cur.execute('UPDATE SET error=? WHERE url=?', (doc.getcode(), url))
        # check if content type is text/html
        if doc.info().get_content_type() != 'text/html':
            print('Not text/html page:', doc.info().get_content_type())
            cur.execute('DELETE FROM Pages WHERE url=?', (url,))
            conn.commit()
            continue
        print('('+str(len(html))+')', end=' ')
        # parse the html
        soup = BeautifulSoup(html, 'html.parser')
    except KeyboardInterrupt:  # if user wants to quit while programming is running
        print('\nProgram interrrupted by user...')
        break
    except:
        print('Unable to retrieve or parse page')
        cur.execute('UPDATE Pages SET error=-1 WHERE url=?', (url,))
        conn.commit()
        continue
    # update the url's html in db
    cur.execute('INSERT OR IGNORE INTO Pages(url, html, new_rank) VALUES(?, NULL, 1.0)', (url,))
    cur.execute('UPDATE Pages SET html=? WHERE url=?', (memoryview(html), url))
    conn.commit()

    # retrieve all the anchor tags in that html
    tags = soup('a')
    count = 0
    for tag in tags:
        href = tag.get('href', None)
        if href is None:
            continue
        # resolve relative references like href="/contact"
        up = urlparse(href)
        if len(up.scheme) < 1:
            href = urljoin(url, href)
        # chop off some parts
        ipos = href.find('#')
        if ipos > 1:
            href = href[:ipos]
        if href.endswith('.png') or href.endswith('.jpg') or href.endswith('gif'):
            continue
        if href.endswith('/'):
            href = href[:-1]
        if len(href) < 1:
            continue

        # check if this url is in any of the Websites
        found = False
        for web in webs:
            if href.startswith(web):
                found = True
                break
        if not found:
            continue

        # insert the url found in the anchor tag (href) in Pages table in db
        cur.execute('INSERT OR IGNORE INTO Pages(url, html, new_rank) VALUES(?, NULL, 1.0)', (href,))
        count += 1
        conn.commit()
        # retrieve it's id
        cur.execute('SELECT id FROM Pages WHERE url=? LIMIT 1', (href,))
        try:
            row = cur.fetchone()
            toid = row[0]
        except:
            print('Could not retrieve id')
            continue
        # insert from_id and to_id in the Links table
        cur.execute('INSERT OR IGNORE INTO Links(from_id, to_id) VALUES(?, ?)', (fromid, toid))

    print(count, 'of', len(tags))

cur.close()
