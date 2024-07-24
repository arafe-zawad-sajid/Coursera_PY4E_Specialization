x = 10

if x < 2:
    print('smaller than 2')
    print('still smaller')
# it's ok
elif x < 10:
    print('between 2 and 9')  # dealing with int
    print('still in between 2 and 9')
    # it's ok
# it's still ok
elif x < 20: print('between 9 and 19')  # dealing with int
    # print('still in between 9 and 19')
else:
    print('larger than 19')
    print('still larger')

print('all done')
