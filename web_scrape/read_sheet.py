from openpyxl import load_workbook
import physician

# File and sheet being used
FILE_PATH = 'C:\\Users\\jalip\\OneDrive\\Documents\\physician_web_scraper\\web_scrape\\Scraping_Sheet_Short.xlsx'
SHEET_NAME = 'Sheet 1 - American Head and Nec'

# Creates a workbook to read from
WB = load_workbook(filename = FILE_PATH)
SHEET = WB[SHEET_NAME]

def get_physicians() -> list[physician.Physician]:
    '''
    Gets all physicians from excel file
    And sets ID, first name, last name, and links
    Returns a physician object
    '''
    list_of_physicians = [] # Contains all physicians

    for line_number in range(2, SHEET.max_row):
        p = physician.Physician()
        p.set_id(SHEET['A' + str(line_number)].value)
        p.set_first_name((SHEET['B' + str(line_number)].value).strip())
        p.set_last_name((SHEET['C' + str(line_number)].value).strip())
        p.set_links('Healthgrades', SHEET['D' + str(line_number)].value)
        p.set_links('Vitals', SHEET['E' + str(line_number)].value)
        p.set_links('RateMDs', SHEET['F' + str(line_number)].value)
        p.set_links('Yelp', SHEET['G' + str(line_number)].value)
        p.set_residency((SHEET['H' + str(line_number)].value).strip())

        list_of_physicians.append(p) # Adds physician to list

    return list_of_physicians