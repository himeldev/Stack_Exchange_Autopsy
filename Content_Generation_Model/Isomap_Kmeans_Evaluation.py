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

#def symmetric_KL_divergence(X, Y):
    #return scipy.stats.entropy(X, Y)+scipy.stats.entropy(Y, X)

site_topic_distribution = []
site = []

for filename in os.listdir('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Topic_Proportions/7'):
    if filename.endswith('.csv'):
        site.append(filename[0:len(filename)-16])
        data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Topic_Proportions/7/'+filename)
        csv_data = csv.reader(data_file)
        first_row = next(csv_data)
        topic_distribution = []
        for row in csv_data:
            topic_distribution.append(float(row[1]))
        site_topic_distribution.append(topic_distribution)

min_error = 10000

figure_count = 1

for n_neighbors in range(2, 21):
    fig = plt.figure(figure_count)
    ax = fig.add_subplot(111)
    ax.set_xlabel('No. of Dimension')
    ax.set_ylabel('Reconstruction Error')
    n_components_list = []
    error_list = []    
    for n_components in range(1, 8):
        error = sklearn.manifold.Isomap(n_neighbors, n_components).fit(site_topic_distribution).reconstruction_error()
        print 'No. of Neighbors:', n_neighbors, 'No. of Components:', n_components, 'Error:', error
        n_components_list.append(n_components)
        error_list.append(error)
        if error <min_error:
            min_error = error
            optimal_n_neighbors = n_neighbors
            optimal_n_components = n_components
    ax.plot(n_components_list, error_list)
    ax.scatter(n_components_list, error_list)
    fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Isomap/Topic_Proportions/7/Number_of_Neighbors_'+str(n_neighbors))
    plt.close(fig)
    figure_count += 1
    
#print optimal_n_neighbors, optimal_n_components

optimal_n_neighbors =20
optimal_n_components = 3

reduced_data = manifold.Isomap(optimal_n_neighbors, optimal_n_components).fit_transform(site_topic_distribution)
#print reduced_data

max_silhouette_avg = 0

for n_clusters in range(2, 11):
    kclusterer = nltk.cluster.kmeans.KMeansClusterer(n_clusters, distance = nltk.cluster.util.euclidean_distance, repeats=25, avoid_empty_clusters=True)
    cluster_labels = kclusterer.cluster(reduced_data, assign_clusters=True)
    silhouette_avg = silhouette_score(reduced_data, cluster_labels)
    #print n_clusters, silhouette_avg
    if silhouette_avg > max_silhouette_avg:
        max_silhouette_avg = silhouette_avg
        optimal_labels = cluster_labels
        optimal_n_clusters = n_clusters

print 'Optimal No. of Clusters:', optimal_n_clusters

if optimal_n_components == 2:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(reduced_data[:, 0], reduced_data[:, 1], s=20, c=optimal_labels, marker='o')
    ax.set_xlabel('Dimension 1')
    ax.set_ylabel('Dimension 2')
    fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Isomap/Topic_Proportions/7/Cluster_Visualization')
    plt.close(fig)

elif optimal_n_components == 3:
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    ax.scatter(reduced_data[:, 0], reduced_data[:, 1], reduced_data[:, 2] , c=optimal_labels, s=30, marker='*', edgecolors='none', depthshade=0)
    ax.set_xlabel('Dimension 1')
    ax.set_ylabel('Dimension 2')
    ax.set_zlabel('Dimension 3')
    fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Isomap/Topic_Proportions/7/Cluster_Visualization')
    plt.close(fig)


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
    fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Figures/Isomap/Topic_Proportions/7/Cluster_Health_C'+str(i+1))
    plt.close(fig)
    stat1[:] = []
    stat2[:] = []
    stat3[:] = []




