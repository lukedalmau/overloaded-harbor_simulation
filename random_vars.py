import random as r
import math as m

def U(a,b):
    """
    Use the uniform distribution to generate a random variable within the range [a,b]
    """
    return lambda : r.uniform(0,1)*(b-a) + a

def exponential_random_variable(alpha):
    """
    Use the uniform distribution to generate a random variable with exponential distribution
    """
    uniform = U(0,1)
    return lambda : -m.log(uniform())/alpha

def normal_random_variable(mu,sigma):
    """
    Use the uniform distribution to generate a random variable with normal distribution
    """
    u1 = U(0,1)
    u2 = U(0,1)
    return lambda : mu + sigma*m.sqrt(-2*m.log(u1()))*m.cos(2*m.pi*u2())
    #return lambda :r.normalvariate(mu,sigma)
