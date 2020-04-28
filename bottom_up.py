from scrapeOlin import Major, pickle_data, load_pickle_data
from datetime import datetime
import os
import glob
import time
import re
"""
Stuff to work on:
co recs, semeseter availability, forge_semester(),

"""


class Schedule:
    """
       This class represents your entrire stay at olin aka 10 semesters max?
       can be stored locally to save progress or specific plans that are generated"""

    def __init__(self, pot_majors, course_catalog, schedule=[], major_nm='ME'):
        """
        Constructor to initialize a student schedule
        :param pot_majors: potential majors for a student (parsed from Olin catalog)
        :param course_catalog: all available courses for students, parsed from Olin Catalog
        :param schedule: Current schedule to work with if there is one (typically will start first year classes)
        :param major_nm: Name of major to pursue, defaults to Mech E
        """
        # things to note: courses taken is list of lists,
        self.major_reqs = pot_majors
        self.major = major_nm
        self.catalog = course_catalog
        self.schedule = schedule
        self.loa_credits = {'engr': 0, 'ahse': 0}
        self.study_away_credits = {'engr': 0, 'ahse': 0, 'sci': 0, 'mth': 0}
        self.general_reqs = {'engr': 46, 'mth': 10, 'sci': 12, 'mth+sci': 30, 'ahse': 28,
                             'all': 120}  # 'ahs': 12, # we don't keep track of e credits...

    def sum_credits(self, field=None, semester=None, single_sem=False):
        """
        Iterate through students courses and return number of credits that  a student has taken
        :param field: which type of credit to look for (ie 'ENGR or AHSE')
        :param semester: semester from 0-10 to specifically look at
        :param single_sem: Boolean indicating whether to return data fro that single semester or for all previous
        :return: Total amount of credits of specified type
        """
        credits_num = 0
        start_sem = 0
        if field:
            field = field.lower()
        if semester is not None:
            if single_sem:
                start_sem = semester - 1
            schedule = self.schedule[start_sem:semester]  # Assuming numeric input
            # if start_sem==end_sem-1:
            #     schedule = [schedule]
        else:
            schedule = self.schedule
        for semester in schedule:
            for crn in semester:
                course_credits_dict = self.catalog[crn]['credit_dict']
                if crn == 'LOA':
                    course_credits_dict = self.loa_credits
                elif crn == 'STUDY_AWAY':
                    course_credits_dict = self.study_away_credits
                if field is None:
                    credits_num += sum(course_credits_dict.values())
                else:
                    if field == 'ahse':
                        credits_num += course_credits_dict.get('sust', 0)
                    credits_num += course_credits_dict.get(field, 0)
        return credits_num

    def get_general_progress(self, tuple_flag=False, semester=None):
        """Sum up credits uof each type of course and compare to requirements
        :return a dictionary with keys and values of how many credits of a filed need to be taken still"""
        credits_left = {}
        credits_completed = {}
        for key, value in self.general_reqs.items():
            fields = key.split('+')
            field_sum = 0
            if key == 'all':
                fields = [None]
            for field in fields:
                field_sum += self.sum_credits(field, semester)
            credits_left[key] = value - field_sum
            credits_completed[key] = (field_sum, value)

        if not tuple_flag:
            return credits_left
        else:
            return credits_completed


    def evaluate_progress(self, semester=None):
        """
        Test whether a schedule has met all general graduating requirements
        :param semester: Semester of which to look below (if you have scheduled classes higher up)
        :return: True or false if you have met general requirements to graduate
        """
        progress = self.get_general_progress(semester)
        for key, value in progress.items():
            if value > 0:
                return False
        return True

    def save_schedule(self, directory=None, filenm=None, pickled=None):
        """Saves the current Schedule as a text file as well as a pickled object that could be reloaded """
        schedule_to_save = self.schedule
        if directory is None:
            directory = 'saved_schedules/'
        if filenm is None or filenm == '':
            filenm = datetime.now().strftime("%m_%d-%H_%M_%S")
        where_save = directory + filenm
        if not os.path.exists(where_save + '.txt'):
            f = open(filenm+'.txt', "w")
            f.write(str(schedule_to_save))
            # TODO add in course names to the saved text file and formatting
            f.close()
        if pickled:
            pickle_data(filenm + '.pkl', schedule_to_save, True)
        return

    def get_recs(self, crn, course_lst=[]):
        """Recursively build a list of all the courses that are needed for a given course
        :param crn: CRN to ger reqs for
        :param course_lst: list to be appended to as it is passed down recursively
        :return: list that has all of the courses that are prereqs for a course
        """

        # TODO: what about alternate recommendations? and what about recommendedReqs?
        courses = course_lst
        courses.append(crn)
        reqs = sum(self.catalog[crn]['pre_req'], [])  # TODO: should be changed ONLY LOOK AT the first option's recs
        # Remove duplicates
        reqs = list(set(reqs))
        for i in reqs:
            self.get_recs(i, courses)
        # REMOVING DUPLICATES MIGHT NTO BE NECCESARY (might want to be able to tell which recs are helpful)
        return list(set(courses))

    def taken_course(self, crn, semester=None):
        """Check to see if this course has been taken up until a certain semester
        :param crn: CRN string to check against schedule
        :param semester: semester to check below
        :return: True or False if course has been taken"""
        if semester is None:
            semester = len(self.schedule)
        return any(crn in semester_ls for semester_ls in self.schedule[0:semester])

    def difficulty_take(self, crn, semester=None):
        """
        This function is intended as a helper function runnable on a crn to determine how many additional prereqs (you haven't already taken) are required
        This is useful determining which class to take for 1 requirements (one_reqs)

        :return: number of reqs you haven't yet taken that are required for a course
        """
        # finding prereqs for CRN
        total_reqs = self.get_recs(crn)
        cleaned_reqs = [req for req in total_reqs if not self.taken_course(req)]
        # cleaned_reqs = self.clean_course_list(total_reqs, semester)
        return len(cleaned_reqs)

    def valid_course(self, crn, semester=None):
        """
        Returns whether or not course can be taken
        :param crn: Course to check validity
        :param semester: semester to check if is valid
        :return: True or False whether a class can be taken for a give semester
        """
        # TODO: Corecs?, concurrentReqs?

        if semester is None:  # handle semester==None
            semester = len(self.schedule)
        # start by creating course object
        course = self.catalog[crn]

        # Edge Case Handling - if course has already been taken, or if course has a specified semester requirement.
        if self.taken_course(crn) or (
                course['term_requirement'] is not None and course['term_requirement'] != semester):
            return False
        term = semester % 2
        if term == 0:  # If an even term number (Spring)
            if not self.catalog[crn]['spring']:
                return False
        else:  # Fall
            if not self.catalog[crn]['fall']:
                return False

        # Normal Case Handling - Options indicate differnt combinations of reqs ie ENGR3110
        for req_option in course['pre_req']:
            # If the list empty than there aren't prereqs! Exit for loop and return true
            if len(req_option) == 0:
                return True
            # stop checking options if you find one that works
            else:
                for req in req_option:
                    if not self.taken_course(req, semester):
                        # Don't have req, break out and skip to next pre_req track
                        break
                    if req == req_option[-1]:  # If you get to the last prereq in a pre_req track you are good!
                        return True

        # TODO: Check to see if the student is in the right grade for a course?
        return False  # default case if True hasn't already been returned

    def clean_course_list(self, course_lst, semester=None):
        # Not sure if code is needed
        """
        Runs valid course on a list of courses and returns the valid ones
        :return:
        """
        return [course for course in course_lst if self.valid_course(course, semester)]

    def get_required_major_courses(self, semester=None, add_reqs_abs=True, add_reqs_one=False):
        """
        :param semester: Checks to see if there is a semester to reference - defaults to None.
        :param add_reqs: If True includes all recursively generated requirements in the list and cuts duplicates
        :return: returns a dictionary valid courses of all the types of coureses you can take.
        """

        # Setting temp var lists based on total major requirements
        course_list_abs = self.major_reqs[self.major].abs_reqs
        course_list_ones = self.major_reqs[self.major].one_reqs

        # Defining valid_courses dictionary that will be returned after modifications
        valid_courses = {'major_abs_requirements': [], 'major_one_requirements': []}

        for sub_course_list in course_list_abs:
            # print('Sub course list', sub_course_list)

            # Includes extra requirements and adds them to individual list.
            if add_reqs_abs:
                for course in sub_course_list:
                    reqs = self.get_recs(course)
                    set_1 = set(sub_course_list)
                    set_2 = set(reqs)
                    new_reqs = list(set_2 - set_1)
                    sub_course_list += new_reqs
                    # print(sub_course_list) # view the change in the list
            # TODO: Issue with Linearity/dynamics
            # Set's major_abs_requirements value of dictionary based on what valid courses are in the sub_list.
            # TODO: Noc functionality to check if meeting major requirements (this only shows what you need and could take)
            valid_courses['major_abs_requirements'].append(self.clean_course_list(sub_course_list, semester))

        # Handling one_reqs
        for one_req_set in course_list_ones:
            # Including temp bool for inclusion (equivalent of deletion)
            satisfied_bool = False
            # Walk thorugh CRNS, if course is taken, break loop and trigger bool.
            for crn in one_req_set:
                if self.taken_course(crn, semester):
                    satisfied_bool = True
                    break
            # Logic if set of courses is not satisfied - includes requirement handling.
            if not satisfied_bool:
                if add_reqs_one:
                    for course in one_req_set:
                        # Add in the Pre reqs
                        reqs = self.get_recs(course)
                        set_1 = set(one_req_set)
                        set_2 = set(reqs)
                        new_reqs = list(set_2 - set_1)
                        one_req_set += new_reqs
                valid_courses['major_one_requirements'].append(self.clean_course_list(one_req_set, semester))
        return valid_courses



    def printProgressBar (self, iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
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



    def displayProgressDifference(self, preSemesterProgress, postSemesterProgress):
        """
        Funcitonal objective:
        display a set of progress bars for your credit requirements
        Have the progressbars grow (or shrink) based on the differences in credits before and after this semester.
        use sleeps and pauses effectively for ease of interpretation.
        """
        if len(preSemesterProgress)==len(postSemesterProgress):
            for key in preSemesterProgress:
                self.printProgressBar(preSemesterProgress[key][0], preSemesterProgress[key][1], prefix =key + ' Credits now ', suffix = 'Complete', length = 50)
                difference = postSemesterProgress[key][0] - preSemesterProgress[key][0]
                for credit in range(difference):
                    time.sleep(0.25)
                    self.printProgressBar(preSemesterProgress[key][0] + 1 + credit, preSemesterProgress[key][1], prefix =key + ' Credits now ', suffix = 'Complete', length = 50)
                print('')

    def build_semester(self, semester=None):

        """
        General UI Todos @Adi
        adi work on :
        what required abs_reqs and one_offs need to be taken
        displaying abs_reqs , one_reqs , and pre_req recommendations with colorcoding (& color key)
        perhaps displaying which prereqs align with which paths and end results so that users can make more informed
        decisions about their schedues.

        """

        # TODO: (UI?) implement options for user to call core functionalities - reseting, clearing current semester recommendations, etc.
        if semester is None:  # handle semester==None
            semester = len(self.schedule)
        print('Planning Semester: ', semester + 1)

        # Check to see if you have made the list for this semester, make the lists up to tha point if necessary
        while len(self.schedule) <= semester:
            self.schedule.append([])
        # TODO: Display what required credits musts still be taken
        # TODO: Display what one off seciotns still ened to be taken
        preSemesterProgress = self.get_general_progress(tuple_flag=True)
        # Present possible options based on major Requirements
        major_requirements = self.get_required_major_courses(semester, add_reqs_abs=True, add_reqs_one=False)
        absolute = major_requirements['major_abs_requirements']
        one_offs = major_requirements['major_one_requirements']

        print('Of courses that must be taken, you can currently take these: ')
        # ge the course names via a list copmrehension
        print([(course, self.catalog[course]['course_nm']) for course in absolute[0]])

        for section in one_offs:
            print('\nOf One-Off requirements these are available (options with pre-reqs removed)')
            # ge the course names via a list copmrehension
            print([(course, self.catalog[course]['course_nm']) for course in section])
        # TODO: write helper function that takes a list of courses and nicely displays them
        choices = []
        # make sure uppercase because all CRNs are, handle, commas, spaces, or both
        while True:
            clean_input = True
            selected_crns = input("\nPlease input CRN's with spaces or commas in between them").upper().replace(',',
                                                                                                                ' ').split()
            for crn in selected_crns:
                # If you type in an invlaid crn
                if crn not in self.catalog:
                    print(crn, ' isn\'t a valid CRN!!!')
                    clean_input = False
                    break
                # If you type a crn that you can't actually take
                elif not self.valid_course(crn, semester=semester):
                    print(crn, ' can\'t be taken this semester')
                    # TODO return why (return a message from the valid course function)
                    clean_input = False
                    break
                # TODO : Check for concurrent recs here
                # TOdo: add mesgae about classes if they have recommended reqs etc and printout if it's valid
            if clean_input:
                break
        choices.extend(selected_crns)
        if 'LOA' in choices:
            choices = ['LOA']
            self.loa_credits = int(input("Input number of credits that you will be taking on your LOA"))

        elif 'STUDY_AWAY' in choices:  # adjust for actual CRNs
            choices = ['STUDY_AWAY']
            self.study_away_credits = int(input("Input number of credits that you will be taking on your Study Away"))
        self.schedule[semester].extend(choices)
        postSemesterProgress =  self.get_general_progress(tuple_flag=True)
        self.displayProgressDifference(preSemesterProgress, postSemesterProgress)
        print(self.schedule)
        return choices

    def forge_schedule(self, semester=None):
        """
        :param semester: Semester for which to forge, is none specified, moves to the next one without any classes
        :return: returns schedule attribute, which contains all student's course choices for schedule.
        """
        if semester is None:
            semester = len(self.schedule) + 1  # real semester not the schedule index (-1)

        # Subtract to get the semester index rather than actual semester
        semester -= 1
        more_semesters = True

        while more_semesters:  # check if major requirements and graduation requirements are
            print("Building sem: ", semester + 1)
            # Go Build a semester
            self.build_semester(semester)
            semester += 1
            # Take input on whether to save or re edit that semester
            continue_response = input(color['RED'] + "Hit enter to progress to semester: " + str(
                semester + 1) + ", (S) to save, (R) to redo semester, (#) for specific semester, (Q) to quit or a combo "
                                "ie: (SQ)\n" +
                                      color['END']).strip().upper().replace(' ', '')

            if continue_response == '':  # Enter
                continue

            if 'S' in continue_response:
                save_name = input("If you would like to name this saved schedule, enter a name: ")
                # let the save funciton shoose a filename if nothing supplied
                student_schedule.save_schedule(filenm=save_name, pickled=True)

            if any(map(str.isdigit, continue_response)):
                input_num = int(re.search(r'\d+', continue_response).group())
                # As long as input is good, edit that semester
                if 1 <= input_num <= 10:
                    semester = input_num-1
            if 'Q' in continue_response:
                more_semesters = False  # Equivalent of break
        return self.schedule


if __name__ == '__main__':
    color = {'PURPLE': '\033[95m',
             'CYAN': '\033[96m',
             'DARKCYAN': '\033[36m',
             'BLUE': '\033[94m',
             'GREEN': '\033[92m',
             'YELLOW': '\033[93m',
             'RED': '\033[91m',
             'BOLD': '\033[1m',
             'ITALIC': '\033[3m',
             'UNDERLINE': '\033[4m',
             'END': '\033[0m'}
    # Load the majors and course data
    catalog = load_pickle_data('data/catalog4_pickle')
    # TODO: Adi's note: not sure if we really need to pass in all major information into the schedule class? @Nathan?
    # NATHAN --Reason for this was because then we can save what was available when someone made their schedule...

    majors = load_pickle_data('data/majors3_pickle')

    # Load schedule
    os.chdir("saved_schedules")
    saved_schedules = [file for file in glob.glob("*.pkl")]
    schedule_loaded = False
    initial_schedule = None
    if len(saved_schedules) > 0:
        # TODO: Allwo import of multiple schedules
        print('We found these saved Schedules, enter the number associated to load, or enter to restart:')
        count = 1
        for saved in saved_schedules:
            print(saved.split('.')[0], '({}), '.format(count), end='')
            count += 1
        file_to_open = input('\nFile Number: ')
        if file_to_open != '':
            # TODO: HAndle this input better
            new_schedule = load_pickle_data(saved_schedules[int(file_to_open) - 1])
            initial_schedule = new_schedule
            schedule_loaded = True
    # Otherwise ou need to build a schedule or use the default
    if not schedule_loaded:
        nathan_courses = [['ENGR1125', 'ENGR1200', 'MTH1111', 'SCI1111', 'AHSE1135', 'OIE1000'],
                          ['ENGX2000', 'ENGX2001', 'ENGR2510', 'AHSE1515', 'SUST2201']]
        initial_schedule = nathan_courses

    # Make a student Schedule
    student_schedule = Schedule(majors, catalog, initial_schedule)

    '''
    TESTING
    '''
    # print(student_schedule.get_required_major_courses())
    # print(student_schedule.sum_credits(field='ENGR'), 'test')
    # print(student_schedule.get_general_progress())
    # student_schedule.build_semester()
    student_schedule.forge_schedule()
    # print(student_schedule.valid_course('ENGR3590', 2))
