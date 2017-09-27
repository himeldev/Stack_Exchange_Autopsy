import csv
import math
import copy
import random
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Cobb_Douglas_Parameters.csv')
csv_data = csv.reader(data_file)

site_beta_1 = {}
site_lambda_1 = {}
site_beta_2 = {}
site_lambda_2 = {}
site_lambda_3 = {}

for row in csv_data:
    site_beta_1[row[0]] = float(row[1])
    site_lambda_1[row[0]] = float(row[2])
    site_beta_2[row[0]] = float(row[3])
    site_lambda_2[row[0]] = float(row[4])
    site_lambda_3[row[0]] = float(row[5])


data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/site_beta_stats.csv')
csv_data = csv.reader(data_file)

site_list = []
x = []
y = []
z1 = []
z2 = []
z3 = []
z4 = []
z5 = []

for row in csv_data:
    if row[0] in site_beta_1:
        site_list.append(row[0])
        x.append(float(row[2]))
        y.append(float(row[1]))
        z1.append(site_beta_1[row[0]])
        z2.append(site_lambda_1[row[0]])
        z3.append(site_beta_2[row[0]])
        z4.append(site_lambda_2[row[0]])
        z5.append(site_lambda_3[row[0]])

figure_count = 1


fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
scatter_plot = ax.scatter(x, y, c = z1, s = 40)
scatter_colorbar = plt.colorbar(scatter_plot)
ax.plot(y, y)
ax.set_xlabel('beta_min')
ax.set_ylabel('beta_max')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test/'+'Beta_Question')
plt.close(fig)

fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
scatter_plot = ax.scatter(x, y, c = z2, s = 40)
scatter_colorbar = plt.colorbar(scatter_plot)
ax.plot(y, y)
ax.set_xlabel('beta_min')
ax.set_ylabel('beta_max')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test/'+'Lambda_Question')
plt.close(fig)


fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
scatter_plot = ax.scatter(x, y, c = z3, s = 40)
scatter_colorbar = plt.colorbar(scatter_plot)
ax.plot(y, y)
ax.set_xlabel('beta_min')
ax.set_ylabel('beta_max')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test/'+'Beta_Answer')
plt.close(fig)


fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
scatter_plot = ax.scatter(x, y, c = z4, s = 40)
scatter_colorbar = plt.colorbar(scatter_plot)
ax.plot(y, y)
ax.set_xlabel('beta_min')
ax.set_ylabel('beta_max')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test/'+'Lambda_1_Answer')
plt.close(fig)

fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
scatter_plot = ax.scatter(x, y, c = z5, s = 40)
scatter_colorbar = plt.colorbar(scatter_plot)
ax.plot(y, y)
ax.set_xlabel('beta_min')
ax.set_ylabel('beta_max')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test/'+'Lambda_2_Answer')
plt.close(fig)


        

        

        

        

        






        
        
