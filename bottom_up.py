from scrapeOlin import Major, pickle_data, load_pickle_data
from datetime import datetime
import os
import glob
import re

class Schedule:
    """
       This class represents your entire stay at Olin
       can be stored locally to save progress or specific plans that are generated
       This class also contains methods to modify and save this schedule"""

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
        self.loa_credits = {'engr': 0, 'ahse': 0} # These are lost when a aschedule is reloaded with these fields
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
        else:
            schedule = self.schedule
        for semester in schedule:
            for crn in semester:
                course_credits_dict = self.catalog[crn]['credit_dict']
                # Special handling of LOA since they are specific
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
        """
        Sum up credits of each type of course and compare to requirements
        :param tuple_flag   Iddicates whether to return credits as a tuple  of done to total, or the amt needed to do
        :param semester Semester for which to look at progress up to
        :return:        Returns a dictionary with keys and values of how many credits of a filed need to be taken still
        """
        credits_left = {}
        credits_completed = {}
        for key, value in self.general_reqs.items():
            fields = key.split('+')
            field_sum = 0
            if key == 'all': # Look at the total requirement aka use all credits
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
        """Saves the current Schedule as a text file as well as a pickled object that could be reloaded
        :param directory:   Parameter for location of files to be saved
        :param filenm:      Parameter for filename to be saved
        :param pickled:     Boolean to represent whether file should be pickled or not
        :return:            Returns Nothing.
        """
        schedule_to_save = self.schedule
        if directory is None:
            directory = 'saved_schedules/'
        else:
            directory + '/'
        if filenm is None or filenm == '':
            filenm = datetime.now().strftime("%m_%d-%H_%M_%S")
        where_save = directory + filenm
        if not os.path.exists(where_save + '.txt'):
            f = open(filenm + '.txt', "w")
            f.write(self.format_saved_schedule())   # Format the schedule nicely for text formatting
            f.close()
        if pickled:
            pickle_data(filenm + '.pkl', schedule_to_save, True)
        return

    def format_saved_schedule(self):
        """
        Takes the current schedule class attribute and turns it into a logical string to make a nice .txt file
        :return: Returns pretty_schedule,  the 'prettified' string output
        """
        pretty_schedule = ''
        semester_num = 1
        for semester in self.schedule:
            pretty_schedule += ('\n\nSemester ' + str(semester_num) + ' courses\n‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')
            # Show CRN and Course name, and how many credits it is
            semester_list = [(course, self.catalog[course]['course_nm'], self.catalog[course]['credit_dict']) for course
                             in semester]
            for crs in semester_list:
                # Some nasty string replace
                semester_tuple_str = '\n' + str(crs).replace(',', ' |')
                formatted_tuple = ''.join(filter(lambda ch: ch not in "'(){}", semester_tuple_str))
                pretty_schedule += formatted_tuple
            # Add Credit breakdown
            pretty_schedule += '\nCredits in Semester: ' + str(self.sum_credits(semester=semester_num, single_sem=True))
            semester_num += 1

        progress = self.display_progress(self.get_general_progress(tuple_flag=True))
        pretty_schedule += ('\n\nCareer Credits: \n' + progress)
        return pretty_schedule

    def get_recs(self, crn, course_lst=None):
        """Recursively build a list of all the courses that are needed for a given course,
        Only looks at prereqs
        :param crn: CRN to ger reqs for
        :param course_lst: list to be appended to as it is passed down recursively
        :return: list that has all of the courses that are prereqs for a course as well as the course itself
        """
        if course_lst is None:
            course_lst = []
        courses = course_lst
        courses.append(crn)
        reqs = sum(self.catalog[crn]['pre_req'], [])
        # Remove duplicates
        reqs = list(set(reqs))
        for i in reqs:
            self.get_recs(i, courses)   # Pass a mutable object into each branch
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
        This function is intended as a helper function runnable on a crn to determine how many additional prereqs
        (you haven't already taken) are required. This will be useful determining which class to take for (one_reqs)
        :param crn: CRN course input to reference for function
        :return: number of reqs you haven't yet taken that are required for a course
        """
        total_reqs = self.get_recs(crn)
        cleaned_reqs = [req for req in total_reqs if not self.taken_course(req, semester)]
        # cleaned_reqs = self.clean_course_list(total_reqs, semester)
        return len(cleaned_reqs)

    def valid_course(self, crn, semester=None):
        """
        Returns whether or not course is 'valid' - whether or not it can be taken at the given semester
        :param crn: Course to check validity
        :param semester: semester to check if is valid
        :return: True or False whether a class can be taken for a give semester
        """
        if semester is None:  # handle semester==None
            semester = len(self.schedule)
        # start by creating course object
        course = self.catalog[crn]

        # Edge Case Handling - if course has already been taken, or if course has a specified semester requirement.
        if self.taken_course(crn) or (
                course['term_requirement'] is not None and course['term_requirement'] != semester):
            return False

        # if the course isn't offered then it can't be taken
        term = semester % 2
        if term == 0:  # If an even term number (Spring)
            if not self.catalog[crn]['spring']:
                return False
        else:  # Fall
            if not self.catalog[crn]['fall']:
                return False

        # Normal Case Handling - Checking Prerequisites. Options indicate different combinations of reqs (ie ENGR3110)
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

        return False  # default case if True hasn't already been returned

    def clean_course_list(self, course_lst, semester=None, taken_only=False):
        """
        Runs valid_course() or taken_course() on a list of courses and returns the valid or taken ones
        For looking at requirements we only care about if class has been taken
        :param semester: Checks to see if there is a semester to reference - defaults to None.
        :param taken_only: Boolean to only run taken_course() or entire valid_course() function.
        :return: Returns valid courses in a list of input courses.
        """
        if taken_only:
            return [course for course in course_lst if not self.taken_course(course, semester)]
        return [course for course in course_lst if self.valid_course(course, semester)]

    def get_required_major_courses(self, semester=None, add_reqs_abs=True, add_reqs_one=False):
        """
        :param semester: Checks to see if there is a semester to reference - defaults to None.
        :param add_reqs: If True includes all recursively generated requirements in the list and cuts duplicates
        :return: returns a dictionary valid courses, which contains different types of courses you can take, and prereq lists.
        """

        # Setting temp var lists based on total major requirements
        course_list_abs = self.major_reqs[self.major].abs_reqs
        course_list_ones = self.major_reqs[self.major].one_reqs

        # Defining valid_courses dictionary that will be returned after modifications/additions
        valid_courses = {'major_abs_requirements': [], 'major_abs_prereqs': {}, 'major_one_requirements': [],
                         'major_one_prereqs': {}}

        # Add vlaid courses to the valid ocurse list
        for sub_course_list in course_list_abs:
            valid_courses['major_abs_requirements'].append(self.clean_course_list(sub_course_list, semester))

        # Includes extra pre-requirements and adds them associated with keys within a dict.
        # Only adds prereqs to generated key if: add_req_abs is toggled true, and if the course cannot be taken.
        if add_reqs_abs:
            for sub_course_list in course_list_abs:
                for course in sub_course_list:
                    # THE BELOW LINE CONDITIONALLY EXCLUDS REGULAR ABSOLUTE COURSES THAT TAKEABLE
                    if course not in valid_courses['major_abs_requirements'][0]:
                        new_pre_reqs = self.get_recs(course)
                        new_pre_reqs.remove(course)
                        valid_courses['major_abs_prereqs'][str(course)] = self.clean_course_list(new_pre_reqs, semester,
                                                                                                 taken_only=True)

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
                valid_courses['major_one_requirements'].append(one_req_set)

        # Check has already been done if set of requirements has been satisfied with the boolean loops above.
        if add_reqs_one:
            counter = 0 # Corresponds to grouping
            # Walk through sets of one_reqs
            for one_req_set in valid_courses['major_one_requirements']:
                # Assigns each set of one_reqs to an int key for dictionary, based on counter int
                counter += 1
                # Defines each grouping to a dictionary, meant to hold courses and their prereqs
                valid_courses['major_one_prereqs'][str(counter)] = {}
                for course in one_req_set:
                    # walks through every course in every grouping
                    new_pre_reqs = self.get_recs(course)
                    new_pre_reqs.remove(course)
                    # Accesses and sets the prereqs for each course in the grouping in the set of one_req groupings
                    valid_courses['major_one_prereqs'][str(counter)][course] = self.clean_course_list(new_pre_reqs, semester,
                                                                                             taken_only=True)

        # Here, we finally run clean_course_list() on the major_one_requirements in the valid_courses dict
        valid_courses['major_one_requirements'] = [self.clean_course_list(course_set, semester) for course_set in valid_courses['major_one_requirements']]
        return valid_courses

    def print_progress_bar(self, iteration, total, prefix='', length=100, fill='█'):
        """
        Returns a progress bar string based on progress level, to print or save to .txt file
        :param iteration: Current iteration within overall progress
        :param total: Total possible progress, ideally an int
        :param prefix: Prefix string for bar
        :param length: Length of bar as displayed in terminal
        :param fill: Bar Fill character
        :return: Returns progress bar string with prefix & suffix details
        """
        suffix = 'Credits Complete'
        percent = (str(iteration) + ' / ' + str(total))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        # made function return text so that it is easier to track print statements and it can be used to save
        to_print = '\r |%s| %s %s %s' % (bar, prefix, percent, suffix)
        return to_print + '\n'

    def display_progress(self, pre_semester_progress):
        """
        Displays a set of credit-based progress bars based on credit progress inputs
        :param pre_semester_progress: Credit Progress dictionary to reference, generated via get_general_progress()
        :return: Returns the string to be printed or saved to a .txt file
        """
        ret_string = ''
        for key in pre_semester_progress:
            ret_string += self.print_progress_bar(pre_semester_progress[key][0], pre_semester_progress[key][1],
                                                  prefix=key + '-->', length=50)
        return ret_string

    def display_major_requirements(self, semester, add_reqs_abs=True, add_reqs_one=False):
        """
        Displays abs_reqs and one_reqs based on major requirments to help students make informed choices to fill
        their schedules. Uses Color Coding, and automatically sorted prerequisites for courses (optional) to help
        students make functional choices about their courses.
        :param semester: Checks to see if there is a semester to reference - defaults to None.
        :param add_reqs_abs: If True includes all recursively generated requirements for all absolute requirements, and
        cuts duplicates
        :param add_reqs_one: If True includes all recursively generated requirements for each course in each grouping
        of one requirements, and cuts duplicates
        """
        # Define Color Key dictionary
        ckey = {'abs': '\033[1m\033[96m',  # bold cyan
                'one': '\033[1m\033[91m',  # bold red
                'prereq': '\033[1m\033[92m',  # bold green
                'extra': '\033[4m\033[93m',  # underline yellow
                'END': '\033[0m'}

        # Print Color Key
        print(ckey['extra'] + 'COLOR KEY' + ckey['END'] + '\n' + ckey['abs'] + 'Absolute Requirments' + ckey[
            'END'] + '\t\t' + ckey['one'] + 'One Requirments' + ckey['END'] + '\t\t' + ckey[
                  'prereq'] + 'Prerequisites' + ckey['END'] + '\t\t' + ckey['extra'] + 'Extra' + ckey['END'])

        # Calling get_required_major_courses() function and storing results
        major_requirements = self.get_required_major_courses(semester, add_reqs_abs, add_reqs_one)
        absolute = [(course, self.catalog[course]['course_nm']) for course in
                    major_requirements['major_abs_requirements'][0]]
        one_offs = major_requirements['major_one_requirements']
        abs_prereqs = major_requirements['major_abs_prereqs']
        one_prereqs = major_requirements['major_one_prereqs']

        # Handling abs_requirement
        print('Of courses that must be taken, you can currently take' + ckey['abs'] + ' these options:' + ckey['END'])
        for combo in absolute:
            print(ckey['abs'] + combo[1] + ' - (' + combo[0] + ')' + ckey['END'])

        # Handling abs_requirement prereqs
        if add_reqs_abs:
            print('These are also' + ckey['abs'] + ' required courses' + ckey['END'] + ' but you have to take the ' + ckey[
                'prereq'] + ' prereqs listed ' + ckey['END'] + 'first.')

            for unTakeableCourse in abs_prereqs:
                print(ckey['abs'] + self.catalog[unTakeableCourse]['course_nm'] + ' - (' + unTakeableCourse + ')' + ckey[
                    'END'])
                for prereq in abs_prereqs[unTakeableCourse]:
                    print('\t\t' + ckey['prereq'] + self.catalog[prereq]['course_nm'] + ' - (' + prereq + ')' + ckey['END'])

        # Handling One-Off requirements
        print('\nOf One-Off requirements, you can currently take ' + ckey['one'] + ' these options:' + ckey['END'])
        counter = 0
        for grouping in one_offs:
            # Line below generates a combo for every course in the one_off grouping; generated via a list comprehension
            counter += 1
            print(ckey['extra'] + 'Grouping ' + str(counter) + ckey['END'])
            for combo in [(course, self.catalog[course]['course_nm']) for course in grouping]:
                print(ckey['one'] + combo[1] + ' - (' + combo[0] + ')' + ckey['END'])

        # Handling One-off requirement prereqs
        if add_reqs_one:
            # Print clarifying statement
            print('These are also' + ckey['one'] + ' required courses' + ckey['END'] + ', separated by grouping. You have to take the' +
                  ckey['prereq'] + ' prereqs listed ' + ckey['END'] + 'first before you take the course. You only '
                                                                      'need to take one required course per grouping. ')
            # Walk through groupings
            for grouping in one_prereqs:
                print(ckey['extra'] + 'Grouping ' + grouping + ckey['END'])
                # Walk through 'untakeable courses'
                for unTakeableCourse in one_prereqs[grouping]:
                    print(ckey['one'] + self.catalog[unTakeableCourse]['course_nm'] + ' - (' + unTakeableCourse + ')' +
                          ckey['END'])
                    # Walk through prereqs for that 'untakeable course'
                    for prereq in one_prereqs[grouping][unTakeableCourse]:
                        print('\t\t' + ckey['prereq'] + self.catalog[prereq]['course_nm'] + ' - (' + prereq + ')' +
                              ckey['END'])

    def build_semester(self, semester=None):
        """
        Semester building function - provides recommended & required courses for informed decision making, parses
        text input for course choices & scheduling, checks course validity, handles scheduling 'edge cases' like
        LOA's and study aways, all for a single semester, bundled into one function that can be called for each semester.
        :param semester: Checks to see if there is a semester to reference - defaults to None.
        :return: Returns validated & verified student choices as a list to be referenced outside the function.
        """

        if semester is None:  # handle semester==None
            semester = len(self.schedule)
        print('Planning Semester: ', semester + 1)

        # Check to see if you have made the list for this semester, make the lists up to that point if necessary
        while len(self.schedule) <= semester:
            self.schedule.append([])
        preSemesterProgress = self.get_general_progress(tuple_flag=True)
        progress_str = self.display_progress(preSemesterProgress)
        print(progress_str)

         # make sure uppercase because all CRNs are, handle, commas, spaces, or both
        while True:
            clean_input = True
            selected_crns = input("\nInput '*' to see course requirements/progress or input CRN's with spaces or "
                                  "commas in between them ").upper().replace(',', ' ').split()
            # DOo a  variety of cases based on input
            for crn in list(selected_crns):
                # DISPLAY DEGREE PROGRESS
                if '*' in crn:
                    self.display_major_requirements(semester, add_reqs_abs=True, add_reqs_one=True)
                    clean_input = False
                    break
                # SUBTRACT COURSE
                if '-' in crn:
                    selected_crns.remove(crn)
                    crn = crn.replace('-', '')
                    if crn not in self.schedule[semester]:
                        print('You can\'t remove a class you didn\'t take :/')
                        clean_input = False
                        break
                    # Remove the crn if it is there
                    self.schedule[semester].remove(crn)
                    print('Succesfully removed: ', crn)
                    continue
                # INVALID CRN HANDLING
                if crn not in self.catalog:
                    print(crn, ' isn\'t a valid CRN!!!')
                    clean_input = False
                    break
                # INVALID COURSE
                elif not self.valid_course(crn, semester=semester):
                    print(crn, ' can\'t be taken this semester')
                    # TODO return why (return a message from the valid course function)
                    clean_input = False
                    break
                # TODO : Only checks forst Concurrent Rec
                # CONCURRENT REC?!
                elif self.catalog[crn]['con_req'][0]:
                    con_crn = self.catalog[crn]['con_req'][0][0]
                    if con_crn not in selected_crns and not self.taken_course(con_crn, semester):
                        print(color['RED'], crn, 'is missing concurrent req: ', self.catalog[crn]['con_req'][0][0], color['END'])
                        clean_input = False
                        break
                # INFORM REC REQ
                if self.catalog[crn]['rec_req'][0]:
                    print(color['RED'], crn, 'has a recommended req: ', self.catalog[crn]['rec_req'][0], color['END'])
                # TODO: Add option for an override even though it's not a valid crn
            if clean_input:
                break
        choices = selected_crns
        # If there is an loa or study away, prompt for credits
        if 'LOA' in choices:
            choices = ['LOA']
            self.loa_credits = int(input("Input number of credits that you will be taking on your LOA"))
        elif 'STUDY_AWAY' in choices:  # adjust for actual CRNs
            choices = ['STUDY_AWAY']
            self.study_away_credits = int(input("Input number of credits that you will be taking on your Study Away"))
        self.schedule[semester].extend(choices)
        # print(self.schedule)
        return choices

    def forge_schedule(self, semester=None, saveDirectory="saved_schedules"):
        """
        :param saveDirectory: directory path for where things should be saved
        :param semester:    Semester for which to forge, is none specified, moves to the next one without any classes
        :return:            schedule attribute, which contains all student's course choices for schedule.
        """
        if semester is None:
            semester = len(self.schedule) + 1  # real semester not the schedule index (-1)

        # Subtract to get the semester index rather than actual semester
        semester -= 1
        more_semesters = True

        while more_semesters:  # check if major requirements and graduation requirements are
            # Go Build a semester
            self.build_semester(semester)

            # Increment to the next semester
            semester += 1
            # Take input on whether to save or re edit that semester
            continue_response = input(color['RED'] + "Hit enter to progress to semester: " + str(
                semester + 1) + ", (S) to save, (R) to redo semester, (#) for specific semester, (Q) to quit or a combo "
                                "ie: (SQ)\n" +
                                      color['END']).strip().upper().replace(' ', '')
            # Handle different responses
            if continue_response == '':  # Enter, move to next semester
                continue

            if 'S' in continue_response: # Save the schedule
                save_name = input("If you would like to name this saved schedule, enter a name: ")
                # let the save function shoose a filename if nothing supplied
                student_schedule.save_schedule(directory=saveDirectory, filenm=save_name, pickled=True)

            if any(map(str.isdigit, continue_response)): # If any number is input (navigate to that semester)
                input_num = int(re.search(r'\d+', continue_response).group())
                # As long as input is good, edit that semester
                if 1 <= input_num <= 10:
                    semester = input_num - 1
            if 'Q' in continue_response: # Quit
                more_semesters = False  # Equivalent of break

            if 'R' in continue_response: # Redo current semester
                # Redo the semester
                semester -= 1
                continue
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
    majors = load_pickle_data('data/majors3_pickle')
    saveFolder = "saved_schedules"

    # Load schedule if there are some available
    if not os.path.exists(saveFolder):
        os.makedirs(saveFolder)
    os.chdir(saveFolder)
    saved_schedules = [file for file in glob.glob("*.pkl")]
    schedule_loaded = False
    initial_schedule = None
    if len(saved_schedules) > 0:
        print('We found these saved Schedules, enter the number associated to load, or enter to restart:')
        count = 1
        for saved in saved_schedules:
            print(saved.split('.')[0], '({}), '.format(count), end='')
            count += 1
        file_to_open = input('\nFile Number: ')
        # Open file, but if nothing input then load a default
        if file_to_open != '':
            new_schedule = load_pickle_data(saved_schedules[int(file_to_open) - 1])
            initial_schedule = new_schedule
            schedule_loaded = True
    # Otherwise ou need to build a schedule or use the default
    if not schedule_loaded:
        nathan_courses = [['ENGR1125', 'ENGR1200', 'MTH1111', 'SCI1111', 'AHSE1135', 'OIE1000'],
                          ['ENGX2000', 'ENGX2001', 'ENGR2510', 'AHSE1515', 'SUST2201']]
        initial_schedule = nathan_courses

    # hardcoding valid majors
    # Selct which degree to work towards
    valid_majors = ['ME', 'ECE']
    valid_major = False
    while not valid_major:
        major_input = input('Are you working towards an ME or ECE degree? Input "ece" or "me" ->').upper()
        if major_input in valid_majors:
            valid_major = True

    # Make a student Schedule
    # TODO: Somehow save major that a student is working towards... pickle the entire schedule? in filename?
    student_schedule = Schedule(majors, catalog, initial_schedule, major_nm='ME')
    student_schedule.forge_schedule(saveDirectory=saveFolder)