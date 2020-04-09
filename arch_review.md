# Olinvisor, a scheduling program for Olin students
## Background and context 
The goal of this project is to make a semi-automated course scheduler for students. They will be able to input their current courses and other restraints (LOA, study away, etc) and their degree and recieve potential schedules they could take.
We plan to do this off of various information that we have access to:
* Olin course online catalgue (has CRN and credits etc, as well as degree requirements)
* This year's fall and spring offerings(to establish which semeseters courses are offered)

## Key questions
Our current concerns are mainly centered around how to build our algorithm to determine what courses to take(iteratively, or top down).
We also are interested in thoughts and feedback onto datatype choices for the various pieces of our model.
Our current implentations stores courses and their data as a dictionary of dictionaries. We are unsure if this would be more benefitial in a class.
We also need to store data for an individual user (what classes they have taken etc). We feel this belongs in a class so that supporting methods regarding filling in the schedule can be applied. The course requirements are also stored in a class so that supporting methods can be written. We are very interested in feedback on these decisions.

## Agenda for technical review session 
https://docs.google.com/presentation/d/13o11vtV_CnRqjwEzais8MNkHSxNGDNZTTsFdXRmnxQk/edit?usp=sharing
* Intro to our project and what we are trying to do (2mins)
* Intro into our current implentation strategy and MVP  (2mins)
* Questions about our implemntation strategy (2min)
* Feedback/Discussion (3mins)
We will use a google slide to attempt to visualize what we are attempting to do

## Feedback form
https://docs.google.com/forms/d/e/1FAIpQLSeZTni63e7iXQN79HMJLp0FXd5wcCXFLQNPRyuSbtoOiWGMjQ/viewform
