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
1. Execute the main script via command line:

        python3 bottom_up.py
2. Script will prompt you to input courses you have taken, or you can choose a template schedule (basic first year requirements)
3. Script will continue to move forward through your time at Olin giving suggestions for potentially benefitial courses and requiring you to select them.
4. Final part of this script will allow you to save your schedule as a text file and as a format that can be reopend again from this script
