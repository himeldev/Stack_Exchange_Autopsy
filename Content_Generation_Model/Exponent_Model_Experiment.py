import csv
import numpy
import matplotlib.pyplot as plt

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Contribution_of_Top_Answerers.csv')
#data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Contribution_of_Top_Askers.csv')
#data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Contribution_of_Top_Questions.csv')
csv_data = csv.reader(data_file)

figure_count = 1

first_row = next(csv_data)
current_site = first_row[0]

user_contribution = float(first_row[3])
contribution_list = []
contribution_list.append(user_contribution)

for row in csv_data:

    #If current site and month, add data for model construction
    
    if row[0] == current_site:   
        user_contribution = float(row[3])
        contribution_list.append(user_contribution)
        
    #If current site and new month, construct and plot current model, and reassign the data variables
        
    else: 

        #At least 100 user months for model construction
        
        if len(contribution_list) >= 100:
            
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
            ax.plot(numpy.unique(x), numpy.poly1d(numpy.polyfit(x, y, 1))(numpy.unique(x)), c='r')
            ax.set_title(current_site+' :'+str(slope))
            ax.set_xlabel("$log_{10}$(# of Contributions)")
            ax.set_ylabel("$log_{10}$(Answerer Frequency)")
            #ax.set_ylabel("$log_{10}$(Asker Frequency)")
            #ax.set_ylabel("$log_{10}$(Question Frequency)")
            fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Exponent Model/Experiment/'+current_site)
            #fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Exponent Model/Experiment/'+current_site+'_'+str(current_month))
            #fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Exponent Model/Experiment/'+current_site+'_'+str(current_month))
            plt.close(fig)

        current_site = row[0]
        contribution_list[:] = []  
        user_contribution = float(row[3])
        contribution_list.append(user_contribution)




