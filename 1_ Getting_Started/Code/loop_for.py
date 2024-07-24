for friend in ['Fareen', 'Rabid', 'Sami', 'Shafkat']:
    print('friend =', friend)
    if friend == 'Sami':
        print(friend, 'is kutta')
    else:
        print(friend, 'is good')
    print('next?')
print('end of list')


# comment for friends in myFriends list
def comment(friends):
    for friend in friends:
        print('friend =', friend)
        if friend == 'Sami':
            print(friend, 'is kutta')
        else:
            print(friend, 'is good')
        print('next?')
    print('end of list')

myFriends = ['Fareen', 'Rabid', 'Sami', 'Shafkat']
comment(myFriends)


# find maximum number in a list of numbers
def maxInList(numbers):
    largest = numbers[0]
    print('let largest = ', largest)
    count = 0
    for n in numbers:
        count = count + 1
        print('in pos', count, ', n =', n)
        if n > largest:
            largest = n
            print('largest =', largest)
    return largest
num_list = [23, 21, 14, 65, 43]
print('max in the list =', maxInList(num_list))


# input_list = []
# while True:
#     input_list = input('>')
#     if input_list == 'q':
#         print("break loop")
#         break
# for i in input_list:
#     print(i)


# find average from a list of numbers
def avgInList(numbers):
    count = 0
    add = 0
    for val in numbers:
        count = count + 1
        add = add + val
        print('count = ', count, ', value =', val, ', sum =', add)
    return add/count

num_list = [23, 21, 14, 65, 43]
print('average is =', avgInList(num_list))
