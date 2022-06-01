from openpyxl.workbook import Workbook
import physician





# Data to write:
def write_physician(physician: physician.Physician, row: int, wb, page) -> int:
    '''
    Wrties a single physician
    '''
    sources_set = set()

    print(physician.get_tier())

    for date, source, rating, comment, useful_count in physician.get_comments():
        sources_set.add(source)

        data = [physician.get_id(), physician.get_first_name(), physician.get_last_name(), source,
                physician.get_overall_rating(source), physician.get_residency(), physician.get_tier(), date, rating, comment, useful_count]

        for col in range(0, len(data)):
            page.cell(row, col + 1).value = data[col]

        row += 1
    
    # Add defualt for sources with no link
    missing_sources = {'Healthgrades', 'Vitals', 'RateMDs', 'Yelp'} - sources_set
    for source in missing_sources:
        data = [physician.get_id(), physician.get_first_name(), physician.get_last_name(), source,
                physician.get_overall_rating(source), physician.get_residency(), physician.get_tier(), 'N/A', 'N/A', 'N/A', 'N/A']

        for col in range(0, len(data)):
            page.cell(row, col + 1).value = data[col]

        row += 1
    return row