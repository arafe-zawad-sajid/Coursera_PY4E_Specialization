# Sockets (Chapter 12)
def socket_connect(host, port):
    import socket as st
    mysock = st.socket(st.AF_INET, st.SOCK_STREAM)
    mysock.connect((host, port))
    return mysock

def socket_get(mysock, url):
    cmd = ('GET ' + url + ' HTTP/1.0\r\n\r\n').encode()
    mysock.send(cmd)
    return mysock

def socket_recv(mysock):
    lines = ''
    while True:
        data = mysock.recv(512)
        if len(data) < 1:
            break
        lines += data.decode()
    mysock.close()
    return lines

# implementation
host_add = 'data.pr4e.org'
port_num = 80
ms = socket_connect(host_add, port_num)

url = 'http://' + host_add + '/romeo.txt'
sg = socket_get(ms, url)

content = socket_recv(sg)
print(content)
# -----------------------------------------------------

# urllib (Chapter 12)
import urllib.request, urllib.parse, urllib.error

# printing
fhand = urllib.request.urlopen('http://data.pr4e.org/romeo.txt')
for line in fhand:
    print(line.decode().strip())
print()

# counting words
fhand = urllib.request.urlopen('http://data.pr4e.org/romeo.txt')  # again open
counts = dict()
for line in fhand:
    words = line.decode().split()
    for word in words:
        counts[word] = counts.get(word, 0) + 1
print(counts)
print()
# ------------------------------------------------------------


# BeautifulSoup (Chapter 12): spidering url links
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# ignores SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'http://www.dr-chuck.com/page1.htm'
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

tags = soup('a')
for tag in tags:
    print(tag.get('href', None))
