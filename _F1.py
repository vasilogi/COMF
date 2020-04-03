# Developer: Yannis Vasilopoulos
# UCT Prague, June 2018
# Linkedin: https://www.linkedin.com/in/giannis-vasilopoulos/

import numpy as np
import sys
import sympy as sp

# F1 model
# Solid state reaction rate expressions

def g(a): # integral form g(a) = kt
	return -np.log(1.0-a)

def f(a): # differential form f(a) = (1/k) dadt
	return 1.0-a

def gsy(a): # for symbolic calculations
	return -sp.log(1.0-a)

# the conversion fraction solution for isothermal cases
# conventional method
def sol(t,k):
	return 1.0-np.exp(-k*t)

# the conversion fraction solution for non-isothermal cases
# using the Coats-Redfern approximation
def nitsol(A,Ea,beta,Texp,T):
	R  = 8.314 # Ideal gas constant J / (mol.K)
	F1 = ((A*R*T**2.0)/(beta*Ea))*np.exp(-Ea/(R*T))
	F2 = ((2.0*Texp*A*R**2.0)/(beta*Ea**2.0))*(T**2.0)*np.exp(-Ea/(R*T))
	return 1.0 - np.exp(-F1)*np.exp(F2)

module_name = str(sys.modules[__name__])
module_name = module_name[-7:]
module_name = module_name[:-5]