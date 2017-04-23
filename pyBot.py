# -*- coding: utf-8 -*-


# %% imports 

from numpy.random import uniform
from numpy import sin, cos, tan, arctan, arcsin, arccos, pi, e, power


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


# %% Integrals

# %% Integral 

def properIntegral(f,a,b,n=10**6):
    a,b = _float(a),_float(b)
    rnd = uniform(a,b,size=n)
    return (b-a)*sum(list(map(f,rnd)))/n 

def changeLimits(a,b):
    from numpy import float as _float
    a = -pi/2 if (a=='-inf' or a=='-infinite') else arctan(_float(a))
    b =  pi/2 if (b=='inf' or b=='infinite')  else arctan(_float(b))
    return a,b

def integral(f,a,b,n=10**6):
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

