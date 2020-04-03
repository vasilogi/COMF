# Developer: Yannis Vasilopoulos
# UCT Prague, June 2018
# Linkedin: https://www.linkedin.com/in/giannis-vasilopoulos/

import sys
import sympy as sp

# D4 model
# Solid state reaction rate expressions

def g(a): # integral form g(a) = kt
	return 1.0 - (2.0/3.0)*a - (1.0-a)**(2.0/3.0)

def f(a): # differential form f(a) = (1/k) dadt
	return (3.0/2.0)*((1.0-a)**(-1.0/3.0)-1.0)**(-1.0)

def gsy(a):
	return 1.0 - sp.Rational(2.0,3.0)*a - (1.0-a)**sp.Rational(2.0,3.0)

module_name = str(sys.modules[__name__])
module_name = module_name[-7:]
module_name = module_name[:-5]