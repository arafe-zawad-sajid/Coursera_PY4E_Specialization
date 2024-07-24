# 7.1: Files
# 7.2: Processing Files
stuff = 'X\nY'  # '\n' new line (enter button) is considered as 1 single character
print(stuff)
print(len(stuff))  # print() by default sticks a new line at the end

# counting lines in a file
fhandle = open('read me.txt')
lcount = 0
for line in fhandle:
    lcount = lcount + 1
    print(lcount, line)  # outputs 2 '\n', one from the end of each line, another from print()
print("this file has " + str(lcount) + " lines")

# reading the whole file
fhandle = open('read me.txt')  # had to open file again
inp = fhandle.read()  # 1 big blob of characters punctuated by '\n'
print(inp)
print(len(inp))  # number of chars
print(inp[:20])  # first 20 chars


# searching through a file

# ex 1: print lines starting with 'From:'
fhandle = open('mbox-short.txt')
lcount = 0
for line in fhandle:
    line = line.rstrip()  # stripping the '\n' (whitespaces) at the end of each line
    if line.startswith('From:'):
        lcount = lcount + 1
        print(lcount, line)  # outputs one '\n' from print()
print("this file has " + str(lcount) + " lines starting with 'From:''")


# ex 1 by flipping the logic
# generally it's better to skip the bad lines
fhandle = open('mbox-short.txt')  # had to open file again
lcount = 0
for line in fhandle:
    line = line.rstrip()
    if not line.startswith('From:'):  # if line doesn't start with 'From:'
        continue  # basically skipping uninterested lines
    lcount = lcount + 1
    print(lcount, line)  # outputs 1 new line
print("this file has " + str(lcount) + " lines starting with 'From:''")


# ex 2: print lines containing  'uct.ac.za'
# using 'in' to search through lines
fhandle = open('mbox-short.txt')  # had to open file again
for line in fhandle:
    line = line.rstrip()
    if '@uct.ac.za' not in line:  # if not '@uct.ac.za' in line:
        continue  # skip
    print(line)


# ex 3: find number of 'Subject' lines in a file
# read the file name/file path using input()
# deal with bad input
fpath = input("Enter the file path: ")
try:
    fhand = open(fpath)
except:
    print('File cannot be opened:', fpath)
    quit()

lcount = 0
for line in fhand:
    if line.startswith('Subject:'):
        lcount = lcount + 1
print('There were', lcount, 'subject lines in', fpath)
