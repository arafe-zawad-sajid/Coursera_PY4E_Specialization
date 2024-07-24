# 11.1 - Regular Expressions
import re

# we can use re.search() like str.find()
count_s = 0
count_f = 0
fhand = open('mbox-short.txt')
for line in fhand:
    line = line.rstrip()
    if re.search('From:', line):  # returns boolean
        count_s += 1
    if line.find('From:') > -1:  # library_name.function()
        count_f += 1
print(count_s, count_f)


# using re.search() like str.startswith()
count_s = 0
count_f = 0
fhand = open('mbox-short.txt')
for line in fhand:
    line = line.rstrip()
    if re.search('^From:', line):  # ^ indicates at the start of a string
        count_s += 1
    if line.startswith('From:'):  # library_name.function()
        count_f += 1
print(count_s, count_f)
print()


# regex wild-card characters
regex = '^X.*:'
word_list = ['X-DSPAM: CMU', 'X-DSPAM-Result: Innocent', 'X-Plane is behind schedule: 2 weeks']
for word in word_list:
    if re.search(regex, word):
        print('True:', regex, 'matches with string', word)
    else:
        print('False:', regex, 'does not match with string', word)
print()

# fine-tuning regex
regex = '^X-\S+:'
for word in word_list:
    if re.search(regex, word):
        print('True:', regex, 'matches with string', word)
    else:
        print('False:', regex, 'does not match with string', word)
print()
# ------------------------------------------------------

# 11.2 - Extracting Data
# using re.findall() to extract data
x = 'My 2 favourite numbers are 19 and 42'
regex = '[0-9]+'
num_list = re.findall(regex, x)  # returns a list of all possible matches
print(num_list)
print()

# greedy vs non-greedy matching
x = 'From: Using the: character'
regex1 = '^F.+:'  # ''+' and '*' is greedy
regex2 = '^F.+?:'  # '+?' and '*?' is non-greedy, '?' indicates don't be greedy
print(re.findall(regex1, x))  # longest posible string
print(re.findall(regex2, x))  # shortest possible string
print()

# extracting email address: at least 1 non-whitespace character surrounding an '@'
line = 'From stephen.king@uct.ac.za Sat Jan 5'
regex1 = '\S+@\S+'  # greedy
regex2 = '\S+?@\S+?'  # non-greedy
print(re.findall(regex1, line))
print(re.findall(regex2, line))
print()

# fine-tuning string extraction: search for a longer string but extract a part
line = 'From stephen.king@uct.ac.za Sat Jan 5'
regex1 = '\S+@\S+'  # greedy
regex2 = '^From (\S+@\S+)'  # greedy
print(re.findall(regex1, line))
print(re.findall(regex2, line))
print()


# extracting host name: using str.find() and string slicing
line = 'From stephen.king@uct.ac.za Sat Jan 5'
atpos = line.find('@')  # find the position of first '@'
sppos = line.find(' ', atpos)  # find the position of first space after '@'
print(line[atpos+1:sppos])  # start slicing the string after atpos and end slicing before sppos

# extracting host name: using double split patter
line = 'From stephen.king@uct.ac.za Sat Jan 5'
words = line.split()  # split the line into words
email = words[1]
pieces = email.split('@')  # split the email after '@'
print(pieces[1])  # 2nd piece is the host

# extracting host name: using regex.findall(), basic regex
line = 'From stephen.king@uct.ac.za Sat Jan 5'
regex1 = '@(\S+)'  # greedy
regex2 = '@([^ ]*)'  # greedy
print(re.findall(regex1, line))
print(re.findall(regex2, line))

# extracting host name: using regex.findall(), cooler regex
line = 'From stephen.king@uct.ac.za Sat Jan 5'
regex1 = '^From .*@(\S+)'  # greedy
regex2 = '^From .*@([^ ]*)'  # greedy
print(re.findall(regex1, line))
print(re.findall(regex2, line))
print()


# filtering + split: using regex to pick lines and extract data
fhand = open('mbox-short.txt')
numlist = list()
for line in fhand:
    line = line.rstrip()
    # extract if character ranges from '0' to '9' or '.' repeating 1 or more times
    numbers = re.findall('^X-DSPAM-Confidence: ([0-9.]+)', line)  # filter + split
    if len(numbers) != 1:
        continue  # skip
    fnum = float(numbers[0])
    numlist.append(fnum)
print('Maximum:', max(numlist))
print()


# using '\' to make a special regex character behave like a normal character
x = 'We just received $10.00 for cookies.'  # extract the price
regex = '\$[0-9.]+'
print(re.findall(regex, x))

x = 'We just received $ for cookies.'
regex2 = '\$[0-9.]*'  # char repeated zero or more times
print(re.findall(regex2, x))


# phone number in BD
regex = '\+880[^0][0-9]+'
phone = '+8801535524246'
print(re.search(regex, phone))
