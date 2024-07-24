import sqlite3
import string

# connect to index.sqlite database
db = 'index.sqlite'
conn = sqlite3.connect(db)
cur = conn.cursor()

# create subjects dict mapping id to subject
subjects = dict()
cur.execute('SELECT id, subject FROM Subjects')
for row in cur:
    subjects[row[0]] = row[1]  # id to subject

# create counts dict (histogram) mapping word to frequency
counts = dict()
cur.execute('SELECT subject_id FROM Messages')
for row in cur:
    subject = subjects[row[0]]  # subject line
    # get rid of punctuations, digits, whitespaces, force lowercase
    subject = subject.translate(str.maketrans('', '', string.punctuation))
    subject = subject.translate(str.maketrans('', '', string.digits))
    subject = subject.strip()
    subject = subject.lower()
    # split the lines into words
    words = subject.split()
    for word in words:
        if len(word) < 4:
            continue
        counts[word] = counts.get(word, 0)+1  # histogram

# sort the histogram
x = sorted(counts, key=counts.get, reverse=True)
# find the max and min count for top 100
max = counts[x[0]]
min = counts[x[99]]
print('Range of counts:', max, min)

# spread the font sizes across 20-80 based on the count, and write word.js
bigsize = 80
smallsize = 20

# open word.js with write permission
js = 'gword2.js'
fhand = open(js, 'w')
fhand.write('gword = [')
first = True
for word in x[:100]:
    if not first:
        fhand.write(',\n')
    first = False
    count = counts[word]
    size = (count-min)/(max-min)
    size = int((size*bigsize)+smallsize)
    fhand.write('{text: "'+word+'", size: '+str(size)+'}')
fhand.write('\n];\n')

print('Output written to gword.js')
print('Open gword.htm in a browser to see the visualization')
