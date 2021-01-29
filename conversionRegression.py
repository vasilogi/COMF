# we supposed that the data have been filtered already by some other script

# PACKAGES
import os
import numpy as np
from classes.reaction_rates import Model
from classes.arrhenius import rateConstant
from classes.regressors import conversionRegression, integralRateRegression
import pandas as pd
import matplotlib.pyplot as plt

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

# conversion regression
yfit, r_squared = conversionRegression(time, conversion, model)

# integral rate regression
yfit, r_squared = integralRateRegression(time, conversion, model)

# g = np.array([model.g(i) for i in conversion])

# plt.plot(time,g)
# plt.plot(time,yfit,linestyle='--')
