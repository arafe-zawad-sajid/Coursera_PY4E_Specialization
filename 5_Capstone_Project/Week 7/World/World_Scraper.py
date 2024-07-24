from urllib.request import urlopen, Request
import ssl
from bs4 import BeautifulSoup
import xlsxwriter

workbook = xlsxwriter.Workbook('World_COVID.xlsx')
worksheet = workbook.add_worksheet('all over the world')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
url = 'https://www.worldometers.info/coronavirus'
req = Request(url, headers=headers)
uhand = urlopen(req, context=ctx).read()

soup = BeautifulSoup(uhand, 'html.parser')
tags = soup('tr')
serial = 0
countries = dict()
colnames = ['#', 'Country, Other', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered', 'Active Cases', 'Serious, Critical', 'Tot Cases/ 1M pop', 'Deaths/ 1M pop', 'TotalTests', 'Tests/ 1M pop', 'Population', 'Continent']
col = 0
for name in colnames:
    print(name, end=' | ')
    worksheet.write(0, col, name)
    col += 1
print()
row = 1
for tag in tags:
    if len(tag.attrs)==1 and 'style' in tag.attrs:
        data = tag.get_text().split('\n')  # index 0 and index 16 has empty strings
        serialnow = int(data[1])
        if serialnow < serial:
            break
        serial = serialnow
        col = 0
        for val in data[1:-1]:
            print(val, end=' | ')
            worksheet.write(row, col, val)
            col += 1
        row += 1
        print()
workbook.close()
