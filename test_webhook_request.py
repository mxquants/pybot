#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# %% imports 

import requests


# %% Request similar to FB-Messenger API

def simulateWebhookRequest(challenge="pyBot's webhook works fine!"):
    
    parameters = {"hub.mode":"subscribe","hub.challenge":challenge,"hub.verify_token":"subscribe"}
    r = requests.get("https://amazing-pybot.herokuapp.com/",
                     params=parameters)
    
    return r


# %% 

def interpretResponse(r,_print=True):
    
    if _print:
        print('\nResponse code: {}'.format(r.status_code))
        print('Response text (challenge): {}'.format(r.text))
        print('Response status: {}\n'.format(r.status_code == requests.codes.ok))
    
    return r.status_code == requests.codes.ok

# %% 


def main():
    r = simulateWebhookRequest()
    return interpretResponse(r)

# %% 

if __name__ == '__main__':
  main()
