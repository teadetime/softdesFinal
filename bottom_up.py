from scrapeOlin import Major, pickle_data, load_pickle_data

class Schedule:
    """
       This class represents your entrire stay at olin aka 10 semesters max?
       can be stored locally to save progress or specific plans that are generated"""

    def __init__(self, pot_majors, course_catalog, schedule = [], major_nm='ME'):
        # things to note: courses taken is list of lists,
        self.major_reqs = pot_majors
        self.major = major_nm
        self.catalog = course_catalog
        #self.name = Major.name
        self.schedule = schedule

    def sum_credits(self,semester = None , type = None):
        '''Iterate through students courses and return number of credits'''
        credits_num = 0
        if semester is not None:
            semester = self.schedule[semester-1] # Assuming numeric input
            for crn in semester:
                course = self.catalog[crn]
                if type is None:
                    credits_num += sum(course['credit_dict'].values())
                else:
                    credits_num += course['credit_dict'].get(type, 0)
        else:
            for semester in self.schedule:
                for crn in semester:
                    course = self.catalog[crn]
                    if type is None:
                        credits_num += sum(course['credit_dict'].values())
                    else:
                        credits_num += course['credit_dict'].get(type, 0)
        return credits_num

    def possible_required_classes(self, semester):
        '''Get the possible classes for a student for their major'''
        # Get the list of required classes
        self.major_reqs


    def get_recs(self, crn, course_lst):
        '''Recuresively build a list of all the courses that are needed for a given course'''
        courses = course_lst
        courses.append(crn)
        reqs= self.catalog[crn]['pre_req']
        for i in reqs:
            self.get_recs(i,courses)
        return courses

    def taken_course(self, crn):
        '''Check to see if this course has been taken'''
        return any(crn in semester_ls for semester_ls in self.schedule)

    def valid_course(self, crn, semester=None):
        # Check to see if you have the pre reqs
        course = self.catalog[crn]
        validity = True
        for course in course['pre_req']:
            if not self.taken_course(course):
                validity = False
                break
        # Also return false if you've already taken the course
        if self.taken_course(crn):
            validity = False
        # if the term has a specified semester/requirement
        if course['term_requirement'] is not None and course['term_requirement'] != semester:
            validity = False
        # Check to see if the student is in the right grade

        # Concurrent recs?

        return validity



if __name__ == '__main__':
    # Load the majors and course data
    catalog = load_pickle_data('catalog_pickle')
    majors = load_pickle_data('majors_pickle')
    # TODO: make script that can be run to input your current schedule
    # Make a student Schedule
    student_schedule = Schedule(majors,catalog, [])
    print(student_schedule.get_recs('ENGR3330', []))