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
        self.pre_req =              # store prereqs in a list
        self.mth_crds =
        self.sci_crds =
        self.ahs_crds =
        self.eng_crds =
        self.offered_fall = True
        self.offered_spring = None
        self.seats =
        self.term_requirement = 1 # Term that this course is required to be taken (like qea)
        self.grade_limit = 1 #First Year only class (1st semester ahs)

"""
Techincal questions:
how to represent interchangable course options (tuples?)
how to represent course options
work from top down or bottom up?

start with absolute courses, work top down

how to represent LOA's?
How to optimize for different weight_preferences?

"""

# Adi's assumption that there is a hashmap where you can access a Course object from its CRN
allCoursesKeys = {}

class Schedule:
    """
    This class represents your entrire stay at olin aka 10 semesters max?
    can be stored locally to save progress or specific plans that are generated"""
    # TODO: fill courses taken default constructor with sem 1 & sem 2 courses below somehow
    def __init__(self, major, weight_preferences, courses_taken=[], BOW_classes=None, LOA_sems=None): # include *args or **kwargs to account for external factors, BOW classes, etc.
        # Initialize Empty Schedule with built in LOA's, courses_taken
        # things to note: courses taken is list of lists,
        self.major = Major
        self.name = Major.name
        self.course_progression = []
        self.course_progression = self.course_progression.extend(courses_taken)
        for i in range(len(10-len(self.course_progression))): # TODO: numbers might be off
            course_progression.append([])

        if LOA_sems is not None:
            for semester in LOA_sems:
                self.course_progression[semester] = ['LOACRN'] # TODO: placeholder - We need to add a CRN for LOA's etc.
        self.weight_preferences = weight_preferences


    # begin helper function definitions for primary forge_schedule function
    def insertAbsCoursesHelper(self,courseList ):
        """
        top down - find highest course (w/ most prereqs) in absolute list, break down prereqs, insert recursively at top as needed
        """
        for course in reveresed(courseList):
            self.insertCoursesRec(course, self.findTopSlot(course))

    def insertOptCoursesHelper(self):
        """
        TODO: For the MVP this groups the interchangable courses that require the same number of prereqs and inserts them into the course structure.  
        """


    def insertCoursesRec(self, course, slot): # course to insert, slot is an index
        # conditional to check for prereqs
        """
        TODO: Do we want to use findTopSlot() in the function call of insertCoursesRec or do we want to use it here?
        related TODO: Should findTopSlot() take in a top possibility? That would make it more versatile.
        """
        if course.pre_req is not None:
            for prereq in course.pre_req: # walk through list
                self.insertCoursesRec(prereq, slot-1)
        self.course_progression[slot].append(course)


    def findTopSlot(self, testCourse):
        """A lot of code to do something very simple: find the highest possible slot to insert a course"""
        temp = len(self.course_progression)
        for semester in reversed(self.course_progression):
            temp -= 1
            semesterCredits = 0
            if len(semester) is not None:
                for course in semester:
                    semesterCredits+=course.credits
            if self.weight_preferences - semesterCredits > testCourse.credits:
                return(temp)

    def reorganizeCoures(self):
        # TODO: schedule reorganizaiton functionality
        pass


    def forgeSchedule(self):
        """Walks through all required courses in a major starting with abs_reqs, then one_reqs,
        and fills out schedule from end to start.  """
        self.insertAbsCoursesHelper(self.major.abs_reqs)
        # for optional_course_list in self.major.one_reqs:
        self.insertOptCoursesHelper()


        # rebuild schedule based
        # Alternatively - define intermediary data structure to store course progression before this reorganizaiton step
        self.reorganizeCoures()
        return self.course_progression




        return self.course_progression
