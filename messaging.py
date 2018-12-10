"""
short program to send a text using the twilio service
https://www.twilio.com

author: Jai Smith
date: December 2018
"""

# imports

from twilio.rest import Client

# variables
number = None
client = None


def configure_twilio(sid, auth_token, set_number):
    global number, client

    number = set_number
    client = Client(sid, auth_token)


def send_sms(content, recipient):
    message = client.messages.create(
        body=content,
        from_=number,
        to=recipient)

    print('Message sent to {0} successfully'.format(recipient))

    return message.sid
