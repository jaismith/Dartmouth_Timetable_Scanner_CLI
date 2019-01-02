# Dartmouth_Timetable_Scanner
A simple program to scan the Dartmouth Timetable for open seats. Supports SMS notifications through [Twilio](https://www.twilio.com).

### Requirements

- [Python 3](https://www.python.org/downloads/)
- pip3 (should be installed by default with Python 3)

### Setup

Run setup.py and provide the requested parameters. Course CRN's and Departments should be provided as shown on the Dartmouth Timetable.

###### Example:
CS10, Problem Solving: Object Oriented (19W Section 1) corresponds to the following parameters:
- CRN: 10517
- DEPT: COSC
- TERM: 201901

### Twilio

To utilize the SMS functionality of this project, you will need a Twilio account. A free trial works fine, and can be signed up for [here](https://www.twilio.com/try-twilio). Add your cell phone number as a verified number from your account settings page, and copy the requested values into the setup.py script to enable SMS. Please note that with this setting enabled, the program will send a text for each class with an empty seat at the frequency with which it scans (can be high!).

Note: "Twilio Number" refers to your trial number on your twilio account, NOT your own phone number.
