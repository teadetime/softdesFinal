from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import requests
import urllib.request
import os
import re
from pickle import dump, load



# Technical Considerations & Needs
"""
Grab Major
Grab different types of requirement courses, differentiate by optionality






Workflow:
setup specific functions
setup vars for url access, etc.

"""

# function definitions



# Var definitions for bs4

base_link = "https://olin.smartcatalogiq.com/"
root_link = base_link + "en/2019-20/Catalog/Programs-of-Study-and-Degree-Requirements/Academic-Programs/"
major_groups = ['Electrical-and-Computer-Engineering-ECE/', 'Mechanical-Engineering-ME/']


# walk through all majors @olin based on list above
for major in major_groups:
    link_page = requests.get(root_link+major)
    soup = bs(link_page.content, 'html.parser')
    groups_rec_names = soup.find_all('h3', attrs={"class": 'sc-RequiredCoursesHeading1'})  #grab all instances of required course headings
    print(major)
    groups_rec_tables = soup.find_all('table')
    for table in groups_rec_tables:
        table_links = table.find_all('a', attrs={"class": 'sc-courselink'})  #
        for link in table_links:
            print(link.contents)

    for i in range(len(groups_rec_names))


    # match up the groups_rec_names with the groups_rec_tables, return as a pickle
