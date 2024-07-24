import sqlite3  # for databasing
import re  # for regex
import dateutil.parser as dateparser  # for parsing email dates
import zlib  # for compressing

# databases to be used
indexdb = 'index.sqlite'
mappingdb = 'mapping.sqlite'
contentdb = 'content.sqlite'

# global variables
dns_mapping = dict()  # mapping of old dns to new dns
email_mapping = dict()  # mapping of old email to new email

# function: to clean sender, find real sender if gmane.org email, truncate dns, update dns
def fixsender(sender, allsenders=None):
    global dns_mapping
    global email_mapping
    if sender is None:
        return None
    # clean the sender email
    sender = sender.strip().lower()
    sender = sender.replace('<', '').replace('>', '')

    # if we have an email with 'gmane.org' (person did not share email), we find the real one
    # example: arwhyte-63aXycvo3TyHXe+LvDLADg@public.gmane.org
    if allsenders is not None and sender.endswith('gmane.org'):
        pieces = sender.split('-')
        realsender = None
        # check if 'email' in allsender starts with the 1st part of this sender
        for email in allsenders:
            if email.startswith(pieces[0]):
                realsender = sender
                sender = email
                break
        if realsender is None:  # real sender not found
            # check if 'old email' in mapping starts with the 1st part of this sender
            for email in email_mapping:
                if email.startswith(pieces[0]):
                    realsender = sender
                    sender = email_mapping[email]  # updated email
                    break
        if realsender is None:  # real sender still not found
            # takes 1st part of this sender and ignores the rest
            sender = pieces[0]

    # truncate dns portion
    spieces = sender.split('@')
    if len(spieces) != 2:
        return sender  # gmane.org emails without a real sender
    dns = spieces[1]
    dpieces = dns.split('.')
    # truncated to two levels
    if dns.endswith('.com') or dns.endswith('.edu') or dns.endswith('.org') or dns.endswith('.net'):
        dns = '.'.join(dpieces[-2:])
    # truncated to three levels
    else:
        dns = '.'.join(dpieces[-3:])
    # get updated dns from dnsmapping
    dns = dns_mapping.get(dns, dns)
    return spieces[0]+'@'+dns

# function: to parse out the info from email headers
def parseheader(hdr, allsenders=None):
    # if there's nothing in hdr there's nothing to parse
    if hdr is None or len(hdr) < 1:
        return None

    # extract sender email address
    sender = None
    x = re.findall('\nFrom: .* <(\S+@\S+)>\n', hdr)
    if len(x) >= 1:
        sender = x[0]
    else:  # without the angle brackets
        x = re.findall('\nFrom: (\S+@\S+)\n', hdr)
        if len(x) >= 1:
            sender = x[0]
    # fix senders before returning
    sender = fixsender(sender, allsenders)

    # extract the date the email was sent at
    sent_at = None
    x = re.findall('\nDate: .*, (.*)\n', hdr)
    if len(x) >= 1:
        tdate = x[0]
        tdate = tdate[:26]  # take first 26 chars
        try:
            sent_at = dateparser.parse(tdate)
        except Exception as ex:
            print('date parsing failed', tdate)
            return None

    # extract the subject of the email
    subject = None
    x = re.findall('\nSubject: (.*)\n', hdr)
    if len(x) >= 1:
        subject = x[0].strip().lower()

    # extract message-id of the email (a.k.a global unique id = guid)
    guid = None
    x = re.findall('\nMessage-ID: (.*)\n', hdr)
    if len(x) >= 1:
        guid = x[0].strip().lower()

    # if any of the info is None then return None
    if sender is None or sent_at is None or subject is None or guid is None:
        return None
    # else return a tuple with the values
    return (guid, sender, subject, sent_at)


# main driver code
# connect to index.sqlite database
con_index = sqlite3.connect(indexdb)
cur_index = con_index.cursor()
# non-restartable
cur_index.executescript('''
    DROP TABLE IF EXISTS Messages;
    DROP TABLE IF EXISTS Senders;
    DROP TABLE IF EXISTS Subjects;
    DROP TABLE IF EXISTS Replies;
''')

cur_index.executescript('''
    CREATE TABLE Senders(
        id INTEGER PRIMARY KEY,
        sender TEXT UNIQUE
    );
    CREATE TABLE Subjects(
        id INTEGER PRIMARY KEY,
        subject TEXT UNIQUE
    );
    CREATE TABLE Replies(
        from_id INTEGER,
        to_id INTEGER
    );
    CREATE TABLE Messages(
        id INTEGER PRIMARY KEY,
        guid TEXT UNIQUE,
        sent_at INTEGER,
        sender_id INTEGER,
        subject_id INTEGER,
        headers BLOB,
        body BLOB
    );
''')

# connect to mapping.sqlite database
con_mapping = sqlite3.connect(mappingdb)
cur_mapping = con_mapping.cursor()

# populate dns_mapping
cur_mapping.execute('SELECT old, new FROM DNSMapping')
for row in cur_mapping:
    dns_mapping[row[0].strip().lower()] = row[1].strip().lower()

# populate email_mapping
cur_mapping.execute('SELECT old, new FROM Mapping')
for row in cur_mapping:
    # fix senders before populating
    old = fixsender(row[0])
    new = fixsender(row[1])
    email_mapping[old] = new
# done with mapping.sqlite
con_mapping.close()


# connect to content.sqlite database in read only
con_content = sqlite3.connect('file:'+contentdb+'?mode=ro', uri=True)
cur_content = con_content.cursor()

# create allsenders list, populate with unique senders that are not 'gmane.org'
allsenders = list()
cur_content.execute('SELECT email FROM Messages')
for row in cur_content:
    # fix senders and check before populating
    sender = fixsender(row[0])
    if sender is None:
        continue
    if 'gmane.org' in sender:
        continue
    if sender in allsenders:
        continue
    allsenders.append(sender)
print('loaded allsenders', len(allsenders), 'and mapping', len(email_mapping), 'dnsmapping', len(dns_mapping))

# go through content.sqlite to build index.sqlite
senders = dict()
subjects = dict()
guids = dict()
cur_content.execute('SELECT headers, body, sent_at FROM Messages ORDER BY sent_at')
count = 0

for row in cur_content:
    hdr = row[0]
    body = row[1]
    parsed = parseheader(hdr, allsenders)
    if parsed is None:
        continue
    guid, sender, subject, sent_at = parsed

    # get new email address if changed
    sender = email_mapping.get(sender, sender)
    # print first 250 header info
    count = count+1
    if (count % 250) == 1:
        print(count, guid, sender, sent_at)

    # check if sender contains 'gmane.org'
    if 'gmane.org' in sender:
        print('ERROR: gmane.org in sender', sender)

    # try to get the respective id from their respective dictionary
    sender_id = senders.get(sender, None)
    subject_id = subjects.get(subject, None)
    guid_id = guids.get(guid, None)

    # if sender_id not found in senders then it's a new entry
    if sender_id is None:
        cur_index.execute('INSERT OR IGNORE INTO Senders(sender) VALUES(?)', (sender,))
        con_index.commit()
        cur_index.execute('SELECT id FROM Senders WHERE sender=? LIMIT 1', (sender,))
        try:
            row = cur_index.fetchone()
            sender_id = row[0]
            # populate senders
            senders[sender] = sender_id
        except:
            print('ERROR: could not retrieve sender id', sender)
            break

    # if subject_id not found in subjects then it's a new entry
    if subject_id is None:
        cur_index.execute('INSERT OR IGNORE INTO Subjects(subject) VALUES(?)', (subject,))
        con_index.commit()
        cur_index.execute('SELECT id FROM Subjects WHERE subject=? LIMIT 1', (subject,))
        try:
            row = cur_index.fetchone()
            subject_id = row[0]
            subjects[subject] = subject_id
        except:
            print('ERROR: could not retrieve subject id', subject)
            break

    # since guid is unique so guid_id will always be None
    cur_index.execute('''INSERT OR IGNORE INTO Messages(guid, sender_id, subject_id, sent_at, headers, body)
    VALUES(?, ?, ?, datetime(?), ?, ?)''', (guid, sender_id, subject_id, sent_at, zlib.compress(hdr.encode()), zlib.compress(body.encode())))
    con_index.commit()
    cur_index.execute('SELECT id FROM Messages WHERE guid=? LIMIT 1', (guid,))
    try:
        row = cur_index.fetchone()
        guid_id = row[0]
        guids[guid] = guid_id
    except:
        print('ERROR: could not retrieve guid id', guid)
        break
print(len(senders), len(subjects), len(guids))  #
cur_index.close()
cur_content.close()
