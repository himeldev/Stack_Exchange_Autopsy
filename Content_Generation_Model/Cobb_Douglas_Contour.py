import csv
import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def cobb_douglas_answer(x, A, lambda_0, lambda_1):
    return A * np.power(x[0], lambda_0) * np.power(x[1], lambda_1)

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Monthly_QA_Activity.csv')
csv_data = csv.reader(data_file)

first_row = next(csv_data)
current_site = first_row[0]

question_count = []
answer_count = []
answerer_count = []

question_count.append(int(first_row[2]))
answer_count.append(int(first_row[3]))
answerer_count.append(int(first_row[5]))

figure_count = 1

for row in csv_data:

    #If current site, add data for model construction
    
    if row[0] == current_site:

        question_count.append(int(row[2]))
        answer_count.append(int(row[3]))
        answerer_count.append(int(row[5]))
        
    #If new site, construct and plot current model, and reassign the data variables
        
    else:

        #Delete the last (broken/partial) data point
        
        question_count = question_count[:-1]
        answer_count = answer_count[:-1]
        answerer_count = answerer_count[:-1]

        #One in ten rule: at least 20 points for a 2 variable regression
        
        if len(answer_count) >= 10:
            
            answer_factors = np.array([question_count, answerer_count])
            optimal_parameters_answer, covariance_of_parameters_answer = curve_fit(cobb_douglas_answer, answer_factors, answer_count, bounds=([0, 0, 0],[np.inf, 1.0, 1.0]))
            
            print current_site, optimal_parameters_answer[0], optimal_parameters_answer[1], optimal_parameters_answer[2]
            
            fig = plt.figure(figure_count)
            figure_count += 1
            ax = fig.add_subplot(111)

            # Set up a regular grid of interpolation points
            xi, yi = np.linspace(min(answer_factors[0]), max(answer_factors[0]), 100), np.linspace(min(answer_factors[1]), max(answer_factors[1]), 100)
            xi, yi = np.meshgrid(xi, yi)

            zi = cobb_douglas_answer(np.array([xi, yi]), *optimal_parameters_answer)

            #print zi

            ax.imshow(zi, vmin=min(answer_count), vmax=max(answer_count), origin='lower', aspect="auto",
                       extent=[min(answer_factors[0]), max(answer_factors[0]), min(answer_factors[1]), max(answer_factors[1])])
            ax.scatter(answer_factors[0], answer_factors[1], c=answer_count)
            #ax.colorbar()

            ax.set_xlabel('# of Questions')
            ax.set_ylabel('# of Answerers')
            fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Cobb-Douglas/Month/Contour/Answer/'+current_site)
            plt.close(fig)

        current_site = row[0]
        
        question_count[:] = []
        answer_count[:] = []
        answerer_count[:] = []
        
        question_count.append(int(row[2]))
        answer_count.append(int(row[3]))
        answerer_count.append(int(row[5]))



