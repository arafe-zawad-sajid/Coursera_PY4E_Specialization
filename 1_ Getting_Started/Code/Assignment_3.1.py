hr = input("Enter Hours:")
rphr = input("Enter Rate:")

f_hr = float(hr)
f_rphr = float(rphr)

max = 40
multiplier = 1.5
f_extra = 0.0

if f_hr > max:
    f_extra = f_hr - float(max)

pay = (max*f_rphr) + ((multiplier*f_rphr)*f_extra)

print(pay)
