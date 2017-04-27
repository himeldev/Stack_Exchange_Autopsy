import csv
import copy
import datetime
import time
import matplotlib.pyplot as plt

f = open('Sessionwise_Activity.txt')

question_activity_count_list = []
answer_comment_activity_count_list = []
activity_count_list = []


for line in f:
    activity_count = 0
    question_activity_count = 0
    answer_comment_activity_count = 0
    for ch in line:
        if ch == 'Q':
            question_activity_count += 1
            activity_count += 1
        elif ch == 'A' or ch == 'C':
            answer_comment_activity_count += 1
            activity_count += 1
        else:
            if question_activity_count < 10:
                question_activity_count_list.append(question_activity_count)
            if answer_comment_activity_count < 10:
                answer_comment_activity_count_list.append(answer_comment_activity_count)
            if activity_count < 10:
                activity_count_list.append(activity_count)
            #print activity_count
            activity_count = 0
            question_activity_count = 0
            answer_comment_activity_count = 0

fig1 = plt.figure(1)
plt.hist(question_activity_count_list)
plt.title('per session question distribution')
plt.xlabel("# of activities")
plt.ylabel("frequency")
fig1.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/User_Session/sessionwise_question_activity')
plt.close(fig1)

fig2 = plt.figure(2)
plt.hist(answer_comment_activity_count_list)
plt.title('per session answer/comment distribution')
plt.xlabel("# of activities")
plt.ylabel("frequency")
fig2.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/User_Session/sessionwise_answer_comment_activity')
plt.close(fig2)

fig3 = plt.figure(3)
plt.hist(activity_count_list)
plt.title('per session activity distribution')
plt.xlabel("# of activities")
plt.ylabel("frequency")
plt.savefig('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/User_Session/sessionwise_all_activity')
plt.close(fig3)
            

 
