import csv
import math
import copy
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

figure_count = 1

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Death_Answerer.csv')
csv_data = csv.reader(data_file)

first_row = next(csv_data)
current_site = first_row[0]
current_user = int(first_row[1])

global_age_list = []
global_contribution_list = []

global_norm_age_list = []
global_norm_contribution_list = []

site_age_list = []
site_contribution_list = []

current_age = 1
total_contribution = int(first_row[3])

for row in csv_data:

    if row[0] == current_site and int(row[1]) == current_user:
        current_age += 1
        total_contribution += int(row[3])
        
    elif row[0] == current_site and int(row[1]) <> current_user:
        site_age_list.append(current_age)
        site_contribution_list.append(float(total_contribution)/current_age)

        current_user = int(row[1])
        current_age = 1
        total_contribution = int(row[3])
        
    else:
        x = []
        y = []
        err = []
        for age in range(1, max(site_age_list)+1):
            data = []
            for i, contribution in enumerate(site_contribution_list):
                if site_age_list[i] == age:
                    data.append(contribution)
            #At least two users for computing mean and SEM
            if len(data) >= 2:
                x.append(age)
                data = np.array(data)
                y.append(np.mean(data))
                err.append(np.std(data)/math.sqrt(len(data)))

        x2 = []
        y2 = []
        err2 = []
        for contribution in range(int(min(site_contribution_list)), int(max(site_contribution_list)+1), 5):
            data = []
            for i, age in enumerate(site_age_list):
                if site_contribution_list[i] >= contribution and site_contribution_list[i] < contribution+5:
                    data.append(age)
            #At least two users for computing mean and SEM
            if len(data) >= 5:
                x2.append(contribution)
                data = np.array(data)
                y2.append(np.mean(data))
                err2.append(np.std(data)/math.sqrt(len(data)))

        #print 'X:', x
        #print 'Y:', y
        #print 'E:', err
            
        fig = plt.figure(figure_count)
        figure_count += 1
        ax = fig.add_subplot(111)
        ax.errorbar(x, y, yerr = err, capsize=3, fmt='--o')
        ax.set_xlabel('Active Age')
        ax.set_ylabel('Contribution')
        fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test2/'+current_site)
        plt.close(fig)

        fig = plt.figure(figure_count)
        figure_count += 1
        ax = fig.add_subplot(111)
        ax.errorbar(x2, y2, yerr = err2, capsize=3, fmt='--o')
        ax.set_xticks(x2)
        ax.set_xticklabels([str(a)+'-'+str(a+5) for a in x2])
        ax.set_xlabel('Contribution')
        ax.set_ylabel('Active Age')
        fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test3/'+current_site)
        plt.close(fig)
        
        current_site = row[0]
        current_user = int(row[1])
        current_age = 1
        total_contribution = int(row[3])

        global_age_list.extend(copy.deepcopy(site_age_list))
        global_contribution_list.extend(copy.deepcopy(site_contribution_list))

        global_norm_age_list.extend(copy.deepcopy([float(a)*100/max(site_age_list) for a in site_age_list]))
        global_norm_contribution_list.extend(copy.deepcopy([float(a)*100/max(site_contribution_list) for a in site_contribution_list]))

        site_age_list [:] = []
        site_contribution_list[:] = []

#text_file = open("output.txt", "w")
#text_file.write("%s\n\nABCD%s\n\nABCD%s\n\nABCD%s" % (global_age_list, global_contribution_list, global_norm_age_list, global_norm_contribution_list))
#text_file.close()

print max(global_norm_age_list)
print max(global_norm_contribution_list)
'''
x2 = []
y2 = []
err2 = []
for contribution in range(int(min(global_contribution_list)), int(max(global_contribution_list)+1), 5):
    data = []
    for i, age in enumerate(global_age_list):
        if global_contribution_list[i] >= contribution and global_contribution_list[i] < contribution+5:
            data.append(age)
    #At least two users for computing mean and SEM
    if len(data) >= 5:
        x2.append(contribution)
        data = np.array(data)
        y2.append(np.mean(data))
        err2.append(np.std(data)/math.sqrt(len(data)))

fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
ax.errorbar(x2, y2, yerr = err2, capsize=3, fmt='--o')
ax.set_xticks(x2)
ax.set_xticklabels([str(a) for a in x2])
ax.set_xlabel('Contribution')
ax.set_ylabel('Active Age')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test3/'+'111')
plt.close(fig)


x2 = []
y2 = []
err2 = []
for contribution in range(int(min(global_norm_contribution_list)), int(max(global_norm_contribution_list)+1), 5):
    data = []
    for i, age in enumerate(global_age_list):
        if global_norm_contribution_list[i] >= contribution and global_norm_contribution_list[i] < contribution+5:
            data.append(age)
    #At least two users for computing mean and SEM
    if len(data) >= 5:
        x2.append(contribution)
        data = np.array(data)
        y2.append(np.mean(data))
        err2.append(np.std(data)/math.sqrt(len(data)))

fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
ax.errorbar(x2, y2, yerr = err2, capsize=3, fmt='--o')
ax.set_xticks(x2)
ax.set_xticklabels([str(a) for a in x2])
ax.set_xlabel('Contribution')
ax.set_ylabel('Active Age')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test3/'+'112')
plt.close(fig)

x2 = []
y2 = []
err2 = []
for contribution in range(int(min(global_norm_contribution_list)), int(max(global_norm_contribution_list)+1), 5):
    data = []
    for i, age in enumerate(global_norm_age_list):
        if global_norm_contribution_list[i] >= contribution and global_norm_contribution_list[i] < contribution+5:
            data.append(age)
    #At least two users for computing mean and SEM
    if len(data) >= 5:
        x2.append(contribution)
        data = np.array(data)
        y2.append(np.mean(data))
        err2.append(np.std(data)/math.sqrt(len(data)))

fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
ax.errorbar(x2, y2, yerr = err2, capsize=3, fmt='--o')
ax.set_xticks(x2)
ax.set_xticklabels([str(a) for a in x2])
ax.set_xlabel('Contribution')
ax.set_ylabel('Active Age')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test3/'+'113')
plt.close(fig)  
        '''

x2 = []
y2 = []
err2 = []
for contribution in range(int(min(global_contribution_list)), int(max(global_contribution_list)+1), 5):
    data = []
    for i, age in enumerate(global_norm_age_list):
        if global_contribution_list[i] >= contribution and global_contribution_list[i] < contribution+5:
            data.append(age)
    #At least two users for computing mean and SEM
    if len(data) >= 5:
        x2.append(contribution)
        data = np.array(data)
        y2.append(np.mean(data))
        err2.append(np.std(data)/math.sqrt(len(data)))

fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
ax.errorbar(x2, y2, yerr = err2, capsize=3, fmt='--o')
ax.set_xticks(x2)
ax.set_xticklabels([str(a) for a in x2])
ax.set_xlabel('Contribution')
ax.set_ylabel('Active Age')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test3/'+'114')
plt.close(fig)  

