import re

fpath = 'actual.txt'
fhand = open(fpath)
regex = '[0-9]+'
total = 0
count = 0
for line in fhand:
    numlist = re.findall(regex, line)
    if len(numlist) > 0:
        for num in numlist:
            total += int(num)
            count += 1
print(total)


# using list comprehension
print(sum([int(n) for n in re.findall(regex, open(fpath).read())]))
