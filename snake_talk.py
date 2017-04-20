#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 19:27:55 2017

@author: rhdzmota
"""

# %% Simulate user's input

def simulateInput(script=None):
    
    if script is None:
        script = """\


import numpy as np
np.arange(10)
print("Hey")




        """
    
    return script

# %% Make wrapper function

def wrapperFunc(string):
    _str = '\n    '.join(string.split('\n'))
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

# %% 

class SpeakPython(object):
    
    def __init__(self,script='print("No code send!")',user='anonymous'):
        self.text_script = script
        self.user = user 
        
    def interpret(self):
        self.file_name   = 'temp.py'    if 'anony' in self.user else '{}_file.py'.format(self.user)
        self.output_name = 'output.txt' if 'anony' in self.user else '{}_out.py'.format(self.user)
        
        self.code = wrapperFunc(self.text_script)
        
        # Save code and generate output file
        saveIntoPyScript(self.code,file=self.file_name)
        status = generateOutput(file=self.file_name,output=self.output_name)
        
        result = "Sorry! Coudn't run script." if not status else readOutput(self.output_name)
        return result


# %% 


# %% 