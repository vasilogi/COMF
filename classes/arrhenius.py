import numpy as np

def rateConstant(frequency,enthalpy,temperature):
    # S.I.
    # the units of frequency are identical to those of the rate constant k
    # e.g. for a first-order reaction it's s-1
    R    = 8.31446261815324 # J K-1 mol-1
    beta = 1.0/(R*temperature)
    return frequency*np.exp(-beta*enthalpy)