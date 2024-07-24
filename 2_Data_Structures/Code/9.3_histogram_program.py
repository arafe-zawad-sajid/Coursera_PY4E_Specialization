# output the most common word and its frequency
print('Enter file path: ')
while True:
    fpath = input()
    if fpath == 'q':
        print('program shutdown successful.')
        break
    try:
        fhand = open(fpath)
    except:
        print('Error. Enter the correct file path: ')
        continue  # skips to beginning

    # create a histogram
    word_count = dict()
    for line in fhand:
        word_list = line.split()  # split lines into list of words
        for word in word_list:
            word_count[word] = word_count.get(word, 0) + 1  # increment word count

    # find the max freq and that word
    max_word = None
    max_count = 0
    for kword in word_count:
        if max_word is None or word_count[kword] > max_count:
            max_word = kword
            max_count = word_count[kword]

    print(max_word, max_count)
    print('Enter file path: ')
