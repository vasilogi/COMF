# Developer: Yannis Vasilopoulos
# UCT Prague, June 2018
# Linkedin: https://www.linkedin.com/in/giannis-vasilopoulos/

import numpy as np
import sys
import sympy as sp

# F3 model
# Solid state reaction rate expressions

def g(a): # integral form g(a) = kt
	return 0.5*((1.0-a)**(-2.0) - 1.0)

def f(a): # differential form f(a) = (1/k) dadt
	return (1.0-a)**3.0

def gsy(a): # for symbolic calculations
	return 0.5*((1.0-a)**(-2.0) - 1.0)

# the conversion fraction solution for isothermal cases
# conventional method
def sol(t,k):
	return (1.0 + 2.0*k*t - (1.0 + 2.0*k*t)**0.5)/(1.0 + 2.0*k*t)

# the conversion fraction solution for non-isothermal cases
# using the Coats-Redfern approximation
def nitsol(A,Ea,beta,Texp,T):
	R  = 8.314 # Ideal gas constant J / (mol.K)
	F1 = 2.0*A*Ea*R*T**2.0
	F2 = 4.0*A*Texp*(R*T)**2.0
	F3 = beta*(Ea**2.0)*np.exp(Ea/(R*T))
	F4 = F1
	F5 = F2
	F6 = F3
	F7 = Ea*np.sqrt(beta*(F1-F2+F3)*np.exp(Ea/(R*T)))
	return (1.0/(F1-F2+F3))*(F4-F5+F6-F7)

module_name = str(sys.modules[__name__])
module_name = module_name[-7:]
module_name = module_name[:-5]