import physician
import requests
from bs4 import BeautifulSoup
import json
import math

def convert_to_date(date: str) -> str:
    '''
    Converts date in format 'Jan 03, 2021' to 1/3/21
    '''
    formatted_date = ''
    date_conversion_dict = {'Jan' : 1, 'Feb' : 2, 'Mar' : 3, 'Apr' : 4,
                            'May' : 5, 'Jun' : 6, 'Jul' : 7, 'Aug' : 8,
                            'Sep' : 9, 'Oct' : 10, 'Nov' : 11, 'Dec' : 12}
    date = date.split()

    if date[0] not in date_conversion_dict:
        raise AttributeError(f'{date[0]} not in date_conversion_dict')
    else:
        formatted_date += str(date_conversion_dict[date[0]]) + '/'
        formatted_date += str(int(date[1][:-1])) + '/'
        formatted_date += date[2][2:]
    
    return formatted_date
    

def set_source(physician: physician.Physician, source: str) -> None:
    '''
    Sets source during webscrape
    '''
    physician.set_source(source)

def set_tier(physician: physician.Physician) -> None:
    '''
    Sets tier based on residency
    '''
    tier_dict = {'T20_Rsrch' : ['Harvard', 'Grossman', 'Columbia', 'Hopkins', 'Francisco', 
                                'Duke', 'Perelman', 'Stanford', 'University of Washington', 
                                'Yale', 'Icahn', 'Washington University', 'Vanderbilt', 
                                'Cornell', 'Mayo', 'Mayo Medical School', 'University of Pittsburgh', 'Northwestern', 
                                'University of Michigan', 'Los Angeles', 'San Diego', 'Pritzker'],
                'T50_Rsrch' : ['Baylor', 'Emory', 'Case Western', 'University of North Carolina', 
                                'Southwestern', 'Colorado', 'Southern California', 'Maryland', 
                                'Ohio State', 'University of Virginia', 'Boston', 'Oregon Health and Science', 
                                'Alabama', 'Brown', 'University of Utah', 'Albert Einstein', 
                                'University of Florida', 'University of Rochester', 'University of Wisconsin', 
                                'Indiana University', 'University of Iowa', 'University of Cincinnati', 
                                'University of Miami', 'University of Minnesota', 'University of South Florida', 
                                'Dartmouth', 'University of Massachusetts', 'Texas Health and Science', 
                                'Wake Forest', 'Davis'],
                'T20_PC' : ['University of Washington', 'Francisco', 'Minnesota', 'Oregon Health and Science', 
                            'University of North Carolina', 'University of Colorado', 'University of Nebraska', 
                            'Davis', 'Harvard', 'University of Kansas', 'University of Massachusetts', 
                            'University of PIttsburgh', 'Los Angeles', 'Brown', 'Maryland', 'Baylor', 'Iowa', 
                            'New Mexico', 'Texas Southwestern', 'University of Michigan', 'University of Pennsylvania', 
                            'University of Wisconsin'],
                'T50_PC' : ['Indiana University', 'University of Hawaii', 'University of Utah', 'East Carolina University', 
                            'University of Alabama', 'University of Rochester', 'University of Tennessee', 'Stanford', 
                            'Pritzker', 'Ohio State', 'San Diego', 'University of Vermont', 'Virginia', 'Boston University', 
                            'Dartmouth', 'Mayo', 'University of Arkansas', 'University of North Texas', 
                            'University of Texas Health Science Center', 'Emory', 'Northwestern', 'Vanderbilt', 'Cornell', 
                            'Tufts', 'University of Oklahoma', 'Grossman', 'Texas Tech University Health Sciences Center', 
                            'University of Florida', 'Virginia Commonwealth'],
                'T20_Resi' : ['Memorial Sloan', 'Massachusetts General', 'Hopkins', 'Mayo', 'San Fran', 'Penn Presbyterian', 
                                'Ohio State', 'University of Michigan', 'Vanderbilt', 'MD Anderson', 'Los Angeles', 'UCLA', 
                                'Stanford', 'MUSC Health', 'OHSU', 'Presbyterian', 'University of Kansas', 'Cedars-Sinai', 
                                'Brigham', 'Barnes-Jewish']
                }
    
    if physician.get_residency() == 'N/A':
        physician.set_tier('N/A')
        return

    found = False
    for key, _ in tier_dict.items():
        if physician.get_tier() in tier_dict[key]:
            physician.set_residency = key
            found = True
            break
    
    if found == False:
        raise AttributeError(f'Residency: {physician.get_residency()} not in a tier')


def set_overall_rating(physician: physician.Physician, soup: BeautifulSoup) -> None:
    '''
    Sets overall rating during webscrape
    '''
    overall_rating = soup.select('div.overall-rating-wrapper strong')
    try:
        physician.set_overall_rating(float(overall_rating[0].text.strip())) # Converts the html to float
    except IndexError:
        physician.set_overall_rating('N/A')

def set_comment(physician: physician.Physician, soup: BeautifulSoup) -> None:
    '''
    Sets the comment as a 3-tuple of (date, rating, comment)
    '''
    # API GET request
    url = 'https://www.healthgrades.com/api4/providerprofile/comments'
    pwid = physician.get_link('Healthgrades')[-5:]
    page_num = 1
    data = {'currentPage': page_num, 'includeAllAnswers': True, 'perPage': 5, 'pwid': pwid, 'sortOption': 1}
    headers = {"accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"101\", \"Google Chrome\";v=\"101\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "Referer": physician.get_link('Healthgrades'),
    "Referrer-Policy": "strict-origin-when-cross-origin"}

    request = requests.post(url, data = data, headers=headers)

    json_data = json.loads(request.text)

    # If no comments then skip
    if json_data['totalCommentCount'] == 0:
        physician.add_comment('N/A')
        return

    total_comment_count = json_data['totalCommentCount']
    num_loops = math.ceil(total_comment_count / 5)

    for i in range(0, num_loops):
        page_num += 1

        data = {'currentPage': page_num, 'includeAllAnswers': True, 'perPage': 5, 'pwid': pwid, 'sortOption': 1}
        headers = {"accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"101\", \"Google Chrome\";v=\"101\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "Referer": physician.get_link('Healthgrades'),
        "Referrer-Policy": "strict-origin-when-cross-origin"}
        
        for j in range(0, len(json_data['results'])):
            comment_text = json_data['results'][j]['commentText'].strip()
            comment_date = convert_to_date(json_data['results'][j]['submittedDate'])
            comment_rating = json_data['results'][j]['overallScore']

            physician.add_comment((comment_date, comment_rating, comment_text))
        
def webscrape_healthgrades(physician: physician.Physician) -> None:
    '''
    Webscrapes healthgrades for the given physician
    '''
    url = physician.get_link('Healthgrades')

    if url != 'N/A':
        set_source(physician, 'Healthgrades')
        set_tier(physician)

        request = requests.get(url) # Gets HTML of website
        soup = BeautifulSoup(request.content, 'html.parser')

        set_overall_rating(physician, soup)
        set_comment(physician, soup)
        

def webscrape_links(physician: physician.Physician) -> None:
    '''
    Calls the webscrape on each link in the physican
    '''
    if physician.get_link('Healthgrades') != 'N/A':
        webscrape_healthgrades(physician)

    # if physician.get_link('Vitals' != 'N/A'): change .html to /reviews?page=1&sort=updated_at_dt%20desc
    #     webscrape_vitals(physician)

    # if physician.get_link('RateMDs' != 'N/A'): Does by page num in link
    #     webscrape_ratemds(physician)

    # if physician.get_link('Yelp' != 'N/A'): Does by num queries in link
    #     webscrape_yelp(physician)
    

def webscrape_list(list_of_physicians: list[physician.Physician]) -> None:
    '''
    Calls webscrape on all physicians
    '''
    for physician in list_of_physicians:
        webscrape_links(physician)

