fpath = input('Enter file path: ')
fhand = open(fpath)
wordlist = list()

for line in fhand:
    # line = line.rstrip()
    pieces = line.split()
    for word in pieces:
        if word in wordlist:
            continue  # skips
        wordlist.append(word)

wordlist.sort()
print(wordlist)
