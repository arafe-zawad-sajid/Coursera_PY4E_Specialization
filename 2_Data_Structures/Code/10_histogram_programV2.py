# output top N most common words and their respective frequencies
print('Enter file path:')
while True:
    fpath = input()
    if fpath == 'q':
        print('program shutdown successful.')
        quit()
    try:
        fhand = open(fpath)
    except:
        print('Error. Enter the correct file path:')
        continue  # skips to beginning

    # create a histogram
    word_count = dict()
    for line in fhand:
        word_list = line.split()
        for word in word_list:
            word_count[word] = word_count.get(word, 0) + 1

    # create a value-key list, sorted based on value
    slcount_word = sorted([(vcount, kword) for kword, vcount in word_count.items()], reverse=True)

#line 22 shortcut for lines 25-31
    # lcount_word = list()
    # lword_count = word_count.items()
    # for kword, vcount in lword_count:
    #     newtup = (vcount, kword)
    #     lcount_word.append(newtup)
    #
    # slcount_word = sorted(lcount_word, reverse=True)

    #print(slcount_word)  # checker

    # print top N words
    length = len(slcount_word)
    print('There are total', length, 'unique words.')
    sval = input('Want to see top N commonly used words? Enter an int value: ')
    N = int(sval)

    # print with list slicing
    for vcount, kword in slcount_word[:N]:
        print(kword, vcount)

# first N words # bad way
#lines 42 & 43 is shorcut for lines 46-51
    # N = N - 1
    # tmp = N
    # while N < length and N >= 0:
    #     index = tmp - N  # 0 to N
    #     print(slcount_word[index])
    #     N = N - 1

    print('Enter file path:')
