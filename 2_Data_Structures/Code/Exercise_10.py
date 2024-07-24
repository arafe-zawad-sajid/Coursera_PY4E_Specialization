# top 5 most common word
fpath = input('Enter file path: ')
fhand = open(fpath)


# histogram
word_count = dict()
for line in fhand:
    word_list = line.split()
    for word in word_list:
        word_count[word] = word_count.get(word, 0) + 1  # idiom: retrieve/create/update counter


# value-key list of tuples sorted by values

# line 24 shorcut for line 18-24
# value-key list of tuples
# flipped_list = list()
# for k, v in word_count.items():
#     newtup = (v, k)
#     flipped_list.append(newtup)

# sort based on values
# sorted_flipped_list = sorted(flipped_list, reverse=True)

sorted_flipped_list = sorted([(v, k) for k, v in word_count.items()], reverse=True)


# print top 5
# printing a list of top 5 tuples in value-key (always default) order through list slicing
print(sorted_flipped_list[:5])  # order cannot be interchanged


# line 41 shorcut for line 36-37
# printing top 5 tuples in value-key order using for loop through a list slice of 5 tuples
for v, k in sorted_flipped_list[:5]:
    print(k, v)  # order can be interchanged


# printing a list of top 5 tuples in key-value order without using loop through a list slice of 5 tuples
print([(k, v) for v, k in sorted_flipped_list[:5]])  # order can be interchanged
