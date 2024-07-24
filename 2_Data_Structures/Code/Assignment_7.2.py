fpath = input('Enter file path: ')
try:
    fhand = open(fpath)
except:
    print(fpath, ': this file cannot be opened')
    quit()

count = 0
total = 0.0
for line in fhand:
    if line.startswith('X-DSPAM-Confidence:'):
        #ln = line.rstrip()
        start = line.rfind(':')
        fval = float(line[start+1:].strip())
        total = total + fval
        count = count + 1
        
print('Average spam confidence:', total/count)
