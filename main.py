"""
main file for timetable scanner

author: Jai Smith
date: December 2018
"""

# imports

import requests

# settings

SMS_ACTIVE = False
TERMS = [201901]
COURSES = [('COSC', 10517)]
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
    response = requests.post('https://oracle-www.dartmouth.edu/dart/groucho/timetable.display_courses', headers=headers, data=data)

    return response


print(headers)
print(data)

print("making query")

print(query_timetable().text)
