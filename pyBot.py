# -*- coding: utf-8 -*-
"""
PyBot standard functions
These are the main functionalities of pyBot.

@author: Rodrigo Hernández-Mota
Contact: rhdzmota@mxquants.com
"""

from numpy.random import uniform
from numpy import log, sin, cos, tan, arctan, arcsin, arccos, pi, e, \
                  exp, power, arange, sqrt
import sympy as sy


def fibo(n):
    """Recursive fibonacci function."""
    return 1 if n < 2 else fibo(n - 1) + fibo(n - 2)


def factorial(n):
    """Recursive factorial function."""
    return 1 if n == 0 else n*factorial(n-1)


def flipCoin():
    """Just flip a coin."""
    return 'Heads!' if uniform() < 0.5 else "Tails!"


def rollDice():
    """Just roll a dice."""
    return int(uniform(0, 6))+1.0


def randomChoice(_list):
    """Choose elements from a list."""
    elements = len(_list)
    choice = int(uniform(0, elements))
    return _list[choice]


def calculator(string):
    """Perform calculations."""
    def security(string):
        if "import" in string:
            return 0
        return 1

    def basicFormatting(string):
        return string.replace("ln", "log").replace("^", "**")

    fail_answer = "Oh! I'm afraid I can't do that."
    if not security:
        return fail_answer

    try:
        res = eval(basicFormatting(string))
        return str(res)
    except:
        return fail_answer
# Integrals


def properIntegral(f, a, b, n=10**6):
    """Montecarlo methods for proper integrals."""
    from numpy import float as _float
    a, b = _float(eval(a)), _float(eval(b))
    rnd = uniform(a, b, size=n)
    return (b-a)*sum(list(map(f, rnd)))/n


def changeLimits(a, b):
    """Change integral limits using arctan (from x=tan(u) transform)."""
    from numpy import float as _float
    a = -pi/2 if (a == '-inf' or a == '-infinite') else arctan(_float(eval(a)))
    b = pi/2 if (b == 'inf' or b == 'infinite') else arctan(_float(eval(b)))
    return a, b


def integral(f, a, b, n=50**6, lambda_transf=1):
    """Solve proper/improper integrals using x = tan(u)."""
    def lambdaFunc(f, lambda_transf):
        if lambda_transf:
            return lambda x: f(tan(x))/(cos(x)**2)
        return lambda x: 2*f(tan(x))/(1+cos(2*x))

    a, b = changeLimits(a, b)
    return properIntegral(lambdaFunc(f, lambda_transf), a, b, n)


def integralWrapper(param):
    """Integral Wrapper for pyBot."""
    def str2lambda(func):
        """Transform string function to lambda."""
        func = func.lower()
        return eval("lambda x: "+func)

    def doIntegral(fromto):
        """Choose if integral or properIntegral is needed."""
        if 'inf' in fromto:
            return integral
        return properIntegral

    try:
        _integral = doIntegral(param["from"]+param["to"])(f=str2lambda(
                            param["function"]), a=param["from"], b=param["to"])
    except:
        _integral = "Error: Something went wrong and we couldn't calculate" + \
                    "your integral. Be sure you are using the notation: in" + \
                    "tegrate <func> from <lower_limit> to <upper_limit>."

    return _integral

# Plot


def plot(f, a, b, legend='', filename=''):
    """Plot function."""
    import matplotlib.pyplot as plt
    delta = (b-a)/20000
    x = arange(a, b, delta)
    list(map(lambda z: plt.plot(x, z(x)), f))
    # plt.plot(x,f(x))  # Use this to debug.
    plt.xlabel('x-axis')
    plt.ylabel('y-value')
    plt.legend([L.replace("**", "^") for L in legend])
    plt.grid()
    plt.savefig(filename, dpi=500)
    plt.close()


def plotWrapper(param, sender):
    """Wrapper for plot func."""
    from numpy import float as _float

    def str2lambda(func):
        func = func.lower()
        return eval("lambda x: "+func)

    filename = 'plot_{}.png'.format(sender)

    try:
        a, b = _float(eval(param['from'])), _float(eval(param['to']))
        flist = list(map(str2lambda, param['function'].split(",")))
        plot(f=flist, a=a, b=b,
             legend=param['function'].split(","),
             filename=filename)
    except:
        filename = None

    return filename

# Optimization


def gradient(f, _vars):
    """Get a list of partial derivatives for a function f."""
    return [sy.diff(f, i) for i in _vars]


def valueOrWarning(value, ref=''):
    """Get a value or a Warning."""
    if value is None:
        return 'Something went wrong! Not optim_val:' + \
               '{} found. Try "optim".'.format(ref)
    return value


class Optimizer(object):
    """Optimize a func."""

    def __init__(self):
        """Initialize obj."""
        return None

    def getOptimVals(self, f, _vars, feval=None):
        """Optim values."""
        import numpy as np
        solution = sy.solve(gradient(f, _vars))
        self.solution = solution
        feval = f if feval is None else feval

        def minmax(feval, solution):
            value = feval.evalf(subs=solution)
            reference = solution.copy()
            reference[list(solution.keys())[0]] += 0.01
            ref_val = feval.evalf(subs=reference)
            return 'max' if (value-ref_val) > 0 else 'min'

        if type(solution) == dict:
            return {minmax(feval, solution): {'value': f.evalf(subs=solution),
                                              'solution': solution}}

        results = {
            'max': {'value': None, 'solution': None},
            'min': {'value': None, 'solution': None}
        }

        max_ref, min_ref = -np.float('inf'), np.float('inf')

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

    def getMax(self, f, _vars):
        """Return max."""
        return valueOrWarning(self.getOptimVals(f,
                                                _vars).get('max'), ref='max')

    def getMin(self, f, _vars):
        """Return min."""
        return valueOrWarning(self.getOptimVals(f,
                                                _vars).get('min'), ref='min')

    def getBoth(self, f, _vars):
        """Get both."""
        return valueOrWarning(self.getOptimVals(f,
                                                _vars), ref='both')

    def getAll(self, f, _vars):
        """Get all."""
        self.getOptimVals(f, _vars)
        return self.solution


class LagrangeMultipliersSolver(object):
    """Lagrange mult."""

    def __init__(self):
        """Initialize."""
        return None

    def getSolution(self, f, g, _vars):
        """Get the general solution."""
        lmda = sy.symbols('lmda')
        # lagrangian function and gradient
        self.lagrangian = f - lmda*g
        self.lagrangian_grad = gradient(self.lagrangian, _vars+[lmda])
        # solution
        Op = Optimizer()
        self.results = Op.getOptimVals(self.lagrangian, _vars+[lmda], feval=f)
        return self.results


def optimHandler(text):
    """Handle optimization functions."""
    text = text.replace('^', '**')

    def getRidOfSpecialFunc(text):
        return text.replace("sin", " ").replace("pi", " ")

    def getSyntaxRight(text):
        return text.replace("e", "sy.exp(1)").replace(
                                                      "sin", "sy.sin").replace(
                                                      "cos", "sy.cos").replace(
                                                      "tan", "sy.tan").replace(
                                                      "pi", "sy.pi")
    # get variables
    variables = list(set([i for i in getRidOfSpecialFunc(text.split(
                ' of')[-1]) if (i not in ' / * - + ( ) [ ] e 123456789 ^ ')]))
    text_func = getSyntaxRight(text.split(' of')[-1])

    # create required variables
    exec(', '.join(variables)+""" = sy.symbols('""" +
         ' '.join(variables)+"""')""")
    _vars = eval('['+', '.join(variables)+']')

    # create function
    f = eval(text_func)

    # Optimize
    Opt = Optimizer()

    if ' min ' in text.lower():
        return str(Opt.getMin(f, _vars))
    if ' max ' in text.lower():
        return str(Opt.getMax(f, _vars))
    if ' minmax ' in text.lower():
        return str(Opt.getBoth(f, _vars))
    if 'optim' in text.lower():
        return str(Opt.getAll(f, _vars))

    return 'Something went wrong! Not sure what happend.'


def lagrangeHandler(text):
    """Text parser for lagrangian."""
    text = text.replace('^', '**')

    def getRidOfSpecialFunc(text):
        return text.replace("sin", " ").replace("pi", " ")

    def getSyntaxRight(text):
        return text.replace("e", "sy.exp(1)").replace(
                                                      "sin", "sy.sin").replace(
                                                      "cos", "sy.cos").replace(
                                                      "tan", "sy.tan").replace(
                                                      "pi", "sy.pi")

    # get elements
    variables = list(set([i for i in getRidOfSpecialFunc(text.split(
                            ' of')[-1].split('with')[0]) if (
                            i not in ' / * - + ( ) [ ] e 123456789 ^ ')]))
    text_f = getSyntaxRight(text.split(' of')[-1].split('with')[0])
    text_g = getSyntaxRight(text.split('constraints')[-1])

    # create required variables
    exec(', '.join(variables)+""" = sy.symbols('""" +
         ' '.join(variables)+"""')""")
    _vars = eval('['+', '.join(variables)+']')

    # create function
    f = eval(text_f)
    g = eval(text_g)

    # Optimize
    LMS = LagrangeMultipliersSolver()

    return str(LMS.getSolution(f, g, _vars))
