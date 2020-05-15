# Developer: Yannis Vasilopoulos
# UCT Prague, June 2018
# Linkedin: https://www.linkedin.com/in/giannis-vasilopoulos/

import numpy as np
import sys
import sympy as sp

# P4 model
# Solid state reaction rate expressions

def g(a): # integral form g(a) = kt
	return a**0.25

def f(a): # differential form f(a) = (1/k) dadt
	return 4.0*(a**(3.0/4.0))

def gsy(a): # for symbolic calculations
	return a**sp.Rational(1.0,4.0)

# the conversion fraction solution for isothermal cases
# conventional method
def sol(t,k):
	return k*k*k*k*t*t*t*t

# the conversion fraction solution for non-isothermal cases
# using the Coats-Redfern approximation
def nitsol(A,Ea,beta,Texp,T):
	R  = 8.314 # Ideal gas constant J / (mol.K)
	F1 = ((A*R/beta)**4.0)*(T/Ea)**8.0
	F2 = (Ea - 2.0*R*Texp)**4.0
	F3 = np.exp(-4.0*Ea/(R*T))
	return F1*F2*F3

module_name = str(sys.modules[__name__])
module_name = module_name[-7:]
module_name = module_name[:-5]