score = input("Enter Score:\n")

try:
    fsc = float(score)
except:
    print("TypeError! Numeric value expected")
    quit()

if fsc < 0.0 and fsc > 1.0:
    print("RangeError: Acceptable range between 0.0 and 1.0")
elif fsc >= 0.0 and fsc <0.6:
    print("F")
elif fsc >= 0.6 and fsc < 0.7:
    print("D")
elif fsc >= 0.7 and fsc < 0.8:
    print("C")
elif fsc >= 0.8 and fsc < 0.9:
    print("B")
elif fsc >= 0.9 and fsc < 1.0:
    print("A")
