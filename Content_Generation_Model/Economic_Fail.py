import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

figure_count = 1

site_question_count = {}
site_answer_count = {}
site_asker_count = {}
site_answerer_count = {}

site_delta_question_count = {}
site_delta_answer_count = {}
site_delta_asker_count = {}
site_delta_answerer_count = {}


for i in range(2):

    data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Contribution_of_Top_Answerers.csv')
    data_file_2 = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Contribution_of_Top_Askers.csv')

    csv_data = csv.reader(data_file)
    

    
    if i == 1:
        csv_data = csv.reader(data_file_2)
        
    first_row = next(csv_data)
    current_site = first_row[0]
    current_month = int(first_row[1])

    contribution_count = int(first_row[3])
    population_size = 1
        
    cumulative_contribution = []
    cumulative_population = []

    cumulative_contribution.append(contribution_count)
    cumulative_population.append(population_size)

    for row in csv_data:

        if row[0] == current_site and int(row[1]) == current_month:

            if current_month >= 5:

                contribution_count = contribution_count + int(row[3])
                population_size = population_size + 1
                cumulative_contribution.append(contribution_count)
                cumulative_population.append(population_size)

        else:

             if i == 0 and population_size >= 20 or i == 1 and population_size >= 20:

                 if i == 0:

                     if current_site in site_answer_count:

                         answer_count = site_answer_count[current_site]
                         answer_count.append(contribution_count)
                         site_answer_count[current_site] = answer_count

                         answerer_count = site_answerer_count[current_site]
                         answerer_count.append(population_size)
                         site_answerer_count[current_site] = answerer_count

                         delta_answer_count = site_delta_answer_count[current_site]
                         delta_answer_count.append(cumulative_contribution[int(len(cumulative_contribution)*0.2)])
                         site_delta_answer_count[current_site] = delta_answer_count

                         delta_answerer_count = site_delta_answerer_count[current_site]
                         delta_answerer_count.append(cumulative_population[int(len(cumulative_population)*0.2)])
                         site_delta_answerer_count[current_site] = delta_answerer_count

                     else:

                         answer_count = []
                         answer_count.append(contribution_count)
                         site_answer_count[current_site] = answer_count

                         answerer_count = []
                         answerer_count.append(population_size)
                         site_answerer_count[current_site] = answerer_count

                         delta_answer_count = []
                         delta_answer_count.append(cumulative_contribution[int(len(cumulative_contribution)*0.2)])
                         site_delta_answer_count[current_site] = delta_answer_count

                         delta_answerer_count = []
                         delta_answerer_count.append(cumulative_population[int(len(cumulative_population)*0.2)])
                         site_delta_answerer_count[current_site] = delta_answerer_count
                            
                 elif i == 1:

                        if current_site in site_question_count:

                            question_count = site_question_count[current_site]
                            question_count.append(contribution_count)
                            site_question_count[current_site] = question_count

                            asker_count = site_asker_count[current_site]
                            asker_count.append(population_size)
                            site_asker_count[current_site] = asker_count

                            delta_question_count = site_delta_question_count[current_site]
                            delta_question_count.append(cumulative_contribution[int(len(cumulative_contribution)*0.2)])
                            site_delta_question_count[current_site] = delta_question_count

                            delta_asker_count = site_delta_asker_count[current_site]
                            delta_asker_count.append(cumulative_population[int(len(cumulative_population)*0.2)])
                            site_delta_asker_count[current_site] = delta_asker_count

                        else:
                            
                            question_count = []
                            question_count.append(contribution_count)
                            site_question_count[current_site] = question_count

                            asker_count =[]
                            asker_count.append(population_size)
                            site_asker_count[current_site] = asker_count

                            delta_question_count = []
                            delta_question_count.append(cumulative_contribution[int(len(cumulative_contribution)*0.2)])
                            site_delta_question_count[current_site] = delta_question_count

                            delta_asker_count = []
                            delta_asker_count.append(cumulative_population[int(len(cumulative_population)*0.2)])
                            site_delta_asker_count[current_site] = delta_asker_count
                            

             current_site = row[0]
             current_month = int(row[1])
             cumulative_contribution[:] = []
             cumulative_population[:] = []

             contribution_count = int(first_row[3])
             population_size = 1

             cumulative_contribution.append(contribution_count)
             cumulative_population.append(population_size)

def cobb_douglas_answer(x, A, lambda_0, lambda_1):
    return A * np.power(x[0], lambda_0) * np.power(x[1], lambda_1)

def cobb_douglas_question(x, A, lambda_0):
    return A * np.power(x, lambda_0)

#print site_question_count
#print site_answer_count
#print site_asker_count
#print site_answerer_count

for site in site_answer_count:

    if site not in ['coffee', 'networkengineering', 'martialarts', 'cogsci', 'italian', 'gardening', 'ebooks', 'sustainability', 'beer', 'emacs', 'sound', 'windowsphone', 'avp', 'poker']:
        #print site
        question_count = site_question_count[site]
        question_count_train = question_count[0:int(len(question_count)*0.8)]
        delta_question_count = site_delta_question_count[site]
        question_count_test_1 = np.subtract(question_count[int(len(question_count)*0.8):len(question_count)], delta_question_count[int(len(question_count)*0.8):len(question_count)])
        question_count_test_2 = question_count[int(len(question_count)*0.8):len(question_count)]
        

        answer_count = site_answer_count[site]
        answer_count_train = answer_count[0:int(len(question_count)*0.8)]
        delta_answer_count = site_delta_answer_count[site]
        answer_count_test = np.subtract(answer_count[int(len(question_count)*0.8):len(question_count)], delta_answer_count[int(len(question_count)*0.8):len(question_count)])

        asker_count = site_asker_count[site]
        asker_count_train = asker_count[0:int(len(question_count)*0.8)]
        delta_asker_count = site_delta_asker_count[site]
        asker_count_test = np.subtract(asker_count[int(len(question_count)*0.8):len(question_count)], delta_asker_count[int(len(question_count)*0.8):len(question_count)])

        answerer_count = site_answerer_count[site]
        answerer_count_train = answerer_count[0:int(len(question_count)*0.8)]
        delta_answerer_count = site_delta_answerer_count[site]
        answerer_count_test = np.subtract(answerer_count[int(len(question_count)*0.8):len(question_count)], delta_answerer_count[int(len(question_count)*0.8):len(question_count)])


        #print len(question_count), len(answer_count), len(asker_count), len(answerer_count)
                
        optimal_parameters_question, covariance_of_parameters_question = curve_fit(cobb_douglas_question, asker_count_train, question_count_train)
        answer_factors_train = np.array([question_count_train, answerer_count_train])
        #print len(answer_factors_train[0]), len(answer_factors_train[1]), len(answer_count_train)
        optimal_parameters_answer, covariance_of_parameters_answer = curve_fit(cobb_douglas_answer, answer_factors_train, answer_count_train, bounds=([0, 0, 0],[np.inf, 1.0, 1.0]))

        answer_factors = np.array([question_count_test_2, answerer_count_test])

        print abs(answer_count_test-cobb_douglas_answer(answer_factors, *optimal_parameters_answer))
        print answer_count_test
                 
        print (site, np.mean(abs(answer_count_test-cobb_douglas_answer(answer_factors, *optimal_parameters_answer))/answer_count_test)*100)
        

			
