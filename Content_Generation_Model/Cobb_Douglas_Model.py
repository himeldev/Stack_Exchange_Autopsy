import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def cobb_douglas_answer(x, A, lambda_0, lambda_1):
    return A * np.power(x[0], lambda_0) * np.power(x[1], lambda_1)

def cobb_douglas_question(x, A, lambda_0):
    return A * np.power(x, lambda_0)

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Monthly_QA_Activity.csv')
csv_data = csv.reader(data_file)

first_row = next(csv_data)
current_site = first_row[0]

question_count = []
answer_count = []
asker_count = []
answerer_count = []

question_count.append(int(first_row[2]))
answer_count.append(int(first_row[3]))
asker_count.append(int(first_row[4]))
answerer_count.append(int(first_row[5]))

figure_count = 1

for row in csv_data:

    #If current site, add data for model construction
    
    if row[0] == current_site:

        question_count.append(int(row[2]))
        answer_count.append(int(row[3]))
        asker_count.append(int(row[4]))
        answerer_count.append(int(row[5]))
        
    #If new site, construct and plot current model, and reassign the data variables
        
    else:

        #Delete the last (broken/partial) data point
        
        question_count = question_count[:-1]
        answer_count = answer_count[:-1]
        asker_count = asker_count[:-1]
        answerer_count = answerer_count[:-1]

        #One in ten rule: at least 20 points for a 2 variable regression
        
        if len(answer_count) >= 10:
            
            optimal_parameters_question, covariance_of_parameters_question = curve_fit(cobb_douglas_question, asker_count, question_count)
            answer_factors = np.array([question_count, answerer_count])
            optimal_parameters_answer, covariance_of_parameters_answer = curve_fit(cobb_douglas_answer, answer_factors, answer_count, bounds=([0, 0, 0],[np.inf, 1.0, 1.0]))
            
            print '%s, %.6f, %.6f, %.6f, %.6f , %.6f' % (current_site, optimal_parameters_question[0], optimal_parameters_question[1], optimal_parameters_answer[0], optimal_parameters_answer[1], optimal_parameters_answer[2])

            fig = plt.figure(figure_count)
            figure_count += 1
            ax = fig.add_subplot(111)
            asker_count_sorted = sorted(asker_count)
            ax.plot(asker_count_sorted, cobb_douglas_question(asker_count_sorted, *optimal_parameters_question), c='b')
            ax.scatter(asker_count,  question_count, c='r', marker='o')
            ax.set_xlabel('# of Askers')
            ax.set_ylabel('# of Questions')
            fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Cobb-Douglas/Month/Question/'+current_site)
            plt.close(fig)
            
            fig = plt.figure(figure_count)
            figure_count += 1
            ax = fig.add_subplot(111)
            scatter_model = ax.scatter(answer_factors[0], answer_factors[1], c = cobb_douglas_answer(answer_factors, *optimal_parameters_answer), s = 90, marker = '_', lw = 2.5)
            scatter_data = ax.scatter(answer_factors[0], answer_factors[1],  c = answer_count, s = 90, marker = '|', lw = 2.5)
            if max(cobb_douglas_answer(answer_factors, *optimal_parameters_answer)) > max(answer_count):
                scatter_colorbar = plt.colorbar(scatter_model)
            else:
                scatter_colorbar = plt.colorbar(scatter_data)          
            scatter_colorbar.set_label('# of Answers')
            ax.set_xlabel('# of Questions')
            ax.set_ylabel('# of Answerers')
            fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Cobb-Douglas/Month/Answer/'+current_site)
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



