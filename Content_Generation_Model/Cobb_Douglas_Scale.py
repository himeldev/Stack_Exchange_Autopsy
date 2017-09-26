import csv
import math
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def cobb_douglas_answer(x, A, lambda_0, lambda_1):
    return A * np.power(x[0], lambda_0) * np.power(x[1], lambda_1)

def cobb_douglas_question(x, A, lambda_0):
    return A * np.power(x, lambda_0)

figure_count = 1

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Site_Monthly_Stats.csv')
csv_data = csv.reader(data_file)


first_row = next(csv_data)
current_site = first_row[0]

month_no_of_questions = []
month_no_of_answers = []
month_no_of_askers = []
month_no_of_answerers = []
month_no_of_users = []

month_no_of_questions.append(int(first_row[2]))
month_no_of_answers.append(int(first_row[3]))
month_no_of_askers.append(int(first_row[6]))
month_no_of_answerers.append(int(first_row[7]))
month_no_of_users.append(int(first_row[14]))

for row in csv_data:

    if row[0] == current_site:
        month_no_of_questions.append(int(row[2]))
        month_no_of_answers.append(int(row[3]))
        month_no_of_askers.append(int(row[6]))
        month_no_of_answerers.append(int(row[7]))
        month_no_of_users.append(int(row[14]))
        
    else:
        month_no_of_questions = month_no_of_questions[:-1]
        month_no_of_answers = month_no_of_answers[:-1]
        month_no_of_askers = month_no_of_askers[:-1]
        month_no_of_answerers = month_no_of_answerers[:-1]
        month_no_of_users = month_no_of_users[:-1]

        if len(month_no_of_questions) >= 24:

            optimal_parameters_question, covariance_of_parameters_question = curve_fit(cobb_douglas_question, month_no_of_askers, month_no_of_questions)
            answer_factors = np.array([month_no_of_questions, month_no_of_answerers])
            optimal_parameters_answer, covariance_of_parameters_answer = curve_fit(cobb_douglas_answer, answer_factors, month_no_of_answers, bounds=([0, 0, 0],[np.inf, 1.0, 1.0]))

            month_fraction_of_askers = [float(a)/b for a,b in zip(month_no_of_askers, month_no_of_users)]
            month_fraction_of_answerers = [float(a)/b for a,b in zip(month_no_of_answerers, month_no_of_users)]

            month_no_of_users_sorted = sorted(month_no_of_users)
            
            month_potential_no_of_askers =  [x*sum(month_fraction_of_askers)/float(len(month_fraction_of_askers)) for x in month_no_of_users_sorted]
            month_potential_no_of_answerers =  [x*sum(month_fraction_of_answerers)/float(len(month_fraction_of_answerers)) for x in month_no_of_users_sorted]

            month_potential_no_of_questions = cobb_douglas_question(month_potential_no_of_askers, *optimal_parameters_question)
            month_potential_no_of_answers = cobb_douglas_answer(np.array([month_potential_no_of_questions, month_potential_no_of_answerers]), *optimal_parameters_answer)

            fig = plt.figure(figure_count)
            figure_count += 1
            ax = fig.add_subplot(111)
            ax.scatter(month_no_of_users, [float(a)/b for a,b in zip(month_no_of_answers, month_no_of_questions)], color = 'black')
            fit = np.polyfit(month_no_of_users, [float(a)/b for a,b in zip(month_no_of_answers, month_no_of_questions)], 1)
            fit_function = np.poly1d(fit)
            ax.plot(month_no_of_users, fit_function(month_no_of_users), 'b', label = 'Linear Regression')
            ax.plot(month_no_of_users_sorted, [float(a)/b for a,b in zip(month_potential_no_of_answers, month_potential_no_of_questions)],'r', label = 'Economic Model')
            ax.legend(loc='upper right')
            ax.set_xlabel('No. of Users (U)')
            ax.set_ylabel('Avg. No. of Answers per Question (N_a/N_q)')
            fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Cobb-Douglas/Scale/'+current_site)
            plt.close(fig)


        current_site = row[0]
        
        month_no_of_questions[:] = []
        month_no_of_answers[:] = []
        month_no_of_askers[:] = []
        month_no_of_answerers[:] = []
        month_no_of_users[:] = []

        month_no_of_questions.append(int(row[2]))
        month_no_of_answers.append(int(row[3]))
        month_no_of_askers.append(int(row[6]))
        month_no_of_answerers.append(int(row[7]))
        month_no_of_users.append(int(row[14]))


