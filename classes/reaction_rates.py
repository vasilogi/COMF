#!/usr/bin/env python
# coding: utf-8

import numpy as np
import sys

class Model:
    """A class that contains the conversion, integral
       and differential reaction rates for each model.
       
       name   = the name of the model                   (string)
       alpexp = the experimentally recorded conversion  (array)
       
       """
    def __init__(self,modelname):
        self.name   = modelname
    
    def g(self,alpexp):
        
        """Return the integral reaction rate for each different model"""
        if (self.name == 'A2'):
            rate = [np.sqrt(-np.log(1.0-a)) for a in alpexp]
        elif (self.name == 'A3'):
            rate = [(-np.log(1.0-a))**(1.0/3.0) for a in alpexp]
        elif (self.name == 'A4'):
            rate = [(-np.log(1.0-a))**(1.0/4.0) for a in alpexp]
        elif (self.name == 'D1'):
            rate = [a**2.0 for a in alpexp]
        elif (self.name == 'D2'):
            rate = [(1.0-a)*np.log(1.0-a)+a for a in alpexp]
        elif (self.name == 'D3'):
            rate = [(1.0-(1.0-a)**(1.0/3.0))**2.0 for a in alpexp]
        elif (self.name == 'D4'):
            rate = [1.0 - (2.0/3.0)*a - (1.0-a)**(2.0/3.0) for a in alpexp]
        elif (self.name == 'F0'):
            rate = [a for a in alpexp]
        elif (self.name == 'F1'):
            rate = [-np.log(1.0-a) for a in alpexp]
        elif (self.name == 'F2'):
            rate = [(1.0/(1.0-a))-1.0 for a in alpexp]
        elif (self.name == 'F3'):
            rate = [0.5*((1.0-a)**(-2.0) - 1.0) for a in alpexp]
        elif (self.name == 'P2'):
            rate = [a**0.5 for a in alpexp]
        elif (self.name == 'P3'):
            rate = [a**(1.0/3.0) for a in alpexp]
        elif (self.name == 'P4'):
            rate = [a**0.25 for a in alpexp]
        elif (self.name == 'R2'):
            rate = [1.0-(1.0-a)**0.5 for a in alpexp]
        elif (self.name == 'R3'):
            rate = [1.0-(1.0-a)**(1.0/3.0) for a in alpexp]
        else:
            print('Wrong model choice')
            print('Instead, choose one from the list: "A2","A3","A4","D1","D2","D3","D4","F0","F1","F2","F3","P2","P3","P4","R2","R3"')
            sys.exit('Program Stopped')
        
        return rate
    
    def f(self,alpexp):
        
        """Return the differential reaction rate for each different model"""
        if (self.name == 'A2'):
            rate = [2.0*(1.0-a)*np.sqrt(-np.log(1.0-a)) for a in alpexp]
        elif (self.name == 'A3'):
            rate = [3.0*(1.0-a)*(-np.log(1.0-a))**(2.0/3.0) for a in alpexp]
        elif (self.name == 'A4'):
            rate = [4.0*(1.0-a)*(-np.log(1.0-a))**(3.0/4.0) for a in alpexp]
        elif (self.name == 'D1'):
            rate = [1.0/(2.0*a) for a in alpexp]
        elif (self.name == 'D2'):
            rate = [-1.0/np.log(1.0-a) for a in alpexp]
        elif (self.name == 'D3'):
            rate = [(3.0*(1.0-a)**(2.0/3.0))/(2.0*(1.0-(1.0-a)**(1.0/3.0))) for a in alpexp]
        elif (self.name == 'D4'):
            rate = [(3.0/2.0)*((1.0-a)**(-1.0/3.0)-1.0)**(-1.0) for a in alpexp]
        elif (self.name == 'F0'):
            rate = [1.0 for a in alpexp]
        elif (self.name == 'F1'):
            rate = [1.0-a for a in alpexp]
        elif (self.name == 'F2'):
            rate = [(1.0-a)**2.0 for a in alpexp]
        elif (self.name == 'F3'):
            rate = [(1.0-a)**3.0 for a in alpexp]
        elif (self.name == 'P2'):
            rate = [2.0*(a**(1.0/2.0)) for a in alpexp]
        elif (self.name == 'P3'):
            rate = [3.0*(a**(2.0/3.0)) for a in alpexp]
        elif (self.name == 'P4'):
            rate = [4.0*(a**(3.0/4.0)) for a in alpexp]
        elif (self.name == 'R2'):
            rate = [2.0*((1.0-a)**(1.0/2.0)) for a in alpexp]
        elif (self.name == 'R3'):
            rate = [3.0*((1.0-a)**(2.0/3.0)) for a in alpexp]
        else:
            print('Wrong model choice')
            print('Instead, choose one from the list: "A2","A3","A4","D1","D2","D3","D4","F0","F1","F2","F3","P2","P3","P4","R2","R3"')
            sys.exit('Program Stopped')
            
        return rate