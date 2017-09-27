import csv
import math
import copy
import random
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Site_Monthly_Stats.csv')
csv_data = csv.reader(data_file)

site_avg_no_of_questions = {}
site_avg_no_of_answers = {}
site_avg_no_of_askers = {}
site_avg_no_of_answerers = {}
site_avg_no_of_users = {}

site_avg_fraction_of_answered_question = {}
site_avg_fraction_of_questions_with_accepted_answer = {}

first_row = next(csv_data)
current_site = first_row[0]

month_no_of_questions = []
month_no_of_answers = []
month_no_of_askers = []
month_no_of_answerers = []
month_no_of_users = []

month_fraction_of_answered_question = []
month_fraction_of_questions_with_accepted_answer = []

month_no_of_questions.append(int(first_row[2]))
month_no_of_answers.append(int(first_row[3]))
month_no_of_askers.append(int(first_row[6]))
month_no_of_answerers.append(int(first_row[7]))
month_no_of_users.append(int(first_row[14]))

month_fraction_of_answered_question.append(float(first_row[4])/float(first_row[2]))
month_fraction_of_questions_with_accepted_answer.append(float(first_row[5])/float(first_row[2]))

for row in csv_data:

    if row[0] == current_site:
        month_no_of_questions.append(int(row[2]))
        month_no_of_answers.append(int(row[3]))
        month_no_of_askers.append(int(row[6]))
        month_no_of_answerers.append(int(row[7]))
        month_no_of_users.append(int(row[14]))

        month_fraction_of_answered_question.append(float(row[4])/float(row[2]))
        month_fraction_of_questions_with_accepted_answer.append(float(row[5])/float(row[2]))
        
    else:

        if len(month_no_of_questions) >= 10:
            month_no_of_questions = month_no_of_questions[:-1]
            month_no_of_answers = month_no_of_answers[:-1]
            month_no_of_askers = month_no_of_askers[:-1]
            month_no_of_answerers = month_no_of_answerers[:-1]
            month_no_of_users = month_no_of_users[:-1]

            month_fraction_of_answered_question[:-1]
            month_fraction_of_questions_with_accepted_answer[:-1]   

            site_avg_no_of_questions[current_site] = sum(month_no_of_questions) / float(len(month_no_of_questions))
            site_avg_no_of_answers[current_site] = sum(month_no_of_answers) / float(len(month_no_of_answers))
            site_avg_no_of_askers[current_site] = sum(month_no_of_askers) / float(len(month_no_of_askers))
            site_avg_no_of_answerers[current_site] = sum(month_no_of_answerers) / float(len(month_no_of_answerers))
            site_avg_no_of_users[current_site] = sum(month_no_of_users) / float(len(month_no_of_users))

            site_avg_fraction_of_answered_question[current_site] = sum(month_fraction_of_answered_question) / float(len(month_fraction_of_answered_question))
            site_avg_fraction_of_questions_with_accepted_answer[current_site] = sum(month_fraction_of_questions_with_accepted_answer) / float(len(month_fraction_of_questions_with_accepted_answer))

        current_site = row[0]
        
        month_no_of_questions[:] = []
        month_no_of_answers[:] = []
        month_no_of_askers[:] = []
        month_no_of_answerers[:] = []
        month_no_of_users[:] = []

        month_fraction_of_answered_question[:] = []
        month_fraction_of_questions_with_accepted_answer[:] = []

        month_no_of_questions.append(int(row[2]))
        month_no_of_answers.append(int(row[3]))
        month_no_of_askers.append(int(row[6]))
        month_no_of_answerers.append(int(row[7]))
        month_no_of_users.append(int(row[14]))

        month_fraction_of_answered_question.append(float(row[4])/float(row[2]))
        month_fraction_of_questions_with_accepted_answer.append(float(row[5])/float(row[2]))


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
z6 = []
z7 = []

for row in csv_data:
    if row[0] in site_avg_no_of_questions:
        site_list.append(row[0])
        x.append(float(row[2]))
        y.append(float(row[1]))
        z1.append(site_avg_no_of_questions[row[0]])
        z2.append(site_avg_no_of_answers[row[0]])
        z3.append(site_avg_no_of_askers[row[0]])
        z4.append(site_avg_no_of_answerers[row[0]])
        z5.append(site_avg_no_of_users[row[0]])
        
        z6.append(site_avg_fraction_of_answered_question[row[0]])       
        z7.append(site_avg_fraction_of_questions_with_accepted_answer[row[0]])

figure_count = 1

fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
scatter_plot = ax.scatter(x, y, c = z5, s = 50)
scatter_colorbar = plt.colorbar(scatter_plot)
ax.plot(y, y)
ax.set_xlabel('beta_min')
ax.set_ylabel('beta_max')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test/'+'User_Count')
plt.close(fig)

fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
scatter_plot = ax.scatter(x, y, c = z1, s = 50)
scatter_colorbar = plt.colorbar(scatter_plot)
ax.plot(y, y)
ax.set_xlabel('beta_min')
ax.set_ylabel('beta_max')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test/'+'Question_Count')
plt.close(fig)

fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
scatter_plot = ax.scatter(x, y, c = z2, s = 50)
scatter_colorbar = plt.colorbar(scatter_plot)
ax.plot(y, y)
ax.set_xlabel('beta_min')
ax.set_ylabel('beta_max')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test/'+'Answer_Count')
plt.close(fig)


fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
scatter_plot = ax.scatter(x, y, c = z3, s = 50)
scatter_colorbar = plt.colorbar(scatter_plot)
ax.plot(y, y)
ax.set_xlabel('beta_min')
ax.set_ylabel('beta_max')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test/'+'Asker_Count')
plt.close(fig)


fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
scatter_plot = ax.scatter(x, y, c = z4, s = 50)
scatter_colorbar = plt.colorbar(scatter_plot)
ax.plot(y, y)
ax.set_xlabel('beta_min')
ax.set_ylabel('beta_max')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test/'+'Answerer_Count')
plt.close(fig)

fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
scatter_plot = ax.scatter(x, y, c = z6, s = 50)
scatter_colorbar = plt.colorbar(scatter_plot)
ax.plot(y, y)
ax.set_xlabel('beta_min')
ax.set_ylabel('beta_max')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test/'+'Fraction_of_Answered_Questions')
plt.close(fig)

fig = plt.figure(figure_count)
figure_count += 1
ax = fig.add_subplot(111)
scatter_plot = ax.scatter(x, y, c = z7, s = 50)
scatter_colorbar = plt.colorbar(scatter_plot)
ax.plot(y, y)
ax.set_xlabel('beta_min')
ax.set_ylabel('beta_max')
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Test/'+'Fraction_Of_Questions_with_Accepted_Answer')
plt.close(fig)

        

        

        

        

        






        
        
