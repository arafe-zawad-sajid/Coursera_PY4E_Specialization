from urllib.request import urlopen, Request
import ssl
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
url = 'https://www.worldometers.info/coronavirus'
req = Request(url, headers=headers)
uhand = urlopen(req, context=ctx).read()

soup = BeautifulSoup(uhand, 'html.parser')
tags = soup('a')
count = 1
countries = dict()
for tag in tags:
    if len(tag.attrs) == 2:
        atclass = tag.get('class', None)
        athref = tag.get('href', None)
        print(tag.attrs)
        if atclass is None and athref is None:
            continue
        if atclass == 'mt_a' and athref.startswith('country/') and athref not in countries:
            countries[athref] = count
            count += 1
for key, count in countries.items():
    print(count, key)
print(len(countries))
