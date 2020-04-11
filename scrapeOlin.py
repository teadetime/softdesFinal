from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
from time import sleep
import requests
import urllib.request
import os
import re
from pickle import dump, load
import sys


class Major:
    """
    This class is used to store information about majors
    """

    def __init__(self, name, reqs_list):
        self.name = name
        self.abs_reqs = reqs_list[0]
        # reqs_list.pop(0)
        self.one_reqs = []
        for group in reqs_list:
            self.one_reqs.append(group)  # list of lists for one required Courses


def pickle_data(file_path, data, overwrite):
    """
    Pickle a specific piece of data in binary. Can be pickled at any directory, will not overwrite current data unless
        overwite is specified
    :param file_path: Npath to file to be pickled. Can contain just a file name to pickle in CWD
    :param data: The data that will be pickled
    :param overwrite: Boolean that indicates whether the file should be overwritten even if it exists
    :return: #TODO Nothing currently should return True if succesful
    """
    sys.setrecursionlimit(10 ** 6)
    if not os.path.exists(file_path) or overwrite:
        f = open(file_path, "wb")
        dump(data, f)
        f.close()


def load_pickle_data(file_path):
    """
    Unpickles data stored at a given file path (or filename in CWD) and returns it
    :param file_path: path to file that is to be un-pickled (can be file name for items in CWD)
    :return: Returns None or that data that was stored in pickle form at the location
    """
    # Initialize data so that None is returned if file path doesn't work
    pickled_data = None
    if os.path.exists(file_path):
        f = open(file_path, "rb+")
        pickled_data = load(f)
        f.close()
    return pickled_data


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
    for credit_typ, credits in credit_dictionary.items():
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

    credit_text = credit_div[0].getText().lower()
    if not bool(re.search(r'\d', credit_text)):
        # then this is likely a special topics class with variable credits
        credit_text.replace('variable credits', '')
        return {credit_text: 4, 'flagged': True}
    # Check to see if it has parentheses (aka weird split(QEA))
    if '(' in credit_text:
        credit_text = credit_text.split('(', 1)[-1].split(')')[0]
        credit_text.replace(',', '')

    split_credits = credit_text.split()
    if len(split_credits) % 2 != 0:
        return {'elec': int(split_credits[0])}
    credit_dict = {}
    # count by twos and iteare through the list
    for i in range(0, len(split_credits), 2):
        credit_dict[split_credits[i + 1]] = int(split_credits[i])
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


def get_group_links(page_base_link, other_link):
    # Set up Scraping links for Beautiful Soup
    root_link = page_base_link + other_link
    # Extract the contents of the link
    link_page = requests.get(root_link)
    soup = bs(link_page.content, 'html.parser')
    right_pnl = soup.find_all('div', attrs={"id": 'rightpanel'})
    groups = right_pnl[0].find_all('a', attrs={"href": re.compile('Catalog/Courses-Credits-Hours/')})  #
    # Now lets put those urls into a dictionary
    groupLst = []
    for aGroup in groups:
        groupUrl = aGroup.get('href')
        group_name = aGroup.getText()
        # There are duplicate links so don't duplicate entries
        if group_name not in groupLst:
            groupLst.append({'url': groupUrl})
    return groupLst


def parse_bulid_course(a_course_link, crn):
    print(crn)
    course_page = requests.get(a_course_link)
    course_soup = bs(course_page.content, 'html.parser')
    reqs_pre = course_soup.find_all('div', attrs={"class": 'sc-preReqs'})
    page_credits = course_soup.find_all('div', attrs={"class": 'credits'})
    reqs_co = course_soup.find_all('div', attrs={"class": 'sc-coReqs'})
    reqs_con = course_soup.find_all('div', attrs={"class": 'sc-concurrentReqs'})
    reqs_rec = course_soup.find_all('div', attrs={"class": 'sc-recommendedReqs'})
    hours_div = course_soup.find_all('div', attrs={"class": 'sc-Attributes'})
    info_div = course_soup.find_all('div', attrs={"class": 'desc'})
    reqs_pre_list = parse_req(reqs_pre)
    reqs_co_list = parse_req(reqs_co)
    reqs_con_list = parse_req(reqs_con)
    reqs_rec_list = parse_req(reqs_rec)
    credit_dict = parse_cred(page_credits)
    # print(credit_dict)
    info = parse_info(info_div)
    hours_dict = parse_hrs(hours_div, True)
    # print(hours_dict)
    return course_dict(crn, reqs_pre_list, reqs_co_list, reqs_con_list, reqs_rec_list, info, credit_dict, hours_dict)


def collect_majors(root_lnk, major_link, major_nm):
    link_page = requests.get(root_lnk + major_link)
    soup = bs(link_page.content, 'html.parser')
    groups_rec_names = soup.find_all('h3', attrs={
        "class": 'sc-RequiredCoursesHeading1'})  # grab all instances of required course headings
    major_link = major_link.replace('/', '')
    major_link = major_link.split('-')[-1]
    groups_rec_tables = soup.find_all('table')
    temp_list_major = []
    for table in groups_rec_tables:
        table_links = table.find_all('a', attrs={"class": 'sc-courselink'})  #
        table_temp = []
        for link in table_links:
            # print(link.contents)
            if len(link.contents) > 0:
                table_temp.append(link.contents[0])
        temp_list_major.append(table_temp)
    # print(temp_list_major)
    return Major(major_nm, temp_list_major)


if __name__ == '__main__':
    base_link = "https://olin.smartcatalogiq.com/"
    groupDict = get_group_links(base_link, "en/2019-20/Catalog/Courses-Credits-Hours")

    # Now scrape each of the links

    catalog = {}
    for group in groupDict:
        url = group['url']
        group_link = base_link + url
        print(group_link)
        # Get links for each page and store them in a list
        link_page = requests.get(group_link)
        soup = bs(link_page.content, 'html.parser')
        right_pnl = soup.find_all('div', attrs={"id": 'rightpanel'})
        classes = right_pnl[0].find_all('a', attrs={"href": re.compile(url + '/')})

        for course in classes:
            # PARSE THE COURSE PAGE!!!!
            course_link = base_link + course.get('href')
            # course_link = "https://olin.smartcatalogiq.com/en/2019-20/Catalog/Courses-Credits-Hours/OIE-Olin-Intro-Experience/1000/OIE1000" # Test an individual site!
            crn = course_link.split('/')[-1]
            catalog[crn] = parse_bulid_course(course_link, crn)
            sleep(.2)
    pickle_data('catalog_pickle', catalog, True)

    # Now get the data for majors
    majors = {}
    major_root_link = base_link + "en/2019-20/Catalog/Programs-of-Study-and-Degree-Requirements/Academic-Programs/"
    major_groups = ['Electrical-and-Computer-Engineering-ECE/', 'Mechanical-Engineering-ME/']

    for major in major_groups:
        major_name = major.replace('/', '').split('-')[-1]
        majors[major_name] = collect_majors(major_root_link, major, major_name)
        # TODO: Add a timestamp into the majors dict
    pickle_data('majors_pickle', majors, True)