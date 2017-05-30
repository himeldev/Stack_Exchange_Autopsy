import csv
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def cobb_douglas_answer(x, A, lambda_0, lambda_1):
    return A * np.power(x[0], lambda_0) * np.power(x[1], lambda_1)

def cobb_douglas_question(x, A, lambda_0):
    return A * np.power(x, lambda_0)

data_file = open('Monthly_QA_Activity.csv')
csv_data = csv.reader(data_file)

question_count = []
answer_count = []
asker_count = []
answerer_count = []


first_row = next(csv_data)
current_site = first_row[0]

site_count = 1

for row in csv_data:

    #If current site, add data to model
    
    if row[0] == current_site:
        question_count.append(int(row[2]))
        answer_count.append(int(row[3]))
        asker_count.append(int(row[4]))
        answerer_count.append(int(row[5]))
        
    #If new site, plot current model and reassign the required variables
        
    else:

        #One in ten rule: at least 20 points for a 2 variable regression
        if len(question_count) >= 20:
            
            answer_factors = np.array([question_count, answerer_count])
            popt, pcov = curve_fit(cobb_douglas_question, asker_count, question_count)
            popt_2, pcov_2 = curve_fit(cobb_douglas_answer, answer_factors, answer_count, bounds=([0, 0, 0],[np.inf, 1.0, 1.0]))
            
            print current_site, "[ A:", popt[0], "lambda_1:", popt[1], "] [A:", popt_2[0], "lambda_1:", popt_2[1], "lambda_2:", popt_2[2], "]"

            fig = plt.figure(site_count)
            site_count += 1
            ax = fig.add_subplot(111)
            asker_count_sorted = sorted(asker_count)
            ax.plot(asker_count_sorted, cobb_douglas_question(asker_count_sorted, *popt), c='b')
            ax.scatter(asker_count,  question_count, c='r', marker='o')
            ax.set_xlabel('# of Askers')
            ax.set_ylabel('# of Questions')
            fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Growth_Model/Figures/Month/question_growth_'+row[0])
            plt.close(fig)
            
            fig = plt.figure(site_count)
            site_count += 1
            ax = fig.add_subplot(111)
            scatter_1 = ax.scatter(answer_factors[0], answer_factors[1], c = cobb_douglas_answer(answer_factors, *popt_2), s = 90, marker = '_', lw = 2.5)
            scatter_2 = ax.scatter(answer_factors[0], answer_factors[1],  c = answer_count, s = 90, marker = '|', lw = 2.5)
            colorbar_1 = plt.colorbar(scatter_1)
            colorbar_1.set_label('# of Answers')
            ax.set_xlabel('# of Questions')
            ax.set_ylabel('# of Answerers')
            fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Growth_Model/Figures/Month/answer_growth_'+row[0])
            plt.close(fig)

        current_site = row[0]
        
        question_count[:] = []
        answer_count[:] = []
        asker_count[:] = []
        answerer_count[:] = []
        
        question_count.append(int(row[2]))
        answer_count.append(int(row[3]))
        asker_count.append(int(row[5]))
        answerer_count.append(int(row[5]))
        


