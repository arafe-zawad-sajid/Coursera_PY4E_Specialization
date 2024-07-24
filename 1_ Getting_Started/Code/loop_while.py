n = 5 # n is iteration variable
while n > 0 :
    print(n)
    n = n-1 # without this -> infinite looping since n not changing
print("End")
print("Residual value of n:", n)

while True:
    line = input('> ')
    print("in:", line)
    if line[0] == '#':
        print('continue to next iteration')
        continue
    if line == 'q':
        print('break out of the loop')
        break
    print('not q')
    print('loop again')
print('Finally done!')
