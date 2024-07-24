# Scraping HTML Data with BeautifulSoup
import urllib.request as ur
import ssl
from bs4 import BeautifulSoup

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url_sample = 'http://py4e-data.dr-chuck.net/comments_42.html'
url_actual = 'http://py4e-data.dr-chuck.net/comments_408954.html'
html = ur.urlopen(url_actual, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

tags = soup('span')
total = 0
for tag in tags:
    ival = int(tag.contents[0])
    total += ival
print(total)
# --------------------------------------------------------

# Following Links in HTML Using BeautifulSoup
import urllib.request as urlreq
from bs4 import BeautifulSoup as bsoup
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url_sample = 'http://py4e-data.dr-chuck.net/known_by_Fikret.html'
url_actual = 'http://py4e-data.dr-chuck.net/known_by_Bobby.html'

pos = 18
repeat = 7
url = url_actual
while repeat > 0:
    html = urlreq.urlopen(url, context=ctx).read()
    soup = bsoup(html, 'html.parser')
    tags = soup('a')
    url = tags[pos-1].get('href', None)  # next url
    name = tags[pos-1].contents[0]  # name
    repeat -= 1
print(name)
