#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 15:01:34 2017

@author: rhdzmota
"""

from snake_talk import *
# %% Sample message

def generateSampleData(message='#pycode print("hey")'):
    
    data =     {
                "object":"page",
                "entry":[
                    {
                        "messaging":[
                            {
                                "message":{
                                    "text":message,
                                    "seq":20,
                                    "mid":"mid.1466015596912:7348aba4de4cfddf91"
                                },
                                "timestamp":1466015596919,
                                "sender":{
                                    "id":"885721401551027"
                                },
                                "recipient":{
                                    "id":"260317677677806"
                                }
                            }
                        ],
                        "time":1466015596947,
                        "id":"260317677677806"
                    }
                ]
            }
    
    return data

def messagingEvent(message='#pycode print("hey")'):
    msg = {
                                "message":{
                                    "text":message,
                                    "seq":20,
                                    "mid":"mid.1466015596912:7348aba4de4cfddf91"
                                },
                                "timestamp":1466015596919,
                                "sender":{
                                    "id":"885721401551027"
                                },
                                "recipient":{
                                    "id":"260317677677806"
                                }
                            }
    return msg 

def simulateEntry(n=1,message='#pycode print("hey")'):
    
    entry = {
                        "messaging":[
                            {
                                "message":{
                                    "text":message,
                                    "seq":20,
                                    "mid":"mid.1466015596912:7348aba4de4cfddf91"
                                },
                                "timestamp":1466015596919,
                                "sender":{
                                    "id":"885721401551027"
                                },
                                "recipient":{
                                    "id":"260317677677806"
                                }
                            }
                        ]*n,
                        "time":1466015596947,
                        "id":"260317677677806"
                    }
    return entry 
    

# %% Interpret

def getUserInfo(sender_id='1657838257577411'):
    import requests
    pat = 'EAAaiAN9H6KEBANNiZCZA1xnwt1wxd9twtZADhHkfvpWHCh8JaVd7CNZB61Yb0jMZA4KAFChAyDNz74ZCpoaWyvNGH2khu6N8LdVEzePFJZC6ueCfvM9Tm9R0d8Ebj4DoZC8CTNbrVISI3DB0MMZBFtNQRlvH9WRcc2xfhS1tCTNJyOQZDZD'
    userprofile_api = 'https://graph.facebook.com/v2.6/{USER_ID}?fields=first_name,profile_pic,gender&access_token={PAGE_ACCESS_TOKEN}'
    return eval(requests.get(userprofile_api.format(USER_ID=sender_id,PAGE_ACCESS_TOKEN=pat)).text)


def firstGreetingMessage(sender):
    _user = getUserInfo(sender).get('first_name')
    user_name =  _user if _user is not None else 'Crabisiño'
    return 'Hello {}! My name is pyBot, a basic AI capable of talking with sankes.\nYou can write python 3.6.1 code and I will return whatever you specify in the print() function. Use the hashtag #py at the beginning of the message so I can tell you are speaking Parseltongue.\n\n Happy coding!'.format(user_name)
    
def identifyShortMessageAndGreeting(text):
    n = len(text)
    if n > 25:
        return 0
    if 'hola' in text.lower():
        return 1
    if 'que onda' in text.lower():
        return 1
    if 'que tal' in text.lower():
        return 1
    if 'saludos' in text.lower():
        return 1
    if 'hello' in text.lower():
        return 1
    if 'hi' in text.lower():
        return 1
    if 'hey' in text.lower():
        return 1
    return 0

def identifyWhoYouAre(text):
    if 'quien eres' in text.lower():
        return 1
    if 'que eres' in  text.lower():
        return 1
    if 'quién eres' in text.lower():
        return 1
    if 'qué eres' in  text.lower():
        return 1
    return 0

def identifyWhatsYourName(text):
    if 'nombre' in text.lower():
        return 1
    if 'name' in text.lower():
        return 1
    if 'como' in text.lower() and 'llamas' in text.lower():
        return 1
    if 'apodo' in text.lower():
        return 1
    return 0

def identifyPyCode(text):
    if "#py" in text.lower():
        return 1
    if "# py" in text.lower():
        return 1
    if "#python" in text.lower():
        return 1
    if "# python" in text.lower():
        return 1
    return 0

def getPyCode(text):
    if 'python' in text.lower():
        return text.split("python")[-1]
    return text.split("py")[-1]

def myNameIs():
    return 'My name is... Heissenberg!\n\nJK, you can call me pyBot.' 

def genericGreetingMesasge():
    return 'Hey pythonist! Is a pleasure to hear about you.'
    
    
def IDontUnserstand(sender):
    _user = getUserInfo(sender).get('first_name')
    user_name =  _user if _user is not None else 'Pythonist'
    return 'Iam sorry {}, still learning to talk here. You can use #py and some python code and I will surely understand!'.format(user_name)

# %% Generate Response



def generateResponse(text,sender):
    
    if identifyPyCode(text):
        text_script = getPyCode(text)
        SP = SpeakPython(script=text_script,user=sender)
        return SP.interpret()
    
    if identifyShortMessageAndGreeting(text):
        return genericGreetingMesasge()
    
    if identifyWhoYouAre(text):
        return firstGreetingMessage(sender)
    
    if identifyWhatsYourName(text):
        return myNameIs()
    
    return IDontUnserstand(sender)

# %% 

class Test(object):
    
    def __init__(self,message='Qué tal Crabo'):
        self.text_message = message
        
    def perform(self,_inplace=True):
        self.data = generateSampleData(self.text_message)
        self.respond = generateResponse(self.data)
        if _inplace:
            return self.respond 
    
    
# %% 

class RespondEntryMessages(object):
    
    def __init__(self,entry):
        self.entry = entry
        #self.message_list = [mevent for mevent in entry['messaging'] if mevent.get('message')]
        self.message_list,self.delivery_list,self.optin_list,self.postback_list = [],[],[],[]
        for mevent in entry['messaging']:
            
            if mevent.get('message'):
                self.message_list.append(mevent)
                
            if mevent.get('delivery'):
                self.delivery_list.append(mevent)
                
            if mevent.get('optin'):
                self.optin_list.append(mevent)
                
            if mevent.get('postback'):
                self.postback_list.append(mevent)
        
    def now(self):
        
        def getSenderAndText(mevent):
            sender = mevent['sender']['id']
            text   = mevent['message']['text'] if mevent['message'].get('text') else 0
            if not text:
                response = 'Nice '+str(mevent['message']['attachments']['type'])
            else: 
                response = generateResponse(text,sender)
            
            return {'Sender':sender,'OriginalText':text, 'Response':response}
        
        if len(self.message_list):
            return 'Okay!'
            
        self.respond_list = map(getSenderAndText,self.message_list)
        return self.respond_list

# %% 