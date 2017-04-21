#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 19:27:55 2017

@author: rhdzmota
"""


# %% Imports 

import signal

# %% Handle long functions 


def handler(signum, frame):
    raise OSError("Limit time exceeded!")

    
# %% Simulate user's input

def simulateInput(script=None):
    
    if script is None:
        script = """\
print('\n---- mxquant input test / expected output ----\n\n')

import numpy as np
np.arange(10)
for i in range(4):
    a = 1
print("Hey")



print('\n\n---- mxquant input test / expected output ----\n')
        """
    
    return script

# %% Make wrapper function

def wrapperFunc(string):
    _str = """\
import signal 

# signal handler function
def handler(signum, frame):
    raise OSError("Limit time exceeded!")

signal.signal(signal.SIGALRM, handler)
signal.alarm(30)
{}
signal.alarm(0)
"""
    _str = _str.format(string)#'import signal\nsignal.signal(signal.SIGALRM, handler)\nsignal.alarm(300)\n'+string+'\nsignal.alarm(0)'
    _str = '\n    '.join(_str.split('\n'))
    str_func = "def basicWrapper():\n    {}\n    return 1\n\nif __name__ == '__main__':\n    basicWrapper()".format(_str)
    return str_func


# %% 

def saveIntoPyScript(text_script,file='temp.py'):
    
    with open(file, 'w') as f:
        f.write(text_script)
        

# %% 

def runPyScript(file='temp.py'):
    exec('from {} import basicWrapper'.format(file.split('.')[0]))
    return basicWrapper()

def generateOutput(file='temp.py',output='output.txt'):
    import subprocess
    bash_command = 'python {} > {}'.format(file,output)
    
    try:
        subprocess.check_output(['bash','-c', bash_command])
    except:
        print('Error')
        return 0
    return 1

def readOutput(output='output.txt'):
    with open(output, 'r') as f:
        output_string = f.read()
    return output_string

def beSave(script_text):
    if 'write' in script_text:
        return 0
    if 'open(' in script_text:
        return 0
    if 'while' in script_text:
        return 0
    return 1

# %% 

def sorryMessage():
    return "Whoops! Coudn't run script! \nTime's up or maybe I just can't handle that code... Might be a bug or something else! Beware and code safe.\n\nSidenote: max 30 sec. of processing per message."

def riskyCode():
    return "Sorry Dave, I'm afraid I cannot do that. \n\nReason: unsafe code detected, I don't wanna be hurt.\nPlease avoid writing to disk, while loops and other dangerous code!"

class SpeakPython(object):
    
    def __init__(self,script='print("No code send!")',user='anonymous'):
        self.text_script = script
        self.user = user 
        
    def interpret(self):
        
        if 'mxquant:command -do test'==self.text_script:
            a = simulateInput(None)
            b = wrapperFunc(a)
            saveIntoPyScript(b)
            _status = generateOutput()
            _result = sorryMessage() if not _status else readOutput(self.output_name)
            return _result
        
        # Be save! 
        _save = beSave(self.text_script)
        if not _save:
            return riskyCode()
        
        # Create file names for source (temp.py / {}) and output (output.txt / {})
        self.file_name   = 'temp.py'    if 'anony' in self.user else '{}_file.py'.format(self.user)
        self.output_name = 'output.txt' if 'anony' in self.user else '{}_out.py'.format(self.user)
        
        # Create code with wrapper func.
        self.code = wrapperFunc(self.text_script)
        
        # Generate source code, run and save output file
        saveIntoPyScript(self.code,file=self.file_name)
        status = generateOutput(file=self.file_name,output=self.output_name)
        
        # Get results or say sorry
        result = sorryMessage() if not status else readOutput(self.output_name)
        return result


# %% 

def test(script_as_string=None):
    a = simulateInput(script_as_string)
    sp = SpeakPython(a)
    return sp.interpret()
    
    

#%% 
