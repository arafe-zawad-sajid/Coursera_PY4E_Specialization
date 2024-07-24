fpath = input('Enter file name: ')
fhand = open(fpath)
ecount = 0
for line in fhand:
    if not line.startswith('From:'):
        continue  # skip
    lst = line.split()
    ecount = ecount + 1
    print(lst[1])
print('There were', ecount, 'lines in the file with From as the first word')
