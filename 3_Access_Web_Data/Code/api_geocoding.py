import urllib.request as urlReq
import urllib.parse as urlParse
import ssl
import json

api_key = '42'
service_url = 'http://py4e-data.dr-chuck.net/json?'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

input_address = input('Enter Location:\n')
url = service_url + urlParse.urlencode({'address': input_address, 'key': api_key})
print('Retrieiving', url)

uhand = urlReq.urlopen(url, context=ctx)
raw_data = uhand.read()
decoded_data = raw_data.decode()
print('Retrieved', len(decoded_data), 'characters')

#print(decoded_data)  # prints json content

try:
    js = json.loads(decoded_data)
except:
    js = None

if not js or 'status' not in js or js['status'] != 'OK':
    print('Failed To Retrieve\n')
    print(decoded_data)
    quit()

results_list = js['results']  # 1 list
results_dict = results_list[0]  # 1 dict
geometry_dict = results_dict['geometry']
location_dict = geometry_dict['location']
lat_val = location_dict['lat']
lng_val = location_dict['lng']

formatted_address = results_dict['formatted_address']
print(formatted_address)
print('latitude:', lat_val, ', longitude:', lng_val)
