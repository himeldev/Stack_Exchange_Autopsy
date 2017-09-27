import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sklearn import svm
from sklearn.model_selection import cross_val_score
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
month_answerer_data = []

classification_data = []
label = []
pos_count = 0
neg_count = 0
sd = []

for site in sorted(site_month_aggregate_data.keys()):
    data_row = []
    
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
        month_answerer_data_train = month_answerer_data[0:12]

        question_count_test = question_count[12:24]
        answer_count_test = answer_count[12:24]
        asker_count_test = asker_count[12:24]
        answerer_count_test= answerer_count[12:24]
        month_answerer_data_test = month_answerer_data[12:24]

        optimal_parameters_question, covariance_of_parameters_question = curve_fit(cobb_douglas_question, asker_count_train, question_count_train)
        answer_factors_train = np.array([question_count_train, answerer_count_train])
        optimal_parameters_answer, covariance_of_parameters_answer = curve_fit(cobb_douglas_answer, answer_factors_train, answer_count_train, bounds=([0, 0, 0],[np.inf, 1.0, 1.0]))
        sd.append(np.sqrt(np.diag(covariance_of_parameters_answer)))

        question_percent_error = np.mean(abs(question_count_test-cobb_douglas_question(asker_count_test, *optimal_parameters_question))/question_count_test)*100
        answer_factors_test = np.array([question_count_test, answerer_count_test])
        answer_percent_error = np.mean(abs(answer_count_test-cobb_douglas_answer(answer_factors_test, *optimal_parameters_answer))/answer_count_test)*100
        answer_signed_error = np.mean((answer_count_test-cobb_douglas_answer(answer_factors_test, *optimal_parameters_answer))/answer_count_test)*100
        
        top_user_contribution_train = []
        bottom_user_contribution_train = []
        ab_threshold = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
        
        for theta in ab_threshold:
            monthly_top_user_contribution = []
            monthly_bottom_user_contribution = []

            for i, answerer_data in enumerate(month_answerer_data_train):
                top_user_total_contribution = 0
                bottom_user_total_contribution = 0

                for N in range(0, int(theta*len(answerer_data))):
                    top_user_total_contribution = top_user_total_contribution+answerer_data[N]                   
                    
                for N in range(len(answerer_data)-int(theta*len(answerer_data)), len(answerer_data)):
                    bottom_user_total_contribution = bottom_user_total_contribution+answerer_data[N]

                monthly_top_user_contribution.append(float(top_user_total_contribution)/answer_count_train[i]*100)
                monthly_bottom_user_contribution.append(float(bottom_user_total_contribution)/answer_count_train[i]*100)
                
            top_user_contribution_train.append(monthly_top_user_contribution)
            bottom_user_contribution_train.append(monthly_top_user_contribution)

        top_user_contribution_train = np.array(top_user_contribution_train)
        
        #print site+', '+str(optimal_parameters_answer[0])+', '+str(optimal_parameters_answer[1])+', '+str(optimal_parameters_answer[2])+','+str(np.mean(top_user_contribution_train[4]))+', '+str(answer_percent_error)+','+str(answer_signed_error)
        data_row.append(optimal_parameters_answer[0])
        data_row.append(optimal_parameters_answer[1])
        data_row.append(optimal_parameters_answer[2])
        data_row.append(np.mean(answerer_count_train))
        data_row.append(np.mean(question_count_train))
        data_row.append(np.mean(top_user_contribution_train[4]))
        classification_data.append(data_row)
       
        if answer_percent_error >= 10:
            label.append(0)
            neg_count = neg_count + 1
            print site+', '+str(optimal_parameters_answer[0])+', '+str(optimal_parameters_answer[1])+', '+str(optimal_parameters_answer[2])+',  -', np.sqrt(np.diag(covariance_of_parameters_answer))
        else:
            label.append(1)
            pos_count = pos_count+1
            print site+', '+str(optimal_parameters_answer[0])+', '+str(optimal_parameters_answer[1])+', '+str(optimal_parameters_answer[2])+', +', np.sqrt(np.diag(covariance_of_parameters_answer))
        #print site+', '+str(answer_percent_error)+',', top_user_contribution_train[:, 1]
        

    question_count[:] = []
    answer_count[:] = []
    asker_count[:] = []
    answerer_count[:] = []
    month_answerer_data[:] = []

print classification_data
print label
print float(pos_count)/(pos_count+neg_count), float(neg_count)/(pos_count+neg_count)

classification_data = np.array(classification_data)
label = np.array(label)
clf = svm.SVC(kernel='linear', C = 1.0)
#clf.fit(classification_data, label)
print cross_val_score(clf, classification_data, label, scoring='accuracy')
print cross_val_score(clf, classification_data, label, scoring='precision')
print cross_val_score(clf, classification_data, label, scoring='recall')
print "NONE"

sd = np.array(sd)
label = np.array(label)
clf_2 = svm.SVC(kernel='linear', C = 1.0)
#clf.fit(classification_data, label)
print cross_val_score(clf_2, sd, label, scoring='accuracy')
print cross_val_score(clf_2, sd, label, scoring='precision')
print cross_val_score(clf_2, sd, label, scoring='recall')



        
        
        
        
