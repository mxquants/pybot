#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# %% Requirements 

import os
import sys
import json

import requests
from flask import Flask, request
from interact import * 

# %% Declare App 

app = Flask(__name__)


# %% GET and verify() function 

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world, this is pyBot by mxquants. Have a pythonic day! ", 200

# %% POST 

@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":
        

        for entry in data["entry"]:
            
            Respond = RespondEntryMessages(entry)
            temp = list(map(sendMessage, Respond.now()))
            
            """
            
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text

                    response_text = generateResponse(data)
                    sendMessage(sender_id, str(response_text))#"got it, thanks!")

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass
            """

    return "ok", 200


# %% sendMessage 

def sendMessage(repond_info):
    recipient_id, message_text = repond_info["Sender"],repond_info["Response"]
    
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

# %% Log function -- simple wrapper for logging to stdout on heroku

def log(message):
    print(str(message))
    sys.stdout.flush()



# %% Test  

@app.route('/test', methods=['GET'])
def returnTestImage():
    html = """\ 
<!DOCTYPE html>
<html>
<body>
<h2>The Incredible pyBot!</h2>
<img src="https://scontent-dft4-2.xx.fbcdn.net/v/t34.0-12/18051760_10156149925989966_1903532741_n.png?oh=d54e7de3f9776a37d92ecd402d1f97a6&oe=58FFBAD0">
</body>
</html>
    """
    return html 
# %% 

if __name__ == '__main__':
    app.run(debug=True)
