from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import requests
import urllib.request
import os
import re
from pickle import dump, load



class Major:
    """
    This class is used to store information about majors
    """
    def __init__(self, name, reqs_list ):
        self.name = ''
        self.abs_reqs = reqs_list[0]
        reqs_list.pop(0)
        self.one_reqs = []
        for group in reqs_list:
            self.one_reqs.append(group) # list of lists for one required Courses


# Var definitions for bs4

base_link = "https://olin.smartcatalogiq.com/"
root_link = base_link + "en/2019-20/Catalog/Programs-of-Study-and-Degree-Requirements/Academic-Programs/"
major_groups = ['Electrical-and-Computer-Engineering-ECE/', 'Mechanical-Engineering-ME/']


# walk through all majors @olin based on list above
majors = {}
for major in major_groups:
    link_page = requests.get(root_link+major)
    soup = bs(link_page.content, 'html.parser')
    groups_rec_names = soup.find_all('h3', attrs={"class": 'sc-RequiredCoursesHeading1'})  #grab all instances of required course headings
    print(major)
    groups_rec_tables = soup.find_all('table')
    temp_list_major = []
    for table in groups_rec_tables:
        table_links = table.find_all('a', attrs={"class": 'sc-courselink'})  #
        table_temp = []
        for link in table_links:
            # print(link.contents)
            if len(link.contents)>0:
                table_temp.append(link.contents[0])
        temp_list_major.append(table_temp)
    majors[major]= Major(major, temp_list_major)

# Major objects are stored in majors dictionary

print(majors)








    # match up the groups_rec_names with the groups_rec_tables, return as a pickle
