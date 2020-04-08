# Olinvisor, a scheduling program for Olin students
## Background and context 
The goal of this project is to make a semi-automated course scheduler for students. They will be able to input their current courses and other restraints (LOA, study away, etc) and their degree and recieve potential schedules they could take.
We plan to do this off of various information that we have access to:
* Olin course online catalgue (has CRN and credits etc, as well as degree requirements)
* This year's fall and spring offerings(to establish which semeseters courses are offered)

What information about your project does the audience need to participate fully in the technical review? You should share enough to make sure your audience understands the questions you are asking, but without going into unnecessary detail.

## Key questions
Our current concerns are mainly centered around how to build our algorithm to determine what courses to take. We also are interested in thoughts and feedback onto datatype choices for the various pieces of our model.
Our current implentations stores courses and their data as a dictionary of dictionaries. We are unsure if this would be more benefitial in a class. We are debating making the catalogue a class. 
We also need to store data for an individual user (what classes they have taken etc). We feel this belongs in a class so that supporting methods regarding filling in the schedule can be applied. The course requirements are also stored in a class so that supporting methods can be written. We are very interested in feedback on theses decisions.


What do you want to learn from the review? What are the most important decisions your team is currently contemplating? Where might an outside perspective be most helpful? As you select key questions to ask during the review, bear in mind both the time limitations and background of your audience.

## Agenda for technical review session 
* Intro to our project and what we are trying to do (2mins)
* Intro into our current implentation strategy and MVP  (3mins)
* Concerns of having the correct/complete data and what that means (1min)
* Questions about our implemntation strategy (1min)
* Feedback/Discussion (4mins)
We will use a google slide to attempt to visualize what we are attempting to do

Be specific about how you plan to use your allotted time. What strategies will you use to communicate with your audience?

## Feedback form

Create a Google form that folks in the review will use to provide you with feedback or answers to various questions you pose to your audience. Since, at least for the first review, the time you have to present will be relatively short you should expect much of the feedback you get to come from this form rather than thoughts expressed orally during your session. Please create a feedback form tailored for your architectural review and share the link no less than 2 hours before class.
