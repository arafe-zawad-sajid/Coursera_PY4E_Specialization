# restartable spider: collects the gmane data
import sqlite3  # databasing
from urllib.request import urlopen  # opening url
import ssl  # ignoring SSL certificate errrors
import re  # using regular expressions
import dateutil.parser as dateparser  # parsing a date
import time  # for delay

# connect to content.sqlite database
conn = sqlite3.connect('content.sqlite')
cur = conn.cursor()

# restartable process: create Messages table if not exists
cur.execute('''
    CREATE TABLE IF NOT EXISTS Messages(
        id INTEGER UNIQUE,
        email TEXT,
        sent_at TEXT,
        subject TEXT,
        headers TEXT,
        body TEXT
    )
''')

# pick up where we left off
start = None
cur.execute('SELECT max(id) FROM Messages')
try:
    row = cur.fetchone()
    if row is None:
        start = 0
    else:
        start = row[0]
except:
    start = 0
# sanity check
if start is None:
    start = 0

# ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# the base url
baseurl = 'http://mbox.dr-chuck.net/sakai.devel/'

# ask how many messages to retrieve
many = 0
# some counters
count = 0
fail = 0
while True:
    if many < 1:
        conn.commit()
        sval = input('how many messages: ')
        if len(sval) < 1:
            break
        try:
            many = int(sval)
        except:
            print('Expecting numeric value')
            continue

    # start after max id
    start = start+1
    # sanity check
    cur.execute('SELECT id FROM Messages WHERE id=?', (start,))
    try:
        row = cur.fetchone()
        if row is not None:
            continue  # already retrieved this message so skip
    except:
        row = None
    # till now we are good
    many = many-1

    # make the url to hit for 1 message
    url = baseurl+str(start)+'/'+str(start+1)

    text = 'None'
    # open url with a 30 second timeout, decode the email data
    try:
        doc = urlopen(url, None, 30, context=ctx)
        text = doc.read().decode()
        # check if status code is OK (200)
        if doc.getcode() != 200:
            print('Error Code =', doc.getcode(), url)
            break
    except KeyboardInterrupt:
        print('Program interrupted by user ...')
        break
    except Exception as ex:
        print('Unable to retrieve or parse page', url)
        print('Error', ex, '. fail', fail)
        fail = fail+1
        if fail > 5:
            break
        continue

    # till now we've successfully retrieved the url
    count = count+1
    print(count, start, url, len(text))

    # ignore bad data (does not start with 'From ')
    if not text.startswith('From '):
        print(text)
        print('Bad data. Did not start with "From ". fail', fail)
        fail = fail+1
        if fail > 5:
            break
        continue

    # find the 1st blank line that seperates the headers and the body of the email
    pos = text.find('\n\n')
    if pos > 0:
        hdr = text[:pos]
        body = text[pos+2:]
    else:
        print(text)
        print('Bad data. Could not find blank line between headers and body. fail', fail)
        fail = fail+1
        if fail > 5:
            break
        continue

    # use regex to pull out 1 email address from the headers
    email = None
    x = re.findall('\nFrom: .* <(\S+@\S+)>\n', hdr)
    if len(x) == 1:
        email = x[0]
        # clean up
        email = email.strip().lower()
        email = email.replace('<', '')
    else:
        x = re.findall('\nFrom: (\S+@\S+)\n', hdr)
        if len(x) == 1:
            email = x[0]
            # clean up: strip whitespaces, to lower case, replace '<' with empty
            email = email.strip().lower()
            email = email.replace('<', '')

    # use regex to pull out 1 date from the headers
    date = None
    y = re.findall('\nDate: .*, (.*)\n', hdr)
    if len(x) == 1:
        tdate = y[0]
        # clean up: chop at 26th char
        tdate = tdate[:26]
        # standardize the date by parsing the date
        try:
            sent_at = dateparser.parse(tdate)
        except:
            print(text)
            print('Date parsing failed:', tdate, '. fail', fail)
            fail = fail+1
            if fail > 5:
                break
            continue

    # use regex to pull out 1 subject from the headers
    subject = None
    z = re.findall('\nSubject: (.*)\n', hdr)
    if len(x) == 1:
        subject = z[0]
        # clean up: strip whitespaces, to lower case
        subject = subject.strip().lower()

    # till now we have everything we wanted, reset the fail counter
    fail = 0
    print(' ', email, sent_at, subject)
    # insert the data in Messages table
    cur.execute('''INSERT OR IGNORE INTO Messages(id, email, sent_at, subject, headers, body)
    VALUES(?, ?, ?, ?, ?, ?)''', (start, email, sent_at, subject, hdr, body))

    # commit every 50th time
    if count % 50 == 0:
        conn.commit()
    # delay for 1 second every 100th time
    if count % 100 == 0:
        time.sleep(1)

conn.commit()
cur.close()
