# Developer: Yannis Vasilopoulos
# UCT Prague, June 2018
# https://www.linkedin.com/in/giannis-vasilopoulos/
# Revisited at UCL, January 2020

# Program for performing the model-fitting method
# on isothermal thermogravimetric data (TGA)

# FIT ON THE DIFFERENTIAL REACTION RATE

# IMPORTANT NOTICE
# This code has been developed on Windows OS, and it's usage might be
# affected when running on different OS

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.misc import derivative
import pandas as pd
from importlib import import_module
import csv

# Mass conversion
def conversion(m0,mf,mi):
    return (m0-mi)/(m0-mf)

# Enable LaTEX
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# Basic plot settings
file_format = 'png'
dpi         = 300
font_size   = 13
lwidth      = 3
palette     = ['#161925','#ba1f33','#1412ad'] # eerie black, cardinal, zaffree

# Turn interactive plotting off
plt.rcParams.update({'figure.max_open_warning': 0}) # Remove warnings about memory
matplotlib.use('Agg') # Do not interactively show the exported figures
plt.ioff()

cwd         = os.getcwd()                                       # current working directory
data_path   = os.path.join(cwd,'data')                          # csv data files directory
csv_files   = [x for x in os.listdir(data_path) if ".csv" in x] # list all the csv files in cwd
csv_names   = [x.split(".")[0] for x in csv_files]              # list only the names of the csv files
output_path = os.path.join(cwd,'output')                        # output directory
output_path = os.path.join(output_path,'f-regression')

for i_file in range(len(csv_files)):

    # Read the CSV file
    df         = pd.read_csv(os.path.join(data_path,csv_files[i_file])) # open the CSV file
    t          = np.array(df["Time (min)"])                             # time
    m          = np.array(df["TG (mg)"])                                # thermogravimetric mass
    T          = df["Temperature (Celsius)"][0]                         # temperature
    time_units = 'min'

    # Convert the mass to the conversion fraction
    a = [conversion(m[0],m[-1],x) for x in m]

    # Restrict the conversion fraction
    b_lim = 0.10 # bottom limit
    u_lim = 0.90 # upper limit

    a = [x for x in a if x >= b_lim] ; t = [t[i] for i in range(len(a)) if a[i] >= b_lim]
    a = [x for x in a if x <= u_lim] ; t = [t[i] for i in range(len(a)) if a[i] <= u_lim]

    # Create a directory for the particular CSV data file
    csv_path = os.path.join(output_path,csv_names[i_file])
    if not os.path.exists(csv_path): os.makedirs(csv_path)

    # Fit the conversion fraction with a polynomial

    fit_degree = 9 # degree of the polynomial
    z          = np.polyfit(t,a,fit_degree)
    polynomial = np.poly1d(z) 
    t_polfit   = np.linspace(t[0],t[-1],2000) # interpolate to these new points
    a_polfit   = polynomial(t_polfit)

    plotname = 'a_vs_t.png'
    if not os.path.isfile(os.path.join(csv_path,plotname)):
        fig = plt.figure()
        plt.plot(t, a, lw=lwidth, ls='dashed', c=palette[0], label='Experiment')
        plt.plot(t_polfit, a_polfit, lw=lwidth, c=palette[1], label='Polynomial fit')
        plt.xlabel(r'$ t ('+time_units+') $', fontsize=font_size)
        plt.ylabel(r'$ a  $', fontsize=font_size)
        plt.xlim(0.0,)
        plt.ylim(0.0, 1.0)
        plt.legend()
        plt.tight_layout()
        plt.savefig(plotname, format=file_format, dpi=dpi)
        os.rename(plotname, os.path.join(csv_path,plotname))

    # Read the ranking of the models from g-regression
    g_path     = os.path.join(cwd,'output')                       # output directory
    g_path     = os.path.join(g_path,'g-regression')              # g-regression path
    g_csv_path = os.path.join(g_path,csv_names[i_file])           # path for the specific csv file inside the regression path
    g_rank_csv = os.path.join(g_csv_path,'Models_Ranking.csv')    # models ranking file from the g-regression

    # Read the ranking CSV file
    df     = pd.read_csv(g_rank_csv)
    models = df["Model"].values ; modelnames = ['_'+x for x in models]
    ks     = np.array(df["k"])
    Rs     = np.array(df["R2"])

    # Loop over the different models
    for i_model in range(len(modelnames)):

        # Pick up one model from the list
        model = import_module(modelnames[i_model], package=None)

        # Calculate the derivative of the experimental data
        dadt = [derivative(polynomial,ti,dx=1e-6) for ti in t_polfit]

        fexp     = dadt                             # The experimental dadt
        k        = ks[i_model]                      # The k parameter
        fcal     = [k*model.f(i) for i in a_polfit] # Calculate k f(a) (the simulated rate)
        fexpmean = np.mean(fexp, dtype=np.float64)  # The mean of the experimental values

        # Calculate the coefficient of determination
        SSres = 0.0 ; SStot = 0.0
        for i in range(len(fcal)):
            SSres += (fexp[i] - fcal[i])*(fexp[i] - fcal[i])   # Residual sum of squares
            SStot += (fexp[i] - fexpmean)*(fexp[i] - fexpmean) # Total sum of squares

        R2 = 1.0 - SSres/SStot                                 # Determination coefficient

        # Store the error data
        data = [model.module_name,repr(R2)]

        # Create a directory to store all the models in
        models_path = os.path.join(csv_path,'models')
        if not os.path.exists(models_path): os.makedirs(models_path)

        # Create a CSV file containing the Model's name,k,R2,SStot,SSres,eta,epsilon
        filename = 'Models_Ranking.csv'
        filepath = os.path.join(csv_path,filename)
        if not filename in os.listdir(csv_path):
           f= open(filepath,'w')
           f.write('Model,R2\n')
           f.write(''+data[0]+','+data[1]+'\n')
        else:
           f= open(filepath,'a')
           f.write(''+data[0]+','+data[1]+'\n')
        f.close()

        # Create a directory for this particular model
        spec_model_path = os.path.join(models_path,''+model.module_name+'')  # Name the directory for the particular model
        if not os.path.exists(spec_model_path): os.makedirs(spec_model_path) # Create this directory

        
        # Plot the calculated f rate along with the experimental
        plotname = 'f_vs_t_'+model.module_name+'_model.png'
        if not os.path.isfile(os.path.join(spec_model_path,plotname)):
            fig = plt.figure()
            plt.plot(t_polfit, dadt, lw=lwidth, c=palette[0], ls='dashed', label=r'Experimental at $T = '+str(T)+' ^{o}C$')
            plt.plot(t_polfit, fcal, lw=lwidth, c=palette[1], label=r''+model.module_name+' model, $R^{2} = '+str(round(R2,3))+'$')
            plt.legend()
            plt.xlabel(r'$ t ('+time_units+') $', fontsize=font_size)
            plt.ylabel(r'$ f (a)  $', fontsize=font_size)
            # plt.xlim(0.0,) ; plt.ylim(0.0,)  # Axes limits
            plt.tight_layout()
            plt.savefig(plotname, format=file_format, dpi=dpi)
            os.rename(plotname, os.path.join(spec_model_path,plotname))

        # Export the experimental f rate
        filename = 'fexp_vs_t_'+model.module_name+'_model.csv'
        if not os.path.isfile(os.path.join(spec_model_path,filename)):
            filepath = os.path.join(spec_model_path,filename)
            tmp = np.transpose([fexp,t_polfit])
            np.savetxt(filepath, tmp, delimiter=",")
            # Add header in the csv file
            with open(filepath,newline='') as f:
                r = csv.reader(f)
                data = [line for line in r]
            with open(filepath,'w',newline='') as f:
                w = csv.writer(f)
                w.writerow(['fexp','t_polfit'])
                w.writerows(data)

        # Export the calculated g rate
        filename = 'fcalc_vs_t_'+model.module_name+'_model.csv'
        if not os.path.isfile(os.path.join(spec_model_path,filename)):
            filepath = os.path.join(spec_model_path,filename)
            tmp = np.transpose([fcal,t_polfit])
            np.savetxt(filepath, tmp, delimiter=",")
            # Add header in the csv file
            with open(filepath,newline='') as f:
                r = csv.reader(f)
                data = [line for line in r]
            with open(filepath,'w',newline='') as f:
                w = csv.writer(f)
                w.writerow(['fcal','t_polfit'])
                w.writerows(data)