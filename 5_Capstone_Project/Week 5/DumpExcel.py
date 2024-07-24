import xlrd
wb = xlrd.open_workbook('Covid19_BD.xlsx')

sheets = wb.sheet_names()
for sheet in sheets:
    ws = wb.sheet_by_name(sheet)
    print('sheet:', sheet)
    for i in range(ws.nrows):
        print(ws.row_values(i))
    print()
