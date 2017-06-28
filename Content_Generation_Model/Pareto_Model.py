import csv
import matplotlib.pyplot as plt

#data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Contribution_of_Top_Answerers.csv')
#data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Contribution_of_Top_Askers.csv')
data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Contribution_of_Top_Questions.csv')
csv_data = csv.reader(data_file)

figure_count = 1

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

    #If current site, add data to model
    
    if row[0] == current_site and int(row[1]) == current_month:   
        contribution_count = contribution_count + int(row[3])
        population_size = population_size + 1
        cumulative_contribution.append(contribution_count)
        cumulative_population.append(population_size)
        
    #If new site, plot current model and reassign the required variables
        
    else:

        #One in ten rule: at least 20 points for a 2 variable regression
        if population_size >= 20:
            
            fig = plt.figure(figure_count)
            figure_count += 1
            ax = fig.add_subplot(111)
            ax.plot(cumulative_population, cumulative_contribution)
            #ax.set_xlabel('Cumulative Top Answerer Population')
            #ax.set_ylabel('Cumulative Answer Contribution')
            #ax.set_xlabel('Cumulative Top Asker Population')
            #ax.set_ylabel('Cumulative Question Contribution')
            ax.set_xlabel('Cumulative Top Question Magnitude')
            ax.set_ylabel('Cumulative Answer Magnitude')
            #fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Pareto/Answerer/'+current_site+'_'+str(current_month))
            #fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Pareto/Asker/'+current_site+'_'+str(current_month))
            fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Pareto/Question/'+current_site+'_'+str(current_month))
            plt.close(fig)

        current_site = row[0]
        current_month = int(row[1])
        
        cumulative_contribution[:] = []
        cumulative_population[:] = []
        
        contribution_count = int(first_row[3])
        population_size = 1

        cumulative_contribution.append(contribution_count)
        cumulative_population.append(population_size)
        


