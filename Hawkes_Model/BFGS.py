import sys, getopt
import csv
import numpy as	np
from scipy.optimize import fmin_l_bfgs_b
import matplotlib.pyplot as plt


all_channels = []
all_parameters = []
observed_q = []
observed_a = []
observed_c = []

final_q = []
final_a = []
final_c = []

T1 = 5
T2 = 5
T3 = 5

# parse the input csv file into [[channel_1,[time_11, type_11, intensity_11], ..., [time_1n,type_1n, intensity_1n]],....,[channel_m,[time_m1,type_m1,intensity_mn],...,[time_mn,type_mn,intensity_mn]]]
def parseEvents(path):
    previous_channel = "null"
    tmp_list = []
    first = True
    with open(path, 'rU') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            #print(row)
            #print(row[0])
            if row[0] != previous_channel and first == False :
                all_channels.append(tmp_list)
                first = False
                tmp_list = []
                tmp_list.append(row[0])
                tmp_list.append([int(row[1]),0,int(row[2])])
                tmp_list.append([int(row[1]),1,int(row[3])])
                tmp_list.append([int(row[1]),2,int(row[4])])
                previous_channel = row[0]
            elif first == True:
                first = False
                tmp_list = []
                tmp_list.append(row[0])
                tmp_list.append([int(row[1]), 0, int(row[2])])
                tmp_list.append([int(row[1]), 1, int(row[3])])
                tmp_list.append([int(row[1]), 2, int(row[4])])
                previous_channel = row[0]
            else:
                first = False
                tmp_list.append([int(row[1]), 0, int(row[2])])
                tmp_list.append([int(row[1]), 1, int(row[3])])
                tmp_list.append([int(row[1]), 2, int(row[4])])
                previous_channel = row[0]
    #print(np.matrix(all_channels))




# J_q defines the equation for generating questions based on previous questions
# N_q[t] = mu1 + C1 * sum(N_q[t-tau](tau + c1)^(-(1+theta1)))  tau = 1, ..., T1
def J_q(x):
    [mu1, C1, c1, theta1] = x
    expected_q = []
    global final_q
    final_q = []
    length = len(observed_q)
    #print(length)
    dif = 0
    for i in range(0, T1):
        expected_q.append(observed_q[i])
        final_q.append(observed_q[i])
    #print(np.matrix(expected_q))
    for i in range(T1, length):
        tmp_sum = mu1
        for j in range(i - T1, i):
            #print(expected_q[j][1])
            #print(observed_q[i][0])
            #print(expected_q[j][0])
            tmp_sum += C1 * expected_q[j][1] * ((observed_q[i][0] - expected_q[j][0] + c1) ** (-(1 + theta1)))
        expected_q.append([int(observed_q[i][0]),tmp_sum])
        final_q.append([int(observed_q[i][0]), tmp_sum])
        dif += (observed_q[i][1] - tmp_sum) ** 2
    #print(np.matrix(observed_q))
    #print(np.matrix(expected_q))
    final_q = expected_q
    return float(dif)/2

# J_a defines the equation for generating answers based on previous answers
# N_a[t] = mu2 + C2 * sum(N_a[t-tau](tau + c2)^(-(1+theta2)))  tau = 1, ..., T2
def J_a(x):
    [mu2, C2, c2, theta2] = x
    expected_a = []
    global final_a
    final_a = []
    length = len(observed_a)
    dif = 0
    for i in range(0, T2):
        expected_a.append(observed_a[i])
        final_a.append(observed_a[i])
    for i in range(T2, length):
        tmp_sum = mu2
        for j in range(i - T2, i):
            tmp_sum += C2 * expected_a[j][1] * ((observed_a[i][0] - expected_a[j][0] + c2) ** (-(1 + theta2)))
        expected_a.append([int(observed_a[i][0]),tmp_sum])
        final_a.append([int(observed_a[i][0]),tmp_sum])
        dif += (observed_a[i][1] - tmp_sum) ** 2

    return float(dif)/2

# J_c defines the equation for generating comments based on previous comments
# N_c[t] = mu3 + C3 * sum(N_c[t-tau](tau + c3)^(-(1+theta3)))  tau = 1, ..., T3
def J_c(x):
    [mu3, C3, c3, theta3] = x
    expected_c = []
    global final_c
    final_c = []
    length = len(observed_c)
    dif = 0
    for i in range(0, T3):
        expected_c.append(observed_c[i])
        final_c.append(observed_c[i])
    for i in range(T3, length):
        tmp_sum = mu3
        for j in range(i - T3, i):
            tmp_sum += C3 * expected_c[j][1] * ((observed_c[i][0] - expected_c[j][0] + c3) ** (-(1 + theta3)))
        expected_c.append([int(observed_c[i][0]),tmp_sum])
        final_c.append([int(observed_c[i][0]), tmp_sum])
        dif += (observed_c[i][1] - tmp_sum) ** 2
    final_c = expected_c
    return float(dif)/2


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print("BFGS.py -i <inputfile> -o <outputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("BFGS.py -i <inputfile> -o <outputfile>")
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print("inputfile is", inputfile, "outputfile is",outputfile )
    parseEvents(inputfile)
    try:
        out = open(outputfile, 'w')
    except:
        print("Fail to open outputfile")
    outwriter = csv.writer(out, delimiter=',')


    #observed_q represents the observed questions, and it is in the format of [[time_1,intensity_1],...,[time_n,intensity_n]]
    #expected_q represents the expected questions, and it is in the format of [[time_1,intensity_1],...,[time_n,intensity_n]]
    for channel in all_channels:
        channel_name = channel[0]
        observed_q[:] = []
        observed_a[:] = []
        observed_c[:] = []
        first = True
        for event in channel:
            if first:
                first = False
                continue
            if event[1] == 0:
                observed_q.append([event[0],event[2]])
            elif event[1] == 1:
                observed_a.append([event[0],event[2]])
            elif event[1] == 2:
                observed_c.append([event[0],event[2]])
        #print(np.matrix(observed_q))
        #print(np.matrix(observed_a))
        #print(np.matrix(observed_c))
        if len(observed_q) <= T1:
            continue
        # initial guess for the parameters
        x0 = np.array([5, 1, 1, 1])
        x1 = np.array([5, 1, 1, 1])
        x2 = np.array([5, 1, 1, 1])
        res_q = fmin_l_bfgs_b(J_q, x0, approx_grad=True)
        print (res_q)
        res_a = fmin_l_bfgs_b(J_a, x1, approx_grad=True)
        print(res_a)
        res_c = fmin_l_bfgs_b(J_c, x2, approx_grad=True)
        print(res_c)
        outwriter.writerow([channel_name, "q", res_q[:], "a", res_a[:], "c", res_c[:]])



        # get the final expected questions, answers and comments, and it is in the format of [[time_1,intensity_1],...,[time_n,intensity_n]]
        J_q(res_c[0])
        J_a(res_a[0])
        J_c(res_c[0])
        print(np.matrix(final_q))
        print(np.matrix(final_a))
        print(np.matrix(final_c))


        # plotting

        month = []
        o_q = []
        e_q = []
        o_a = []
        e_a = []
        o_c = []
        e_c = []
        length = len(observed_q)
        for k in range(0,length):
            month.append(observed_q[k][0])
            o_q.append(observed_q[k][1])
            e_q.append(final_q[k][1])
            o_a.append(observed_a[k][1])
            e_a.append(final_a[k][1])
            o_c.append(observed_c[k][1])
            e_c.append(final_c[k][1])

        fig = plt.figure()
        plt.plot(month, o_q, 'r--', label='Observed Questions')
        plt.plot(month, e_q, 'r^', label='Expected Questions')
        plt.plot(month, o_a, 'b--', label='Observed Answers')
        plt.plot(month, e_a, 'b^', label='Expected Answers')
        plt.plot(month, o_c, 'g--', label='Observed Comments')
        plt.plot(month, e_c, 'g^', label='Expected Comments')
        plt.legend()

        fig.suptitle(channel_name)
        plt.xlabel('Month')
        plt.ylabel('Number of Activities')
        plt.show()
        fig.savefig(channel_name + '_one_factor')

        '''
        trace0 = go.Scatter(
            x = month,
            y = o_q,
            name = 'Observed Questions',
            line = dict(
                color = ('rgb(205, 12, 24)'),
                width = 4,
                dash='dash')
        )
        trace1 = go.Scatter(
            x=month,
            y=e_q,
            name='Expected Questions',
            line=dict(
                color=('rgb(205, 12, 24)'),
                width=4,
                dash = 'dot')
        )
        trace2 = go.Scatter(
            x=month,
            y=o_a,
            name='Observed Answers',
            line=dict(
                color=('rgb(22, 96, 167)'),
                width=4,
                dash = 'dash')
        )
        trace3 = go.Scatter(
            x=month,
            y=e_a,
            name='Expected Answers',
            line=dict(
                color=('rgb(22, 96, 167)'),
                width=4,
                dash='dot')
        )
        trace4 = go.Scatter(
            x=month,
            y=o_c,
            name='Observed Comments',
            line=dict(
                color=('rgb(50,205,50)'),
                width=4,
                dash = 'dash')
        )
        trace5 = go.Scatter(
            x=month,
            y=e_c,
            name='Expected Comments',
            line=dict(
                color=('rgb(50,205,50)'),
                width=4,
                dash='dot')
        )
        data = [trace0, trace1, trace2, trace3, trace4, trace5]
        layout = dict(title = channel_name,
                      xaxis = dict(title = 'Month'),
                      yaxis = dict(title = 'Number of Activities'),
                      )

        fig = dict(data = data, layout = layout)
        py.plot(fig, filename = channel_name + ' one factor')
        '''






if __name__ == "__main__":
    main(sys.argv[1:])


