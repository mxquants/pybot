#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 23:15:06 2017

@author: rhdzmota
"""

# %%
def jokeStack():
    
    jokes = {}
    
    jokes["HalloweenChristmas"] = """\
Q: Why do programmers always mix up Halloween and Christmas?
A: Because Oct 31 == Dec 25.
    """
    
    jokes["FinlandProgrammer"] = """\
Q: What do you call a programmer from Finland?
A: A Nerdic.     
    """
    
    jokes["QuitYourJob"] = """\
Q: Why did the programmer quit his job?
A: Because he didn’t get arrays. 
    """
    
    jokes["FlaseIsTrue"] = """\
Q: 0 is false and 1 is true, right?
A: 1
    """
    
    jokes["AirConditioner"] = """\
Q: What do computers and air conditioners have in common?
A: They both become useless when you open windows. 
    """
    
    jokes["Glasses"] = """\
Q: Why most Python programmers have to wear glasses?
A: Because they don’t C#. 
    """
    
    
    jokes["NoClass"] = """\
Q: Why did C++ uninvited C to the party?
A: Because C has no class.
    """
    
    jokes["LongPause"] = """\
A: “knock, knock”
B: Who’s there?

- - very long pause - -

A: Java. 
    """
    
    jokes["NoTable"] = """\
A SQL-query goes into a bar, walks up to two tables and asks; “can I join you?”
    """
    
    jokes["CppAndHammer"] = """\
When your hammer is C++ everything begins to look like a thumb. 
    """
    
    
    jokes["MillionMonkeys"] = """\
If you put a million monkeys at a million keyboards, one of them will eventually write a Scala program.

The rest of them will write Perl programs. 
    """
    
    jokes["Recursion"] = """\
To understand what recursion is, you must first understand recursion. 
    """
    
    jokes["BinaryPeople"] = """\
There are only 10 kinds of people in this world: those who know binary and those who don’t.
    """
    
    jokes["WarningsAndErrors"] = """\
A man is smoking a cigarette and blowing smoke rings into the air.  His girlfriend becomes irritated with the smoke and says, “Can’t you see the warning on the cigarette pack?  Smoking is hazardous to your health!”
To which the man replies, “I am a programmer.  We don’t worry about warnings; we only worry about errors.”
    """
    
    jokes["ManComputer"] = """\
Why computers are like men:\n
1. In order to get their attention, you have to turn them on.
2. They have a lot of data, but are still clueless.
3. They are supposed to help you solve problems, but half the time they are the problem.
4. As soon as you commit to one, you realize that if you had waited a little longer, you could have had a better model.
    """
    
    jokes["WomenComputer"] = """\
Why computers are like women:\n
1. No one but the Creator understands their internal logic.
2. The native language they use to communicate with other computers is incomprehensible to everyone else.
3. Even your smallest mistakes are stored in long-term memory for later retrieval.
4. As soon as you make a commitment to one, you find yourself spending half your paycheck on accessories for it.    
    """
    
    jokes["Coffe2Code"] = """\
Definition of programmer: a machine that turns coffee into code. 
    """
    
    jokes["DefinitionProgrammer"] = """\
Definition of programmer: a person that fixed a problem that you don’t know you have in a way that you don’t understand.
    """
    
    jokes["DefinitionAlgorithm"] = """\
Definition of algorithm: word used by programmers when they don’t want to explain their code. 
    """
    
    jokes["ChuckNorris"] = """\
Chuck Norris can take a screenshot of his blue screen. 
    """
    
    jokes["NoSqlBar"] = """\
3 SQL-queryies walked into a NoSQL bar. 

A while later they walked out because they couldn't find a table for them.     
    """
    
    jokes["BetterThanWindows"] = """\
If the box says; this software requires WindowsXP or better. Does that mean it’ll run on Linux? 
    """
    
    return jokes 

# %%

def chooseJoke():
    import numpy as np
    jokes  = jokeStack()
    _index = np.random.uniform()
    _list  = list(jokes.keys())
    return jokes[_list[int(len(_list)*_index)]]
    

# %%

# %%

# %%

# %%

# %%

# %%