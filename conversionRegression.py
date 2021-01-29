# we supposed that the data have been filtered already by some other script

# PACKAGES
import os
import numpy as np
from scipy.optimize import curve_fit
from classes.reaction_rates import Model
from classes.arrhenius import rateConstant
import pandas as pd
import matplotlib.pyplot as plt

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

# DIRECTORIES
MAIN_DIR  = os.getcwd()                   # current working directory
DATA      = os.path.join(MAIN_DIR,'data') # data directory

# models names supported in this code
modelNames = ["A2","A3","A4","D1","D3","F0","F1","F2","F3","P2","P3","P4","R2","R3"]

# get the data from the csv files
Csvs = os.listdir(DATA)
Csvs = [os.path.join(DATA,i) for i in Csvs]

# read the CSV file
df           = pd.read_csv(Csvs[0])
conversion   = df['conversion'].to_numpy()
time         = df['time'].to_numpy()
temperature  = df['temperature'].to_numpy()[0]

# pick up the model
model = Model('A2')

yfit, r_squared = conversionRegression(time, conversion, model)

plt.plot(time,conversion)
plt.plot(time,yfit,linestyle='--')