#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pyBot Rest API.
This is pyBot's rest API.

@author: Rodrigo Hernández-Mota
rhdzmota@mxquants.com
"""

import os
import io
import sys
import json
import requests
import datetime as dt
from flask import Flask, request, render_template
from interact import RespondEntryMessages


def readJson(filename):
    """Read a .txt file that contains a json."""
    with open(filename) as file:
        data = json.load(file)
    return data


def saveJson(variable, filename):
    """Save a dict as a .txt containing a json."""
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(variable, ensure_ascii=False))


#  Declare App
app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    """Verify if FB-Messenger or something else."""
    if request.args.get("hub.mode") == "subscribe" and \
            request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == \
             os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return render_template('index.html'), 200


@app.route('/', methods=['POST'])
def webhook():
    """Facebook Messenger Webhook."""
    data = request.get_json()
    log(data)
    data = generalFilter(data)
    if data["object"] == "page":
        for entry in data["entry"]:
            Respond = RespondEntryMessages(entry)
            list(map(sendMessage, Respond.now()))
    return "ok", 200


# Send Message
def generatePostJsonData(response_info):
    """Generate Json Data for FB-M Post."""
    _type = response_info['_type']
    recipient_id = response_info["Sender"]
    if "text" in _type:
        message_text = response_info["Text"]
        data = json.dumps({
                            "recipient": {"id": recipient_id},
                            "message": {"text": message_text}
                            })
        return data
    if "image" in _type:
        image_url = response_info["ImageURL"]
        data = json.dumps({
                            "recipient": {"id": recipient_id},
                            "message": {"attachment": {
                                    "type": "image",
                                    "payload": {
                                            "url": image_url,
                                            "is_reusable": True}}}})
        return data


def sendMessage(response_info):
    """Send Message to FB-Messenger."""
    params = {"access_token": os.environ["PAGE_ACCESS_TOKEN"]}
    headers = {"Content-Type": "application/json"}
    data = generatePostJsonData(response_info)
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params,
                      headers=headers,
                      data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


# Log data at Heroku
def log(message):
    """Log data into Heroku."""
    print(str(message))
    sys.stdout.flush()


# Filter data (not functional)
def generalFilter(data):
    """Filter data."""
    def createEntryLog():
        # entry_log =[]
        # np.save('entry_log.npy',entry_log)
        entry_log = {}
        saveJson(entry_log, 'entry_log.txt')

    try:
        entry_log = readJson('entry_log.txt')
    except:
        createEntryLog()
        entry_log = entry_log = readJson('entry_log.txt')

    # get entries
    entries = data.get('entry')
    if entries is None:
        return data

    # get new ids
    good_entries = [entry for entry in entries
                    if (str(entry) not in entry_log.keys())]
    for entry in entries:
        entry_log[str(entry)] = dt.datetime.now().strftime('%Y%m%d %H:%M:%S')

    # save
    # np.save('entry_log.npy',entry_log)
    # saveJson(entry_log,'entry_log.txt')
    data['entry'] = good_entries
    return data


if __name__ == '__main__':
    app.run(debug=True)
