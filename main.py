"""
main file for timetable scanner

author: Jai Smith
date: December 2018
"""

# imports

import requests
from time import sleep, time
import pickle

# settings

# for sms updates
SMS_ACTIVE = None
SMS_RECIPIENT = None
TWILIO_SID = None
TWILIO_AUTH_TOKEN = None
TWILIO_NUMBER = None

# other
TERM = None
COURSES = list()
INTERVAL = None

last_scan = None
last_update_text = None

with open('preferences', 'rb') as f:
    (TERM, COURSES, INTERVAL, SMS_ACTIVE, SMS_RECIPIENT,
     TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER) = pickle.load(f)

# variables

headers = dict()
data = list()

# setup (get request parameters from parameters.txt)

parameters = open('post_parameters', 'r')

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

data.append(('terms', TERM))

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

print("Current configuration: TERM: {0}, COURSES: {1}".format(TERM, COURSES))

if SMS_ACTIVE:
    from messaging import configure_twilio, send_sms

    configure_twilio(TWILIO_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER)

    send_sms(str("Dartmouth_Timetable_Scanner program started and configured" +
                 " to text this number."), SMS_RECIPIENT)

while True:
    if last_scan is None or time() - last_scan > INTERVAL:
        timetable = query_timetable()

        course_data = find_courses(timetable.text)

        if len(course_data) < 1:
            break

        for i in range(len(COURSES)):
            if course_data[i][1] < course_data[i][0]:
                message = ('Seat(s) available in {0}, {1} department.' +
                           ' Current enrollment: {2} / {3}'
                           ).format(COURSES[i][1], COURSES[i][0],
                                    course_data[i][1], course_data[i][0])

                if SMS_ACTIVE:
                    send_sms(message, SMS_RECIPIENT)

                print(message)

        last_scan = time()

    # hourly update text
    if last_update_text is None or time() - last_update_text > 3600:
        message = '*Hourly update*\nCourse enrollment:\n'
        for i in range(len(COURSES)):
            course = '{0} {1}: {2} / {3}\n'.format(COURSES[i][1],
                                                   COURSES[i][0],
                                                   course_data[i][1],
                                                   course_data[i][0])

            message += course

        send_sms(message, SMS_RECIPIENT)

        last_update_text = time()

    sleep(1)
