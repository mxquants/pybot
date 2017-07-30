#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Interact Module.

Functions created to facilitate interaction with humans.

@author: Rodrigo Hernández-Mota
rhdzmota@mxquants.com
"""

import os
import requests
import numpy as np
import pyBot as py
import jokes as jk
from PIL import Image
import urllib.request
from snake_talk import SpeakPython
import image_hosting as ih


def getUserProfilePic(sender='1657838257577411'):
    """Get user's profile pic."""
    # set filename
    tempo_filename = "profilepic_{}.jpg".format(sender)
    filename = "profilepic_{}.png".format(sender)

    # Page Access Token
    pat = 'EAAaiAN9H6KEBANNiZCZA1xnwt1wxd9twtZADhHkfvpWHCh8JaVd7CNZ' + \
          'B61Yb0jMZA4KAFChAyDNz74ZCpoaWyvNGH2khu6N8LdVEzePFJZC6ueC' + \
          'fvM9Tm9R0d8Ebj4DoZC8CTNbrVISI3DB0MMZBFtNQRlvH9WRcc2xfhS1' + \
          'tCTNJyOQZDZD'

    # FB API for user's info
    userprofile_api = 'https://graph.facebook.com/v2.6/{USER_ID}?fi' + \
                      'elds=first_name,profile_pic,gender&access_to' + \
                      'ken={PAGE_ACCESS_TOKEN}'

    # get user's data
    temp = eval(requests.get(userprofile_api.format(
                        USER_ID=sender, PAGE_ACCESS_TOKEN=pat)).text)
    if not temp.get('profile_pic'):
        return "https://www.dropbox.com/s/ph4kd5pmrln49oi/" + \
               "NotAvailable.png?dl=0"

    urllib.request.urlretrieve(temp['profile_pic'].replace("\\", ""),
                               tempo_filename)

    # convert to .png
    im = Image.open(tempo_filename)
    im.save(filename)

    # upload to dropbox
    DBM = ih.DropBoxManager()
    DBM.deleteFile(path="/profile_pics", filename=filename)
    DBM.uploadFile(path="/profile_pics", filename=filename)
    temo = DBM.getTemporaryUrl(path="/profile_pics", filename=filename)
    os.remove(tempo_filename)
    os.remove(filename)
    # print(temo['url'])
    return temo['url']


def getUserInfo(sender_id='1657838257577411'):
    """Get user's info such as name, gender, etc."""
    pat = 'EAAaiAN9H6KEBANNiZCZA1xnwt1wxd9twtZADhHkfvpWHCh8JaVd7CNZB6' + \
          '1Yb0jMZA4KAFChAyDNz74ZCpoaWyvNGH2khu6N8LdVEzePFJZC6ueCfvM9' + \
          'Tm9R0d8Ebj4DoZC8CTNbrVISI3DB0MMZBFtNQRlvH9WRcc2xfhS1tCTNJyOQZDZD'
    userprofile_api = 'https://graph.facebook.com/v2.6/{USER_ID}?fiel' + \
                      'ds=first_name,profile_pic,gender&access_token=' + \
                      '{PAGE_ACCESS_TOKEN}'
    return eval(requests.get(userprofile_api.format(
                    USER_ID=sender_id,
                    PAGE_ACCESS_TOKEN=pat)).text)


def firstGreetingMessage(sender):
    """Create first greeting message."""
    _user = getUserInfo(sender).get('first_name')
    user_name = _user if _user else 'Pythonist'
    _text = """\
Hi there! Nice to meet you {}.

My name is pyBot, the only bot that can talk with snakes! """+"""\
Use #py at the beginning of your code so I can speak Parse"""+"""\
ltongue with you! Btw, I can also help you with some math!
    """
    return _text.format(user_name)


def deleteFirstWhitespace(text):
    """Delete the first whitespace."""
    return (text if text[0] != ' ' else deleteFirstWhitespace(text[1:]))


def identifyShortMessageAndGreeting(text):
    """Identify a short message."""
    n = len(text)
    if n > 25:
        return 0
    if ('hola' in text.lower()) or ('que onda' in text.lower()) or \
       ('que tal' in text.lower()) or ('saludos' in text.lower()) or \
       ('hello' in text.lower()) or ('hi' in text.lower()) or \
       ('hey' in text.lower()):
        return 1
    return 0


def identifyWhoYouAre(text):
    """Idenfiy who you are."""
    if ('quien eres' in text.lower()) or ('que eres' in text.lower()) or \
       ('quién eres' in text.lower()) or ('qué eres' in text.lower()):
        return 1
    return 0


def identifyWhatsYourName(text):
    """Get pyBot's name."""
    if ('nombre' in text.lower()) or ('name' in text.lower()) or \
       ('apodo' in text.lower()) or (('como' in text.lower() or
                                     'cómo' in text.lower()) and
                                     'llamas' in text.lower()):
        return 1
    return 0


def identifyHowAreYou(text):
    """How you are."""
    if 'how' in text.lower() and 'are' in text.lower() and \
       'you' in text.lower():
        return 1
    if 'how' in text.lower() and 'its' in text.lower() and \
       'going' in text.lower():
        return 1
    if 'cómo' in text.lower() and ('estas' in text.lower() or
                                   'andas' in text.lower()):
        return 1
    if 'fine' in text.lower() or 'good' in text.lower() or \
       'great' in text.lower():
        return 1
    return 0


def getResponseForHowAreYouAndOkays():
    """Get responses set."""
    possible_responses = {}
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
    possible_responses[11] = """\
    You know, just going on.
    """
    _index = np.random.uniform()
    _list = list(possible_responses.keys())
    return possible_responses[_list[int(len(_list)*_index)]]


def identifyPyCode(text):
    """Identify when a message is a python code."""
    if ("#py" in text.lower()) or ("# py" in text.lower()) or \
       ("#python" in text.lower()) or ("# python" in text.lower()):
        return 1
    return 0


def getPyCode(text):
    """Extract python code from text."""
    if text == '#py' or text == '# py' or text == '#py 'or text == ' #py ':
        return 'print(No code found!)'
    if text == '#python' or text == '# python':
        return 'print(No code found!)'
    if 'python' in text.lower():
        code = 'python'.join(text.split("python")[1:])
        return (code[1:] if code[0] == " " else code)
    code = 'py'.join(text.split("py")[1:])
    return (code[1:] if code[0] == " " else code)

# Solve Integrals


def identifyIntegrals(text):
    """Identify integral command."""
    if 'integrate' in text.lower():
        if 'from' in text.lower() and 'to' in text.lower():
            return 1
    return 0


def getIntegralElements(text):
    """Extract integral elements from text."""
    text = text.replace("^", "**")
    from_to = list(map(deleteFirstWhitespace,
                       text.lower().split("from")[-1].split("to")))
    return {"function": deleteFirstWhitespace(
                        text.lower().split("from")[0].split("integrate")[-1]),
            "from": from_to[0],
            "to": from_to[-1]}


def integralAnswer(text):
    """Get integral answer."""
    answer = py.integralWrapper(getIntegralElements(text))
    complete = "The result for your integral, using " +\
               "Monte-Carlo approx is: \n\n\t{}"
    return complete.format(answer)

# Matplotlib plots


def identifyPlot(text):
    """Identify plot command."""
    if 'plot' in text.lower():
        if 'from' in text.lower() and 'to' in text.lower():
            return 1
    return 0


def getPlotElements(text):
    """Extract plot elements from text."""
    text = text.replace("^", "**")
    from_to = list(map(deleteFirstWhitespace,
                       text.lower().split("from")[-1].split("to")))
    return {"function": deleteFirstWhitespace(
                        text.lower().split("from")[0].split("plot")[-1]),
            "from": from_to[0],
            "to": from_to[-1]}


def makePlot(text, sender):
    """Generate plot."""
    filename = py.plotWrapper(getPlotElements(text), sender)
    if filename is None:
        return "https://www.dropbox.com/s/ph4kd5pmrln49oi/NotAvail" + \
                "able.png?dl=0"

    DBM = ih.DropBoxManager()
    DBM.deleteFile(path="/plots", filename=filename)
    DBM.uploadFile(path="/plots", filename=filename)
    temo = DBM.getTemporaryUrl(path="/plots", filename=filename)
    os.remove(filename)
    return temo['url']

# Jokes


def identifyJoke(text):
    """Identify when someone asks for jokes."""
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
    """Get one joke."""
    _text = "I've got a joke for you: \n\n"
    return _text + jk.chooseJoke()


def myNameIs():
    """Get name."""
    return 'My name is... Heissenberg!\n\nJK, you can call me pyBot.'

# Random


def identifyCoin(text):
    """Identify when someone asks a flipped coin."""
    if 'flip' in text.lower() and 'coin' in text.lower():
        return 1
    if "PAYLOAD_COIN" == text:
        return 1
    return 0


def identifyDice(text):
    """Identify when someone ask for a rolled dice."""
    if 'roll' in text.lower() and 'dice' in text.lower():
        return 1
    if "PAYLOAD_DICE" == text:
        return 1
    return 0


def identifyChoice(text):
    """Identify when someone asks for a choice among elements."""
    if 'random choice:' in text.lower():
        return 1
    return 0


def getRandomChoice(text):
    """Get random choice."""
    elements = [elms for elms in
                text.split(':')[-1].replace(',', ' ').split(" ") if elms != '']
    if (elements is None) or (len(elements) == 0):
        return "Sorry, I'm confused!"
    return str(py.randomChoice(elements))

# Optimiztion


def identifyOptimTask(text):
    """Identify for optim. tasks."""
    if ('find min' in text.lower()) or ('find max' in text.lower()) or \
       ('find opt' in text.lower()):
        if ('of' in text.lower()) and ('constr' not in text.lower()):
            return 1
    return 0


def identifyLagrangeTask(text):
    """Identify for lagrange optim. request."""
    if ('find' in text.lower()) or ('opt' in text.lower()):
        if ('of' in text.lower()) and ('with' in text.lower()) and \
           ('constraints' in text.lower()):
            return 1
    return 0

# generic message


def genericGreetingMesasge(sender):
    """Generic Greeting."""
    _user = getUserInfo(sender).get('first_name')
    user_name = _user if _user is not None else 'Pythonist'
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
    _list = list(generic_message.keys())
    return generic_message[_list[int(len(_list)*_index)]]


def identifySendNudes(text):
    """Send nudes."""
    if 'send nudes' in text.lower():
        return 1
    if 'pack' in text.lower():
        return 1
    return 0


def sendNudes():
    """Get nudes."""
    return "https://scontent-dft4-2.xx.fbcdn.net/v/t34.0-12/18051760_1" + \
           "0156149925989966_1903532741_n.png?oh=d54e7de3f9776a37d92ec" + \
           "d402d1f97a6&oe=58FFBAD0"


def identifyMe(text):
    """Identify the word "me"."""
    if "me" == text.lower():
        return 1
    return 0


def getProfilePic(sender):
    """Get profile pic of user."""
    pic = getUserInfo(sender).get('profile_pic')
    if pic is None:
        return "https://lh3.googleusercontent.com/UBz80Hwz87KC" + \
               "4Aw3q1_F9gZjLz3NyDagC52GtubICL84ERRrq6vwOPZcMULqaSJFc" + \
               "jaOWBA1KEUNPW6y4VrfqkzsZrxEX6xZyhzGnJ6u_u50CVlgIGA6oT" + \
               "Sml2TucDvZ7MvcfyY7mK99QH3Ug2G7sHt3Kfx6uZX_YNfe-rN_kEC" + \
               "doQCz1MHjx3w0NflEcoc0muX3CTVcMUnrVjJQvEP5DaheeApIJEKC" + \
               "NNIrvfFt5DChj1VPtaitFyYejfuQKc2OjlBrMPELpanQPADvoKUep" + \
               "xRiVAyn-xmUSw_xcdLbbGu8y8r9mz2dVyiasepnakwZNzuRRHbC4B" + \
               "yv66kQ_Pqv4S2lHo5OIK65pnQN0RxJNnkWXDgelmrvmAVL4E4vcrg" + \
               "90QhYuL4GNyH7AsCKNegTPE5kjNvmrfNpY-DxDjVyCQMBkxg9rcpm" + \
               "vtEKTx3BYyPnWi0w9l8WjugPjPMSrgZNiFclD7i3DLgTCzLtf0PSk" + \
               "sLmv6exPHswnTA5JKU200yIgQKhf3b3THCF4YpqMUVQvlyxRL6KVb" + \
               "H0uJN_un5ZfbXuuppcauvs1O_XEYoOHTkbgSPMGuAWMjT2CuTDRpm" + \
               "Q3P_rGNiEanQtM-Ypx-e5Ax0Xrkc=s170-no"
    return getUserProfilePic(sender)


def IDontUnserstand(sender):
    """Message when pyBot don't uderstands."""
    _user = getUserInfo(sender).get('first_name')
    user_name = _user if _user is not None else 'Pythonist'
    _text = """\
I'm sorry {}, still learning to talk here. You can use #py """+"""\
before writing some python code and I'll certainly understa"""+"""\
nd. Let's talk with snakes! Btw I can also do some maths.

...or you can ask me some jokes. ;)
    """
    return _text.format(user_name)


def identifyMoreOptions(text):
    """Get more options."""
    if text == "PAYLOAD_MORE_OPTS":
        return 1
    return 0


def identifyCalculatorInstr(text):
    """Identify when the calculator is needed."""
    if "PAYLOAD_CALC" == text:
        return 1
    return 0


def identifyCalculator(text):
    """Identify when the calculator is needed."""
    if "calculate" in text.lower()[:9]:
        return 1
    return 0


def identifyFibo(text):
    """Identify fibonacci function."""
    if text.lower()[:10] == "fibonacci(":
        return 1
    return 0


def evalFibo(text, sender):
    """Evaluate fibo func."""
    script = """\
#python
import pyBot as pb
pb.{}
""".format(text)
    if identifyPyCode(script):
        text_script = getPyCode(script)
        SP = SpeakPython(script=text_script, user=sender)
        return SP.interpret()
    return "Whoa, that's not the good ol'fibo."


def identifyCreatorQuestion(text):
    """Identify creator."""
    if ("who" in text.lower()) and (("creator" in text.lower()) or
                                    ("god" in text.lower()) or
                                    ("developer" in text.lower()) or
                                    ("master" in text.lower()) or
                                    ("engineer" in text.lower())):
        return 1
    if (("developer" in text.lower()) or
        ("coder" in text.lower()) or
        ("programmer" in text.lower())) and \
       ("info" in text.lower()):
        return 1
    return 0

# Generate Response


def generateResponse(text, sender):
    """Generate appropiate response."""
    if identifyCreatorQuestion(text):
        return "I was coded by Rodrigo Hernández-Mota (rhdzmota@mxq" + \
               "uants.com). Feel free to contact!", "text", "options"
    if identifyPyCode(text):
        try:
            nothing_warn = "Nothing came out from your code. Remember to add print() statements! Or maybe there is an undefined variable (each message is independent)."
            too_much_warn = "Code output too large to send throw FB-Messenger. Please ask Mark to change this setting. :)"
            text_script = getPyCode(text)
            SP = SpeakPython(script=text_script, user=sender)
            code_ans = SP.interpret()
            code_ans = nothing_warn if len(cocode_ansde) == 0 else code_ans if len(code_ans) < 640 else too_much_warn
            # code_ans = code_ans if len(code_ans) > 0 else "Nothing came out from your code. Remember to add print() statements! Or maybe there is an undefined variable (each message is independent)."
        except:
            code_ans = """\
Whoa! Something went wrong. Make sure to put #py at the beginning of your message and respect identation. :)
"""
        return code_ans, 'text', 'options'
    if identifyCalculatorInstr(text):
        return "Write 'calculate ...' and substitute the ... " + \
                "with your (simple) math.", "text", "options"
    if identifyCalculator(text):
        ans = py.calculator(text.lower().replace("calculate ", ""))
        return ans, "text", "options"
    if identifyFibo(text):
        return evalFibo(text, sender), "text", "options"
    if identifyShortMessageAndGreeting(text):
        return genericGreetingMesasge(sender), 'text', 'options'
    if identifyWhoYouAre(text):
        return firstGreetingMessage(sender), 'text', 'options'
    if identifyWhatsYourName(text):
        return myNameIs(), 'text', 'options'
    if identifyHowAreYou(text):
        return getResponseForHowAreYouAndOkays(), 'text', 'options'
    if identifyIntegrals(text):
        return integralAnswer(text), 'text', 'options'
    if identifyPlot(text):
        return makePlot(text, sender), 'image', 'options'
    if identifyJoke(text):
        return getOneJoke(), 'text', 'options'
    if identifySendNudes(text):
        return sendNudes(), 'image', 'options'
    if identifyMe(text):
        return getUserProfilePic(sender), 'text', 'options'
    if identifyCoin(text):
        return py.flipCoin(), 'text', 'options'
    if identifyDice(text):
        return py.rollDice(), 'text', 'options'
    if identifyChoice(text):
        return getRandomChoice(text), 'text', 'options'
    if identifyMoreOptions(text):
        return "Okay!", "text", "more_options"
    if identifyOptimTask(text):
        try:
            resp = py.optimHandler(text)
        except:
            resp = "Something went wrong! Check your syntax."
        return resp, 'text', 'options'
    if identifyLagrangeTask(text):
        try:
            resp = py.lagrangeHandler(text)
        except:
            resp = "Something went wrong! Check your syntax."
        return resp, 'text', 'options'
    return IDontUnserstand(sender), 'text', 'options'


class RespondEntryMessages(object):
    """Respond Entry Messages Handler."""

    def __init__(self, entry):
        """Initialize."""
        self.entry = entry
        self.message_postback_list = []
        self.delivery_list = []
        self.optin_list = []
        for mevent in entry['messaging']:
            if mevent.get('message') or mevent.get('postback'):
                self.message_postback_list.append(mevent)
            if mevent.get('delivery'):
                self.delivery_list.append(mevent)
            if mevent.get('optin'):
                self.optin_list.append(mevent)

    def now(self):
        """Now method."""
        def getSenderAndText(mevent):

            if(mevent.get('message')):
                sender = mevent['sender']['id']
                text = mevent['message'].get('text')
                if mevent['message'].get('quick_reply'):
                    payload = mevent['message']['quick_reply']['payload']
                    response, _type, quick_reply = generateResponse(payload,
                                                                    sender)
                elif not text:
                    response = 'Nice '+str(
                                   mevent['message']['attachments'][0]['type'])
                    _type = "text"
                    quick_reply = "none"
                else:
                    response, _type, quick_reply = generateResponse(text,
                                                                    sender)
                if "text" in _type:
                    return {'Sender': sender,
                            'OriginalText': text,
                            'Payload': False,
                            'Text': response,
                            '_type': _type,
                            'quick_reply': quick_reply
                            }
                if "image" in _type:
                    return {'Sender': sender,
                            'OriginalText': text,
                            'Payload': False,
                            'ImageURL': response,
                            '_type': _type,
                            'quick_reply': quick_reply
                            }

        self.respond_list = map(getSenderAndText, self.message_postback_list)
        return self.respond_list
