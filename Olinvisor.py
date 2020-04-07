"""
Main File for Olinvisor, a virtual advisor deisnged for Olin College
Started 4/2/2020
Adi R, Nathan F

"""
class Olin:
    """
    Class that defines Olin/college specific requirements
    Contains Majors, and total degree requirements etc.
    """
    def __init__(self, degrees):
    self.semester = True
    self.degrees = degrees
    pass


class Course:
    """
    this object defines a course, credits, offering times
    use bs4 to scrape: https://olin.smartcatalogiq.com/2019-20/Catalog/Courses-Credits-Hours/ENGR-Engineering
    """

    def __init__(self):
    # Maybe there should be a list of credit types, that are passes
        self.crn =
        self.pre_req =
        self.mth_crds =
        self.sci_crds =
        self.ahs_crds =
        self.eng_crds =
        self.offered_fall = True
        self.offered_spring = None
        self.seats =
        self.term_requirement = 1 # Term that this course is required to be taken (like qea)
        self.grade_limit = 1 #First Year only class (1st semester ahs)


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


class Schedule:
    """
    This class represents your entrire stay at olin aka 10 semesters max?
    can be stored locally to save progress or specific plans that are generated"""
    # TODO: fill sem1_classes default constructor below
    def __init__(self, major, weight_preferences, sem2_classes,sem1_classes=[], BOW_classes=None, LOA_sems=None): # include *args or **kwargs to account for external factors, BOW classes, etc.
        # Initialize Empty Schedule
        self.major = Major
        self.name = Major.name
        self.sem1 = sem1_classes
        self.sem2 = sem2_classes
        self.sem9 = []
        self.sem3 = []
        self.sem4 = []
        self.sem5 = []
        self.sem5 = []
        self.sem7 = []
        self.sem8 = []
        self.sem10 = []
        self.course_progression = [self.sem1, self.sem2, self.sem3, self.sem4, self.sem5, self.sem6, self.sem7, self.sem8, self.sem9, self.sem10]
        self.weight_preferences = weight_preferences

    def insertCourse(self,course):
        findOpening(course,

    def findOpening(self, course):
        for i in range(len(self.course_progression)):
            if self.course_progression[i]

    def checkPrereqs(self, course, position):



    def forge_schedule(self):
        for course in self.major.abs_reqs:
            self.insertCourse(course)
        for course in self.major.one_reqs:
            self.insertCourse


        return self.course_progression
