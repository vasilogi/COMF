# Developer: Yannis Vasilopoulos
# UCT Prague, June 2018
# Linkedin: https://www.linkedin.com/in/giannis-vasilopoulos/

import numpy as np
import sys
import sympy as sp

# D1 model
# Solid state reaction rate expressions

def g(a): # integral form g(a) = kt
	return a**2.0

def f(a): # differential form f(a) = (1/k) dadt
	return 1.0/(2.0*a)

def gsy(a): # for symbolic calculations
	return a**2.0

# the conversion fraction solution for isothermal cases
# conventional method
def sol(t,k):
	return (k*t)**0.5

# the conversion fraction solution for non-isothermal cases
# using the Coats-Redfern approximation
def nitsol(A,Ea,beta,Texp,T):
	R  = 8.314 # Ideal gas constant J / (mol.K)
	F1 = T/Ea
	F2 = A*R/beta
	F3 = Ea-2.0*R*Texp
	F4 = np.exp(-Ea/(R*T))
	return F1*np.sqrt(F2*F3*F4)

module_name = str(sys.modules[__name__])
module_name = module_name[-7:]
module_name = module_name[:-5]