# 12.4 - Retrieving Web Pages
import urllib.request as ur
import urllib.parse as up
import urllib.error as ue

# urlopen: treats it like a file (internet file)
# the headers are not shown but can be called later
fhand = ur.urlopen('http://data.pr4e.org/romeo.txt')  # almost same as open() for a file
for line in fhand:
    print(line.decode().rstrip())  # decode the bytes
print()

# count words in a file
fhand = ur.urlopen('http://data.pr4e.org/romeo.txt')  # again open
counts = dict()
for line in fhand:
    words = line.decode().split()
    for word in words:
        counts[word] = counts.get(word, 0) + 1
print(counts)
print()


# extract all links
import re
fhand = ur.urlopen('http://data.pr4e.org/page1.htm')
list_links = []
for line in fhand:
    text = line.decode().rstrip()
    print(text)
    links = re.findall('href=\"(http://.+)\"', text)
    # if len(links) > 0:  # not necessary
    for link in links:
        list_links.append(link)
print('links:', list_links)
