fpath = input('Enter file path: ')
try:
    fhand = open(fpath)
except:
    print('Error. Wrong file path.')
    quit()

# create histogram
word_count = dict()
for line in fhand:
    if line.startswith('From '):
        word_list = line.split()
        # idiom: retrieve/create/update counter
        word_count[word_list[1]] = word_count.get(word_list[1], 0) + 1

# find most common word
max_word = None
max_count = 0
for word in word_count:
    if word_count[word] > max_count:
        max_count = word_count[word]
        max_word = word  # capture/remember the key that has largest count

print(max_word, max_count)
