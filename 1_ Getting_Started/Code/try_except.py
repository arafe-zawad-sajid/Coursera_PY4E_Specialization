# first prog
first = 'Hello Bob'
try:
    ifirst = int(first)
    print(ifirst, 'is a number')

    if ifirst < 5:
        print(ifirst, 'is smaller than 5')
    elif ifirst < 20:
        print(ifirst, 'is not smaller than 5 but smaller than 20')
    else:
        print(ifirst, 'is not smaller than 20')
except:
    print(first, 'is not a number')

first = '123'
try:
    ifirst = int(first)
    print(ifirst, 'is a number')

    if ifirst < 5:
        print(ifirst, 'is smaller than 5')
    elif ifirst < 20:
        print(ifirst, 'is not smaller than 5 but smaller than 20')
    else:
        print(ifirst, 'is not smaller than 20')
except:
    print(first, 'is not a number')

# second prog
rawstr = input('Enter a number:')
try:
    ival = int(rawstr)
except:
    ival = -1

if ival > 0:
    print('Nice Work')
else:
    print('Not a number')
