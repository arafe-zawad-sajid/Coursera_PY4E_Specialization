def computepay(h, r):
    if r>0:
        if h>=0 and h<=40:
            return h*r
        elif h>40:
            reg = 40.0*r
            otp = (h-40.0)*(r*1.5)
            return reg + otp;
        else:
            print("Hour must be a positive number")
    else:
        print("Rate must be greater than 0")

try:
    fh = float(input("Enter Hours: "))
    fr = float(input("Enter Rate: "))
except:
    print("TypeError: Enter numeric values")
    quit()
p = computepay(fh, fr)
print("Pay", p)
