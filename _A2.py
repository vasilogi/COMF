# Developer: Yannis Vasilopoulos
# UCT Prague, June 2018
# Linkedin: https://www.linkedin.com/in/giannis-vasilopoulos/

import numpy as np
import sys
import sympy as sp

# A2 model
# Solid state reaction rate expressions

def g(a): # integral form g(a) = kt
	return np.sqrt(-np.log(1.0-a))

def f(a): # differential form f(a) = (1/k) dadt
	return 2.0*(1.0-a)*np.sqrt(-np.log(1.0-a))

def gsy(a): # for symbolic calculations
	return sp.sqrt(-sp.log(1.0-a))

# the conversion fraction solution for isothermal cases
# conventional method
def sol(t,k):
	return 1.0-np.exp(-k*k*t*t)

# the conversion fraction solution for non-isothermal cases
# using the Coats-Redfern approximation
def nitsol(A,Ea,beta,Texp,T):
	R  = 8.314 # Ideal gas constant J / (mol.K)
	F1 = (A**2.0)*(R**2.0)*(T**4.0)/((Ea**4.0)*(beta**2.0))
	F2 = (Ea-2.0*R*Texp)**2.0
	F3 = np.exp(-2.0*Ea/(R*T))
	return 1.0 - np.exp(-F1*F2*F3)

module_name = str(sys.modules[__name__])
module_name = module_name[-7:]
module_name = module_name[:-5]