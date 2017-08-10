import csv
import numpy
import matplotlib.pyplot as plt

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Contribution_of_Top_Answerers.csv')
#data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Contribution_of_Top_Askers.csv')
#data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Contribution_of_Top_Questions.csv')
csv_data = csv.reader(data_file)

figure_count = 1
slope_list = []
population_list = []

first_row = next(csv_data)
current_site = first_row[0]
current_month = int(first_row[1])

user_contribution = float(first_row[3])

contribution_list = []

contribution_list.append(user_contribution)

for row in csv_data:

    #If current site and month, add data for model construction
    
    if row[0] == current_site and int(row[1]) == current_month:   
        user_contribution = float(row[3])
        contribution_list.append(user_contribution)
        
    #If current site and new month, construct and plot current model, and reassign the data variables
        
    elif row[0] == current_site and int(row[1]) <> current_month: 

        #At least 50 users for model construction
        
        if len(contribution_list) >= 50:
            
            fig = plt.figure(figure_count)
            figure_count += 1
            ax = fig.add_subplot(111)
            hist, bins = numpy.histogram(contribution_list, bins=50)
            center = (bins[:-1] + bins[1:]) / 2
            x = []
            y = []
            for i, val in enumerate(hist):
                if hist[i] > 0:
                    x.append(numpy.log10(center[i]))
                    y.append(numpy.log10(hist[i]))
            ax.scatter(x, y)
            slope, intercept = numpy.poly1d(numpy.polyfit(x, y, 1))
            slope_list.append(slope)
            population_list.append(len(contribution_list))
            ax.plot(numpy.unique(x), numpy.poly1d(numpy.polyfit(x, y, 1))(numpy.unique(x)), c='r')
            ax.set_title(current_site+'_'+str(current_month)+' :'+str(slope))
            ax.set_xlabel("$log_{10}$(# of Contributions)")
            ax.set_ylabel("$log_{10}$(Answerer Frequency)")
            #ax.set_ylabel("$log_{10}$(Asker Frequency)")
            #ax.set_ylabel("$log_{10}$(Question Frequency)")
            fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Exponent Model/Month/Answerer/'+current_site+'_'+str(current_month))
            #fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Exponent Model/Month/Asker/'+current_site+'_'+str(current_month))
            #fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Exponent Model/Month/Question/'+current_site+'_'+str(current_month))
            plt.close(fig)

        current_month = int(row[1])
        
        contribution_list[:] = []
        
        user_contribution = float(row[3])

        contribution_list.append(user_contribution)

    else:

        if len(slope_list) >= 20:
            
            fig = plt.figure(figure_count)
            figure_count += 1
            ax = fig.add_subplot(111)
            ax.scatter(population_list, slope_list)
            fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Exponent Model/Site/Answerer/'+current_site)
            #fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Exponent Model/Site/Asker/'+current_site)
            #fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Exponent Model/Site/Question/'+current_site)
            plt.close(fig)

        current_site = row[0]

        current_month = int(first_row[1])
        
        contribution_list[:] = []
        
        user_contribution = float(row[3])

        contribution_list.append(user_contribution)

        slope_list[:] = []
        population_list[:] = []


