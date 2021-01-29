import numpy as np
import sys

class Model:

    """A class that contains the conversion, integral
       and differential reaction rates for each model.
       
       name       = the name of the model                   (string)
       conversion = the experimentally recorded conversion  (single value)
       time       = the experimentally recorded time        (single value)
       k          = the Arrhenius constant                  (float)
       
       """
    def __init__(self,modelname):
        self.name   = modelname
    
    def g(self,conversion):
        
        """Return the integral reaction rate for each different model"""

        if (self.name == 'A2'):
            if conversion == 0.0:
                print('A2 model')
                print('the input conversion value is equal to one and the logarithm argument is zero')
                print('the logarithm is not defined')
                print('the recommended conversion range is 0.05-0.95')
                sys.exit('Program Stopped')
            else:
                rate = np.sqrt(-np.log(1.0-conversion))
        elif (self.name == 'A3'):
            if conversion == 0.0:
                print('A3 model')
                print('the input conversion value is equal to one and the logarithm argument is zero')
                print('the logarithm is not defined')
                print('the recommended conversion range is 0.05-0.95')
                sys.exit('Program Stopped')
            else:
                rate = (-np.log(1.0-conversion))**(1.0/3.0)
        elif (self.name == 'A4'):
            if conversion == 0.0:
                print('A4 model')
                print('the input conversion value is equal to one and the logarithm argument is zero')
                print('the logarithm is not defined')
                print('the recommended conversion range is 0.05-0.95')
                sys.exit('Program Stopped')
            else:
                rate = (-np.log(1.0-conversion))**(1.0/4.0)

        # elif (self.name == 'D1'):
        #     rate = [a**2.0 for a in alpexp]
        # elif (self.name == 'D2'):
        #     rate = [(1.0-a)*np.log(1.0-a)+a for a in alpexp]
        # elif (self.name == 'D3'):
        #     rate = [(1.0-(1.0-a)**(1.0/3.0))**2.0 for a in alpexp]
        # elif (self.name == 'D4'):
        #     rate = [1.0 - (2.0/3.0)*a - (1.0-a)**(2.0/3.0) for a in alpexp]
        # elif (self.name == 'F0'):
        #     rate = [a for a in alpexp]
        # elif (self.name == 'F1'):
        #     rate = [-np.log(1.0-a) for a in alpexp]
        # elif (self.name == 'F2'):
        #     rate = [(1.0/(1.0-a))-1.0 for a in alpexp]
        # elif (self.name == 'F3'):
        #     rate = [0.5*((1.0-a)**(-2.0) - 1.0) for a in alpexp]
        # elif (self.name == 'P2'):
        #     rate = [a**0.5 for a in alpexp]
        # elif (self.name == 'P3'):
        #     rate = [a**(1.0/3.0) for a in alpexp]
        # elif (self.name == 'P4'):
        #     rate = [a**0.25 for a in alpexp]
        # elif (self.name == 'R2'):
        #     rate = [1.0-(1.0-a)**0.5 for a in alpexp]
        # elif (self.name == 'R3'):
        #     rate = [1.0-(1.0-a)**(1.0/3.0) for a in alpexp]
        else:
            print('Wrong model choice')
            print('Instead, choose one from the models list: "A2-A4","D1-D4","F0-F3","P2-P4","R2-R3"')
            sys.exit('Program Stopped')
        
        return rate
    
    # def f(self,alpexp):
        
    #     """Return the differential reaction rate for each different model"""
    #     if (self.name == 'A2'):
    #         rate = [2.0*(1.0-a)*np.sqrt(-np.log(1.0-a)) for a in alpexp]
    #     elif (self.name == 'A3'):
    #         rate = [3.0*(1.0-a)*(-np.log(1.0-a))**(2.0/3.0) for a in alpexp]
    #     elif (self.name == 'A4'):
    #         rate = [4.0*(1.0-a)*(-np.log(1.0-a))**(3.0/4.0) for a in alpexp]
    #     elif (self.name == 'D1'):
    #         rate = [1.0/(2.0*a) for a in alpexp]
    #     elif (self.name == 'D2'):
    #         rate = [-1.0/np.log(1.0-a) for a in alpexp]
    #     elif (self.name == 'D3'):
    #         rate = [(3.0*(1.0-a)**(2.0/3.0))/(2.0*(1.0-(1.0-a)**(1.0/3.0))) for a in alpexp]
    #     elif (self.name == 'D4'):
    #         rate = [(3.0/2.0)*((1.0-a)**(-1.0/3.0)-1.0)**(-1.0) for a in alpexp]
    #     elif (self.name == 'F0'):
    #         rate = [1.0 for a in alpexp]
    #     elif (self.name == 'F1'):
    #         rate = [1.0-a for a in alpexp]
    #     elif (self.name == 'F2'):
    #         rate = [(1.0-a)**2.0 for a in alpexp]
    #     elif (self.name == 'F3'):
    #         rate = [(1.0-a)**3.0 for a in alpexp]
    #     elif (self.name == 'P2'):
    #         rate = [2.0*(a**(1.0/2.0)) for a in alpexp]
    #     elif (self.name == 'P3'):
    #         rate = [3.0*(a**(2.0/3.0)) for a in alpexp]
    #     elif (self.name == 'P4'):
    #         rate = [4.0*(a**(3.0/4.0)) for a in alpexp]
    #     elif (self.name == 'R2'):
    #         rate = [2.0*((1.0-a)**(1.0/2.0)) for a in alpexp]
    #     elif (self.name == 'R3'):
    #         rate = [3.0*((1.0-a)**(2.0/3.0)) for a in alpexp]
    #     else:
    #         print('Wrong model choice')
    #         print('Instead, choose one from the list: "A2","A3","A4","D1","D2","D3","D4","F0","F1","F2","F3","P2","P3","P4","R2","R3"')
    #         sys.exit('Program Stopped')
            
    #     return rate

    def alpha(self,time,k):
        
        """Return the simulated conversion for each different model"""

        if (self.name == 'A2'):
            rate = 1.0-np.exp(-k*k*time*time)
        elif (self.name == 'A3'):
            rate = 1.0-np.exp(-k*k*k*time*time*time)
        elif (self.name == 'A4'):
            rate = 1.0-np.exp(-k*k*k*k*time*time*time*time)
        
        # elif (self.name == 'D1'):
        #     rate = [(k*t)**0.5 for t in time]
        # elif (self.name == 'D2'):
        #     rate = False
        #     print('This model does not have an analytical solution for the conversion')
        #     sys.exit('Program Stopped')
        # elif (self.name == 'D3'):
        #     rate = [1.0 - (1.0-(k*t)**0.5)**3.0 for t in time]
        # elif (self.name == 'D4'):
        #     rate = False
        #     print('This model does not have an analytical solution for the conversion')
        #     sys.exit('Program Stopped')
        # elif (self.name == 'F0'):
        #     rate = [k*t for t in time]
        # elif (self.name == 'F1'):
        #     rate = [1.0-np.exp(-k*t) for t in time]
        # elif (self.name == 'F2'):
        #     rate = [(k*t)/(1.0 + k*t) for t in time]
        # elif (self.name == 'F3'):
        #     rate = [(1.0 + 2.0*k*t - (1.0 + 2.0*k*t)**0.5)/(1.0 + 2.0*k*t) for t in time]
        # elif (self.name == 'P2'):
        #     rate = [k*k*t*t for t in time]
        # elif (self.name == 'P3'):
        #     rate = [k*k*k*t*t*t for t in time]
        # elif (self.name == 'P4'):
        #     rate = [k*k*k*k*t*t*t*t for t in time]
        # elif (self.name == 'R2'):
        #     rate = [k*t*(2.0 - k*t) for t in time]
        # elif (self.name == 'R3'):
        #     rate = [k*t*(3.0 - 3.0*k*t + (k*t)**2.0 ) for t in time]
        else:
            print('Wrong model choice')
            print('Instead, choose one from the models list: "A2-A4","D1-D4","F0-F3","P2-P4","R2-R3"')
            sys.exit('Program Stopped')
        
        return rate