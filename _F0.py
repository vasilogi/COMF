# Developer: Yannis Vasilopoulos
# UCT Prague, June 2018
# Linkedin: https://www.linkedin.com/in/giannis-vasilopoulos/

import numpy as np
import sys
import sympy as sp

# F0 model
# Solid state reaction rate expressions

def g(a): # integral form g(a) = kt
	return a

def f(a): # differential form f(a) = (1/k) dadt
	return 1.0

def gsy(a): # for symbolic calculations
	return a

# the conversion fraction solution for isothermal cases
# conventional method
def sol(t,k):
	return  k*t

# the conversion fraction solution for non-isothermal cases
# using the Coats-Redfern approximation
def nitsol(A,Ea,beta,Texp,T):
	R  = 8.314 # Ideal gas constant J / (mol.K)
	F1 = (A*R*T**2.0)/(beta*Ea**2.0)
	F2 = Ea-2.0*R*Texp
	F3 = np.exp(-Ea/(R*T))
	return F1*F2*F3

module_name = str(sys.modules[__name__])
module_name = module_name[-7:]
module_name = module_name[:-5]