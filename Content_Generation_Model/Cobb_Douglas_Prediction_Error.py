import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def cobb_douglas_answer(x, A, lambda_0, lambda_1):
    return A * np.power(x[0], lambda_0) * np.power(x[1], lambda_1)

def cobb_douglas_question(x, A, lambda_0):
    return A * np.power(x, lambda_0)

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
        
#text_file = open("Output.txt", "w")
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
        
#text_file = open("Output_2.txt", "w")
#text_file.write("%s" % site_month_answerer_data)
#text_file.close()

question_count = []
answer_count = []
asker_count = []
answerer_count = []

for site in sorted(site_month_aggregate_data.keys()):
    for month in sorted(site_month_aggregate_data[site].keys()):
        question_count.append(site_month_aggregate_data[site][month][0])
        answer_count.append(site_month_aggregate_data[site][month][1])
        asker_count.append(site_month_aggregate_data[site][month][2])
        answerer_count.append(site_month_aggregate_data[site][month][3])

    question_count = question_count[:-1] 
    answer_count = answer_count[:-1]
    asker_count = asker_count[:-1]
    answerer_count = answerer_count[:-1]

    if len(question_count) >= 18:

        #question_count_train = question_count[0:int(len(question_count)*0.8)]
        #answer_count_train = answer_count[0:int(len(answer_count)*0.8)]
        #asker_count_train = asker_count[0:int(len(asker_count)*0.8)]
        #answerer_count_train = answerer_count[0:int(len(answerer_count)*0.8)]

        #question_count_test = question_count[int(len(question_count)*0.8):len(question_count)]
        #answer_count_test = answer_count[int(len(answer_count)*0.8):len(question_count)]
        #asker_count_test = asker_count[int(len(asker_count)*0.8):len(question_count)]
        #answerer_count_test= answerer_count[int(len(answerer_count)*0.8):len(question_count)]

        question_count_train = question_count[0:12]
        answer_count_train = answer_count[0:12]
        asker_count_train = asker_count[0:12]
        answerer_count_train = answerer_count[0:12]

        question_count_test = question_count[12:18]
        answer_count_test = answer_count[12:18]
        asker_count_test = asker_count[12:18]
        answerer_count_test= answerer_count[12:18]
        
        optimal_parameters_question, covariance_of_parameters_question = curve_fit(cobb_douglas_question, asker_count_train, question_count_train)
        answer_factors_train = np.array([question_count_train, answerer_count_train])
        optimal_parameters_answer, covariance_of_parameters_answer = curve_fit(cobb_douglas_answer, answer_factors_train, answer_count_train, bounds=([0, 0, 0],[np.inf, 1.0, 1.0]))

        question_percent_error = np.mean(abs(question_count_test-cobb_douglas_question(asker_count_test, *optimal_parameters_question))/question_count_test)*100
        answer_factors_test = np.array([question_count_test, answerer_count_test])
        answer_percent_error = np.mean(abs(answer_count_test-cobb_douglas_answer(answer_factors_test, *optimal_parameters_answer))/answer_count_test)*100
        print site+', '+str(question_percent_error)+', '+str(answer_percent_error)
        
    question_count[:] = []
    answer_count[:] = []
    asker_count[:] = []
    answerer_count[:] = [] 

        
        
        
        
