# Developer: Yannis Vasilopoulos
# UCT Prague, June 2018
# Linkedin: https://www.linkedin.com/in/giannis-vasilopoulos/

import numpy as np
import sys
import sympy as sp

# D2 model
# Solid state reaction rate expressions

def g(a): # integral form g(a) = kt
	return (1.0-a)*np.log(1.0-a)+a

def f(a): # differential form f(a) = (1/k) dadt
	return -1.0/np.log(1.0-a)

def gsy(a): # for symbolic calculations
	return (1.0-a)*sp.log(1.0-a)+a

module_name = str(sys.modules[__name__])
module_name = module_name[-7:]
module_name = module_name[:-5]