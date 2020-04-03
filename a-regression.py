# Developer: Yannis Vasilopoulos
# UCT Prague, June 2018
# https://www.linkedin.com/in/giannis-vasilopoulos/
# Revisited at UCL, January 2020

# Program for performing the model-fitting method
# on isothermal thermogravimetric data (TGA)

# FIT ON THE CONVERSION FRACTION ITSELF

# IMPORTANT NOTICE
# This code has been developed on Windows OS, and it's usage might be
# affected when running on different OS

import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
from importlib import import_module
import csv

# Fitting function
def fit(t,k):
    return k*t

# Mass conversion
def conversion(m0,mf,mi):
	return (m0-mi)/(m0-mf)

#            *** IMPORTANT NOTICE ***
# Note that D4 and D2 models have no solution function

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
output_path = os.path.join(output_path,'a-regression')

# Models
scripts = [x for x in os.listdir(cwd) if ".py" in x] # Get the names of the python scripts in this directory
modelnames = [x for x in scripts if "_" in x]        # List only the script names containing a function
modelnames = [x.split(".py")[0] for x in modelnames] # List only the module names
modelnames = sorted(modelnames)                      # sort list alphabetically

for i_file in range(len(csv_files)):

	# Read the CSV file
	df         = pd.read_csv(os.path.join(data_path,csv_files[i_file])) # open the CSV file
	t          = np.array(df["Time (min)"])     						# time
	m          = np.array(df["TG (mg)"])        						# thermogravimetric mass
	T          = df["Temperature (Celsius)"][0] 						# temperature
	time_units = 'min'

	# Convert the mass to the conversion fraction
	a = [conversion(m[0],m[-1],x) for x in m]

	# Restrict the conversion fraction
	
	b_lim = 0.05 # bottom limit
	u_lim = 0.95 # upper limit

	a = [x for x in a if x >= b_lim] ; t = [t[i] for i in range(len(a)) if a[i] >= b_lim]
	a = [x for x in a if x <= u_lim] ; t = [t[i] for i in range(len(a)) if a[i] <= u_lim]

	# Create a directory for the particular CSV data file
	csv_path = os.path.join(output_path,csv_names[i_file])
	if not os.path.exists(csv_path): os.makedirs(csv_path)

	# Plot the conversion fraction over time
	plotname = 'a_vs_t.png'
	if not os.path.isfile(os.path.join(csv_path,plotname)):
		fig = plt.figure()
		plt.plot(t, a, lw=lwidth, c=palette[0])
		plt.xlabel(r'$ t ('+time_units+') $', fontsize=font_size)
		plt.ylabel(r'$ a  $', fontsize=font_size)
		plt.xlim(0.0,)
		plt.ylim(0.0, 1.0)
		plt.tight_layout()
		plt.savefig(plotname, format=file_format, dpi=dpi)
		os.rename(plotname, os.path.join(csv_path,plotname))

	# Plot the conversion fraction versus t
	DeniedModels = ['D2','D4']

	# Loop over the different models
	for i_model in range(len(modelnames)):

		# Pick up one model from the list
		model   = import_module(modelnames[i_model], package=None)

		if not (model.module_name in DeniedModels ):

			# Perform Non-Linear Regression
			params, extras = curve_fit(model.sol,t,a,bounds=(0.0001,0.1))
			k              = params[0]                    # The k parameter
			acal           = [model.sol(i,k) for i in t]  # The simulated a values given the k calculation
			gcal           = [fit(i,k) for i in t]        # The simulated g values given the k calculation
			gexp           = [model.g(i) for i in a]
			aexmean        = np.mean(a, dtype=np.float64) # The mean of the experimental values

			# Calculate the coefficient of determination
			SSres = 0.0 ; SStot = 0.0
			for i in range(len(acal)):
				SSres += (a[i] - acal[i])*(a[i] - acal[i]) # Residual sum of squares
				SStot += (a[i] - aexmean)*(a[i] - aexmean) # Total sum of squares

			R2 = 1.0 - SSres/SStot # Determination coefficient

			# Store the error data
			data = [model.module_name,repr(k),repr(R2)]

			# Create a directory to store all the models in
			models_path = os.path.join(csv_path,'models')
			if not os.path.exists(models_path): os.makedirs(models_path)

			# Create a CSV file containing the Model's name,k,R2,SStot,SSres,eta,epsilon
			filename = 'Models_Ranking.csv'
			filepath = os.path.join(csv_path,filename)
			if not filename in os.listdir(csv_path):
			   f= open(filepath,'w')
			   f.write('Model,k,R2\n')
			   f.write(''+data[0]+','+data[1]+','+data[2]+'\n')
			else:
			   f= open(filepath,'a')
			   f.write(''+data[0]+','+data[1]+','+data[2]+'\n')
			f.close()

			# Create a directory for this particular model
			spec_model_path = os.path.join(models_path,''+model.module_name+'')  # Name the directory for the particular model
			if not os.path.exists(spec_model_path): os.makedirs(spec_model_path) # Create this directory

			# Plot the conversion fractions
			plotname = 'a_vs_t_'+model.module_name+'_model.png'
			if not os.path.isfile(os.path.join(spec_model_path,plotname)):
				fig = plt.figure()
				plt.plot(t, a, lw=lwidth, c=palette[0], ls='dashed', label=r'Experimental at $T = '+str(T)+' ^{o}C$')
				plt.plot(t, acal, lw=lwidth, c=palette[1], label=r''+model.module_name+' model, $R^{2} = '+str(round(R2,3))+'$')
				plt.legend()
				plt.xlabel(r'$ t ('+time_units+') $', fontsize=font_size)
				plt.ylabel(r'$ a  $', fontsize=font_size)
				plt.xlim(0.0,)
				plt.ylim(0.0, 1.0)
				plt.tight_layout()
				plt.savefig(plotname, format=file_format, dpi=dpi)
				os.rename(plotname, os.path.join(spec_model_path,plotname))

			# Plot the experimental g rate
			plotname = 'g_vs_t_'+model.module_name+'_model.png'
			if not os.path.isfile(os.path.join(spec_model_path,plotname)):
				fig = plt.figure()
				plt.plot(t, gexp, lw=lwidth, c=palette[0], ls='dashed', label=r'Experimental at $T = '+str(T)+' ^{o}C$')
				plt.plot(t, gcal, lw=lwidth, c=palette[1], label=r''+model.module_name+' model, $R^{2} = '+str(round(R2,3))+'$')
				plt.legend()
				plt.xlabel(r'$ t ('+time_units+') $', fontsize=font_size)
				plt.ylabel(r'$ g(a)  $', fontsize=font_size)
				# plt.xlim(0.0,) ; plt.ylim(0.0, 1.0)  # Axes limits
				plt.tight_layout()
				plt.savefig(plotname, format=file_format, dpi=dpi)
				os.rename(plotname, os.path.join(spec_model_path,plotname))

			# Export the experimental conversion fraction		
			filename = 'aexp_vs_t_'+model.module_name+'_model.csv'
			if not os.path.isfile(os.path.join(spec_model_path,filename)):
				filepath = os.path.join(spec_model_path,filename)
				tmp = np.transpose([a,t])
				np.savetxt(filepath, tmp, delimiter=",")
				# Add header in the csv file
				with open(filepath,newline='') as f:
					r = csv.reader(f)
					data = [line for line in r]
				with open(filepath,'w',newline='') as f:
					w = csv.writer(f)
					w.writerow(['aexp','t'])
					w.writerows(data)

			# Export the modeled fraction
			filename = 'acalc_vs_t_'+model.module_name+'_model.csv'
			if not os.path.isfile(os.path.join(spec_model_path,filename)):
				filepath = os.path.join(spec_model_path,filename)
				tmp = np.transpose([acal,t])
				np.savetxt(filepath, tmp, delimiter=",")
				# Add header in the csv file
				with open(filepath,newline='') as f:
					r = csv.reader(f)
					data = [line for line in r]
				with open(filepath,'w',newline='') as f:
					w = csv.writer(f)
					w.writerow(['acal','t'])
					w.writerows(data)

			# plt.show()