fpath = input('Enter file path: ')
try:
    fhand = open(fpath)
except:
    print(fpath, ': this file cannot be opened')
    quit()

for line in fhand:
    uline = line.rstrip().upper()
    print(uline)
