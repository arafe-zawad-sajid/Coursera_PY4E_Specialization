from urllib.request import urlopen, Request
import ssl
from bs4 import BeautifulSoup
import xlsxwriter

workbook = xlsxwriter.Workbook('BD_COVID.xlsx')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
url = 'https://www.worldometers.info/coronavirus/country/bangladesh/'
req = Request(url, headers=headers)
uhand = urlopen(req, context=ctx).read()

soup = BeautifulSoup(uhand, 'html.parser')
tags = soup('script')
for tag in tags:
    if len(tag.attrs) == 1 and tag.get('type') == 'text/javascript':
        lines = tag.get_text().split('\n')
        for line in lines:
            if 'Highcharts' in line:
                pos1 = line.find('(')
                pos2 = line.rfind(',')
                title = line[pos1+2:pos2-1].split(',')
                worksheet = workbook.add_worksheet(title[0])
                print(title)
            if 'categories' in line:
                cat = list()
                pos1 = line.find('[')
                pos2 = line.rfind(']')
                categories = line[pos1+1:pos2].split(',')
                row = 1
                worksheet.write(0, 0, 'month_day')
                for date in categories:
                    worksheet.write(row, 0, date.strip('"'))
                    row += 1
                print(len(cat))
            if 'data: [' in line:
                data = list()
                pos1 = line.find('[')
                pos2 = line.rfind(']', 0, -3)
                data = line[pos1+1:pos2].split(',')
                row = 1
                worksheet.write(0, 1, 'number')
                for number in data:
                    worksheet.write(row, 1, number)
                    row += 1
                print(len(data))
                break
workbook.close()
