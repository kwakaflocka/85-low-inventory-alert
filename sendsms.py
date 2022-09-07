import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

def inventorySMS(data):
    account_sid=""
    auth_token=""

    if len(data) > 1600:
        data = data[0:1000] + '...'

    msg= f"Order more {data}"
    print(len(msg))
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=msg,
        from_="",
        to=""
    )
    print(message.status)
