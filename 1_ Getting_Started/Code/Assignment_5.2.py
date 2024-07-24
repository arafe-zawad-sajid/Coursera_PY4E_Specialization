def findMin(a, b):
    if a is None:
        return b
    elif b is None:
        return a
    elif a < b:
        return a
    else:
        return b


def findMax(a, b):
    if a is None:
        return b
    elif b is None:
        return a
    elif a > b:
        return a
    else:
        return b


maximum = None
minimum = None

while True:
    try:
        sval = input('Enter a number:')
        if sval == 'done':
            break
        iVal = int(sval)
    except ValueError:
        print("Invalid input")
        continue

    minimum = findMin(minimum, iVal)
    maximum = findMax(maximum, iVal)

print('Maximum is', maximum)
print('Minimum is', minimum)
