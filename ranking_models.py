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

# library
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

def R2_distance(x1,x2,x3):
    return np.sqrt( (1.0-x1)*(1.0-x1) + (1.0-x2)*(1.0-x2) + (1.0-x3)*(1.0-x3) )

print('COMF ranking')

# Basic plot settings
graph_format = 'png'
graph_dpi    = 300
font_size    = 10
lwidth       = 1
palette      = ['#161925','#ba1f33','#1412ad'] # eerie black, cardinal, zaffree

# Turn interactive plotting off
plt.ioff()

# All the directories
CWD     = os.getcwd()                                  # current working directory
OUTPUT  = os.path.join(CWD,'output')                   # output directory
RANKING = os.path.join(OUTPUT,'ranking')               # output directory for the graphs

# Create necessary output directories
if not os.path.exists(RANKING): os.makedirs(RANKING)

# Limit the fitting region
b_lim = float(sys.argv[1]) # bottom limit
u_lim = float(sys.argv[2]) # upper limit

ACSV = os.path.join(OUTPUT,'areg_blim_'+str(b_lim)+'_ulim_'+str(u_lim))
GCSV = os.path.join(OUTPUT,'greg_blim_'+str(b_lim)+'_ulim_'+str(u_lim))
FCSV = os.path.join(OUTPUT,'freg_blim_'+str(b_lim)+'_ulim_'+str(u_lim))

ACSV = os.path.join(ACSV,'csv') # csv files for the data regarding the conversion
GCSV = os.path.join(GCSV,'csv') # csv files for the data regarding the integral rate fitting
FCSV = os.path.join(FCSV,'csv') # csv files for the data regarding the differential rate fitting

CSV = [ACSV,GCSV,FCSV]
Csv_list = [os.path.join(i,'models_ranking.csv') for i in CSV]

# Load base data frame which containts all the modelnames and constants

df_base   = pd.read_csv(os.path.join(GCSV,'models_ranking.csv')) # read the CSV file as dataframe

# Loop over all the data
for Csv in Csv_list:

	df        = pd.read_csv(Csv)                                  # read the CSV file as dataframe
	df        = df.sort_values(by='model').reset_index(drop=True) # Sort values by 'model' and re-index after sorting
	models    = df["model"].tolist()                              # model's names
	k         = df["arrhenius_k"].to_numpy()                      # arrhenius constant
	r_squared = df["r_squared"].to_numpy()                        # determination coefficient


	if 'areg' in Csv or 'freg' in Csv:
		df        = pd.read_csv(Csv)                                  # read the CSV file as dataframe
		df        = df.append(df_base[df_base.model=='D2'], ignore_index=True)
		df        = df.append(df_base[df_base.model=='D4'], ignore_index=True)
		df        = df.sort_values(by='model').reset_index(drop=True) # Sort values by 'model' and re-index after sorting
		models    = df["model"].tolist()                              # model's names
		k         = df["arrhenius_k"].to_numpy()                      # arrhenius constant
		r_squared = df["r_squared"].to_numpy()                        # determination coefficient

	if 'areg' in Csv:
		R2_a = r_squared
	elif 'greg' in Csv:
		R2_g = r_squared
	elif 'freg' in Csv:
		R2_f = r_squared

# Plot the Euclidean

R2_euclidean = 0.0
R2_euclidean = [R2_distance(R2_g[i],R2_a[i],R2_f[i]) for i in range(len(R2_g))]

# Export a graph for the fitting of the integral reaction rate
Plot = os.path.join(RANKING,'COMF_ranking.png')

fig = plt.figure()
x = range(len(models))
plt.scatter(x,R2_euclidean,
			s=80,
			c=palette[1],
			edgecolors='black')
# Check if there is NaN in euclidean
if R2_euclidean[np.argmin(R2_euclidean)] != R2_euclidean[np.argmin(R2_euclidean)]:
	R2_euclidean[np.argmin(R2_euclidean)] = 1e+2

plt.scatter(x[np.argmin(R2_euclidean)],R2_euclidean[np.argmin(R2_euclidean)],
			s=400,
			c=palette[2],
			marker='*',
			edgecolors='black')
plt.ylabel(r'$ d(R^{2}_{g},R^{2}_{a},R^{2}_{f}) $', fontsize=font_size)
plt.yscale('log')
# plt.ylim(0.0,)
plt.grid(b=False, which='major', color='#D5DFE1', linestyle='-', linewidth=1)
plt.xticks(x, models)
plt.tick_params(which='both',direction='out')
plt.tight_layout()
plt.savefig(Plot, format=graph_format, dpi=graph_dpi)
plt.close() # to avoid memory warnings

# Create a CSV file to store the COMF ranking
File = os.path.join(RANKING,'COMF_ranking.csv')

# Clean previous runs or create the header of this CSV
if os.path.isfile(File):
    os.remove(File)
else:
    with open(File,'w') as comf_csv:
        comf_csv.write('model,euclidean'+'\n')

# Append data to this csv file
with open(File,'a') as comf_csv:
    for i in range(len(R2_euclidean)):
        comf_csv.write(str(models[i])+','+str(R2_euclidean[i])+'\n')
comf_csv.close()

print(models[np.argmin(R2_euclidean)]+' is the best candidate model')