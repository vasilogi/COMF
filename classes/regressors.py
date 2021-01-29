import numpy as np
from scipy.optimize import curve_fit

def simpleLinearFit(time,k):
    return k*time

def conversionRegression(time,conversion,model):
    # perform Non-Linear Regression
    # fit the experimental conversion (conversion)
    # calculate the Arrhenius rate constant (k)

    x          = time
    y          = conversion
    popt, pcov = curve_fit(model.alpha,x,y,p0=0.1)          # p0 : initial guess
    # popt: optimal values for the parameters so that the sum of the squared residuals of f(xdata, *popt) - ydata is minimized.
    k          = popt[0]                                    # Arrhenius rate constant
    yfit       = np.array([model.alpha(t,k) for t in time]) # simulated conversion fraction

    # calculate the determination coefficient
    residuals = y - yfit
    ss_res    = np.sum(residuals**2.0)
    ss_tot    = np.sum((y-np.mean(y))**2.0)
    r_squared = 1.0 - (ss_res / ss_tot)

    return yfit, r_squared

def integralRateRegression(time,conversion,model):
    # perform Non-Linear Regression
    # fit the experimental integral rate conversion (g)
    # calculate the Arrhenius rate constant (k)

    x          = time
    y          = np.array([model.g(a) for a in conversion])
    popt, pcov = curve_fit(simpleLinearFit,x,y,p0=0.1)          # p0 : initial guess
    # popt: optimal values for the parameters so that the sum of the squared residuals of f(xdata, *popt) - ydata is minimized.
    k          = popt[0]                                    # Arrhenius rate constant
    yfit       = np.array([simpleLinearFit(t,k) for t in time]) # simulated conversion fraction

    # calculate the determination coefficient
    residuals = y - yfit
    ss_res    = np.sum(residuals**2.0)
    ss_tot    = np.sum((y-np.mean(y))**2.0)
    r_squared = 1.0 - (ss_res / ss_tot)

    return yfit, r_squared