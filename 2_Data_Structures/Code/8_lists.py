# 8.1: Lists

print([1, 'red', [5, '6'], 3.4])  # list constant in square brackets

# list can be empty; can store multiple types of data at once, even another list
lt = ['hello', 1, 2, 3, ['can', "you add"], 1.0, 'and', 2.5]
for l in lt:
    print(l)

# using [i] operator to get a single element at a specific index
print(lt[0], 'again')

print('len(lt) =', len(lt), ',', type(lt))

print(range(len(lt)))  # range(0, 8), it is a list of int
x = range(len(lt))
print(x[6])
print('len(lt[0]) =', len(lt[0]), ',', type(lt[0]))
print('len(lt[4]) =', len(lt[4]), ',', type(lt[4]))


# strings are not mutable
fruit = 'banana'
print(fruit[0])
# fruit[0] = 'b'  # TypeError, since strings are immutable (hence doesn't support item assignment)
print('len(fruit) =', len(fruit), ',', type(fruit))

# range() returns a list
print(range(len(fruit)))  # range = (0, 6)
# counted loop going through a range of numbers
for i in range(len(fruit)):  # i goes through the numbers (int) in the list generated by range()
    print('fruit[' + str(i) + '] =', fruit[i])

# lists are mutable
# lt = ['hello', 1, 2, 3, ['can', "you add"], 1.0, 'and', 2.5]
lt[0] = 'hi'  # no error, since lists are mutable (hence supports item assignment)
print(lt[0])
print('print(lt) =', lt)


# 8.2: Manipulating Lists

a = [9, 41, 'hi', 2.3, "bye"]
b = [0.0, 21, "hi again", 5.3]
print(a, b)

# concatenating lists using '+' operator (like strings)
c = a + b
print(c)

# list slicing using [m:n] (like strings)
print(c[2:4])

#print(dir(c))  # methods in list library


# initializing a list: creating an empty list object
d = list()
print(d)


# list.append(param): to add things at the end of a list (lists are mutable)
# lists are mutable, original list changes/updates
d.append('hi')
d.append(["hello", 1, 2, 'bye'])
print(d)

# str is converted to a list of chars
e = list("bonjur")
print(e)

# param = [list_constant]
f = list(['bonjur', 'hello'])  # list_constant is just appended
print(f)
f.append(123.5)
f.append('bella')
print(f)

x = f.append('a')  # list are mutable unlike strings
print(x)  # prints None (list x is null)

print(f)  # line 76 is successful and appends 'a' to the list f

x = list(f)  # the list in f is just appended
x.append(10)
print(x)


# using 'in' to verify if something is in a list
print(123.5 in f)
print('bell' in f)
print('bell' not in f)


# list.sort(): to sort a list
g = ['sami', 'sajid', 'Abir', 'fareen', "Borshon"]
print(g)
g.sort()  # sorts and updates list g (lists are mutable)
print(g)

h = ['sami', 'sajid', 'Abir', 1, 4.5, "Borshon"]
#g.sort()  # TypeError: because int and str cannot be compared together

num_list = [2.3, 5, 1, 2.5]  # int and float in a list can be compared together
print(num_list)
num_list.sort(reverse=True)  # works
print(num_list)


# using built-in functions on a list
print('len of above list =', len(num_list))
print('sum of above list =', sum(num_list))
print('avg of above list =', sum(num_list) / len(num_list))
print('max of above list =', max(num_list))
print('min of above list =', min(num_list))


# take numeric inputs until 'done' and print out average using lists
# using the list data structure to find sum, count and avg
numlist = list()
while True:
    sval = input('Enter a number: ')
    if sval == 'q':
        break
    numlist.append(float(sval))

print(numlist)
print('len of above list =', len(numlist))
print('sum of above list =', sum(numlist))
print('avg of above list =', sum(numlist) / len(numlist))
print('max of above list =', max(numlist))
print('min of above list =', min(numlist))
