import csv

all_channels = []


def parseEvents(path):
    previous_channel = "null"
    tmp_list = []
    first = True
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ')
        for row in reader:
            if row[0] != previous_channel and first == False :
                all_channels.append(tmp_list)
                first = False
                del tmp_list[:]
                tmp_list.append(row[0])
                tmp_list.append([row[1],0,row[2]])
                tmp_list.append([row[1],1,row[3]])
                tmp_list.append([row[1],2,row[4]])
                previous_channel = row[0]
            else:
                first = False
                tmp_list.append([row[1], 0, row[2]])
                tmp_list.append([row[1], 1, row[3]])
                tmp_list.append([row[1], 2, row[4]])
                previous_channel = row[0]




def MMEL(mu_q, mu_a,mu_c, D, alpha, delta, *qq, *aq, *cq, *qa, *aa, *ca, *qc, *ac, *cc, **bases, **events):
    while True:
        previous_bases = bases
        previous_mus = [mu_q, mu_a, mu_c ]
        new_mus = [0,0,0]
        previous_as = [[*qq, *qa, *qc], [*aq, *aa, *ac], [*cq, *ca, *cc]]
        new_as = [[*qq, *qa, *qc], [*aq, *aa, *ac], [*cq, *ca, *cc]]
        p_bases = [] #stores the probabilities that an event is sampled from a base kernel
        p_relations = [] #stores the probabilities that a event is influenced by a previous event
        length = len(events)
        total_time = 0
        for i in [0, length]:
            event = events[i]
            time = event[0]
            dimention = event[1]
            total_time += time
            tmp_sum = 0
            for j in [0, i]:
                p_time = events[j][0]
                p_dimention = events[j][1]
                for d in [0, D]:
                    tmp_sum += previous_as[p_dimention][dimention][d] * previous_bases[d][time - p_time]

            p_bases.append(previous_mus[dimention] / (previous_mus[dimention] + tmp_sum))

            tmp_1d = []
            for j in [0, i]:
                tmp_2d = []
                p_time = events[j][0]
                p_dimention = events[j][1]
                for d in [0, D]:
                    tmp_2d.append(previous_as[p_dimention][dimention][d] * previous_bases[d][time - p_time] / (previous_mus[dimention] + tmp_sum))
                tmp_1d.append(tmp_2d)
            p_relations.append(tmp_1d)


        for i in [0, length]:
            dim = events[i][1]
            new_mus[dim] += p_bases[dim]

        for mu in new_mus:
            mu /= total_time

        tc = events[length-1][0]
        for u in [0,3]:
            for v in [0,3]:
                for d in [0,D]:
                    tmp_sum = 0
                    tmp_integral = 0
                    for i in [0,length]:
                        for j in [0,i]:
                            if events[i][1] == u and events[j][1] == v:
                                tmp_sum += p_relations[i][j][d]
                        for j in [0, length]:
                            if events[j][1] == v:
                                upper = tc - events[j][0]
                                tt = 0
                                while tt <= upper:
                                    tmp_integral += previous_bases[d][tt]
                                    tt += delta
                    new_as[u][v][d] = previous_as[u][v][d] * tmp_sum / (tmp_integral + alpha)

        if new_mus == previous_mus and new_as == previous_as:
            return new_mus + new_as

        new_bases = bases
        while True:
            for d in [0, D]:
                tt = 0
                while tt + 2* delta <= tc:
                    C = 0
                    D = 0
                    for i in [0, length]:
                        tim = events[i][0]
                        dim = events[i][1]
                        if tt + delta <= tc - tim:
                            C += new_as[0][dim] + new_as[1][dim] + new_as[2][dim]
                        for j in [0, i]:
                            time_j = events[j][0]
                            if tt + delta == time - time_j:
                                D += p_relations[time][time_j][d]
                    C /= previous_bases[d][tt + delta]
                new_bases[tt] = (C * previous_bases[tt + delta] - D / previous_bases[tt+delta]) * delta * delta / (2 * alpha) + 2 * previous_bases[tt+delta] - previous_bases[tt + 2 * delta]
            if new_bases == previous_bases:
                break
            else:
                previous_bases = new_bases


















