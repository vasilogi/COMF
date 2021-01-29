# PACKAGES
import os
import numpy as np
from classes.reaction_rates import Model
from classes.arrhenius import rateConstant
import pandas as pd

# DIRECTORIES
MAIN_DIR  = os.getcwd()                   # current working directory
DATA      = os.path.join(MAIN_DIR,'data') # data directory

# models names supported in this code
modelNames = ["A2","A3","A4","D1","D3","F0","F1","F2","F3","P2","P3","P4","R2","R3"]

# pick up a model
model = Model('A2')

# determine an Arrhenius rate constant
enthalpy    = 150.0e+3 # J mol-1
frequency   = 2.0e+37
temperature = np.linspace(200.0,300.0,5)

for T in temperature:

    # generate a data set for each temperature
    k           = rateConstant(frequency,enthalpy,T)

    # calculate the start end end time for the sample data
    alpha     = np.linspace(0.05,0.95,100)
    startTime = model.g(alpha[0])/k
    endTime   = model.g(alpha[-1])/k
    time      = np.linspace(startTime,endTime,100)

    # calculate the conversion based on the chosen model
    conversion = np.array([ model.alpha(t,k) for t in time])

    # data to dictionary
    data = {'conversion': conversion, 'time': time, 'temperature': T}
    # dictionary to dataframe
    df = pd.DataFrame(data)
    # CSV filename
    Csv = os.path.join(DATA,str(T)+'_Kelvin.csv')
    # dataframe to csv
    df.to_csv(Csv,index=False)