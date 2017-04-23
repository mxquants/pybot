#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 15:01:34 2017

@author: rhdzmota
"""

from snake_talk import *
from pyBot import *
from jokes import *

# %% Sample message

def generateSampleData(message='integrate x from 0 to 5'):
    
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
    user_name =  _user if _user is not None else 'Pythonist'
    _text = """\
Hi there! 

My name is pyBot, a basic AI capable of talking with sankes.

You can write python 3.6.1 code and I will return whatever you specify in the print() function. Use the hashtag #py at the beginning of the message so I can tell you are speaking Parseltongue.\n\n
                                                                                   
Happy coding {}!
    """
    return _text.format(user_name)

def deleteFirstWhitespace(text):
    return (text if text[0] != ' ' else deleteFirstWhitespace(text[1:])) 

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
    if ('como' in text.lower() or 'cómo' in text.lower()) and 'llamas' in text.lower():
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
    
    if text == '#py' or text == '# py' or text == '#py 'or text == ' #py ':
        return 'print(No code found!)'
    if text == '#python' or text == '# python':
        return 'print(No code found!)'
    
    if 'python' in text.lower():
        code = 'python'.join(text.split("python")[1:])#text.split("python")[-1]
        return (code[1:] if code[0]==" " else code)
    code = 'py'.join(text.split("py")[1:])
    return (code[1:] if code[0]==" " else code)

def identifyIntegrals(text):
    if 'integrate' in text.lower():
        if 'from' in text.lower() and 'to' in text.lower():
            return 1
    return 0

def getIntegralElements(text):
    from_to = list(map(deleteFirstWhitespace,text.split("from")[-1].split("to")))
    return {"function":deleteFirstWhitespace(text.split("from")[0].split("integrate")[-1]),
            "from":from_to[0],"to":from_to[-1]}

def integralAnswer(text):
    answer = integralWrapper(getIntegralElements(text))
    complete = "The result for your integral, using Monte-Carlo approx is: \n\n\t{}"
    return complete.format(answer)

def identifyJoke(text):
    if 'chiste' in text.lower():
        return 1
    if 'joke' in text.lower():
        return 1
    if 'humor' in text.lower():
        return 1
    if 'relax' in text.lower():
        return 1
    return 0

def getOneJoke():
    _text = "I've got a joke for you: \n\n"
    return _text+chooseJoke()

def myNameIs():
    return 'My name is... Heissenberg!\n\nJK, you can call me pyBot.' 

def genericGreetingMesasge(sender):
    import numpy as np
    _user = getUserInfo(sender).get('first_name')
    user_name =  _user if _user is not None else 'Pythonist'
    
    generic_message = {}
    generic_message[1] = """\
    Hey Pyhonist! Good to hear about you. 
    """
    generic_message[2] = """\
    Hello {}! :)
    """.format(user_name)
    
    generic_message[3] = """\
    Hi there. How is it going?
    """
    generic_message[4] = """\
    Er... Huh... Hello. ;) 
    """
    _index = np.random.uniform()
    _list  = list(jokes.keys())
    return generic_message[_list[int(len(_list)*_index)]]
    
    
def IDontUnserstand(sender):
    _user = getUserInfo(sender).get('first_name')
    user_name =  _user if _user is not None else 'Pythonist'
    _text = """\
I'm sorry {}, still learning to talk here. 

You can use #py before writing some python code and I'll certainly understand. Let's talk with snakes! 

...or you can ask me some jokes. ;)
    """
    return _text.format(user_name)

# %% Generate Response



def generateResponse(text,sender):
    
    if identifyPyCode(text):
        text_script = getPyCode(text)
        SP = SpeakPython(script=text_script,user=sender)
        return SP.interpret()
    
    if identifyShortMessageAndGreeting(text):
        return genericGreetingMesasge(sender)
    
    if identifyWhoYouAre(text):
        return firstGreetingMessage(sender)
    
    if identifyWhatsYourName(text):
        return myNameIs()
    
    if identifyIntegrals(text):
        return integralAnswer(text)
    
    if identifyJoke(text):
        return getOneJoke()
    
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
                response = 'Nice '+str(mevent['message']['attachments'][0]['type'])
            else: 
                response = generateResponse(text,sender)
            
            return {'Sender':sender,'OriginalText':text, 'Response':response}
        
        #if len(self.message_list):
        #    return 'Okay!'
            
        self.respond_list = map(getSenderAndText,self.message_list)
        return self.respond_list

# %% 