---
title: Olin Course Scheduling Assistant
description: some description
---

## Why did we do this? 
Worrying about graduating isn't fun! We are both students at Olin College of Engineering and thought that we could alleviate some of this stress. By looking at all course offerings and major requirements we believe that we can help automate that process of building a course schedule for your college career.
Here's a quick screenshot of where this is right now:

## Usage/Installation ->README
This software was developed on both Windows and Linux environments. However, we recommend using linux to run this as it handles our text output and interface much better.
Please check out the readme to understand how to use this tool
[View Readme](/README.md)

## Results/What this does
Please take alook at the doc [View Saving Documentation](/saved_schedules/saving_readme.md)
This tool can be used to achieve several different results. One option is to simply input your schedule as it sits and validate for any errors like a lack of Pre-Reqs etc. Another option is to generate a slew of schedules that let you plan out for less-ideal situations and make sure that you can have a plan if things don't go your way. This tool makes it possible to see flexibility with multiple schedules rather than storing all of these options mentally.
Here you can see what completed schedule looks like(saved as .txt file):

INSERT IMAGE

You can also see warning messages when trying to register for courses that you don't have the pre-reqs for:

INSERT IMAGE

Though the details will be different for each project, show off what your software can do! Screenshots and video are likely helpful. Include graphs or other data if appropriate.

## Project Evolution
Our original goals for this project were centered around making the scheduling process entirely automatic. This would allow students to basically see many different permutations of their schedule and see if ceratin choices significantly limited their options or potential to graduate.

It became clear early on that while this may have been possible, we lacked a lot of data that would make this data useful. We scoped the project down to an assistant that would help students understand which courses they needed to take for requirements and would easily let them store different variations. This was a logical choice because it was more realistic and would require almost the exact same architecture. This meant that moving forward we wouldn't need to do a complete redesign to implement more automatic approaches.

By the time of our first code review we had succesfully parsed all of the major requirements and courses form Olin's site. We had a rough idea of how we would store and build schedules but no code. By our second review we had written out a large amount of background and helper funcitons that allowed us to interact with course and requirement data, as well as user input. From this point we worked to flesh outa workflow that users could viably use to build schedules, leading to most recent design changes reagrding what information and controls the user has while running the program.

_Why a command line tool?_

Originally there were plans to build a formal gui for this tool. These plans were shelved as we built the core of the application. We also feel that a Command line tool in this application is actually very usable so have devoted efforts elsewhere. In the future we would consider making a GUI as it would make this tool easier and more logical to use.

## What we Learned
**Scheduling is hard!** One of the larest roadblocks we ran into was the fact that courses aren't consistentyl offered year to year at Olin. This information is necessary to make this process more automated. There is also nto data for us to take into account for classes that may be offered at the same time during the day. We actually had to register for classes while working on this project, it seems that in many cases student's aren't particularly worried with how the rest of course fit in but more how they can get the courses they want. 

## The Future
We tried to design our program and data structures in a way that could be expanded and moved to potentially other colleges. Whether this is practical is an entirely different matter. Olin has a very unique set of requirements but with little adaptation this could be applied to other school's courses and majors. Development is going to pause on this project as we have other responsibilities at the moment. 


## Implementation information and usage
For a usage guide please refer to the [Readme](/README.md)
TODO:
Code doesn’t tell a story by itself. Use more effective methods such as flowcharts and architectural, class, or sequence diagrams to explain how your code works. You could consider including or linking to snippets of code to highlight a particularly crucial segment.
```py
def clean_course_list(self, course_lst, semester=None):
    # Not sure if code is needed
    """
    Runs valid course on a list of courses and returns the valid ones
    :return:
    """
    return [course for course in course_lst if self.valid_course(course, semester)]
```

## Attribution 
This project relies heavily on the Beautiful Soup 4 ppyhton library which is used to scrape Olin's online catalog. 
