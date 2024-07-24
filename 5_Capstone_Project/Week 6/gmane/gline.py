import sqlite3

# connect to index.sqlite database
db = 'index.sqlite'
conn = sqlite3.connect(db)
cur = conn.cursor()

# generate senders dict, maps id to sender
senders = dict()
cur.execute('SELECT id, sender FROM Senders')
for row in cur:
    senders[row[0]] = row[1]

# generate messages dict, maps id to tuple of sender_id and sent_at
messages = dict()
cur.execute('SELECT id, sender_id, sent_at FROM Messages')
for row in cur:
    messages[row[0]] = (row[1], row[2])

# print the length of senders and messages
print('loaded messages=', len(messages), 'senders=', len(senders))

# generate senderorgs dict, histogram of dns to frequency
senderorgs = dict()
for id, tup in messages.items():
    # split email address, extract dns
    sender_id = tup[0]
    pieces = senders[sender_id].split('@')
    if len(pieces) != 2:
        continue
    dns = pieces[1]
    senderorgs[dns] = senderorgs.get(dns, 0)+1  # histogram

# pick the top 10 orgs
orgs = sorted(senderorgs, key=senderorgs.get, reverse=True)
orgs = orgs[:10]  # top 10
print('Top 10 Organizations')
for org in orgs:
    print(org, senderorgs[org])

# generate months list, containing unique months
# generate counts dict, maps month, dns to frequency
months = list()
counts = dict()
for id, (sender_id, sent_at) in messages.items():
    # split email address, extract dns
    pieces = senders[sender_id].split('@')
    if len(pieces) != 2:
        continue
    dns = pieces[1]
    # dns of top 10 orgs
    if dns not in orgs:
        continue
    # extract month(year-month)
    month = sent_at[:7]  # yyyy-mm
    # unique months
    if month not in months:
        months.append(month)
    # maps key( tuple of month, dns) to frequency
    key = (month, dns)
    counts[key] = counts.get(key, 0)+1  # histogram
# sort months based on key(month, dns)
months.sort()

# write the 1st row of gline.js containing titles of the gline table
js = 'gline.js'
fhand = open(js, 'w')  # write permission
fhand.write("gline = [\n['Month'")
for org in orgs:
    fhand.write(", '"+org+"'")
fhand.write("]")

# write the rows of gline.js containing the data for each column of the gline table
for month in months:
    fhand.write(",\n['"+month+"'")
    for org in orgs:
        key = (month, org)
        val = counts.get(key, 0)
        fhand.write(", "+str(val))
    fhand.write("]")
fhand.write('\n];')
fhand.close()

print("\nOutput written to gline.js")
print("Open gline.htm to visualize the data")
