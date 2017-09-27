import pymc3 as pm
import numpy as np
import theano.tensor as tt
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import seaborn as sb
import csv

sb.set_context(
    "paper",
    font_scale=1,
    rc={
        "lines.linewidth": 2.5,
        "text.usetex": True,
        "font.family": 'serif',
        "font.serif": 'Palatino',
        "font.size": 16
    })
#from matplotlib import rc
# rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica'], 'size': 16})
# ## for Palatino and other serif fonts use:
# rc('font', **{'family': 'serif', 'serif': ['Palatino'], 'size': 16})
# rc('text', usetex=True)

data_file = open('C:/Users/Himel/Documents/GitHub/Stack_Exchange_Autopsy/Datasets/Monthly_QA_Activity.csv')
csv_data = csv.reader(data_file)

first_row = next(csv_data)
current_site = first_row[0]

question_count = []
answer_count = []
asker_count = []
answerer_count = []

question_count.append(int(first_row[2]))
answer_count.append(int(first_row[3]))
asker_count.append(int(first_row[4]))
answerer_count.append(int(first_row[5]))

figure_count = 1

for row in csv_data:

    #If current site, add data for model construction
    
    if row[0] == current_site:

        question_count.append(int(row[2]))
        answer_count.append(int(row[3]))
        asker_count.append(int(row[4]))
        answerer_count.append(int(row[5]))
        
    #If new site, construct and plot current model, and reassign the data variables
        
    else:

        #Delete the last (broken/partial) data point
        
        question_count = question_count[:-1]
        answer_count = answer_count[:-1]
        asker_count = asker_count[:-1]
        answerer_count = answerer_count[:-1]

        #One in ten rule: at least 20 points for a 2 variable regression
        
        if len(answer_count) >= 10:

            # model specifications in PyMC3 are wrapped in a with-statement
            
            with pm.Model() as model: 
                
                # Define priors
                
                A_answer = pm.Normal('A_answer', 0, sd = 50)
                lambda_0_answer = pm.Normal('lambda_0_answer', 0, sd = 20)
                lambda_1_answer = pm.Normal('lambda_1_answer', 0, sd = 20)
                model_answer = pm.Deterministic('model_answer', A_answer * tt.pow(np.array(question_count), lambda_0_answer ) * tt.pow(np.array(answerer_count), lambda_1_answer ))
                sigma = pm.HalfCauchy('sigma', beta=10)

                observations = pm.Normal('observations', mu=model_answer, sd=sigma, observed=np.array(answer_count))

                # Inference!
                step = pm.Metropolis(vars=[A_answer, lambda_0_answer, lambda_1_answer, sigma, model_answer, observations])
                start = pm.find_MAP()  # initialization using MAP
                trace = pm.sample(10000, step=step, start=start)

            # getting rid of the initial part of the MCMC
            
            burned_trace = trace[2000:]  

            pm.summary(trace=burned_trace, varnames=['A_answer'])
            pm.summary(trace=burned_trace, varnames=['lambda_0_answer'])
            pm.summary(trace=burned_trace, varnames=['lambda_1_answer'])
            pm.summary(trace=burned_trace, varnames=['sigma'])

            number_of_rows = 4
            number_of_columns = 2

            fig, axs = sb.plt.subplots(number_of_rows, number_of_columns)
            #fig.set_size_inches(10, 12)
            pm.plots.traceplot(trace=burned_trace, varnames=['A_answer', 'lambda_0_answer', 'lambda_1_answer', 'sigma'],
                               lines={
                                 'A_answer': (burned_trace['A_answer']).mean(),
                                'lambda_0_answer': (burned_trace['lambda_0_answer']).mean(),
                                'lambda_1_answer': (burned_trace['lambda_1_answer']).mean(),
                                'sigma': (burned_trace['sigma']).mean()
                                },
                               ax=axs)
            
            axs[0,0].set_title(r"$A$")
            axs[0,1].set_title(r"$A$")
            axs[1,0].set_title(r"$\lambda_0$")
            axs[1,1].set_title(r"$\lambda_0$")
            axs[2,0].set_title(r"$\lambda_1$")
            axs[2,1].set_title(r"$\lambda_1$")
            axs[3,0].set_title(r"$\sigma$")
            axs[3,1].set_title(r"$\sigma$")
            
            # axs[0,0].locator_params(axis='x', nticks=2)
            axs[0,0].xaxis.set_major_locator(plt.MaxNLocator(3))
            
            for i in range(number_of_rows):
                for j in range(number_of_columns):
                    z = axs[i, j]
                    z.set_xlabel("") # no individual labels
                    z.set_ylabel("")
            #         z.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
            #         if j==1:
                    if not(i==0 and j==1):
                        if j!=0:
                            z.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
                    else:
                        z.yaxis.set_major_formatter(FormatStrFormatter('%.0e'))
                    z.tick_params(direction='in', length=6, width=2, colors='r', which='major')
                    z.tick_params(direction='in', length=4, width=1, colors='k', which='minor')
                    z.xaxis.set_ticks_position('bottom')
                    z.yaxis.set_ticks_position('left')
                    z.minorticks_on()
            plt.savefig(current_site+'.pdf')

        current_site = row[0]
        
        question_count[:] = []
        answer_count[:] = []
        asker_count[:] = []
        answerer_count[:] = []
        
        question_count.append(int(row[2]))
        answer_count.append(int(row[3]))
        asker_count.append(int(row[5]))
        answerer_count.append(int(row[5]))





