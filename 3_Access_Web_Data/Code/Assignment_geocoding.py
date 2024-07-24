import urllib.request as UReq
import urllib.parse as UParse
import ssl
import json

# ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

service_url = 'http://py4e-data.dr-chuck.net/json?'
api_key = 42

actual_address = 'University of Ottawa'
sample_address = 'South Federal University'

url = service_url + UParse.urlencode({'address': actual_address, 'key': api_key})
uhand = UReq.urlopen(url)
data = uhand.read().decode()  # read handle, get byte code. decode byte code, get string

js = json.loads(data)
place_id = js['results'][0]['place_id']
print(place_id)
