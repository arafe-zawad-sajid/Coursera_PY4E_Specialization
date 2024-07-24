x = 5
if x < 10:
#print('smaller') # error
    print('smaller')
    print('part of the block')
print('deindenting')  # out of if block
if x > 20: print('bigger')  # this line is ok
    # print('hi')  # error
print('finis')  # deindenting -> out of if block

if x > 1:
    print('bigger than 1')
    if x < 10:
        print('smaller than 10')
print('all done')
