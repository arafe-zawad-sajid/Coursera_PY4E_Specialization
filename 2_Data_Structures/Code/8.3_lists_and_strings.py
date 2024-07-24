# 8.3: Lists and Strings
line = ' with  three   words   \n  new'

# .split() returs a list of strings splitted based on delimeter
# by default (no delimeter), multiple spaces are treated like one delimeter
wordlist = line.split()
print(wordlist)

for word in wordlist:
    print(word)


line = ' 1      first ;      2 second   ; 3  third       '
list1 = line.split()
print(list1)
print(len(list1))

# splitting based on the delimeter ';'
list1 = line.split(';')
print(list1)
print(len(list1))


# double split pattern
fpath = 'mbox-short.txt'
fhand = open(fpath)

hcount = 0
for line in fhand:
    if not line.startswith('From '):
        continue  # skip
    lpieces = line.split()  # 1st split
    email = lpieces[1]
    epieces = email.split('@')  # 2nd split
    host = epieces[1]
    hcount += 1
    print(host)
print(hcount)


# find all emails from mbox-short.txt file
fpath = 'mbox-short.txt'
fhand = open(fpath)
ecount = 0
for line in fhand:
    if not line.startswith('From '):
        continue  # skip
    line = line.rstrip()  # not necessary because .split() excludes all whitespaces
    pieces = line.split()
    email = pieces[1]
    ecount = ecount + 1
    print('email', ecount, 'is', email)  # print count and email
print('total email =', ecount)
