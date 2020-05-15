# Developer: Yannis Vasilopoulos
# UCT Prague, June 2018
# Linkedin: https://www.linkedin.com/in/giannis-vasilopoulos/

import numpy as np
import sys
import sympy as sp

# A3 model
# Solid state reaction rate expressions

def g(a): # integral form g(a) = kt
	return (-np.log(1.0-a))**(1.0/3.0)

def f(a): # differential form f(a) = (1/k) dadt
	return 3.0*(1.0-a)*(-np.log(1.0-a))**(2.0/3.0)

def gsy(a): # for symbolic calculations
	return (-sp.log(1.0-a))**sp.Rational(1.0,3.0)

# the conversion fraction solution for isothermal cases
# conventional method
def sol(t,k):
	return 1.0-np.exp(-k*k*k*t*t*t)

# the conversion fraction solution for non-isothermal cases
# using the Coats-Redfern approximation
def nitsol(A,Ea,beta,Texp,T):
	R  = 8.314 # Ideal gas constant J / (mol.K)
	F1 = (A**3.0)*(R**3.0)*(T**6.0)/((Ea**6.0)*(beta**3.0))
	F2 = (Ea-2.0*R*Texp)**3.0
	F3 = np.exp(-3.0*Ea/(R*T))
	return 1.0 - np.exp(-F1*F2*F3)

module_name = str(sys.modules[__name__])
module_name = module_name[-7:]
module_name = module_name[:-5]