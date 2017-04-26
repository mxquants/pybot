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

def getUserProfilePic(sender='1657838257577411'):
    from PIL import Image
    import image_hosting as ih
    import urllib.request
    import requests
    import os
    
    # set filename 
    tempo_filename = "profilepic_{}.jpg".format(sender)
    filename = "profilepic_{}.png".format(sender)
    
    # Page Access Token 
    pat = 'EAAaiAN9H6KEBANNiZCZA1xnwt1wxd9twtZADhHkfvpWHCh8JaVd7CNZB61Yb0jMZA4KAFChAyDNz74ZCpoaWyvNGH2khu6N8LdVEzePFJZC6ueCfvM9Tm9R0d8Ebj4DoZC8CTNbrVISI3DB0MMZBFtNQRlvH9WRcc2xfhS1tCTNJyOQZDZD'
    
    # FB API for user's info 
    userprofile_api = 'https://graph.facebook.com/v2.6/{USER_ID}?fields=first_name,profile_pic,gender&access_token={PAGE_ACCESS_TOKEN}'
    
    # get user's data 
    temp = eval(requests.get(userprofile_api.format(USER_ID=sender,PAGE_ACCESS_TOKEN=pat)).text)
    if not temp.get('profile_pic'):
        return "https://www.dropbox.com/s/ph4kd5pmrln49oi/NotAvailable.png?dl=0"
    urllib.request.urlretrieve(temp['profile_pic'].replace("\\",""), tempo_filename)
    
    # convert to .png 
    im = Image.open(tempo_filename)
    im.save(filename)
    
    # upload to dropbox
    DBM = ih.DropBoxManager()
    DBM.deleteFile(path="/profile_pics",filename=filename)
    DBM.uploadFile(path="/profile_pics",filename=filename)
    temo = DBM.getTemporaryUrl(path="/profile_pics",filename=filename)
    os.remove(tempo_filename)
    os.remove(filename)
    print(temo['url'])
    return temo['url']

def getUserInfo(sender_id='1657838257577411'):
    import requests
    pat = 'EAAaiAN9H6KEBANNiZCZA1xnwt1wxd9twtZADhHkfvpWHCh8JaVd7CNZB61Yb0jMZA4KAFChAyDNz74ZCpoaWyvNGH2khu6N8LdVEzePFJZC6ueCfvM9Tm9R0d8Ebj4DoZC8CTNbrVISI3DB0MMZBFtNQRlvH9WRcc2xfhS1tCTNJyOQZDZD'
    userprofile_api = 'https://graph.facebook.com/v2.6/{USER_ID}?fields=first_name,profile_pic,gender&access_token={PAGE_ACCESS_TOKEN}'
    return eval(requests.get(userprofile_api.format(USER_ID=sender_id,PAGE_ACCESS_TOKEN=pat)).text)

# Parseltongue
def firstGreetingMessage():
    #_user = getUserInfo(sender).get('first_name')
    #user_name =  _user if _user is not None else 'Pythonist'
    _text = """\
Hi there! 

My name is pyBot, the only bot that can talk with snakes! Use #py at the beginning of your code so I can speak Parseltongue with you!
    """
    return _text#.format(user_name)

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


def identifyHowAreYou(text):
    if 'how' in text.lower() and 'are' in text.lower() and 'you' in text.lower():
        return 1
    if 'how' in text.lower() and 'its' in text.lower() and 'going' in text.lower():
        return 1
    if 'cómo' in text.lower() and ('estas' in text.lower() or 'andas' in text.lower()):
        return 1
    if 'fine' in text.lower() or 'good' in text.lower() or 'great' in text.lower():
        return 1
    return 0

def getResponseForHowAreYouAndOkays():
    import numpy as np 
    
    possible_responses={}
    
    possible_responses[1] = """\
    Great! 
    """
    possible_responses[2] = """\
    Perfect. :)
    """
    possible_responses[3] = """\
    Fine, good to know! 
    """
    possible_responses[4] = """\
    Everything is perfect. 
    """
    possible_responses[5] = """\
    Good, just chilling. 
    """
    possible_responses[6] = """\
    Okay ;)
    """
    possible_responses[7] = """\
    Awsome! 
    """
    possible_responses[8] = """\
    Pyfanstastic! 
    """
    possible_responses[9] = """\
    Like a pandas in jupyter. (:
    """
    possible_responses[10] = """\
    Same here!
    """
    _index = np.random.uniform()
    _list  = list(possible_responses.keys())
    return possible_responses[_list[int(len(_list)*_index)]]
    

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

# Solve Integrals 

def identifyIntegrals(text):
    if 'integrate' in text.lower():
        if 'from' in text.lower() and 'to' in text.lower():
            return 1
    return 0

def getIntegralElements(text):
    text = text.replace("^","**")
    from_to = list(map(deleteFirstWhitespace,text.lower().split("from")[-1].split("to")))
    return {"function":deleteFirstWhitespace(text.lower().split("from")[0].split("integrate")[-1]),
            "from":from_to[0],"to":from_to[-1]}

def integralAnswer(text):
    answer = integralWrapper(getIntegralElements(text))
    complete = "The result for your integral, using Monte-Carlo approx is: \n\n\t{}"
    return complete.format(answer)

# Matplotlib plots

def identifyPlot(text):
    if 'plot' in text.lower():
        if 'from' in text.lower() and 'to' in text.lower():
            return 1
    return 0

def getPlotElements(text):
    text = text.replace("^","**")
    from_to = list(map(deleteFirstWhitespace,text.lower().split("from")[-1].split("to")))
    return {"function":deleteFirstWhitespace(text.lower().split("from")[0].split("plot")[-1]),
            "from":from_to[0],"to":from_to[-1]}

def makePlot(text,sender):
    import image_hosting as ih
    import os 
    
    # get filename
    filename = plotWrapper(getPlotElements(text),sender)
    
    if filename is None:
        return "https://www.dropbox.com/s/ph4kd5pmrln49oi/NotAvailable.png?dl=0"
    
    DBM = ih.DropBoxManager()
    
    # delete file 
    DBM.deleteFile(path="/plots",filename=filename)
    DBM.uploadFile(path="/plots",filename=filename)
    temo = DBM.getTemporaryUrl(path="/plots",filename=filename)
    os.remove(filename)
    return temo['url']

# Jokes 

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

# Random

def identifyCoin(text):
    if 'flip' in text.lower() and 'coin' in text.lower():
        return 1
    return 0

def identifyDice(text):
    if 'roll' in text.lower() and 'dice' in text.lower():
        return 1
    return 0

def identifyChoice(text):
    if 'random choice:' in text.lower():
        return 1
    return 0

def getRandomChoice(text):
    elements = [elms for elms in text.split(':')[-1].replace(',',' ').split(" ") if elms != '']
    if (elements is None) or (len(elements) == 0):
        return "Sorry, I'm confused!"
    return str(randomChoice(elements))
    

# generic message 

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
    _list  = list(generic_message.keys())
    return generic_message[_list[int(len(_list)*_index)]]
    


def identifySendNudes(text):
    if 'send nudes' in text.lower():
        return 1
    if 'pack' in text.lower():
        return 1
    return 0

def sendNudes():
    return "https://scontent-dft4-2.xx.fbcdn.net/v/t34.0-12/18051760_10156149925989966_1903532741_n.png?oh=d54e7de3f9776a37d92ecd402d1f97a6&oe=58FFBAD0"

def identifyMe(text):
    if "me" == text.lower():
        return 1
    return 0

def getProfilePic(sender):
    pic = getUserInfo(sender).get('profile_pic')
    if pic is None:
        return "https://lh3.googleusercontent.com/UBz80Hwz87KC4Aw3q1_F9gZjLz3NyDagC52GtubICL84ERRrq6vwOPZcMULqaSJFcjaOWBA1KEUNPW6y4VrfqkzsZrxEX6xZyhzGnJ6u_u50CVlgIGA6oTSml2TucDvZ7MvcfyY7mK99QH3Ug2G7sHt3Kfx6uZX_YNfe-rN_kECdoQCz1MHjx3w0NflEcoc0muX3CTVcMUnrVjJQvEP5DaheeApIJEKCNNIrvfFt5DChj1VPtaitFyYejfuQKc2OjlBrMPELpanQPADvoKUepxRiVAyn-xmUSw_xcdLbbGu8y8r9mz2dVyiasepnakwZNzuRRHbC4Byv66kQ_Pqv4S2lHo5OIK65pnQN0RxJNnkWXDgelmrvmAVL4E4vcrg90QhYuL4GNyH7AsCKNegTPE5kjNvmrfNpY-DxDjVyCQMBkxg9rcpmvtEKTx3BYyPnWi0w9l8WjugPjPMSrgZNiFclD7i3DLgTCzLtf0PSksLmv6exPHswnTA5JKU200yIgQKhf3b3THCF4YpqMUVQvlyxRL6KVbH0uJN_un5ZfbXuuppcauvs1O_XEYoOHTkbgSPMGuAWMjT2CuTDRpmQ3P_rGNiEanQtM-Ypx-e5Ax0Xrkc=s170-no"
    return getUserProfilePic(sender)

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
        return SP.interpret(),'text'
    
    if identifyShortMessageAndGreeting(text):
        return genericGreetingMesasge(sender),'text'
    
    if identifyWhoYouAre(text):
        return firstGreetingMessage(sender),'text'
    
    if identifyWhatsYourName(text):
        return myNameIs(),'text'
    
    if identifyHowAreYou(text):
        return getResponseForHowAreYouAndOkays(),'text'
    
    if identifyIntegrals(text):
        return integralAnswer(text),'text'
        
    if identifyPlot(text):
        return makePlot(text,sender),'image'
    
    if identifyJoke(text):
        return getOneJoke(),'text'
    
    if identifySendNudes(text):
        return sendNudes(),'image'
    
    if identifyMe(text):
        return getUserProfilePic(sender),'text'
        
    if identifyCoin(text):
        return flipCoin(),'text'
    
    if identifyDice(text):
        return rollDice(),'text'
    
    if identifyChoice(text):
        return getRandomChoice(text),'text'
    
    return IDontUnserstand(sender),'text'

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
            text   = mevent['message'].get('text')
            if not text:
                response,_type = 'Nice '+str(mevent['message']['attachments'][0]['type']),"text"
            else: 
                response,_type = generateResponse(text,sender)
            if "text" in _type:
                return {'Sender':sender,'OriginalText':text, 'Text':response,'_type':_type}
            if "image" in _type:
                return {'Sender':sender,'OriginalText':text, 'ImageURL':response,'_type':_type}
            
        #if len(self.message_list):
        #    return 'Okay!'
            
        self.respond_list = map(getSenderAndText,self.message_list)
        return self.respond_list

# %% 