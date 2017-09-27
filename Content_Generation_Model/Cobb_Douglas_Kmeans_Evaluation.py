import os
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sklearn
from sklearn import manifold
import nltk
import scipy
import numpy
from sklearn.metrics import silhouette_samples, silhouette_score

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Parameters_Cobb_Douglas.csv')
csv_data = csv.reader(data_file)

parameter_matrix = []
site = []

for row in csv_data:
    if(0.0001 < float(row[4]) <= 1.0 and 0.0001 < float(row[5]) <= 1.0):
        temp = []
        #temp.append(float(row[1]))
        temp.append(float(row[2]))
        #temp.append(float(row[3]))
        temp.append(float(row[4]))
        temp.append(float(row[5]))
        #temp.append(float(row[4])+float(row[5]))
        #temp.append(float(row[4])+float(row[5]))
        parameter_matrix.append(temp)
        site.append(row[0])

parameter_matrix = numpy.array(parameter_matrix)

max_silhouette_avg = 0

for n_clusters in range(2, 3):
    kclusterer = nltk.cluster.kmeans.KMeansClusterer(n_clusters, distance = nltk.cluster.util.euclidean_distance, repeats=25, avoid_empty_clusters=True)
    cluster_labels = kclusterer.cluster(parameter_matrix , assign_clusters=True)
    silhouette_avg = silhouette_score(parameter_matrix , cluster_labels)
    #print n_clusters, silhouette_avg
    if silhouette_avg > max_silhouette_avg:
        max_silhouette_avg = silhouette_avg
        optimal_labels = cluster_labels
        optimal_n_clusters = n_clusters

print 'Optimal No. of Clusters:', optimal_n_clusters

#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.scatter(parameter_matrix[:, 0], parameter_matrix [:, 1], s=20, c=optimal_labels, marker='o')
#ax.set_xlabel('Dimension 1')
#ax.set_ylabel('Dimension 2')
#fig.savefig('Cluster_Visualization')
#plt.close(fig)


data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Site_Monthly_Stats.csv')
csv_data = csv.reader(data_file)

first_row = next(csv_data)
current_site = first_row[0]

percentage_of_answered_question = float(first_row[4])/float(first_row[2])*100
percentage_of_question_with_accepted_answer  = float(first_row[5])/float(first_row[2])*100
avg_time_to_first_answer = float(first_row[10])

monthly_percentage_of_answered_question = []
monthly_percentage_of_question_with_accepted_answer = []
monthly_avg_time_to_first_answer = []

monthly_percentage_of_answered_question.append(percentage_of_answered_question)
monthly_percentage_of_question_with_accepted_answer.append(percentage_of_question_with_accepted_answer)
monthly_avg_time_to_first_answer.append(avg_time_to_first_answer)

site_stats = {}

for row in csv_data:

    #If current site, add data to stats model
    
    if row[0] == current_site:   
        percentage_of_answered_question = float(row[4])/float(row[2])*100
        percentage_of_question_with_accepted_answer  = float(row[5])/float(row[2])*100
        avg_time_to_first_answer = float(row[10])

        monthly_percentage_of_answered_question.append(percentage_of_answered_question)
        monthly_percentage_of_question_with_accepted_answer.append(percentage_of_question_with_accepted_answer)
        monthly_avg_time_to_first_answer.append(avg_time_to_first_answer)

        
    #If new site, store current model and reassign the required variables
        
    else:

        #At least 10 data points
        if len(monthly_percentage_of_answered_question) >= 10:

            stats = [numpy.mean(monthly_percentage_of_answered_question), numpy.mean(monthly_percentage_of_question_with_accepted_answer), numpy.mean(monthly_avg_time_to_first_answer)]
            site_stats[current_site] = stats
            

        current_site = row[0]
        
        monthly_percentage_of_answered_question[:] = []
        monthly_percentage_of_question_with_accepted_answer[:] = []
        monthly_avg_time_to_first_answer[:] = []
        
        percentage_of_answered_question = float(row[4])/float(row[2])*100
        percentage_of_question_with_accepted_answer  = float(row[5])/float(row[2])*100
        avg_time_to_first_answer = float(row[10])

        monthly_percentage_of_answered_question.append(percentage_of_answered_question)
        monthly_percentage_of_question_with_accepted_answer.append(percentage_of_question_with_accepted_answer)
        monthly_avg_time_to_first_answer.append(avg_time_to_first_answer)


stat1 = []
stat2 = []
stat3 = []

for i in range(optimal_n_clusters):
    print '***********'
    print 'Cluster:', i
    print '***********'
    for idx,val in enumerate(optimal_labels):
        if val == i and site[idx] in site_stats:
            print site[idx], site_stats[site[idx]]
            stat1.append(site_stats[site[idx]][0])
            stat2.append(site_stats[site[idx]][1])
            stat3.append(site_stats[site[idx]][2])
    print ''
    fig = plt.figure()
    ax = fig.add_subplot(1, 3, 1)
    ax.boxplot(stat1, 0, '')
    ax.title.set_text('% of AQ - C'+str(i+1))
    ax2= fig.add_subplot(1, 3, 2)
    ax2.boxplot(stat2, 0, '')
    ax2.title.set_text('% of QA - C'+str(i+1))
    ax3 = fig.add_subplot(1, 3, 3)
    ax3.boxplot(stat3, 0, '')
    ax3.title.set_text('% of TA - C'+str(i+1))
    fig.tight_layout()
    fig.savefig('Cluster_Health_C'+str(i+1))
    plt.close(fig)
    stat1[:] = []
    stat2[:] = []
    stat3[:] = []




