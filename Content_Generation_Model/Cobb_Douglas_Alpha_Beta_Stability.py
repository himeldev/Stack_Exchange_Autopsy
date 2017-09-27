import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import math

def cobb_douglas_answer(x, A, lambda_0, lambda_1):
    return A * np.power(x[0], lambda_0) * np.power(x[1], lambda_1)

def cobb_douglas_question(x, A, lambda_0):
    return A * np.power(x, lambda_0)

figure_count = 1

site_month_aggregate_data = {}

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Site_Monthly_Stats.csv')
csv_data = csv.reader(data_file)

for row in csv_data:

    if row[0] not in site_month_aggregate_data:
        site_month_aggregate_data[row[0]] = {}

    if int(row[1]) not in site_month_aggregate_data[row[0]]:
        site_month_aggregate_data[row[0]][int(row[1])] = []
        
    site_month_aggregate_data[row[0]][int(row[1])].append(int(row[2]))
    site_month_aggregate_data[row[0]][int(row[1])].append(int(row[3]))
    site_month_aggregate_data[row[0]][int(row[1])].append(int(row[6]))
    site_month_aggregate_data[row[0]][int(row[1])].append(int(row[7]))       
        
#print site_month_aggregate_data


site_month_answerer_data = {}

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Contribution_of_Top_Answerers.csv')
csv_data = csv.reader(data_file)

for row in csv_data:

    if row[0] not in site_month_answerer_data:
        site_month_answerer_data[row[0]] = {}

    if int(row[1]) not in site_month_answerer_data[row[0]]:
        site_month_answerer_data[row[0]][int(row[1])] = []
        
    site_month_answerer_data[row[0]][int(row[1])].append(int(row[3])) 
        
#text_file = open("Output.txt", "w")
#text_file.write("%s" % site_month_answerer_data)
#text_file.close()


#Calculate alpha beta

question_count = []
answer_count = []
asker_count = []
answerer_count = []

month_answerer_data = []

for site in sorted(site_month_aggregate_data.keys()):
    
    for month in sorted(site_month_aggregate_data[site].keys()):
        
        question_count.append(site_month_aggregate_data[site][month][0])
        answer_count.append(site_month_aggregate_data[site][month][1])
        asker_count.append(site_month_aggregate_data[site][month][2])
        answerer_count.append(site_month_aggregate_data[site][month][3])     
        month_answerer_data.append(site_month_answerer_data[site][month])

    if len(question_count) >= 10:

        optimal_parameters_question, covariance_of_parameters_question = curve_fit(cobb_douglas_question, asker_count, question_count)
        answer_factors = np.array([question_count, answerer_count])
        optimal_parameters_answer, covariance_of_parameters_answer = curve_fit(cobb_douglas_answer, answer_factors, answer_count, bounds=([0, 0, 0],[np.inf, 1.0, 1.0]))

        x = []
        y1 = []
        y2 = []
        for ab_threshold in [0, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.175, 0.2, 0.225, 0.25, 0.275, 0.3]:
            answer_count_test_top = []
            answer_count_test_bottom = []
            answerer_count_test = []
            
            for i, answerer_data in enumerate(month_answerer_data):
                top_user_contribution = 0
                bottom_user_contribution = 0
                
                for N in range(0, int(ab_threshold*len(answerer_data))):
                    top_user_contribution = top_user_contribution+answerer_data[N]
                for N in range(len(answerer_data)-int(ab_threshold*len(answerer_data)), len(answerer_data)):
                    bottom_user_contribution = bottom_user_contribution+answerer_data[N]
                    
                answerer_count_test.append(answerer_count[i] - int(ab_threshold*len(answerer_data)))
                answer_count_test_top.append(answer_count[i] - top_user_contribution)
                answer_count_test_bottom.append(answer_count[i] - bottom_user_contribution)

            answer_factors_test_top = np.array([question_count, answerer_count_test])
            answer_percent_error_top = np.mean(abs(answer_count_test_top-cobb_douglas_answer(answer_factors_test_top, *optimal_parameters_answer))/answer_count_test_top)*100
            answer_factors_test_bottom = np.array([question_count, answerer_count_test])
            answer_percent_error_bottom = np.mean(abs(answer_count_test_bottom-cobb_douglas_answer(answer_factors_test_bottom, *optimal_parameters_answer))/answer_count_test_bottom)*100
            x.append(ab_threshold)
            y1.append(answer_percent_error_top)
            y2.append(answer_percent_error_bottom)
            
        fig = plt.figure(figure_count)
        figure_count += 1
        ax = fig.add_subplot(111)
        ax.plot(x, y1, 'r')
        ax.plot(x, y2, 'b')
        ax.set_xlabel('Percentage Drop in Answerers')
        ax.set_ylabel('Error Percentage in Answer Prediction')
        fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Cobb-Douglas/AB/Month/Answerer/'+site)
        plt.close(fig)

        print site+', '+str(y1[2])
        

    question_count[:] = []
    answer_count[:] = []
    asker_count[:] = []
    answerer_count[:] = []
    month_answerer_data[:] = []

        
        
        
        
