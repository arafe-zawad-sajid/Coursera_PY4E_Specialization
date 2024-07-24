sh = input("Enter Hours:")
sr = input("Enter Rate:")
try:
    fh = float(sh)
    fr = float(sr)
except:
    print("Error, please enter numeric input")
    quit()

if fh > 40:
    reg = 40 * fr
    otp = (fh - 40.0) * (fr * 1.5)
    xp = reg + otp
else:
    xp = fh * fr

print("Pay:", xp)
