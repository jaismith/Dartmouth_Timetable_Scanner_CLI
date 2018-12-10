"""
main file for timetable scanner

author: Jai Smith
date: December 2018
"""

# imports

import requests
from time import sleep

# settings

# for sms updates
SMS_ACTIVE = False
SMS_RECIPIENT = None
TWILIO_SID = None
TWILIO_AUTH_TOKEN = None
TWILIO_NUMBER = None

# other
TERMS = [201901]
COURSES = [('COSC', '10517'), ('ARAB', '10745')]
INTERVAL = 120

# variables

headers = dict()
data = list()

# setup (get request parameters from parameters.txt)

parameters = open('parameters.txt', 'r')

parameters.seek(0, 2)
parameters_size = parameters.tell()
parameters.seek(0, 0)

while parameters_size - parameters.tell() > 0:
    current = parameters.readline().strip()

    if current == 'headers':
        current_line = None

        while True and parameters_size - parameters.tell() > 0:
            current_line = parameters.readline()

            if current_line != '\n':
                new_header = current_line.split(':')
                key, value = new_header[0], new_header[1]

                extra = str.maketrans('', '', " '\n")

                key = key.translate(extra)
                value = value.translate(extra)

                headers[key] = value

            else:
                break

    elif current == 'data':
        current_line = None

        while True and parameters_size - parameters.tell():
            current_line = parameters.readline()

            if current_line != '\n':
                new_data = current_line.split(',')
                key, value = new_data[0], new_data[1]

                extra = str.maketrans('', '', " ()'\n")

                key = key.translate(extra)
                value = value.translate(extra)

                data.append((str(key), str(value)))

for term in TERMS:
    data.append(('terms', term))

for course in COURSES:
    data.append(('depts', course[0]))

# functions


def query_timetable():
    response = requests.post(
        'https://oracle-www.dartmouth.edu/dart/groucho/' +
        'timetable.display_courses', headers=headers, data=data)

    return response


def find_courses(timetable):
    course_data = list()

    for course in COURSES:
        crn_index = timetable.find('crn=' + course[1])

        if crn_index < 0:
            print("Error. Course not found.")
            break

        left_bound = crn_index

        for i in range(8):
            left_bound = timetable.find('<td>', left_bound + 4)

        left_bound += 4
        right_bound = timetable.find('</td>', left_bound)

        course_limit = int(timetable[left_bound: right_bound])

        left_bound = right_bound + 10
        right_bound = timetable.find('</td>', left_bound)

        course_enrollment = int(timetable[left_bound: right_bound])

        course_data.append((course_limit, course_enrollment))

    return course_data


# main code

if SMS_ACTIVE:
    from messaging import configure_twilio, send_sms

configure_twilio(TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER)

while True:
    timetable = query_timetable()

    course_data = find_courses(timetable.text)

    for i in range(len(COURSES)):
        if course_data[1] < course_data[0]:
            message = ('Seat(s) available in {0}, {1} department.' +
                       ' Current enrollment: {2} / {3}'
                       ).format(COURSES[i][1], COURSES[i][0],
                                course_data[i][1], course_data[i][0])

            if SMS_ACTIVE:
                send_sms(message, SMS_RECIPIENT)

            print(message)

    sleep(INTERVAL)
