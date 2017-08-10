import csv
import matplotlib.pyplot as plt
import numpy as np, pandas as pd; np.random.seed(0)
import seaborn as sns; sns.set(style="white", color_codes=True)

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Monthly_QAC_Activity.csv')
csv_data = csv.reader(data_file)

site_size = {}
current_site = 'academia'
answerer_count = 0
month_count = 0

for row in csv_data:
    if(row[0] == current_site):
        answerer_count = answerer_count + int(row[6])
        month_count = month_count+ 1
    else:
        site_size[current_site] = float(answerer_count)/float(month_count)
        current_site = row[0]

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Parameters_Cobb_Douglas.csv')
csv_data = csv.reader(data_file)

lambda_0 = []
lambda_1 = []
size = []

for row in csv_data:
    if(0.01 < float(row[4]) <0.99 and 0.01 < float(row[5]) <0.99):
        lambda_0.append(float(row[4]))
        lambda_1.append(float(row[5]))
        size.append(site_size[row[0]])

lambda_0 = np.array(lambda_0)
lambda_1 = np.array(lambda_1)
size = np.array(size)
                    
ax = sns.jointplot(x = size, y = lambda_1, kind = 'reg')
ax.set_axis_labels(xlabel = 'Avg. # of users (per month)', ylabel = 'lamda_1')
plt.show()
