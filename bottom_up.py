from scrapeOlin import Major, pickle_data, load_pickle_data

class Schedule:
    """
       This class represents your entrire stay at olin aka 10 semesters max?
       can be stored locally to save progress or specific plans that are generated"""

    def __init__(self, pot_majors,course_catalog, schedule = []):
        # things to note: courses taken is list of lists,
        self.major_reqa = pot_majors
        self.catalog = course_catalog
        #self.name = Major.name
        self.schedule = schedule

    def total_credits(self,semester = None , type = None):
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

if __name__ == '__main__':
    # Load the majors and course data
    catalog = load_pickle_data('catalog_pickle')
    majors = load_pickle_data('majors_pickle')
    # TODO: make script that can be run to input your current schedule
    # Make a student Schedule
    student_schedule = Schedule(majors,catalog, [])



