import read_sheet
import webscrape

if __name__ == '__main__':
    physicians = read_sheet.get_physicians()
    webscrape.webscrape_list(physicians)