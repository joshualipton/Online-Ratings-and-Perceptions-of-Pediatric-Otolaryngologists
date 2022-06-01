from asyncore import write
import read_sheet
import webscrape
import write_sheet
from openpyxl.workbook import Workbook

if __name__ == '__main__':
    physicians = read_sheet.get_physicians()
    webscrape.webscrape_list(physicians)

    row = 2

    headers       = ['ID','First Name', 'Last Name', 'Source', 'Overall Rating', 'Residency', 
        'Research Tier', 'Comment Date', 'Comment Rating', 'Comment', 'Comment Helpful Count']

    wb = Workbook()
    page = wb.active
    page.title = 'Tier_Data'
    page.append(headers) # write the headers to the first line

    for physician in physicians:
        row = write_sheet.write_physician(physician, row, wb, page)

    wb.save(filename = 'Tier_Data.xlsx')
