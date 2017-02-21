from pylab import *
from scipy.optimize import curve_fit
import csv
import math
import copy
import datetime
import time
import matplotlib.pyplot as plt
from numpy.random import normal


f = open('Temporal_Action_Sequence.csv')
csv_f = csv.reader(f)

inter_activity_time_per_user = []
inter_activity_time_per_channel = []
inter_activity_time_all_user = []


first_row = next(csv_f)
prev_site = first_row[0]
prev_user_id = first_row[1]
try:
    prev_timestamp = datetime.datetime.strptime(first_row[2], '%Y-%m-%d %H:%M:%S.%f')
except ValueError:
    prev_timestamp = datetime.datetime.strptime(first_row[1], '%Y-%m-%d %H:%M:%S')

site_count = 1

for row in csv_f:

    #If previous user, add inter activity time to per user list
    if row[0] == prev_site and row[1] == prev_user_id:
        
        try:
            current_timestamp = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            current_timestamp = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        ts1 = time.mktime(prev_timestamp.timetuple())
        ts2 = time.mktime(current_timestamp.timetuple())
        delta_time = math.log((ts2 - ts1) if (ts2 - ts1)>0 else 1)
        inter_activity_time_per_user.append(delta_time)
        
    #If previous site, add per user list to per channel list
    elif row[0] == prev_site and row[1] != prev_user_id:
        
        inter_activity_time_per_channel.extend(copy.deepcopy(inter_activity_time_per_user))
        inter_activity_time_per_user[:] = []
        
        prev_user_id = row[1]
        try:
            current_timestamp = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            current_timestamp = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        prev_timestamp = current_timestamp   

    #If new site, add per channel list to all user list
    else:
        
        fig = plt.figure(site_count)
        site_count += 1
        plt.hist(inter_activity_time_per_channel, bins = 100)
        plt.title(row[0])
        plt.xlabel("log(inter-activity time)")
        plt.ylabel("frequency")
        fig.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/User_Session/Figures/'+row[0])
        plt.close(fig)

        inter_activity_time_all_user.extend(copy.deepcopy(inter_activity_time_per_channel))
        inter_activity_time_per_channel[:] = []
        inter_activity_time_per_user[:] = []

        prev_site = row[0]
        prev_user_id = row[1]
        try:
            current_timestamp = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            current_timestamp = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')                    
        prev_timestamp = current_timestamp
        

y,x,_ = plt.hist(inter_activity_time_all_user, bins = 100)
plt.title("all users")
plt.xlabel("log(inter-activity time)")
plt.ylabel("frequency")
plt.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/User_Session/all_users')


x=(x[1:]+x[:-1])/2 # for len(x)==len(y)

def gauss(x,mu,sigma,A):
    return A*exp(-(x-mu)**2/2/sigma**2)

def bimodal(x,mu1,sigma1,A1,mu2,sigma2,A2):
    return gauss(x,mu1,sigma1,A1)+gauss(x,mu2,sigma2,A2)

expected=(7.5,1,20000,18,2,500000)
params,cov=curve_fit(bimodal,x,y,expected)
sigma=sqrt(diag(cov))
plt.plot(x,bimodal(x,*params),color='red',lw=3,label='Mixture Model')
legend()
plt.show()
print(params,'\n',sigma)    

