import csv
import math
import copy
import random
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

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
        
#text_file = open("site_month_aggregate_data.txt", "w")
#text_file.write("%s" % site_month_aggregate_data)
#text_file.close()

site_month_answerer_data = {}

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Contribution_of_Top_Answerers.csv')
csv_data = csv.reader(data_file)

for row in csv_data:

    if row[0] not in site_month_answerer_data:
        site_month_answerer_data[row[0]] = {}

    if int(row[1]) not in site_month_answerer_data[row[0]]:
        site_month_answerer_data[row[0]][int(row[1])] = []
        
    site_month_answerer_data[row[0]][int(row[1])].append(int(row[3])) 
        
#text_file = open("site_month_answerer_data.txt", "w")
#text_file.write("%s" % site_month_answerer_data)
#text_file.close()

#Calculate beta_max, beta_min

site_list = []
beta_max = []
beta_min = []

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

    question_count = question_count[:-1]
    answer_count = answer_count[:-1]
    asker_count = asker_count[:-1]
    answerer_count = answerer_count[:-1]
    month_answerer_data = month_answerer_data[:-1]

    if len(question_count) >= 24:

        question_count_train = question_count[0:12]
        answer_count_train = answer_count[0:12]
        asker_count_train = asker_count[0:12]
        answerer_count_train = answerer_count[0:12]

        question_count_test = question_count[12:24]
        answer_count_test = answer_count[12:24]
        asker_count_test = asker_count[12:24]
        answerer_count_test= answerer_count[12:24]
        month_answerer_data_test = month_answerer_data[12:24]

        optimal_parameters_question, covariance_of_parameters_question = curve_fit(cobb_douglas_question, asker_count_train, question_count_train)
        answer_factors_train = np.array([question_count_train, answerer_count_train])
        optimal_parameters_answer, covariance_of_parameters_answer = curve_fit(cobb_douglas_answer, answer_factors_train, answer_count_train, bounds=([0, 0, 0],[np.inf, 1.0, 1.0]))

        avg_error_answer_top_threshold = []
        avg_error_answer_bottom_threshold = []
        avg_error_answer_avg_threshold = []
        answerer_percent = []
        
        for ab_threshold in [x / 100.0 for x in range(0, 21, 1)]:  
            answerer_count_test = []
            
            answer_count_test_top = []
            answer_count_test_bottom = []
            answer_count_test_avg = []
                     
            for i, answerer_data in enumerate(month_answerer_data):
                top_answerer_contribution = 0
                bottom_answerer_contribution = 0
                avg_answerer_contribution = 0
                
                for N in range(0, int(ab_threshold*len(answerer_data))):
                    top_answerer_contribution = top_answerer_contribution+answerer_data[N]
                for N in range(len(answerer_data)-int(ab_threshold*len(answerer_data)), len(answerer_data)):
                    bottom_answerer_contribution = bottom_answerer_contribution+answerer_data[N]

                #print answerer_data
                number_of_permutations = 20
                for perm in range(number_of_permutations):
                    randomized_answerer_data = copy.deepcopy(answerer_data)
                    random.shuffle(randomized_answerer_data)
                    for N in range(0, int(ab_threshold*len(answerer_data))):
                        avg_answerer_contribution = avg_answerer_contribution+randomized_answerer_data[N]
                avg_answerer_contribution = avg_answerer_contribution / number_of_permutations
                    
                    
                answerer_count_test.append(answerer_count[i] - int(ab_threshold*len(answerer_data)))
                answer_count_test_top.append(answer_count[i] - top_answerer_contribution)
                answer_count_test_bottom.append(answer_count[i] - bottom_answerer_contribution)
                answer_count_test_avg.append(answer_count[i] - avg_answerer_contribution)

            answer_factors_test = np.array([question_count, answerer_count_test])
            
            avg_error_answer_top = np.mean(abs(answer_count_test_top-cobb_douglas_answer(answer_factors_test, *optimal_parameters_answer))/answer_count_test_top*100)
            avg_error_answer_bottom = np.mean(abs(answer_count_test_bottom-cobb_douglas_answer(answer_factors_test, *optimal_parameters_answer))/answer_count_test_bottom*100)
            avg_error_answer_avg = np.mean(abs(answer_count_test_avg-cobb_douglas_answer(answer_factors_test, *optimal_parameters_answer))/answer_count_test_avg*100)
            
            answerer_percent .append(1-ab_threshold)
            avg_error_answer_top_threshold.append(avg_error_answer_top)
            avg_error_answer_bottom_threshold.append(avg_error_answer_bottom)
            avg_error_answer_avg_threshold.append(avg_error_answer_avg)

        #print answerer_percent[5]
        site_list.append(site)
        beta_max.append(avg_error_answer_top_threshold[5])
        beta_min.append(avg_error_answer_bottom_threshold[5])

        #beta = []
        #alpha_max_minus_min = []
        #for a_top, b_top in enumerate(avg_error_answer_top_threshold):
            #for a_bottom, b_bottom in enumerate(avg_error_answer_bottom_threshold):
                #if (b_top-b_bottom)/b_top < 0.001 and a_top > 0:
                    #beta.append((b_top+b_bottom)/2)
                    #alpha_max_minus_min.append(float((100-a_top)-(100-a_bottom))/100)
                    #break
        #norm = [float(i - min(beta))/(max(beta) - min(beta)) for i in beta]
                    
        fig = plt.figure(figure_count, figsize=(15, 6))
        figure_count += 1
        ax = fig.add_subplot(131)
        ax.plot(answerer_percent, avg_error_answer_top_threshold, 'r', label = 'beta_max')
        ax.plot(answerer_percent, avg_error_answer_bottom_threshold, 'b', label = 'beta_min')
        ax.plot(answerer_percent, avg_error_answer_avg_threshold, 'g', label = 'beta_avg')
        ax.legend(loc='upper right')
        ax.set_xlabel('alpha')
        ax.set_ylabel('beta')
        ax = fig.add_subplot(132)
        ax.plot(answerer_percent, np.subtract(avg_error_answer_top_threshold, avg_error_answer_bottom_threshold), 'r')
        ax.set_xlabel('alpha')
        ax.set_ylabel('beta_max - beta_min')
        ax = fig.add_subplot(133)
        ax.plot(answerer_percent,  [float(a)/b for a, b in zip(avg_error_answer_top_threshold, avg_error_answer_bottom_threshold)], 'r')
        ax.set_xlabel('alpha')
        ax.set_ylabel('beta_max / beta_min')

        #fig = plt.figure(figure_count, figsize=(6, 6))
        #ax = fig.add_subplot(111)
        #ax.plot(norm, alpha_max_minus_min, 'r')
        #ax.set_xlabel('beta')
        #ax.set_ylabel('alpha_max - alpha_min')     

        fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Cobb-Douglas/AB/Month/Answerer/'+site)
        plt.close(fig) 

    question_count[:] = []
    answer_count[:] = []
    asker_count[:] = []
    answerer_count[:] = []
    month_answerer_data[:] = []

fig = plt.figure(figure_count, figsize=(6, 6))
ax = fig.add_subplot(111)
ax.scatter(beta_min, beta_max)
ax.plot(beta_max, beta_max)
fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Cobb-Douglas/AB/Month/Test/'+'gg')
plt.close(fig)

text_file = open("site_beta_stats.txt", "w")
for i, site in enumerate(site_list):
    text_file.write("%s, %s, %s\n" % (site_list[i], beta_max[i], beta_min[i]))
text_file.close()

        
        
        
        
