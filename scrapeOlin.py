from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
from time import sleep
import requests
import urllib.request
import os
import re
from pickle import dump, load

def parse_credit_dict(credit_dictionary):
    """
    :param credit_dictionary:
    :return:
    """
    # TODO; THIS ISN'T USED, SEEMED REDUNDANT, HOWEVER, SUS CREDITS NEED TO BE SPLIT OUT NOW ELSEWHERE(a get total fucntion)
    admn_crd = 0
    ahse_crd = 0
    engr_crd = 0
    sci_crd = 0
    mth_crd = 0
    sus_crd = 0
    for credit_typ, credits in credit_dict.items():
        credit_typ.lower()
        if credit_typ == 'admn':
            admn_crd += credits
        elif credit_typ == 'ahse':
            ahse_crd += credits
        elif credit_typ == 'engr':
            engr_crd += credits
        elif credit_typ == 'sci':
            sci_crd += credits
        elif credit_typ == 'mth':
            mth_crd += credits
        elif credit_typ == 'sus':
            ahse_crd += credits / 2
            sci_crd += credits / 2
            sus_crd += credits
    return None

def course_dict(crn, pre_req, co_req, con_req, rec_req, desc, credit_dict, hours, term_requirement=None,
                grade_limit=None, size=32, fall=True, spring=True):
    course = {'crn': crn, 'desc': desc, 'pre_req': pre_req, 'hours': hours, 'term_requirement': term_requirement,
              'grade_limit': grade_limit, 'size': size, 'fall': fall, 'spring': spring, 'co_req': co_req,
              'con_req': con_req, 'rec_req': rec_req, 'credit_dict': credit_dict}
    return course


def parse_cred(credit_div):
    """

    :param credit_div:
    :return:
    """
    if len(credit_div) == 0:
        return {}

    credit_text = credits[0].getText()
    # Check to see if it has parentheses (aka weird split(QEA))
    if '(' in credit_text:
        credit_text = credit_text.split('(', 1)[-1].split(')')[0]
        credit_text.replace(',', '')

    split_credits = credit_text.split()
    credit_dict = {}
    # count by twos and iteare through the list
    for i in range(0, len(split_credits), 2):
        credit_dict[split_credits[i + 1].lower()] = int(split_credits[i])
    return credit_dict


def parse_req(req_div):
    """
    Parse requisites for all different types of requisites
    :param req_div:
    :return: a list that contains what requisites if any
    """
    if len(req_div) == 0 or req_div[0].findChild() is None:  # if there is no data or there was no tag found
        return []

    req_text = req_div[0].contents[-1]
    if any(map(str.isdigit, req_text)):
        req_text = req_text.replace('AND ', '')
        req_list = req_text.split()
        # TODO: check to see if commas are ever present
    else:  # this is a different type of requisite, don't string split
        req_list = [req_text]
    return req_list


def parse_hrs(hrs_div, dict=True):
    if dict:
        hrs = {}
    else:
        hrs = []
    if len(hrs_div) == 0:
        return hrs

    hours_text = hrs_div[0].contents[-1]
    numeric = re.sub("\D", " ", hours_text)
    hrs_split = numeric.split()
    if dict:
        # Make a dictionary with all the diff types
        hrs['contact'] = int(hrs_split[0])
        hrs['noncontact'] = int(hrs_split[1])
        hrs['prep'] = int(hrs_split[2])
    else:
        hrs = hrs_split
    return hrs


def parse_info(info_div):
    if len(info_div) == 0:
        return ''
    info = info_div[0].getText()
    return info



# Set up Scraping links for Beautiful Soup
base_link = "https://olin.smartcatalogiq.com/"
root_link = base_link + "en/2019-20/Catalog/Courses-Credits-Hours"
# Extract the contents of the link
link_page = requests.get(root_link)
soup = bs(link_page.content, 'html.parser')
groups = soup.find_all('a', attrs={"href": re.compile('Catalog/Courses-Credits-Hours/')})  #
print(groups)
# Now lets put those urls into a dictionary
groupDict = []
for aGroup in groups:
    groupUrl = aGroup.get('href')
    group_name = aGroup.getText()
    # print(group_name)
    # print(groupUrl)
    # There are duplicate links so don't duplicate entries
    if group_name not in groupDict:
        groupDict.append({'url': groupUrl})
print(groupDict)

#### Now scrape each of the links
catalog = {}
for group in groupDict:
    print(group)
    print(type(group))
    url = group['url']
    group_link = base_link + url
    print(group_link)

    # Get links for each page and store them in a list
    link_page = requests.get(group_link)
    soup = bs(link_page.content, 'html.parser')

    right_pnl = soup.find_all('div', attrs={"id": 'rightpanel'})  #
    classes = right_pnl[0].find_all('a', attrs={"href": re.compile(url + '/')})  #
    for course in classes:
        # PARSE THE COURSE PAGE!!!!
        course_link = base_link + course.get('href')
        # course_link = "https://olin.smartcatalogiq.com/2019-20/Catalog/Courses-Credits-Hours/ENGR-Engineering/2000/ENGX2000" # Test an individual site!
        crn = course_link.split('/')[-1]
        print(crn)
        link_page = requests.get(course_link)
        soup = bs(link_page.content, 'html.parser')
<<<<<<< HEAD
        credits = soup.find_all('div', attrs={"class": 'credits'})  #

=======
        reqs_pre = soup.find_all('div', attrs={"class": 'sc-preReqs'})
        credits = soup.find_all('div', attrs={"class": 'credits'})
        reqs_co = soup.find_all('div', attrs={"class": 'sc-coReqs'})
        reqs_con = soup.find_all('div', attrs={"class": 'sc-concurrentReqs'})
        reqs_rec = soup.find_all('div', attrs={"class": 'sc-recommendedReqs'})
        hours_div = soup.find_all('div', attrs={"class": 'sc-Attributes'})
        info_div = soup.find_all('div', attrs={"class": 'desc'})

        # print(reqs_pre[0].contents[-1]) # Use contents to get the last child!

        reqs_pre_list = parse_req(reqs_pre)
        reqs_co_list = parse_req(reqs_co)
        reqs_con_list = parse_req(reqs_con)
        reqs_rec_list = parse_req(reqs_rec)
        print("Pre: ", reqs_pre_list)
        print("Co: ", reqs_co_list)
        print("Con: ", reqs_con_list)
        print("Recc: ", reqs_rec_list)
>>>>>>> 778d3364e0beb4d6327c5ae891ba7054d406e71e
        credit_dict = parse_cred(credits)
        print(credit_dict)
        info = parse_info(info_div)
        hours_dict = parse_hrs(hours_div, True)
        print(hours_dict)

