# fpath = input('Enter file path: ')
fhand = open('mbox-short.txt')

# histogram
hour_count = dict()
for sline in fhand:
    if sline.startswith('From '):
        word_list = sline.split()
        stime = word_list[5]
        time_list = stime.split(':')
        hour = time_list[0]
        hour_count[hour] = hour_count.get(hour, 0) + 1

lst = hour_count.items()
lst2 = sorted([(k, v) for k, v in lst])
for v, k in lst2:
    print(v, k)
