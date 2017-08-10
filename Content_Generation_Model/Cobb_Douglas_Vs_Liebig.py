import csv
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def cobb_douglas_answer(x, A, lambda_0, lambda_1):
    return A * np.power(x[0], lambda_0) * np.power(x[1], lambda_1)

def single_factor_answer(x, A, lambda_0):
    return A * np.power(x, lambda_0)

#data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Monthly_QA_Activity.csv')
data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Weekly_QA_Activity.csv')
csv_data = csv.reader(data_file)

first_row = next(csv_data)
current_site = first_row[0]

question_count = []
answer_count = []
answerer_count = []

question_count.append(int(first_row[2]))
answer_count.append(int(first_row[3]))
answerer_count.append(int(first_row[5]))

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
        
        if len(answer_count) >= 20:
            
            question_parameter, question_covariance = curve_fit(single_factor_answer, question_count, answer_count, bounds=([0, 0],[np.inf, 1.0]))
            answerer_parameter, answerer_covariance = curve_fit(single_factor_answer, answerer_count, answer_count, bounds=([0, 0],[np.inf, 1.0]))
            answer_factors = np.array([question_count, answerer_count])
            cobb_douglas_parameters, cobb_douglas_covariance = curve_fit(cobb_douglas_answer, answer_factors, answer_count, bounds=([0, 0, 0],[np.inf, 1.0, 1.0]))


            print (current_site, np.linalg.norm((answer_count-cobb_douglas_answer(answer_factors, *cobb_douglas_parameters))/len(answer_count) ))
            
            #print (current_site,
            #'Cobb-Douglas:', np.linalg.norm(answer_count-cobb_douglas_answer(answer_factors, *cobb_douglas_parameters)),
            #'Liebig:', np.linalg.norm(answer_count-np.minimum(single_factor_answer(question_count, *question_parameter), single_factor_answer(answerer_count, *answerer_parameter))),
            #'Only Question:', np.linalg.norm(answer_count-single_factor_answer(question_count, *question_parameter)),
            #'Only Answerer:', np.linalg.norm(answer_count-single_factor_answer(answerer_count, *answerer_parameter)))


            #myFormattedList = [ '%.2f' % elem for elem in abs(answer_count-cobb_douglas_answer(answer_factors, *cobb_douglas_parameters))/answer_count]
            #print myFormattedList
    

        current_site = row[0]
        
        question_count[:] = []
        answer_count[:] = []
        answerer_count[:] = []
        
        question_count.append(int(row[2]))
        answer_count.append(int(row[3]))
        answerer_count.append(int(row[5]))
        


