total = 0.0
count = 0

while True:
    try:
        i = input("Enter a number: ")
        if i == 'done':
            break
        else:
            f = float(i)
    except:
        print("Invalid input")
        continue
    total = total + f
    count = count + 1

avg = total / count
print(total, count, avg)
