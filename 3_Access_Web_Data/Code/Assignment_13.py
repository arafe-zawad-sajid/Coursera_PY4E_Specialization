import urllib.request as UReq
import ssl
import xml.etree.ElementTree as ETree

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url_sample = 'http://py4e-data.dr-chuck.net/comments_42.xml'
url_actual = 'http://py4e-data.dr-chuck.net/comments_408956.xml'
xml_doc = UReq.urlopen(url_actual, context=ctx).read()

tree = ETree.fromstring(xml_doc)
count_tags = tree.findall('.//count')
total = 0
for count in count_tags:
    total += int(count.text)
print(total)
print()
# ----------------------------------------------
# extract 'count' values from the json and print the sum

import urllib.request as UReq
import ssl
import json

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url_sample = 'http://py4e-data.dr-chuck.net/comments_42.json'
url_actual = 'http://py4e-data.dr-chuck.net/comments_408957.json'

uhand = UReq.urlopen(url_actual, context=ctx)
raw_data = uhand.read()  # byte code
decoded_data = raw_data.decode()  # python string in unicode

js = json.loads(decoded_data)
comments_list = js['comments']  # list of dictionaries
count = 0
for item in comments_list:  # each item is a dictionary
    count += int(item['count'])
print(count)
print()
# ----------------------------------------------
