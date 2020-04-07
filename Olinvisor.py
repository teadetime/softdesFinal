"""
Main File for Olinvisor, a virtual advisor deisnged for Olin College
Started 4/2/2020
<<<<<<< HEAD
Adi R, Nathan F
=======
Adi R, and Nathan F
>>>>>>> 778d3364e0beb4d6327c5ae891ba7054d406e71e
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

class Schedule:
    """
    This class represents your entrire stay at olin aka 10 semesters max?
    can be stored locally to save progress or specific plans that are generated"""
    def __init__(self, major, ):
        sem_1_fall = COME COURSE
        etc...
