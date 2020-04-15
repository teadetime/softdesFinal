import os
from scrapeOlin import pickle_data, load_pickle_data

catalog = load_pickle_data('catalog_pickle')
print(catalog)
print(len(catalog.items()))
print(catalog['ENGR3330'])