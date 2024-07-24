from urllib.request import urlopen
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url1 = 'https://api.covid19india.org/raw_data1.json'  # 30/1 - 19/4
url2 = 'https://api.covid19india.org/raw_data2.json'  # 20/4 - 26/4
url3 = 'https://api.covid19india.org/raw_data3.json'  # 27/4 - 09/5
url4 = 'https://api.covid19india.org/raw_data4.json'  # 10/5 - 15/5
female = 0
male = 0
total = 0
urllist = [url1, url2, url3, url4]
for url in urllist:
    print('collecting data from:', url)
    uhand = urlopen(url, context=ctx).read().decode()
    js = json.loads(uhand)
    for list in js['raw_data']:
        gender = list['gender']
        total += 1
        if gender == 'F':
            female += 1
        elif gender == 'M':
            male += 1
    print('done')
print('From January 30 to May 15,', female, 'females and', male, 'males have been affected out of', total)
