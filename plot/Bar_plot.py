#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 10:50:07 2019

@author: SumeetKumar
"""
import numpy as np
import matplotlib.pyplot as plt

def bar_plot(Fig,Ax,Title,Ydata,Legend,Ylabel,Xlabel,Xticklabels):
    if len(Ydata)>8: Ydata=Ydata[:8]                             #display atmost 8 harmonics only
    index=np.arange(1,1+len(Ydata))
    bar_width = 0.15
    Ax.bar(index, Ydata, bar_width,label=Legend)
    Ax.set_xlabel(Xlabel)
    Ax.set_ylabel(Ylabel)
    Ax.set_title(Title)
    Ax.set_xticks(index + bar_width / 2)
    Ax.set_xticklabels(Xticklabels)
    Ax.legend()
    Ax.spines['right'].set_color('none')
    Ax.spines['bottom'].set_position('zero')
    Ax.spines['top'].set_color('none')
    

def save_this_subplot_as_fig(Figure_name,Xdata_cii,Ydata_cii,Xdata_expt,Ydata_expt,Ylabel,Xtick_labels,Bar_width,Legend,Limits,Directory):
    Axislabel_size=17
    Ticklabel_size=14
    Legend_size=15
    Fig = plt.figure()
    Ax = Fig.add_subplot(1,1,1)
    Bar_cii=Ax.bar(Xdata_cii,Ydata_cii,Bar_width,color='blue',label=Legend[0])
    Bar_expt=Ax.bar(Xdata_expt,Ydata_expt,Bar_width,color='red',label=Legend[1])
    Ax.set_ylim(Limits[0], Limits[1])
    Ax.set_ylabel(Ylabel, fontsize=Axislabel_size)
    Ax.set_xticks([])
    Ax.tick_params(axis='y', labelsize=Ticklabel_size)
    for (rect_expt,rect_cii,xlabel) in zip(Bar_expt,Bar_cii,Xtick_labels):         
        x_loc=rect_expt.get_x()
        shift_above_bar=0.5        
        if rect_expt.get_height()<0 and rect_cii.get_height()<0: y_loc=shift_above_bar     #Placing Xtick_labels like in Ref. P44 
        else: y_loc=shift_above_bar+max(rect_expt.get_height(),rect_cii.get_height())
        Ax.text(x_loc, y_loc, xlabel, ha='center', va='bottom', fontdict={'size': Ticklabel_size})     #Attach a text label above each bar displaying the xticklabel
    Ax.legend(frameon=False, prop={'size': Legend_size})
    Ax.spines['right'].set_color('none')
    Ax.spines['bottom'].set_position('zero')
    Ax.spines['top'].set_color('none')
    Fig.savefig(Directory+'/'+Figure_name+'.png', bbox_inches='tight')
    print('saved: ', Figure_name)
    plt.close(Fig)
    
def save_this_subplot_as_fig_DK(Figure_name,Xdata_cii,Ydata_cii,Xdata_expt,Ydata_expt,Ylabel,Xtick_labels,Bar_width,Legend,Limits,Directory):
    import matplotlib.pylab as pl
#    import matplotlib
#    from matplotlib import rc
#    import matplotlib.ticker as mtick
#    #rc('text', usetex=True)    
#    matplotlib.rcParams['mathtext.fontset'] = 'cm' # 'stix' #'custom'
#    matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
#    matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
#    matplotlib.rcParams['mathtext.bf'] = 'Bitstream Vera Sans:bold'
#    matplotlib.rcParams['font.family'] = 'serif'#'STIXGeneral'
#    matplotlib.rcParams['font.serif'] = ['Times']
    font = {'size'   : 18}    
    colors = pl.cm.viridis(np.linspace(0,0.80,2))       


    Fig = plt.figure()
    Ax = Fig.add_subplot(1,1,1)
    Bar_cii=Ax.bar(Xdata_cii,Ydata_cii,Bar_width,color=colors[0],label=Legend[0])
    Bar_expt=Ax.bar(Xdata_expt,Ydata_expt,Bar_width,color=colors[1],label=Legend[1])
    Ax.set_ylim(Limits[0], Limits[1])
    Ax.set_ylabel(Ylabel, fontsize=font['size'])
    Ax.set_xticks([])
    Ax.tick_params(axis='y', labelsize=font['size'])
    for (rect_expt,rect_cii,xlabel) in zip(Bar_expt,Bar_cii,Xtick_labels):         
        x_loc=rect_expt.get_x()
        shift_above_bar=0.5        
        if rect_expt.get_height()<0 and rect_cii.get_height()<0: y_loc=shift_above_bar     #Placing Xtick_labels like in Ref. P44 
        else: y_loc=shift_above_bar+max(rect_expt.get_height(),rect_cii.get_height())
        Ax.text(x_loc, y_loc, xlabel, ha='center', va='bottom', fontdict={'size': font['size']})     #Attach a text label above each bar displaying the xticklabel
    Ax.legend(frameon=True, prop={'size': 16})
    Ax.spines['right'].set_color('none')
    Ax.spines['bottom'].set_position('zero')
    Ax.spines['top'].set_color('none')
    Ax.grid(True)
    Fig.savefig(Directory+'/'+Figure_name+'.pdf', bbox_inches='tight')
    print('saved: ', Figure_name)
    plt.close(Fig)


def openloop_offline(Figure_name,Ydata_baseline,Ydata_optimal,Power_baseline,Ylabel,Ylabel2,Xtick_labels,Bar_width,Legend,Limits,Directory):
    Ydata_baseline=Ydata_baseline.copy()
    Ydata_baseline.append(Power_baseline)
#    Ydata_optimal=Ydata_optimal.copy()
#    Ydata_optimal.append(Power_optimal)
    Axislabel_size=15
    Ticklabel_size=13
    Legend_size=14
    Fig = plt.figure()
    Ax = Fig.add_subplot(1,1,1)
    Ax2=Ax.twinx()
    Xdata_baseline=np.arange(1,1+len(Ydata_baseline))
    Xdata_optimal=Bar_width+np.arange(1,1+len(Ydata_baseline))   
    Ax.bar(Xdata_baseline[:-1],Ydata_baseline[:-1],Bar_width,color='blue',label=Legend[0])
    Ax.bar(Xdata_optimal[:-1],Ydata_optimal,Bar_width,color='red',label=Legend[1])     ##change this when power result for optimal case is also available!!!!!!!!!!!
    if Limits: Ax.set_ylim(Limits[0], Limits[1])
    Ax.set_ylabel(Ylabel, fontsize=Axislabel_size)
    Ax2.bar(Xdata_baseline[-1],Ydata_baseline[-1],Bar_width,color='blue',label=Legend[0])
#    Ax2.bar(Xdata_optimal[-1]+1,Ydata_optimal[-1],Bar_width,color='red',label=Legend[1])
    Ax2.set_ylabel(Ylabel2, fontsize=Axislabel_size)
    Ax2.tick_params(axis='y', labelsize=Ticklabel_size)
    Ax.set_xticks(Xdata_baseline+Bar_width/2)
    Ax.set_xticklabels(Xtick_labels)
    Ax.tick_params(axis='both', labelsize=Ticklabel_size)
    Ax.legend(frameon=False, prop={'size': Legend_size})
    Fig.savefig(Directory+'/'+Figure_name+'.png', bbox_inches='tight')
    print('saved: ', Figure_name)
    plt.close(Fig)


