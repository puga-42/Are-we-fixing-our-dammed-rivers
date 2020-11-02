import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# from src.helpers import *
from scipy import stats

colors_list = ['#71C348', '#48A9C3']


plt.style.use('ggplot')

def plot_water_bodies(lst, title='Counts of Water Body Types in 303(d) Data', size=(14, 5)):
    '''
        plots a barchart of entries per water body in 303(d) list
        
        ARGS:
            x - list
            y - list
        Return:
            ax - axis with plot
    '''

    fig, ax = plt.subplots(figsize=size)
    plt.title(title)
    
    x_pos = [i for i, _ in enumerate(lst[0])]
    plt.xticks(x_pos, lst[0])
    plt.setp(plt.gca().get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.bar(lst[0], lst[1])

    plt.xlabel("Water Body Type")
    plt.ylabel("Number of Entries")
    plt.title("Counts of Water Body Types in 303(d) Data")
    return ax



def plot_most_potent_stacked_bar(data_dict):
    '''
        Plots a stacked bar graph of the 15 most common pollutants and
        whether they can be solved by TMDLs

        ARGS:
            data_dict - dictionary with keys = pollutants, 
            values = counts of ppollutants
        Returns:
            none. Plots stacked bar chart
    '''
    fig, ax = plt.subplots(figsize=(9, 7))
    r = [0,1]

    df = pd.DataFrame(data_dict)
    
    # From raw value to percentage
    totals = [i+j for i,j in zip(df['Dammed'], df['Natural'])]
    dammed = [i / j * 100 for i,j in zip(df['Dammed'], totals)]
    natural = [i / j * 100 for i,j in zip(df['Natural'], totals)]
    
    # plot
    barWidth = 0.65
    names = ('Dammed', 'Natural')

    plt.bar(r, dammed, color=colors_list[0], edgecolor='white', width=barWidth)
    # Create blue Bars
    plt.bar(r, natural, bottom=[i for i in dammed], color=colors_list[1], edgecolor='white', width=barWidth)
    
    # Custom x axis
    plt.xticks(r, names)

    plt.ylabel('Percent Solvable')
    plt.title('Proportion of Pollutants Solvable with Implementation of TMDLs')
    colors = {'% Unsolvable with TMDLs':colors_list[0], '% Solvable with TMDLs':colors_list[1]}
    labels = ['% Unsolvable with TMDLs', '% Solvable with TMDLs']

    handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    plt.legend(handles, labels)
        
    plt.show()



def plot_most_common_pollutants(dammed_most_potent, undammed_most_potent):
    '''
        Plots side by side bar chart of 15 most common pollutants for
        dammed and natural rivers.

        ARGS:
            dammed_most_potent, undammed_mot_potent - dictionaries with keys = pollutants,
            values = counts of pollutants
        Returns:
            None
    '''

    x_list = []
    for k, v in dammed_most_potent.items():
        if k not in x_list:
            x_list.append(k)
        
    for k, v in undammed_most_potent.items():
        if k not in x_list:
            x_list.append(k)
    x_list = sorted(x_list)

    dammed = []
    for item in x_list:
        if item in dammed_most_potent:
            dammed.append(dammed_most_potent[item])
        else:
            dammed.append(0.5)
    undammed = []
    for item in x_list:
        if item in undammed_most_potent:
            undammed.append(undammed_most_potent[item])
        else:
            undammed.append(0.5)
            
    fig, ax = plt.subplots(figsize=(20, 5))
            
    N = len(x_list)
    ind = np.arange(N)
    width = 0.4
        
    ax.bar(ind, dammed, width, color=colors_list[0], label='Dammed')
    ax.bar(ind + width , undammed, width, color=colors_list[1],
        label='Undammed')

    plt.ylabel('# of Occurances of Impairment')
    plt.title('Top 15 Impairments in Dammed and Undammed Rivers')

    plt.xticks(ind + width / 2, x_list)
    plt.setp(plt.gca().get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.legend(loc='best')
    plt.show()


def plot_simple_bar(figsize, dict_list, title, ylabel, labels):
    '''
        Plots multicolored bar chart with legend

        ARGS:
            figsize - tuple. Figsize of output chart
            dict_list - list of dictionaries
            title, ylabel - str
            labels - list of strings. Titles of each colored section
    '''

    fig, ax = plt.subplots(figsize=figsize)
    i = 0
    for d in dict_list:
        plt.bar(*zip(*d.items()), color=colors_list[i])
        i += 1


    plt.title(title)    
    plt.setp(plt.gca().get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.ylabel(ylabel)

    #set up colors dictionary to manually create a legend
    colors = {}

    i = 0
    for l in labels:
        colors[l] = colors_list[i]
        i += 1
    
    labels = labels
    #create a legend
    rects = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
    plt.legend(rects, labels)
    plt.show()
