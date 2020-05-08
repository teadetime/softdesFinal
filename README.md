# Olin Interactive Advising Tool

### Intro and Description
Our scheduling assistant seeks to help student's easily walk through potential ways to schedule their courses at Olin with computer assistance.
This tool will help student's easily see what classes can be taken at given times. This tool can also help measure  how you are progressing towards major requirements. Future iterations will be able to offer a higher level of automation.

### Authors

This project was co-developed by [Nathan Faber](https://github.com/teadetime "@teadetime") and [Adi Ramachandran](https://github.com/aramachandran7 "@teadetime") for the course Software Design at [Olin College of Engineering](https://github.com/olin).


### Getting started/Installation
1. Clone or pull this github Repo
2. Navigate to root folder of the repo via terminal
3. Ensure that python3 and pip are installed
4. Activate and/or create a python3 venv (optional)
5. To install required packages run the following command from the root of the project (may require sudo privileges)

        pip3 install -r requirements.txt

### Usage/Building a schedule
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

4. When you have reached the desired level of completion of your schedule you can save and exit the program. The output is saved in the working directory/savedSchedules/_filename_.txt
