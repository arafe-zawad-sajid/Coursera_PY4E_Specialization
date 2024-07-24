fpath = 'mbox-short.txt'
fhand = open(fpath)

for line in fhand:
    print(line.rstrip().upper())
