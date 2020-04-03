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
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys

def R2_distance(x1,x2,x3):
    return np.sqrt( (1.0-x1)*(1.0-x1) + (1.0-x2)*(1.0-x2) + (1.0-x3)*(1.0-x3) )

# Enable LaTEX
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# Basic plot settings
file_format = 'png'
dpi         = 300
font_size   = 10
lwidth      = 1
palette     = ['#161925','#ba1f33','#1412ad'] # eerie black, cardinal, zaffree

# Turn interactive plotting off
plt.rcParams.update({'figure.max_open_warning': 0})
matplotlib.use('Agg') # Do not interactively show the exported figures
plt.ioff()

# Directories
cwd         = os.getcwd()                                       # current working directory
data_path   = os.path.join(cwd,'data')                          # csv data files directory
csv_files   = [x for x in os.listdir(data_path) if ".csv" in x] # list all the csv files in cwd
csv_names   = [x.split(".")[0] for x in csv_files]              # list only the names of the csv files
output_path = os.path.join(cwd,'output')                        # output directory

# Loop over all the data
for i_file in range(len(csv_files)):

	# Read the ranking of the models from g-regression
	tmp_path = os.path.join(output_path,'g-regression')     # g-regression path
	csv_path = os.path.join(tmp_path,csv_names[i_file])     # path for the specific csv file inside the regression path
	rank_csv = os.path.join(csv_path,'Models_Ranking.csv')  # models ranking file from the g-regression

	# Read the ranking CSV file
	df_g     = pd.read_csv(rank_csv)
	models_g = df_g["Model"].tolist()
	k_g      = np.array(df_g["k"])
	R2_g     = np.array(df_g["R2"])

	# Read the ranking of the models from f-regression
	tmp_path = os.path.join(output_path,'f-regression')     # g-regression path
	csv_path = os.path.join(tmp_path,csv_names[i_file])     # path for the specific csv file inside the regression path
	rank_csv = os.path.join(csv_path,'Models_Ranking.csv')  # models ranking file from the g-regression

	# Read the ranking CSV file
	df_f     = pd.read_csv(rank_csv)
	models_f = df_f["Model"].tolist()
	R2_f     = np.array(df_f["R2"])

	# Read the ranking of the models from a-regression
	tmp_path = os.path.join(output_path,'a-regression')     # g-regression path
	csv_path = os.path.join(tmp_path,csv_names[i_file])     # path for the specific csv file inside the regression path
	rank_csv = os.path.join(csv_path,'Models_Ranking.csv')  # models ranking file from the g-regression

	# Read the ranking CSV file
	df_a     = pd.read_csv(rank_csv)
	# Append the missing parameters to the dataframe corresponding to the "a" regression
	df_a     = df_a.append(df_g[df_g.Model=='D2'], ignore_index=True)
	df_a     = df_a.append(df_g[df_g.Model=='D4'], ignore_index=True)
	df_a     = df_a.sort_values(by='Model').reset_index(drop=True) # Sort values by 'Model' and re-index after sorting
	models_a = df_a["Model"].tolist()
	k_a      = np.array(df_a["k"])
	R2_a     = np.array(df_a["R2"])

	if (len(R2_f) != len(R2_a)) and (len(R2_f) != len(R2_g)) and (len(R2_a) != len(R2_g)):
		print('Program Stop: The sizes of the input CSV files are not the same')
		sys.exit()

	for i in range(len(R2_f)):
	    if R2_f[i] <= 0.0:
	        R2_f[i] = 0.0
	    if R2_g[i] <= 0.0:
	        R2_g[i] = 0.0
	    if R2_a[i] <= 0.0:
	        R2_a[i] = 0.0
	        
	# Final DataFrame
	df = pd.DataFrame(columns = ['R2-g', 'R2-a','R2-f'])
	df['R2-g'] = R2_g
	df['R2-a'] = R2_a
	df['R2-f'] = R2_f

	# Create a directory for the particular CSV data file
	plt_path = os.path.join(output_path,'models-ranking')
	plt_path = os.path.join(plt_path,csv_names[i_file])
	if not os.path.exists(plt_path): os.makedirs(plt_path)

	# Plot the heatmap

	plotname = 'heatmap_ranking.png'
	if not os.path.isfile(os.path.join(plt_path,plotname)):
		plt.figure()
		xlabels = [r'$ R^{2}_{g} $',r'$ R^{2}_{a} $',r'$ R^{2}_{f} $']
		sns.set(font_scale=1.0)
		sns.heatmap(df, annot=True,
						annot_kws={"size": font_size},
						fmt='.3f',
						linewidth=lwidth,
						xticklabels = xlabels,
						yticklabels = models_g,
						vmin = 0.0,
						vmax = 1.0,
						center = 0.5,
						cmap="YlGnBu")
		# ax=plt.gca()
		# ax.set_xlim(0, 3)
		# ax.set_ylim(0, 16)
		plt.xlim(0,3)
		plt.ylim(0,16)
		plt.tick_params(which='both',direction='out')
		plt.tight_layout()
		plt.savefig(plotname, format=file_format, dpi=dpi)
		os.rename(plotname, os.path.join(plt_path,plotname))

	# Plot the Euclidean

	R2_euclidean = 0.0
	R2_euclidean = [R2_distance(R2_g[i],R2_a[i],R2_f[i]) for i in range(len(R2_g))]

	plotname = 'euclidean_ranking.png'
	if not os.path.isfile(os.path.join(plt_path,plotname)):
		fig = plt.figure()
		x = range(len(models_g))
		plt.scatter(x,R2_euclidean,
					s=80,
					c=palette[1],
					edgecolors='black')
		plt.scatter(x[np.argmin(R2_euclidean)],R2_euclidean[np.argmin(R2_euclidean)],
					s=400,
					c=palette[2],
					marker='*',
					edgecolors='black')
		plt.ylabel(r'$ d(R^{2}_{g},R^{2}_{a},R^{2}_{f}) $', fontsize=font_size)
		# plt.yscale('log')
		plt.ylim(0.0,)
		plt.grid(b=False, which='major', color='#D5DFE1', linestyle='-', linewidth=1)
		plt.xticks(x, models_g)
		plt.tick_params(which='both',direction='out')
		plt.tight_layout()
		plt.savefig(plotname, format=file_format, dpi=dpi)
		os.rename(plotname, os.path.join(plt_path,plotname))