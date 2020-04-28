import os
from scrapeOlin import pickle_data, load_pickle_data
from pathlib import Path
from pickle import dump, load
import time

# catalog = load_pickle_data('data/catalog4_pickle')
# print(catalog)
# print(len(catalog.items()))
# print(catalog['ENGX2000'])

# Testing color output


color = {'PURPLE': '\033[95m',
         'CYAN' : '\033[96m',
         'DARKCYAN' : '\033[36m',
         'BLUE' : '\033[94m',
         'GREEN' : '\033[92m',
         'YELLOW' : '\033[93m',
         'RED' : '\033[91m',
         'BOLD' : '\033[1m',
         'ITALIC' : '\033[3m',
         'UNDERLINE' : '\033[4m',
         'END' : '\033[0m'}
strin = color['BOLD'] + color['CYAN'] + 'Hello World !' + color['END']

print(strin.center(40, '#'))



# PROGRESS BAR TESTING

# What we have to work with
# a dict that looks like this:

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r |%s| %s %s%% %s' % ( bar, prefix, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()



def displayProgressDifference(preSemesterProgress, postSemesterProgress):
    """
    Funcitonal objective:
    display a set of progress bars for your credit requirements
    Have the progressbars grow (or shrink) based on the differences in credits before and after this semester.
    use sleeps and pauses effectively for ease of interpretation.
    """
    if len(preSemesterProgress)==len(postSemesterProgress):
        for key in preSemesterProgress:
            printProgressBar(preSemesterProgress[key][0], preSemesterProgress[key][1], prefix =key + ' Credits now ', suffix = 'Complete', length = 50)
            difference = postSemesterProgress[key][0] - preSemesterProgress[key][0]
            for credit in range(difference):
                time.sleep(0.25)
                printProgressBar(preSemesterProgress[key][0] + 1 + credit, preSemesterProgress[key][1], prefix =key + ' Credits now ', suffix = 'Complete', length = 50)
            print('\n')

# FOR TESTING

presemprog = {'engr': (32,46), 'mth': (6,10), 'sci': (4,12), 'mth+sci': (20,30), 'ahse': (12,28), 'all': (86,120)}
postsemprog = {'engr': (32,46), 'mth': (6,10), 'sci': (12,12), 'mth+sci': (24,30), 'ahse': (16,28), 'all': (102,120)}
displayProgressDifference(presemprog, postsemprog)



# PROVIDED EXAMPLE
# printProgressBar(preSemesterProgress[key][0], preSemesterProgress[key][1], prefix ='', suffix = 'Complete', length = 50)
# time.sleep(.2)
# printProgressBar(postSemesterProgress[key][0], preSemesterProgress[key][1], prefix ='', suffix = 'Complete', length = 50)

# # A List of Items
# items = list(range(0, 57))
# l = len(items)
#
# # Initial call to print 0% progress
# printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
# for i, item in enumerate(items):
#     # Do stuff...
#     time.sleep(0.1)
#     # Update Progress Bar
#     printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
