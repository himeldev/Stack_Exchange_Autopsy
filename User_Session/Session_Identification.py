import csv
import copy
import datetime
import time

f = open('Temporal_Action_Sequence.csv')
csv_f = csv.reader(f)
output_file = open("Sessionwise_Activity.txt", "w")

action_sequence_all_user = []
action_sequence_current_user = []

first_row = next(csv_f)
prev_site = first_row[0]
prev_user_id = first_row[1]
action_sequence_current_user.append((first_row[2], first_row[3]))

for row in csv_f:

    #If previous user, add action to current sequence
    if row[0] == prev_site and row[1] == prev_user_id:
        action_sequence_current_user.append((row[2], row[3]))

    #If new user, dump data and reassign the required variables
    else:
        
        for i in range(len(action_sequence_current_user)):
            
            if i == 0:
                if int(action_sequence_current_user[i][1]) == 1:
                    output_file.write('Q')
                    #print 'Q',
                elif int(action_sequence_current_user[i][1]) == 2:
                    output_file.write('A')
                    #print 'A',
                elif int(action_sequence_current_user[i][1]) == 3:
                    output_file.write('C')
                    #print 'C',
                try:
                    prev_timestamp = datetime.datetime.strptime(action_sequence_current_user[i][0], '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    prev_timestamp = datetime.datetime.strptime(action_sequence_current_user[i][0], '%Y-%m-%d %H:%M:%S')
            else:
                try:
                    current_timestamp = datetime.datetime.strptime(action_sequence_current_user[i][0], '%Y-%m-%d %H:%M:%S.%f')
                except ValueError:
                    current_timestamp = datetime.datetime.strptime(action_sequence_current_user[i][0], '%Y-%m-%d %H:%M:%S')
                    
                ts1 = time.mktime(prev_timestamp.timetuple())
                ts2 = time.mktime(current_timestamp.timetuple())
                delta_time = ts2 - ts1
                
                #Session: consecutive events where any two events are less than 6 hrs apart
                if (delta_time/3600) > 6:
                    output_file.write('-')
                    #print '-',
                    
                if int(action_sequence_current_user[i][1]) == 1:
                    output_file.write('Q')
                    #print 'Q',
                elif int(action_sequence_current_user[i][1]) == 2:
                    output_file.write('A')
                    #print 'A',
                elif int(action_sequence_current_user[i][1]) == 3:
                    output_file.write('C')
                    #print 'C',
                    
                prev_timestamp = current_timestamp
          
        output_file.write('\n\n')
        #print ''
        #print 'Site: ', prev_site, 'User Id: ', prev_user_id, ' Done'
        action_sequence_all_user.append(copy.deepcopy(action_sequence_current_user))
        action_sequence_current_user[:] = []
        action_sequence_current_user.append((row[2], row[3]))
        prev_site = row[0]
        prev_user_id = row[1]
        
output_file.close()
