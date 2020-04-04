from bs4 import BeautifulSoup as bs
from bs4 import SoupStrainer
import requests
import urllib.request
import os
import re
from pickle import dump, load

# Create a directory to store the Lrics in

# Set up Scraping links for Beautiful Soup
root_link = "https://olin.smartcatalogiq.com/en/2019-20/Catalog/Courses-Credits-Hours"

    # Extract the contents of the link
    link_page = requests.get(root_link)
    soup = bs(link_page.content, 'html.parser')
    aTagGroup = soup.find_all('a', attrs={"href": re.compile(^'https://olin.smartcatalogiq.com/en/2019-20/Catalog/Courses-Credits-Hours/')})  #
    '''
    # Now lets put those urls into a dictionary
    songDict = {}
    for aTag in aTagGroup:
        songUrl = aTag.get('href')
        # There are duplicate songnames so don't duplicate entries
        if songName not in songDict:
            songDict[songName] = {'url': songUrl}
