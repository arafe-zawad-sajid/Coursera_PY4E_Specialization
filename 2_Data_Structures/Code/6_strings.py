# 6.1: Strings
print('6.1: Strings')

str1 = "hello"
str2 = 'there'
str3 = "123"

print(str1[1])  # constant in sub operator
x = 3
print(str1[x - 1])  # expression in sub operator

bob = str1 + str2 + str3
print(bob)
istr3 = int(str3)
print(istr3 + 1)
letter = str1[0]
print(letter)
print(len(bob))

index = 0
size = len(str1)
print('Size of str1', str1, 'is', size)
while index < size:
    letter = str1[index]
    print(index, letter)
    index = index + 1
print('End of string')

for letter in str1:
    print(letter)

match = 'l'
count = 0
for letter in str1:
    if letter == match:
        count = count + 1
print(match, 'found', count, 'times')

# slicing strings using [m:n]
# m upto but not including n
s = 'Monty Python'
print(s[0:4])
print(s[6:20])  # if n > last index, it stops at the end
print(s[:3])  # beginning upto but not including n
print(s[8:])  # m upto the end
print(s[:])  # whole

# 6.2: Manipulating Strings
print('6.2: Manipulating Strings')

s = 'Monty Python'

# using 'in' as a logical operator
print('n' in s)
print('python' in s)
if 'a'in s:
    print('found a')
else:
    print('did not find a')

# string comparison using comparison operators
words = ['Monty Python', 'Monty python', 'monty Python', 'monty python']
for word in words:
    if word == s:
        print(word, 'equals', s)
    elif word < s:
        print(word, 'comes before', s)
    elif word > s:
        print(word, 'comes after', s)

#print(type(greet))
#print(dir(greet))  # methods in class str

# str functions
greet = 'HeLlo'
lgreet = greet.lower()
print('greet =', greet, ', greet.lower() =', lgreet)
ugreet = greet.upper()
print('greet =', greet, ', greet.upper() =', ugreet)
cgreet = greet.capitalize()
print('greet =', greet, ', greet.capitalize() =', cgreet)
print('Hi There'.upper())  # constants have this builtin capability as well

# using find() to search for the first occurrence of a substring
greet = 'HeLlo'
pos = greet.find('Ll')  # returns the first index where it found
print(pos)
pos = greet.find('ll')  # returns -1 when not found
print(pos)

# replace('search', 'replace'), search and replace all occurrences of 'search' with 'replace'
# acts as multi replace
greet = 'hello world'
rgreet = greet.replace('l', 'x')
print('greet =', greet, ", greet.replace('l', 'x') =", rgreet)

# stripping whitespace
greet = '   Hello Bob  '
print(greet.lstrip())  # strips from beginning
print(greet.rstrip())  # strips from end
print(greet.strip())  # strips from beginning and end

# search for prefix
line = 'please have a nice day'
print(line.startswith('please'))  # prints true or false
print(line.startswith('p'))

# search for suffix
print(line.endswith('please'))  # prints true or false
print(line.endswith('y'))

# parsing and extracting using find() and string slicing
# find the host of the email from a space seperated data
data = 'From arafe.zawad.sajid@g.bracu.ac.bd Sat Jan 5 09:14:16 2008'

atpos = data.find('@')  # pos of '@'
sppos = data.find(' ', atpos)  # pos of first 'space' afer '@'
host = data[atpos+1:sppos]  # slice after '@' upto but not including the 'space'

frompos = data.find('From')  # pos of 'From'
sp = data.find(' ', frompos)  # pos of first 'space' afer 'From'
email = data[sp+1:sppos]  # slice after 'space' before email upto but not including the 'space' after email

print('Email =' + email + ', Host =' + host)


x = 'From marquard@uct.ac.za'
print(x[14:17])

fruit = 'Banana'
#fruit[0] = 'b'  # TypeError, because strings are immutable (hence doesn't support item assignment)
x = fruit.lower()  # .lower() returns us a copy, doesn't change the original string, because strings are immutable
print(fruit, x)
