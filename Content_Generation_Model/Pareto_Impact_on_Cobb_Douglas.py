import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


site_pareto_stats = {}


for i in range(2):

    data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Answerers_Pareto.csv')
    data_file_2 = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Questions_Pareto.csv')

    csv_data = csv.reader(data_file)
    
    if i == 1:
        csv_data = csv.reader(data_file_2)
        
    first_row = next(csv_data)
    current_site = first_row[0]

    contribution_count = int(first_row[2])
    population_size = 1
        
    cumulative_contribution = []
    cumulative_population = []

    cumulative_contribution.append(contribution_count)
    cumulative_population.append(population_size)

    for row in csv_data:

        if row[0] == current_site:

            contribution_count = contribution_count + int(row[2])
            population_size = population_size + 1
            cumulative_contribution.append(contribution_count)
            cumulative_population.append(population_size)

        else:
            contribution_of_pareto_answerers = float(cumulative_contribution[int(population_size*0.2)-1])/contribution_count

            pareto_index = -1
            for  index, item in enumerate(cumulative_contribution):
                if item >= contribution_count*0.8:
                    pareto_index = index
                    break
            contributors_of_pareto_answers = float(index+1)/population_size

            if i == 0:
                site_pareto_stats[current_site] = [contribution_of_pareto_answerers, contributors_of_pareto_answers]
            else:
                pareto_stats = site_pareto_stats[current_site]
                pareto_stats.append(contribution_of_pareto_answerers)
                pareto_stats.append(contributors_of_pareto_answers)
                site_pareto_stats[current_site] = pareto_stats

            current_site = row[0]

            cumulative_contribution[:] = []
            cumulative_population[:] = []
            contribution_count = int(first_row[2])
            population_size = 1
            cumulative_contribution.append(contribution_count)
            cumulative_population.append(population_size)

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Parameters_Cobb_Douglas.csv')
csv_data = csv.reader(data_file)

for row in csv_data:
    pareto_stats = site_pareto_stats[row[0]]
    pareto_stats.append(float(row[4]))
    pareto_stats.append(float(row[5]))
    print '%s, %.6f, %.6f, %.6f, %.6f , %.6f, %.6f' % (row[0], pareto_stats[0], pareto_stats[1], pareto_stats[2], pareto_stats[3], pareto_stats[4], pareto_stats[5])
    
    

                
                
                

             
                            

             


			
