text = "X-DSPAM-Confidence:    0.8475"
last_sp = text.rfind(' ')
tnum = text[last_sp+1:]
fnum = float(tnum)
print(fnum)
