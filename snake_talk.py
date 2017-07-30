#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 19:27:55 2017
References:
https://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call-in-python
https://stackoverflow.com/questions/10661079/restricting-pythons-syntax-to-execute-user-code-safely-is-this-a-safe-approach
@author: rhdzmota
"""

import signal
import subprocess


def handler(signum, frame):
    """WTF is this."""
    raise OSError("Limit time exceeded!")

def simulateInput(script=None):
    """Simulate user's input for testing."""
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


def wrapperFunc(string):
    """Wrapper Function."""
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
    _str = _str.format(string)
    _str = '\n    '.join(_str.split('\n'))
    str_func = """\

from multiprocessing import Process

def basicWrapper():
    {}
    return 1

def restrictedTime(func, args, kwargs, time):
    p = Process(target=func, args=args, kwargs=kwargs)
    p.start()
    p.join(time)
    if p.is_alive():
        p.terminate()
        print("Timeout: Code exceeded max. execution time.")
        return False
    return True


if __name__ == '__main__':
    #basicWrapper()
    restrictedTime(basicWrapper, (), dict(), 5)
"""
    #str_func = "def basicWrapper():\n    {}\n    " + \
    #           "return 1\n\nif __name__ == '__main__':\n    basicWrapper()"
    return str_func.format(_str)


def saveIntoPyScript(text_script, file='temp.py'):
    """Save text into a temporal python script."""
    with open(file, 'w') as f:
        f.write(text_script)


def runPyScript(file='temp.py'):
    """Run a python script from a python script."""
    exec('from {} import basicWrapper'.format(file.split('.')[0]))
    return basicWrapper()


def generateOutput(file='temp.py', output='output.txt'):
    """Save output into a temporal txt."""
    bash_command = 'python {} > {}'.format(file, output)
    try:
        subprocess.check_output(['bash', '-c', bash_command])
    except:
        print('Error')
        return 0
    return 1


def readOutput(output='output.txt'):
    """Read generated output."""
    with open(output, 'r') as f:
        output_string = f.read()
    return output_string


def safeImport(string):
    """Count number of safe imports."""
    save_imports = ["import pyBot", "import math", "import numpy",
                    "import pandas", "import datetime"]
    n_imp = 0
    for imp in save_imports:
        n_imp += (imp in string)
    return n_imp


def numberOfImports(string, n=0):
    """Count number of imports."""
    res = string.split("import")
    if len(res) == 1:
        return n
    return numberOfImports(string="import".join(res[1:]), n=n+1)


def beSafe(script_text):
    """Safty first."""
    if 'write' in script_text:
        return 0
    if 'open(' in script_text:
        return 0
    if 'while' in script_text:
        return 0
    if "import" in script_text:
        nsafe = safeImport(script_text)
        nimps = numberOfImports(script_text)
        if nimps > nsafe:
            return False
    return True


def sorryMessage():
    """Sorry message."""
    return "Whoops! Coudn't run script! \nTime's up or maybe I j" + \
           "ust can't handle that code... Might be a bug or som" + \
           "ething else! Beware and code safe.\n\nSidenote: max" + \
           " 30 sec. of processing per message."


def riskyCode():
    """Risky code message."""
    return "Sorry Dave, I'm afraid I cannot do that. \n\nReason:" + \
           " unsafe code detected, I don't wanna be hurt.\nPleas" + \
           "e avoid writing to disk, while loops and other dange" + \
           "rous code! Note: do whole imports (import numpy as np)."


class SpeakPython(object):
    """Speak Parseltongue."""

    def __init__(self, script='print("No code send!")', user='anonymous'):
        """Initialize."""
        self.text_script = script
        self.user = user

    def interpret(self):
        """Translate."""
        if 'mxquant:command -do test' == self.text_script:
            a = simulateInput(None)
            b = wrapperFunc(a)
            saveIntoPyScript(b)
            _status = generateOutput()
            _result = sorryMessage() if not _status else readOutput(
                                                            self.output_name)
            return _result

        # Be safe!
        _save = beSafe(self.text_script)
        if not _save:
            return riskyCode()

        # Create file names for source (temp.py / {}) and output
        # (output.txt / {})
        self.file_name = 'temp.py' if 'anony' in self.user else \
            '{}_file.py'.format(self.user)
        self.output_name = 'output.txt' if 'anony' in self.user else \
            '{}_out.py'.format(self.user)

        # Create code with wrapper func.
        self.code = wrapperFunc(self.text_script)

        # Generate source code, run and save output file
        saveIntoPyScript(self.code, file=self.file_name)
        status = generateOutput(file=self.file_name, output=self.output_name)

        # Get results or say sorry
        result = sorryMessage() if not status else readOutput(self.output_name)
        return result


def test(script_as_string=None):
    """Test."""
    a = simulateInput(script_as_string)
    sp = SpeakPython(a)
    return sp.interpret()
