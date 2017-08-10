import numpy
from sklearn import mixture
import csv
import matplotlib.pyplot as plt
import numpy as np, pandas as pd; np.random.seed(0)
import seaborn as sns; sns.set(style="white", color_codes=True)

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Monthly_User_Activity.csv')
csv_data = csv.reader(data_file)

current_site = 'academia'
question_count = 0;

a = np.array([0, 0, 0])

for row in csv_data:
    if(row[0] == current_site):
        b = np.array([float(row[3]), float(row[4]), float(row[5])])
        c = np.hstack((a, np.atleast_2d(b).T))
    else:
        dpgmm = mixture.DPGMM(n_components = 3)
        dpgmm.fit(c)
        clusters = dpgmm.predict(c)
        print clusters
        a = np.array([[0, 0, 0]])
        current_site = row[0]
