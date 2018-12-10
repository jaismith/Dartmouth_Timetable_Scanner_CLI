"""
setup file for Dartmouth_Timetable_Scanner

author: Jai Smith
date: December 2018
"""

# imports

import pip
import pickle

# variables

number_of_courses = None
course_crns = list()
course_depts = list()

SMS_RECIPIENT = None
TWILIO_SID = None
TWILIO_AUTH_TOKEN = None
TWILIO_NUMBER = None

queries = [
    'Number of courses you would like to track: ',
    'CRN of course #{0}: ',
    'Department of course #{0}: ',
    'Target term (numeric): ',
    'Interval between scans (in milliseconds): ',
    'Enable text notifications? (y/n): ',
    'Twilio SID: ',
    'Twilio Auth Token: ',
    'Twilio Number (include +1, no spaces): ',
    'SMS Recipient (include +1, no spaces): ',
]

# functions


def get_int(message):
    token = input(message)

    while True:
        try:
            token = int(token)
            return token

        except ValueError:
            print("Error. Please enter an integer value.")
            token = input(message)


def get_yes_no(message):
    token = input(message)

    while token != 'y' and token != 'n':
        print("Error. Please enter either 'y' or 'n'.")
        token = input(message)

    return token


# main code

print("Running setup...")

for query_index in range(len(queries)):
    if query_index == 0:
        number_of_courses = get_int(queries[0])

    elif query_index == 1:
        for i in range(number_of_courses):
            course_crns.append(str(get_int(queries[1].format(i))))

    elif query_index == 2:
        for i in range(number_of_courses):
            course_depts.append(str(input(queries[2].format(i))))

    elif query_index == 3:
        TERM = get_int(queries[3])

    elif query_index == 4:
        INTERVAL = get_int(queries[4])

    elif query_index == 5:
        SMS_ACTIVE = get_yes_no(queries[5]) == 'y'

    elif query_index == 6 and SMS_ACTIVE:
        TWILIO_SID = input(queries[6])

    elif query_index == 7 and SMS_ACTIVE:
        TWILIO_AUTH_TOKEN = input(queries[7])

    elif query_index == 8 and SMS_ACTIVE:
        TWILIO_NUMBER = input(queries[8])

    elif query_index == 9 and SMS_ACTIVE:
        SMS_RECIPIENT = input(queries[9])

COURSES = list()

for i in range(number_of_courses):
    COURSES.append((course_depts[i], course_crns[i]))

with open('preferences', 'wb') as f:
    pickle.dump([TERM, COURSES, INTERVAL, SMS_ACTIVE, SMS_RECIPIENT,
                 TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER], f)

if SMS_ACTIVE:
    print("Installing twilio package with pip...")
    
    pip.main(['install', 'twilio'])
