---
title: Olin Course Scheduling Assistant
description: some description
---
## A big picture overview!
Hi Guys! We're [Nathan Faber](https://github.com/teadetime "@teadetime") and [Adi Ramachandran](https://github.com/aramachandran7 "@teadetime"), two first years at the Olin College of Engineering. 
For our Software Design course final project, we decided to **build a command-line based course scheduling tool to help students intelligently plan their academic course progression at the Olin College of Engineering**. 

Built with over 1000 lines of python code, the tool **enables students to build a schedule that meets graduation and major requirements and fulfills all course prerequisites, based on information scraped from the Olin online Course Catalog.** 
We as students recognize the difficulty in choosing courses when you must balance interesting options and ones that fulfill your essential graduation and major requirements. We also recognize the superiority of command-line-based user interfaces. 

**The image below shows our program in use!**
![General use](/docs/generalUse.PNG)

**Scroll down to learn more about our work!** 

## Who we are, and why we did this.
Nathan and Adi are both big fans of software and writing high quality, repoducable code. For our software design project, we decided we wanted to do something with real impact - even within the walls of our own school. 

Worrying about graduating isn't fun! As students we both see this process as a huge stress and thought that we could do something about it. By taking in all course offerings and major requirements we believe that we can help students make quicker, more informed decisions when building a course schedule for their time in college.


## More details, and some results!

In essence, we built a student course scheduling assistant/tool for Olin College of Engineering. This Python Command Line tool can be used to help a student build up their schedule, providing course recommendations based on requirements along the way, or could simply be used to validate a schedule and ensure that it meets all graduating and major requirements. This tool allows students to quickly and easily generate potential course schedules so that they can be prepared for potential changes in course offerings, etc. Students can easily view, maintain, build, and test many different schedules iteratively to determine the option that is best for them. Schedules are stored as a readable .txt file

__Some Key screenshots:__

The degree helper (this indicates what courses you can and need to take as well as their pre-reqs) ***based on the users schedule**:
![Degree Helper](/docs/reqProgress.PNG)

Schedules can also be saved as nice text file:
![Saved Output](/docs/savedSchedule.PNG)

## Project evolution
Our original goals for this project were centered around making the scheduling process entirely automatic. This would allow students to basically see many different permutations of their schedule and see if ceratin choices significantly limited their options or potential to graduate.

It became clear early on that while this may have been possible, we lacked a lot of data that would make this data useful. We scoped the project down to an assistant that would help students understand which courses they needed to take for requirements, would let students build schedules iteratively, providing advice and recommendations along the way, adn would easily let students store different variations of their custom schedules. This was a logical choice because it was more realistic and would require a similar architecture, but would be a more usable and useful end product. This meant that moving forward we wouldn't need to do a complete redesign to implement more automatic approaches.

By the time of our first code review we had successfully parsed all of the major requirements and courses form Olin's site. We had a rough idea of how we would store and build schedules, but no code or structure. By our second review we had written out a large amount of background and helper functions that allowed us to interact with course and requirement data, as well as user input. From this point we worked to flesh out a backend and frontend workflow that users would interact with to build their schedules, leading to most recent design changes regarding what information and controls would be presented to users while running the program and building their schedules, semester by semester.

_Why a command line tool?_

Originally there were plans to build a formal gui for this tool. These plans were shelved as we built the core of the application. We also feel that a Command line tool in this application is actually quite usable, and enables us to devote efforts elsewhere, mainly to core functionality. In the future we may consider making a GUI, perhaps a web-based one, as it would make this tool more accessible to use.

## Implementation information
The implementation of our tool can be broken down into two main steps
1. Parsing of courses and degree requirements from online [Olin Catalog](https://olin.smartcatalogiq.com/en/2019-20/Catalog/Courses-Credits-Hours)
    * This involved Beautiful Soup to parse html that contained all of these requirements
    * Heavy amounts of edge case handling and formatting (Olin has many weird requirements formats)
    * Storing this data so it isn't parsed each time. We opted to pickle this data as a dictionary
        ![Course Dictionary](/docs/courseDict.PNG)

2. Building schedule for a given user (key functions)

   *The following functions allow the user to intelligently build a schedule semester by semester while adhering to scheduling rules*
    1. Check if course has been taken before
    1. Check if course can be taken during give semester
    1. Determine requirements that have and have not been met
    1. Get pre-reqs recursively for a course
    1. Calculate credits in each field and progress to general requirements
    1. Other important but non-algorithmic work that had to be done:
        * Input Validation
        * Loading saved data (courses and other schedules)
        * Formatting output and prompts
        
    __While this isn't a fully automated solution we have built most all of the groundwork to create automatically generated schedules. This was an intentional design choice on our part.__


## What we learned
**Scheduling is hard!** By far the biggest and still unresolved challenge we faced is that courses are not consistently offered on a semester by semester or even year by year basis at Olin. This information is absolutely necessary to make this program usable, let alone completely automating the process. There is also nto data for us to take into account for classes that may be offered at the same time during the day. We actually had to register for classes while working on this project, it seems that in many cases students aren't particularly worried with how the rest of course fit in, in the big picture but more how they can get the courses they want. 

Additionally, because of website layouts, we found it easier for this project to only provide the tool for ECE and MechE majors - Olin's other majors, like E:C, E:R, and E:D have looser requirements and less of a need for a tool like this - their requirements are also stored in a different website format that we will scrape from at a later date. 

## The future
We tried to design our program and data structures in a way that could be scaled to other colleges' courses and scheduling systems. Whether this is practical is an entirely different matter. Olin has a very unique set of requirements but with little adaptation this could certainly be applied to other school's courses and majors. Development is going to pause on this project as we have other responsibilities at the moment. 
The biggest change we would add on top of the current system, if we had the time, would be to check for inconsistent course offerings depending on the semester & year. That would make a huge difference in the usability of the software. 

## Usage/Building a schedule
This software was developed on both Windows and Linux environments. However, we recommend using linux to run this as it handles our text output and interface much better.
Please check out the readme to understand how to use install this tool
[view the Readme](/README.md)

__Running the tool!__
1. Execute the main script via command line:

        python3 bottom_up.py
2. If the script detects previously saved schedules, you will be asked if you want to load them, you can do this by specifying the number in parantheses. See screen capture below
![A Rough Digram](/docs/loadSaved.PNG)

3. The script will now display which semester is being built. If you insert "__*__" it will show degree requirements. and progress towards these requirements. These are split into sections of classes which you must take all of. As well as sections of classes where you must only take one class form a short list, we refer to these as "One-Offs"(Pictured Below) ![A Rough Digram](/docs/oneOffs.PNG)

   In order to make some of the text more readable and interactable, we colorcode much of the text spit out, to help users make faster, more informed decisions. 

5. With this information the program asks you to input what course you would like to add to your schedule for the semester. The inpput must be crns, they can be either case, and sperated by spaces, commas, or both.Note that the crn's for loa and study away are "LOA" and "STUDY_AWAY" respectively. See screenshot below for a valid input.![A Rough Digram](/docs/inputStyles.PNG)

6. If input is either not a valid crn, or the crn you have inputted cannot be taken at this time you will receive an error message and you must re-enter valid courses for that semester. This capture shows a potential error message: ![A Rough Digram](/docs/crnError.PNG)

7. If the CRN's given are valid then the user is greeted with ascii charts indicating how close the student is to completing the general graduation requirements(seen above). 

8. The user will presented with another choice that dictates how to continue the program. A user can save their schedule so that it can be built off of another time, they can simply continue to the next semestet, or they can specify a semester to plan for (past or future). Quitting the program is also possible. The most important feature here is that you can do multiple things at once. If there is an 's' in your input the schedule will be saved ('sq', 's10', '5s'). Likewise a 'q' in the input will close the program, if there is an 's' it will save before terminating. See below for an example of saving and moving to edit a previous semester.

9. When you have reached the desired level of completion of your schedule you can save and exit the program. The output is saved in the working directory/savedSchedules/_filename_.txt

## Attribution 
This project relies heavily on the Beautiful Soup 4 python library which is used to scrape Olin's online catalog. 
