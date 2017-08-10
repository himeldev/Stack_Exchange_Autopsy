import csv
import numpy
from scipy.optimize import curve_fit
from scipy.special import zetac
import matplotlib.pyplot as plt

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/User_Contribution.csv')
csv_data = csv.reader(data_file)

figure_count = 1

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

            #y,binEdges=np.histogram(data,bins=100)
            #bincenters = 0.5*(binEdges[1:]+binEdges[:-1])
            #p.plot(bincenters,y,'-')
            #p.show()
            list_of_ones = [1] * len(contribution_list)
            logA = numpy.log10(contribution_list)
            logB = numpy.log10(numpy.cumsum(list_of_ones))

            coefficients = numpy.polyfit(logB, logA, 1)
            polynomial = numpy.poly1d(coefficients)
            ys = polynomial(list_of_ones)
            plt.plot(logB, logA)
            plt.plot(list_of_ones, ys)
            plt.show()
            
            fig = plt.figure(figure_count)
            figure_count += 1
            ax = fig.add_subplot(111)
            #plt.xticks(bins, ["10^%s" % i for i in bins])
            ax.hist(numpy.log10(contribution_list), bins =100, log=True)
            #ax.hist(contribution_list)
            #ax.set_yscale('log')
            ax.set_xscale('log')
            #ax.plot(safe(numpy.cumsum(list_of_ones)), f(safe(numpy.cumsum(list_of_ones)), *popt), c='r')
            #ax.title(row[0])
            ax.set_xlabel("$log_{10}$(# of Contributions)")
            ax.set_ylabel("$log_{10}$(User Frequency)")
            fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/User Contribution LL Plots/'+row[0])
            plt.close(fig)

        current_site = row[0]
        
        contribution_list[:] = []
        
        user_contribution = float(row[5])

        contribution_list.append(user_contribution)
        


