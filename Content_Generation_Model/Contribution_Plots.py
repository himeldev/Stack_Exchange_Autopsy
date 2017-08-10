import csv
import numpy
from scipy.optimize import curve_fit
from scipy.special import zetac
import matplotlib.pyplot as plt


data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/User_Contribution.csv')
csv_data = csv.reader(data_file)

figure_count = 1
slope_list = []

first_row = next(csv_data)
current_site = first_row[0]

user_contribution = float(first_row[5])

contribution_list = []

contribution_list.append(user_contribution)

for row in csv_data:

    #If current site, add data for model construction
    
    if row[0] == current_site:   
        user_contribution = float(row[5])
        contribution_list.append(user_contribution)
        
    #If new site, construct and plot current model, and reassign the data variables
        
    else:

        #At least 100 users for model construction
        
        if len(contribution_list) >= 100:

            print current_site
            fig = plt.figure(figure_count)
            figure_count += 1
            ax = fig.add_subplot(111)
            hist, bins = numpy.histogram(contribution_list, bins=200)
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
            ax.plot(numpy.unique(x), numpy.poly1d(numpy.polyfit(x, y, 1))(numpy.unique(x)), c='r')
            ax.set_title('Site: '+current_site+' Slope:'+str(slope))
            ax.set_xlabel("$log_{10}$(# of Contributions)")
            ax.set_ylabel("$log_{10}$(User Frequency)")
            fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Contribution Plots/'+current_site)
            plt.close(fig)

        current_site = row[0]
        
        contribution_list[:] = []
        
        user_contribution = float(row[5])

        contribution_list.append(user_contribution)

plt.hist(slope_list)
plt.show()




