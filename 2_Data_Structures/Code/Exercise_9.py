fpath = input('Enter file path: ')
if fpath == '1':
    fpath = 'clown.txt'
fhand = open(fpath)

# generate histogram
word_count = dict()
for line in fhand:
    word_list = line.split()
    for word in word_list:
        # idiom: retrieve/ create/ update counter
        word_count[word] = word_count.get(word, 0) + 1  # if key is not there the value is 0
        #oldcount = word_count.get(word, 0)
        #newcount = oldcount + 1
        #word_list[word] = newcount

# find most common word
largest = -1
theword = None
for key, val in word_count.items():
    if val > largest:
        largest = val
        theword = key  # capture/remember the key that was largest
print(theword, largest)
