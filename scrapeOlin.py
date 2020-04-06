from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import requests
import urllib.request
import os
import re
from pickle import dump, load

# Create a directory to store the Lrics in

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
    classes = right_pnl[0].find_all('a', attrs={"href": re.compile(url+'/')})  #
    for course in classes:
        # PARSE THE COURSE PAGE!!!!
        print(course)
        course_link = base_link + course.get('href')
        link_page = requests.get(course_link)
        soup = bs(link_page.content, 'html.parser')
        credits = soup.find_all('div', attrs={"class": 'credits'})  #
        print(credits[0].getText())
    break