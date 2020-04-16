# Feedback and decisions 
We received a variety of feedback to our main questions of how to structure our data and how to algorithmically build a student's schedule.
One of the most important things we took away was the necessity for course data and offerings to be volatile. 
We need to find a way to indicate what time this data has been pulled and at what point does it need to be refreshed. We have made the decision to store the course and major data in the schedule class so that the object can be pickled and stored so that we keep the correct versioning.
The positive feedback on datatypes was helpful, it confirmed we are moving forward in a valid way and we will continue witht he current plan unless we need to expand.
New questions arose in the volatility realm and the problems of dealing with changing requirements.

Our algorithm feedback was also helpful, Steve pointed out some of the benefits of both our "top-down" and "bottom-up" methods. 
Based on this feedback and the fact we wanted to make the most usable product and let the user have input we are working to implement a 'bottom-up' approach.

# Review process reflection
We both felt like we gained useful insight out of the review and validation of our current strategy! 
I think providing more visuals of our method flow and having a fleshed out function diagram would have been helpful, however we simply weren't at that stage yet.
We got answers to some of our big questions and are in a place where we can move forward with the project.
