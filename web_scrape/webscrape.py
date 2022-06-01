import physician
import requests
from bs4 import BeautifulSoup
import json
import math
import random
import time

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
    tier_dict = {'T20_Rsrch' : ['Harvard', 'Harvard University', 'Harvard Medical School', 'Grossman', 'Columbia', 'Hopkins', 'Johns Hopkins Hospital', 'Johns Hopkins University', 'Francisco', 
                                'Duke', 'Duke University Health System', 'Duke University Hospital', 'Perelman', 'Stanford', 'Stanford University', 'University of Washington', 'Washington University/Barnes Hospital', 'University of Washington Medical Center', 
                                'Yale', 'Icahn', 'Icahn School of Medicine at Mount Sinai', 'Washington University', 'Washington University School of Medicine in St. Louis', 'Washington University in St. Louis', 'Washington University in St. Louis', 'Vanderbilt', 'Vanderbilt University', 
                                'Cornell', 'Mayo', 'Mayo Medical School', 'University of Pittsburgh', 'University of Pittsburg', 'University of Pittsburgh Medical Center', 'University Pittsburgh Medical Center Hospitals', 'Northwestern', 'McGaw Medical Center of Northwestern University', 
                                'Northwestern University, Feinberg School of Medicine', 'University of Michigan', 'University of Michigan Health System', 'Los Angeles', 'San Diego', 'Pritzker'],
                'T50_Rsrch' : ['Baylor', 'Baylor College of Medicine', 'Baylor University Medical Center', 'Emory', 'Case Western', 'Case Western University', 'University of North Carolina', 'University of Michigan Hospitals and Health Centers', 
                                'Southwestern', 'Colorado', 'Southern California', 'University of Southern California', 'USC Medical Center', 'Maryland', 'LAC + USC Medical Center',  
                                'Ohio State', 'The Ohio State Wexner Medical Center', 'University of Virginia', 'Boston', 'Oregon Health and Science', 'Oregon Health and Science University', 'Oregon Health Sciences University',  
                                'Alabama', 'University of Alabama at Birmingham', 'Brown', 'University of Utah', 'University of Utah, Salt Lake City', 'University of Utah Medical Center', 'Albert Einstein', 
                                'University of Florida', 'University of Rochester', 'University of Rochester School of Medicine', 'University of Wisconsin', 
                                'Indiana University', 'University of Iowa', 'University of Iowa Hospitals and Clinics', 'University of Iowa, College of Medicine', 'University of Cincinnati', 
                                'University of Miami', 'University of Minnesota', 'University of South Florida', 'University of South Florida Morsani School of Medicine, Mayo School of Graduate Medical Education', 'USF College of Medicine', 'University of South Florida College of Medicine', 
                                'Dartmouth', 'University of Massachusetts', 'Texas Health and Science', 
                                'Wake Forest', 'Davis'],
                'T20_PC' : ['University of Washington', 'Francisco', 'Minnesota', 'Oregon Health and Science', 
                            'University of North Carolina', 'University of North Carolina - Chapel Hill', 'University of North Carolina at Chapel Hill', 'University of Colorado', 'University of Colorado School of Medicine', 'University of Nebraska', 'University of Nebraska Medical Center', 
                            'Davis', 'Harvard', 'University of Kansas', 'University of Kansas Medical Center', 'University of Massachusetts', 
                            'University of Pittsburgh', 'University of Pittsburgh School of Medicine', 'University of Pittsburgh School of Dental Medicine', 'University of Pittsburg Medical Center', 'Los Angeles', 'Brown', 'Maryland', 'University of Maryland Medical Center', 'Baylor', 'Iowa', 
                            'New Mexico', 'Texas Southwestern', 'University of Michigan', 'University of Michicagn', 'University of Pennsylvania', 'University of Pennsylvania School of Medicine', 'Hospital of the University of Pennsylvania', 
                            'University of Pennsylvania Health System', 'Hospital of The University of PA', 'University of Wisconsin'],
                'T50_PC' : ['Indiana University', 'University of Hawaii', 'University of Utah', 'East Carolina University', 
                            'University of Alabama', 'University of Alabama Medical Center', 'University of Rochester', 'University of Tennessee', 'University of Tennessee Health Science Center', 'Stanford', 
                            'Pritzker', 'Ohio State', 'Ohio State UMC', 'San Diego', 'University of California, San Diego', 'University of California - San Diego', 'University of Vermont', 'The University of Vermont Medical Center', 'Virginia', 'Boston University', 'Boston Medical Center',
                            'Dartmouth', 'Mayo', 'University of Arkansas', 'University of North Texas', 
                            'University of Texas Health Science Center', 'University of Texas Medical Branch', 'Emory', 'Emory University', 'Northwestern', 'Vanderbilt', 'Cornell', 
                            'Tufts', 'Boston University/Tufts University', 'University of Oklahoma', 'University of Oklahoma, University of Colorado Health Science Center', 'University Of Oklahoma College of Medicine', 'Grossman', 'Texas Tech University Health Sciences Center', 
                            'University of Florida', 'Virginia Commonwealth', 'Tufts University School of Medicine'],
                'T20_Resi' : ['Memorial Sloan', 'Massachusetts General', 'Hopkins', 'Mayo', 'San Fran', 'University of California, San Francisco', 'Penn Presbyterian', 
                                'Ohio State', 'University of Michigan', 'Vanderbilt', 'MD Anderson', 'Los Angeles', 'UCLA', 'UCLA Medical Center',  'University of California, Los Angeles School of Medicine', 'University of California, Los Angeles School of Medicine', 
                                'Stanford', 'MUSC Health', 'OHSU', 'Presbyterian', 'University of Kansas', 'Cedars-Sinai', 
                                'Brigham', 'Barnes-Jewish', 'University of California, Los Angeles School of Medicine']
                }

    if physician.get_residency() == 'N/A':
        physician.set_tier('N/A')
        print('1')
        return

    found = False
    for key, _ in tier_dict.items():
        if physician.get_residency() in tier_dict[key]:
            physician.set_tier(key)
            found = True
            break
    
    if found == False and physician.get_residency() not in ['University Hospital of Louvain at Mont-Godinne', 'Thomas Jefferson University Hospitals']:
        physician.set_tier('N/A')
        print(3)
    


def set_overall_rating_healthgrades(physician: physician.Physician, soup: BeautifulSoup) -> None:
    '''
    Sets overall rating during webscrape
    '''
    overall_rating = soup.select('div.overall-rating-wrapper strong')
    try:
        physician.set_overall_rating('Healthgrades', float(overall_rating[0].text.strip())) # Converts the html to float
    except IndexError:
        physician.set_overall_rating('Healthgrades', 'N/A')

def set_comment_healthgrades(physician: physician.Physician, soup: BeautifulSoup) -> None:
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

    total_comment_count = json_data['totalCommentCount']
    num_loops = math.ceil(total_comment_count / 5)

    for i in range(0, num_loops):
        # time.sleep(random.random()*10)
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
            useful_count = json_data['results'][j]['helpfulCount']

            physician.add_comment((comment_date, 'Healthgrades', comment_rating, comment_text, useful_count))
        
def webscrape_healthgrades(physician: physician.Physician) -> None:
    '''
    Webscrapes healthgrades.com for the given physician
    '''
    url = physician.get_link('Healthgrades')

    if url != 'N/A':
        set_source(physician, 'Healthgrades')
        # set_tier(physician)

        request = requests.get(url) # Gets HTML of website
        soup = BeautifulSoup(request.content, 'html.parser')

        set_overall_rating_healthgrades(physician, soup)
        set_comment_healthgrades(physician, soup)

def set_overall_rating_vitals(physician: physician.Physician, soup: BeautifulSoup) -> None:
    '''
    Sets overall rating during webscrape
    '''
    time.sleep(random.random()*10)
    overall_rating = soup.select('#app > div.top-section > div.profile-header-container.loc-vs-prvdr > header > div > div > div.header-info > div > div.name-info > div > div.rating-section > a.ratings > span.rating-score')
    try:
        physician.set_overall_rating('Vitals', float(overall_rating[0].text.strip())) # Converts the html to float
    except IndexError:
        physician.set_overall_rating('Vitals', 'N/A')

def webscrape_vitals(physician: physician.Physician) -> None:
    '''
    Webscrapes vitals.com for the given physician
    '''
    url = physician.get_link('Vitals')
    page = 1

    # Redirects url to the reviews page
    if '.html' in url:
        url = url[:-5]
        url += f'/reviews?page={page}&sort=updated_at_dt%20desc'

    if url != 'N/A':
        set_source(physician, 'Vitals')

    #     headers = {'authority': 'www.vitals.com',
    #                 'method': 'GET',
    #                 'path': '/doctors/Dr_Adam_Luginbuhl/reviews',
    #                 'scheme': 'https',
    #                 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #                 'accept-encoding': 'gzip, deflate, br',
    #                 'accept-language': 'en-US,en;q=0.9',
    #                 'cache-control': 'max-age=0',
    #                 'cookie': 'gtinfo={"ct":"Irvine","c":"Orange","cc":"6059","st":"CA","sc":"5","z":"92697","lat":"33.65","lon":"-117.84","dma":"803","cntr":"usa","cntrc":"840","tz":null,"ci":"169.234.45.66"}; notice_behavior=implied,us; _ga=GA1.1.280728103.1653438674; AMCVS_16AD4362526701720A490D45%40AdobeOrg=1; usprivacy=1YNN; s_cc=true; aam_uuid=91305347862693971774061348772953748111; _ibp=0:l3kup39v:f95c0d05-b5f2-4e1c-aea8-40a51ae5865c; TapAd_DID=7b3647c3-c14a-43c4-8917-d452f5028cec; notice_preferences=2:; notice_gdpr_prefs=0,1,2:; aam=aam%3D999996%2C529440%2C32964%2C32920%2C318069%2C663590%2C32539%2C617784%2C18091421%2C18292951%2C21558705%2C22156106%2C22833965%2C22876027%2C23269831%2C23376301%2C23421578%2C24060393; initial_url_path={%22url%22:%22%2Fdoctors%2FDr_Adam_Luginbuhl%2Freviews%22}; s_sq=%5B%5BB%5D%5D; __cfruid=4ddc06e72654592012cac55754a9a775651e3c9e-1653707609; __cf_bm=5cc70kut0gXZ76qYiSMZCN9f7y7GGEhnimld8nfb2fQ-1653707610-0-ARwjyKakQlDYoM83NBqkbqJpH0QvQAMTn2Iy+VhQwb97pO7i4UO24ttK1sod7/mimw3HqBT20E+dvOXVHqUiysyzp62o48BjOzaA1V+hUTwAn5OAZQ9W6OFEbKhBwCcpyLHSOoc/gHVasL0z6IYc+BW5eMOPbpEqzBHlnRISBohbSyGe04cI7LbHs1WPjPFULg==; mnet_session_depth=1%7C1653707611077; _ga_3ZVJC9H4TB=GS1.1.1653707611.5.0.1653707611.0; ui={%22expmatch%22:1%2C%22vtime%22:27561793}; fpci={%22iafValue%22:1%2C%22url%22:%22www.vitals.com%2Fdoctors%2FDr_Adam_Luginbuhl%2Freviews%22}; AMCV_16AD4362526701720A490D45%40AdobeOrg=-432600572%7CMCIDTS%7C19141%7CMCMID%7C91511255161485384144041336488334773784%7CMCAAMLH-1654312411%7C9%7CMCAAMB-1654312411%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1653714811s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.5.2; _ibs=0:l3kup39x:87126a4d-080b-40f0-8864-c106f5a314d6',
    #                 'referer': 'https://www.vitals.com/doctors/Dr_Adam_Luginbuhl.html',
    #                 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    #                 'sec-ch-ua-mobile': '?0',
    #                 'sec-ch-ua-platform': "Windows",
    #                 'sec-fetch-dest': 'document',
    #                 'sec-fetch-mode': 'navigate',
    #                 'sec-fetch-site': 'same-origin',
    #                 'sec-fetch-user': '?1',
    #                 'upgrade-insecure-requests': '1',
    #                 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36}'
    #                 }   
        
    #     request = requests.post(url, headers=headers)
    #     json_data = json.loads(request.text)


        # with requests.session() as s:

        #     # load cookies:
        #     s.get(url, headers=headers)

        #     # get data:
        #     data = s.get(url, headers=headers).json()


        # headers = {'User-agent': 'Mozilla/5.0'}

        # request = requests.get('https://www.vitals.com/doctors/Dr_Adam_Luginbuhl/reviews', headers = headers) # Gets HTML of website
        # page = urllib.request.urlopen(request)
        # soup = BeautifulSoup(request.content, 'html.parser')

        # set_overall_rating_vitals(physician, soup)
        # set_comment_vitals(physician, soup)
        
def webscrape_ratemds(physician: physician.Physician) -> None:
    '''
    Webscrapes ratemds.com for the given physician
    '''
    page_num = 1
    url = physician.get_link('RateMDs') + f'/?page={page_num}'

    if url != 'N/A':
        set_source(physician, 'RateMDs')
        # set_tier(physician)
        time.sleep(random.random()*10)

        request = requests.get(url) # Gets HTML of website
        soup = BeautifulSoup(request.content, 'html.parser')

        # set_overall_rating_healthgrades(physician, soup)
        # set_comment_healthgrades(physician, soup)

def set_overall_rating_yelp(physician: physician.Physician, soup: BeautifulSoup) -> None:
    '''
    Sets overall rating during webscrape
    '''
    overall_rating = soup.select('#main-content > div.margin-b3__09f24__l9v5d.border-color--default__09f24__NPAKY > div > div > div.arrange__09f24__LDfbs.gutter-1-5__09f24__vMtpw.vertical-align-middle__09f24__zU9sE.margin-b2__09f24__CEMjT.border-color--default__09f24__NPAKY > div:nth-child(1) > span > div')

    try:
        physician.set_overall_rating('Yelp', float(overall_rating[0]['aria-label'][0])) # Converts the html to float
    except IndexError:
        physician.set_overall_rating('Yelp', 'N/A')

def set_comment_yelp(physician: physician.Physician, soup: BeautifulSoup) -> None:
    '''
    Sets comment during webscrape
    '''
    comments = soup.find_all('div', {'review__09f24__oHr9V border-color--default__09f24__NPAKY'})

    for comment in comments:
        comment_tag = comment.find('span', {'raw__09f24__T4Ezm'})
        comment_text = comment_tag.text



        rating_tag = comment.find('div', {'i-stars__09f24__M1AR7 i-stars--regular-5__09f24__tKNMk border-color--default__09f24__NPAKY overflow--hidden__09f24___ayzG', 
                                            'i-stars__09f24__M1AR7 i-stars--regular-1__09f24__o88Iy border-color--default__09f24__NPAKY overflow--hidden__09f24___ayzG',
                                            'i-stars__09f24__M1AR7 i-stars--regular-2__09f24__mq_AY border-color--default__09f24__NPAKY overflow--hidden__09f24___ayzG',
                                            'i-stars__09f24__M1AR7 i-stars--regular-4__09f24__qui79 border-color--default__09f24__NPAKY overflow--hidden__09f24___ayzG',
                                            'i-stars__09f24__M1AR7 i-stars--regular-3__09f24__sRNTp border-color--default__09f24__NPAKY overflow--hidden__09f24___ayzG'})
        rating = rating_tag['aria-label'][0]

        comment_date = comment.find('span', {'css-chan6m'}).text



        try:
            useful_count = comment.find('span', {'css-1lr1m88'}).text.strip()
            physician.add_comment((comment_date, 'Yelp', rating, comment_text, useful_count))
        except AttributeError:
            useful_count = 0
            physician.add_comment((comment_date, 'Yelp', rating, comment_text, useful_count))

    
def webscrape_yelp(physician: physician.Physician) -> None:
    '''
    Webscrapes yelp.com for the given physician
    '''
    time.sleep(random.random()*10)
    num_queries = 0
    url = physician.get_link('Yelp')
    # url = f'https://www.yelp.com/biz/chatime-irvine-irvine-2?start={num_queries}'
    request = requests.get(url) # Gets HTML of website
    soup = BeautifulSoup(request.content, 'html.parser')
    total_num_queries = soup.select('#main-content > div.margin-b3__09f24__l9v5d.border-color--default__09f24__NPAKY > div > div > div.arrange__09f24__LDfbs.gutter-1-5__09f24__vMtpw.vertical-align-middle__09f24__zU9sE.margin-b2__09f24__CEMjT.border-color--default__09f24__NPAKY > div.arrange-unit__09f24__rqHTg.arrange-unit-fill__09f24__CUubG.border-color--default__09f24__NPAKY.nowrap__09f24__lBkC2 > span')
    
    if len(total_num_queries) > 0:
        num_queries_left = int(total_num_queries[0].text[0])    
    else:
        num_queries_left = 1

    while num_queries_left > 0:
        # url = f'https://www.yelp.com/biz/chatime-irvine-irvine-2?start={num_queries}'
        url = physician.get_link('Yelp') + f'?start={num_queries}'

        if url != 'N/A':
            set_source(physician, 'Yelp')
            # set_tier(physician)

            request = requests.get(url) # Gets HTML of website
            soup = BeautifulSoup(request.content, 'html.parser')

            set_overall_rating_yelp(physician, soup)
            set_comment_yelp(physician, soup)
        
        num_queries_left -= 10
        num_queries += 10

def webscrape_links(physician: physician.Physician) -> None:
    '''
    Calls the webscrape on each link in the physican
    '''
    # if physician.get_link('Healthgrades') != 'N/A':
    #     webscrape_healthgrades(physician)

    # if physician.get_link('Vitals') != 'N/A': # change .html to /reviews?page=1&sort=updated_at_dt%20desc
    #     webscrape_vitals(physician)

    # if physician.get_link('RateMDs') != 'N/A': # Does by page num in link
    #     webscrape_ratemds(physician)

    # if physician.get_link('Yelp') != 'N/A': # Does by num queries in link
    #     webscrape_yelp(physician)
    

def webscrape_list(list_of_physicians: list[physician.Physician]) -> None:
    '''
    Calls webscrape on all physicians
    '''
    for physician in list_of_physicians:
        set_tier(physician)
        webscrape_links(physician)

