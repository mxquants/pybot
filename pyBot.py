# -*- coding: utf-8 -*-


# %% imports 

from numpy.random import uniform
from numpy import log, sin, cos, tan, arctan, arcsin, arccos, pi, e, exp, power,arange
import sympy as sy 

# %% Fibonacci function
def fibo(n,p=0,q=1,first=True):
    if first:
        print(p,q,sep='\n')
        first = False
    if n==0:
        return 1 
    print(p+q)
    p,q=q,p+q
    return fibo(n-1,p,q,first)


# %% Flip a coin and roll a Dice 

def flipCoin():
    return 'Heads!' if uniform() < 0.5 else "Tails!"

def rollDice():
    return int(uniform(0,6))

def randomChoice(_list):
    elements = len(_list)
    choice = int(uniform(0,elements))
    return _list[choice]

# %% Integrals

def properIntegral(f,a,b,n=10**6):
    from numpy import float as _float
    a,b = _float(eval(a)),_float(eval(b))
    rnd = uniform(a,b,size=n)
    return (b-a)*sum(list(map(f,rnd)))/n 

def changeLimits(a,b):
    from numpy import float as _float
    a = -pi/2 if (a=='-inf' or a=='-infinite') else arctan(_float(eval(a)))
    b =  pi/2 if (b=='inf' or b=='infinite')  else arctan(_float(eval(b)))
    return a,b

def integral(f,a,b,n=50**6):
    f_u = lambda x: 2*f(tan(x))/(1+cos(2*x))
    a,b = changeLimits(a,b)
    return properIntegral(f_u,a,b,n)

def integralWrapper(param):
    
    
    def str2lambda(func):
        func=func.lower()   
        return eval("lambda x: "+func)
    
    def doIntegral(fromto):
        if 'inf' in fromto:
            return integral
        return properIntegral
    
    try:
        _integral = doIntegral(param["from"]+param["to"])(f=str2lambda(param["function"]),a=param["from"],b=param["to"])
    except:
        _integral = "Error: Something went wrong and we couldn't calculate your integral. Be sure you are using the notation: integrate <func> from <lower_limit> to <upper_limit>"

    return _integral

# %% Plot 

def plot(f,a,b,legend='',filename=''):
    import matplotlib.pyplot as plt
    delta = (b-a)/10000
    x = arange(a,b,delta)
    list(map(lambda z: plt.plot(x,z(x)),f))
    #plt.plot(x,f(x))
    plt.xlabel('x-axis')
    plt.ylabel('y-value')
    plt.legend([L.replace("**","^") for L in legend])
    plt.grid()
    plt.savefig(filename)
    plt.close()
    
def plotWrapper(param,sender):
    from numpy import float as _float
    
    def str2lambda(func):
        func=func.lower()   
        return eval("lambda x: "+func)

    filename = 'plot_{}.png'.format(sender)
    
    try:
        
        a,b = _float(eval(param['from'])),_float(eval(param['to']))
        flist = list(map(str2lambda,param['function'].split(",")))
        plot(f=flist,a=a,b=b,
             legend=param['function'].split(","),
             filename=filename)
    except:
        filename = None 
    
    return filename



# %% Optimization 

def gradient(f,_vars):
    return [sy.diff(f,i) for i in _vars]

def valueOrWarning(value, ref=''):
    if value is None:
        return 'Something went wrong! Not optim_val:{} found. Try "optim".'.format(ref)
    return value

class Optimizer(object):
    
    def __init__(self):
        return None
    
    def getOptimVals(self,f,_vars,feval=None):
        import numpy as np 
        
        # get solution
        solution = sy.solve(gradient(f,_vars))
        self.solution = solution
        
        # function to evaluate
        feval = f if feval is None else feval
        
        def minmax(feval,solution):
            value   = feval.evalf(subs=solution)
            reference = solution.copy()
            reference[list(solution.keys())[0]] += 0.01
            ref_val = feval.evalf(subs=reference)
            return 'max' if (value-ref_val)>0 else 'min'
        
        if type(solution)==type({}):
            return {minmax(feval,solution):{'value':f.evalf(subs=solution),'solution':solution}}
        
        results = {
            'max':{'value':None,'solution':None},
            'min':{'value':None,'solution':None}
        }

        max_ref,min_ref = -np.float('inf'),np.float('inf')
        
        try:
            for sol in solution: 
                value = feval.evalf(subs=sol)

                if value < min_ref:
                    min_ref = value 
                    results['min']['value'] = value
                    results['min']['solution'] = sol

                if value > max_ref:
                    max_ref = value 
                    results['max']['value'] = value
                    results['max']['solution'] = sol
        except:
            results = solution
        
        self.results = results 
        
        return results
    
    def getMax(self,f,_vars):
        return valueOrWarning(self.getOptimVals(f,_vars).get('max'),ref='max')
    
    def getMin(self,f,_vars):
        return valueOrWarning(self.getOptimVals(f,_vars).get('min'),ref='min')
    
    def getBoth(self,f,_vars):
        return valueOrWarning(self.getOptimVals(f,_vars),ref='both')
    
    def getAll(self,f,_vars):
        self.getOptimVals(f,_vars)
        return self.solution
    

class LagrangeMultipliersSolver(object):
    
    def __init__(self):
        return None
        
    def getSolution(self,f,g,_vars):
        
        # get lambda 
        lmda = sy.symbols('lmda')
        
        # lagrangian function and gradient 
        self.lagrangian = f - lmda*g
        self.lagrangian_grad = gradient(self.lagrangian,_vars+[lmda])
        
        # solution 
        Op = Optimizer()
        self.results = Op.getOptimVals(self.lagrangian,_vars+[lmda],feval=f)
        
        return self.results 


def optimHandler(text):
    text = text.replace('^','**')
    
    # get elements 
    variables = [i for i in text.split(' of')[-1] if (i not in ' / * - + ( ) [ ] e pi 123456789 ^ ')]
    text_func = text.split(' of')[-1]
    
    # create required variables
    exec(', '.join(variables)+""" = sy.symbols('"""+' '.join(variables)+"""')""")
    _vars = eval('['+', '.join(variables)+']')
    
    # create function
    f = eval(text_func)
    
    # Optimize 
    Opt = Optimizer()
    
    if ' min ' in text.lower():
        return str(Opt.getMin(f,_vars))
    if ' max ' in text.lower():
        return str(Opt.getMax(f,_vars))
    if ' minmax ' in text.lower():
        return str(Opt.getBoth(f,_vars))
    if 'optim' in text.lower():
        return str(Opt.getAll(f,_vars))
    
    return 'Something went wrong! Not sure what happend.'
# %% 


# %% 