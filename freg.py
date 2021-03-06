# Developer: Yannis Vasilopoulos
# https://www.linkedin.com/in/giannis-vasilopoulos/
# Revisited at UCL, January 2020

# Program for performing the model-fitting method
# on isothermal thermogravimetric data (TGA)

# FIT ON THE INTEGRAL REACTION RATE

# IMPORTANT NOTICE
# This code has been developed on Linux

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
from classes.reaction_rates import Model
import sys

# Fitting function
def fit(t,k):
    return k*t

# Limit fitting based on the y-axis
def limit(x,y,blim,ulim):
    
    y_tmp = [i for i in y if i >= blim]                           # Bottom limit of the y-array
    x_tmp = [x[i] for i in range(len(y)) if y[i] >= blim]         # Bottom limit the x-array
    y = [i for i in y_tmp if i <= ulim]                           # Upper limit the y-array
    x = [x_tmp[i] for i in range(len(y_tmp)) if y_tmp[i] <= ulim] # Upper limit the x-array
    
    return x,y

print('')
print('+-------------------------------------+')
print('| Regression in the differential rate |')
print('+-------------------------------------+')


# The names of the models supported in this code
modelnames = ["A2","A3","A4","D1","D3","F0","F1","F2","F3","P2","P3","P4","R2","R3"]

# All the directories
CWD         = os.getcwd()                                  # current working directory
DATA        = os.path.join(CWD,'data')                     # csv data files directory
Csvs        = [x for x in os.listdir(DATA) if ".csv" in x] # list all the csv files in cwd
Csv_names   = [x.split(".")[0] for x in Csvs]              # list only the names of the csv files
OUTPUT_BASE = os.path.join(CWD,'output')                   # output directory

b_lim = float(sys.argv[1]) # bottom limit
u_lim = float(sys.argv[2]) # upper limit

# loop over all CSV files
for Csv_i, Csv in enumerate(Csvs):

    print('')
    print('Data set:', str(Csv_names[Csv_i]))
    print('')

    OUTPUT    = os.path.join(OUTPUT_BASE,str(Csv_names[Csv_i]))                  # output directory for the data regarding the conversion
    OUTPUT    = os.path.join(OUTPUT,'freg_blim_'+str(b_lim)+'_ulim_'+str(u_lim)) # output directory for the data regarding the conversion
    GRAPH     = os.path.join(OUTPUT,'graphs')                                    # output directory for the graphs
    CSV       = os.path.join(OUTPUT,'csv')                                       # output directory for the csv files

    # Create necessary output directories
    if not os.path.exists(GRAPH): os.makedirs(GRAPH)
    if not os.path.exists(CSV): os.makedirs(CSV)

    # Get the CSV file
    Csv = Csvs[Csv_i]

    # Read the CSV file
    df          = pd.read_csv(os.path.join(DATA,Csv)) # open the CSV file
    time        = df["Time (min)"].to_numpy()         # time
    # mass        = df["TG (mg)"].to_numpy()            # thermogravimetric mass
    # temperature = df["Temperature (C)"].to_numpy()    # temperature
    conversion  = df["Conversion"].to_numpy()         # conversion fraction
    time_units  = 'min'                               # time units

    # Get the updated region to fit
    t, a = limit(time, conversion, b_lim, u_lim)

    # Basic plot settings
    graph_format = 'png'
    graph_dpi    = 300
    font_size    = 13
    lwidth       = 3
    palette      = ['#161925','#ba1f33','#1412ad'] # eerie black, cardinal, zaffree
                   
    # Turn interactive plotting off
    plt.ioff()

    # Create a CSV file to store the models_ranking
    Csv = os.path.join(CSV,'models_ranking.csv')

    # Clean previous results
    if os.path.isfile(Csv):
    	os.remove(Csv)

    # Create the file's header
    with open(Csv,'w') as ofile:
    	ofile.write('model,r_squared,bottom_limit,upper_limit,arrhenius_k'+'\n')

    # Loop over all models
    for modelname in modelnames:

    	# Pick up the model
        model = Model(modelname)

        # Perform Non-Linear Regression
        # Fit the experimental integral rate model.g(a) with the linear function fit
        # Calculate the Arrhenius rate constant (k)

        xdata          = t
        ydata          = model.g(a)
        params, extras = curve_fit(fit,xdata,ydata,p0=0.1)
        k              = params[0]  # The Arrhenius k parameter    

        ydata = model.f(a)                     # The experimental differential rate
        yfit  = model.f(model.alpha(xdata,k))  # The simulated differential rate  


        # Calculate the determination coefficient
        residuals = np.array(ydata) - np.array(yfit)
        ss_res    = np.sum(residuals**2.0)
        ss_tot    = np.sum((ydata-np.mean(ydata))**2.0)
        r_squared = 1.0 - (ss_res / (ss_tot + 1.0e-12))

        if r_squared >= 0.98:
            print(modelname+' model has a high determination coefficient: ', round(r_squared,3))

        # Export the statistics data regarding the particular model
        with open(Csv,'a') as ranking_csv:
        	ranking_csv.write(str(modelname)+','+str(r_squared)+','+str(b_lim)+','+str(u_lim)+','+str(k)+'\n')

        # Export a graph for the fitting of the integral reaction rate
        Plot = os.path.join(GRAPH,modelname+'_f_vs_t.png')

        # Clean previous runs
        if os.path.isfile(Plot):
            os.remove(Plot)
        fig  = plt.figure()
        plt.plot(xdata, ydata, lw=lwidth, c=palette[0], label='Experimental rate') 
        plt.plot(xdata ,yfit, lw=lwidth, c=palette[1], label='Fit '+r'$R^{2} = '+str(round(r_squared,3))+'$')    
        plt.xlabel(r'$ t ('+time_units+') $')
        plt.ylabel(r'$ f(a) $')
        plt.xlim(0.0,)
        plt.ylim(0.0,)
        plt.legend()
        plt.tight_layout()
        plt.savefig(Plot, format=graph_format, dpi=graph_dpi)
        plt.close() # to avoid memory warnings


    	# Create a CSV file to store the experimental rate and fit
        File = os.path.join(CSV,modelname+'_frate_vs_t.csv')
        
        # Clean previous runs or create the header of this CSV
        if os.path.isfile(File):
            os.remove(File)
        else:
            with open(File,'w') as grate_csv:
                grate_csv.write('time,experimental_rate,fit_rate'+'\n')
        
        # Append data to this csv file
        with open(File,'a') as grate_csv:
            for i in range(len(xdata)):
                grate_csv.write(str(xdata[i])+','+str(ydata[i])+','+str(yfit[i])+'\n')
        grate_csv.close()

    ranking_csv.close() # close the exported csv