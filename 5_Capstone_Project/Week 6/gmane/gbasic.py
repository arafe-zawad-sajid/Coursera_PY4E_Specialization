import sqlite3  # for databasing

# connect to index.sqlite
indexdb = 'index.sqlite'
conn = sqlite3.connect(indexdb)
cur = conn.cursor()

# mapping of sender_id to sender
senders = dict()
cur.execute('SELECT id, sender FROM Senders')
for row in cur:
    senders[row[0]] = row[1]

# mapping of subject_id to subject
subjects = dict()
cur.execute('SELECT id, subject FROM Subjects')
for row in cur:
    subjects[row[0]] = row[1]

# mapping of message id to details
messages = dict()
cur.execute('SELECT id, sender_id, subject_id FROM Messages')
for row in cur:
    messages[row[0]] = (row[1], row[2])

print('loaded messages=', len(messages), 'subjects=', len(subjects), 'senders=', len(senders))

# fill the per and org
per = dict()
org = dict()
for id, message in messages.items():
    sender_id = message[0]
    per[sender_id] = per.get(sender_id, 0)+1
    pieces = senders[sender_id].split('@')
    if len(pieces) != 2:
        continue
    dns = pieces[1]
    org[dns] = org.get(dns, 0)+1

howmany = int(input("How many to dump? "))

# persons list
print('Top', howmany, 'Email list participants')
x = sorted(per, key=per.get, reverse=True)
for id in x[:howmany]:
    print(senders[id], per[id])
print()
# organizations list
print('Top', howmany, 'Email list organizations')
x = sorted(org, key=org.get, reverse=True)
for dns in x[:howmany]:
    print(dns, org[dns])
