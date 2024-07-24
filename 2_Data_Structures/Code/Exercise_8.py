# Method 1
fpath = input('Enter file path: ')
fhand = open(fpath)

for line in fhand:
    line = line.rstrip()
    # guardian pattern 2: before dangerous statement
    #if line == '':
        #continue  # skips blank lines
    word_list = line.split()
    # guardian pattern 1: before dangerous statement
    if len(word_list) < 3:  # at least 3 words, makes guardian stronger, protects line 13 (at least 1 word) and 15
        continue  # skips empty lists
    if word_list[0] != 'From':  # dangerous statement
        continue  # skips uninteresting lists
    print(word_list[2])  # prints the day
# we can use any of the 2 guardians


# Method 2: same as Method 1 but using or
fpath = input('Enter file path: ')
fhand = open(fpath)

for line in fhand:
    line = line.rstrip()
    word_list = line.split()  # list of words = line
    # guardian pattern 3: guardian in a compound statement (guardian condition before dangerous condition)
    # if line has less than 3 words or first word is not 'From', continue (skip)
    if len(word_list) < 3 or word_list[0] != 'From':  # checks condition from left to right
        continue  # skip
    print(word_list[2])  # prints the day
