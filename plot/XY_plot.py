#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 10:50:07 2019

@author: SumeetKumar
"""
import matplotlib.pyplot as plt
#plt.ioff()
from scipy.interpolate import interp1d
import numpy as np
import math


def xy_plot(Fig,Ax,Title,Xdata,Ydata,Legend,Xlabel,Ylabel,Limits):
    f = interp1d(Xdata, Ydata, kind='cubic')
    Xdata_smooth = np.linspace(min(Xdata), max(Xdata), 3*len(Xdata))
    Ydata_smooth = f(Xdata_smooth)
    
    Ax.plot(Xdata_smooth, Ydata_smooth, '-', label=Legend)
    Ax.set_title(Title, fontsize=9,fontweight='bold',y=1.0) 
    Ax.legend()
    Ax.set_xlabel(Xlabel,fontweight='bold')
    Ax.set_ylabel(Ylabel,fontweight='bold')
    Ax.set_xlim(0.0, 360.0)    #This needs to be changed if output of a non-azimuthal quantity is being plotted
    if Limits: Ax.set_ylim(Limits[0], Limits[1])    
    #plt.show()
    
def xy_plot_widgets(Fig,Ax,Title,Xdata,Ydata,Legend,Xlabel,Limits):
    f = interp1d(Xdata, Ydata, kind='cubic')
    Xdata_smooth = np.linspace(min(Xdata), max(Xdata), 3*len(Xdata))
    Ydata_smooth = f(Xdata_smooth)
    
    line, = Ax.plot(Xdata_smooth, Ydata_smooth, '-', label=Legend)
    Ax.set_title(Title, fontsize=9,fontweight='bold',y=1.0) 
    #Ax.legend()
    if Xlabel=='\Psi':    
        Ax.set_xlabel(Xlabel,fontweight='bold')
        Ax.set_xlim(0.0, 360.0)    #This needs to be changed if output of a non-azimuthal quantity is being plotted
        Ax.set_xticks([0,45,90,135,180,225,270,315,360])
    elif Xlabel=='r/R':
        Ax.set_xlabel(Xlabel,fontweight='bold')
        Ax.set_xlim(0.0, 1.0)    #This needs to be changed if output of a non-azimuthal quantity is being plotted
        Ax.set_xticks(np.linspace(0.0,1.0,5,endpoint=True))            
    Ax.xaxis.grid(True)
    if Limits and Limits[0]!=Limits[1]: 
        #Limits=[math.floor(Limits[0]/50)*50,math.ceil(Limits[1]/50)*50]
        Ax.set_ylim(Limits[0], Limits[1])      #if there are entries in Limits and the entries are not equal (if they are equal an warning is thrown)
        Ax.set_yticks(np.linspace(Limits[0],Limits[1],5,endpoint=True))
    #plt.show()    
    return line

def xy_plot_validation(Fig,Ax,Title,Xdata,Ydata,Legend,Xlabel,Ylabel,Limits):
    f = interp1d(Xdata, Ydata, kind='cubic')
    Xdata_smooth = np.linspace(min(Xdata), max(Xdata), 3*len(Xdata))
    Ydata_smooth = f(Xdata_smooth)    
    Ax.plot(Xdata_smooth, Ydata_smooth, '-', label=Legend)
    Ax.set_title(Title, fontsize=9,fontweight='bold',y=1.0) 
    Ax.legend()
    Ax.set_xlabel(Xlabel,fontweight='bold')
    Ax.set_ylabel(Ylabel,fontweight='bold')
    Ax.set_xlim(0.0, 360.0)    #This needs to be changed if output of a non-azimuthal quantity is being plotted
    if Limits: Ax.set_ylim(Limits[0], Limits[1])    
    

def save_this_subplot_as_fig(Figure_name,Xdata,Ydata_cii,Ydata_expt,Legend,Xlabel,Ylabel,Limits,Directory):
    Axislabel_size=17
    Ticklabel_size=14
    Legend_size=15
    Fig = plt.figure()
    Ax = Fig.add_subplot(1,1,1)
    Ax.plot(Xdata,Ydata_cii,'blue',label=Legend[0])
    Ax.plot(Xdata,Ydata_expt,'red',label=Legend[1])
    Ax.legend(frameon=False, prop={'size': Legend_size})
    Ax.set_xlabel(Xlabel, fontsize=Axislabel_size)
    Ax.set_ylabel(Ylabel, fontsize=Axislabel_size)
    Ax.set_xlim(min(Xdata), max(Xdata))    
    Ax.set_xticks(np.linspace(min(Xdata),max(Xdata),7,endpoint=True))
    Ax.tick_params(axis='both', labelsize=Ticklabel_size)
    Fig.savefig(Directory+'/'+Figure_name+'.png', bbox_inches='tight')
    print('saved: ', Figure_name)
    plt.close(Fig)
 
def save_this_subplot_as_fig_DK(Figure_name,Xdata,Ydata_cii,Ydata_expt,Legend,Xlabel,Ylabel,Limits,Directory):

    import matplotlib.pylab as pl
    import matplotlib
    from matplotlib import rc
    import matplotlib.ticker as mtick
    #rc('text', usetex=True)    
    matplotlib.rcParams['mathtext.fontset'] = 'cm' # 'stix' #'custom'
    matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
    matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
    matplotlib.rcParams['mathtext.bf'] = 'Bitstream Vera Sans:bold'
    matplotlib.rcParams['text.latex.preamble'] = [r'\usepackage{txfonts}']
    matplotlib.rcParams['font.family'] = 'serif'#'STIXGeneral'
    matplotlib.rcParams['font.serif'] = ['Times']
    font = {'size'   : 18}    
    matplotlib.rc('font', **font)
    colors = pl.cm.viridis(np.linspace(0,0.80,2))       
    linestyles = ['-', '-.', ':', (0, (5,2,1,2,1,2)), (0, (5, 2, 5, 2, 1, 2)), '-', '--', '-.', ':','-', '--', '-.', ':','-', '--', '-.', ':',""]
    markers = ['x','o','s','^','+','h','x','s','^','+',(6,2,30)]

    Fig = plt.figure()
    Ax = Fig.add_subplot(1,1,1)
#    Ax.plot(Xdata,Ydata_cii, color=colors[0], linestyle=linestyles[0], marker=markers[0], label=Legend[0])
#    Ax.plot(Xdata,Ydata_expt, color=colors[1], linestyle=linestyles[1], marker=markers[1], label=Legend[1])
    Ax.plot(Xdata,Ydata_cii, color=colors[0], linestyle=linestyles[0], label=Legend[0])
    Ax.plot(Xdata,Ydata_expt, color=colors[1], linestyle=linestyles[1], label=Legend[1])
    Ax.legend(frameon=True, prop={'size': 16})
    Ax.set_xlabel(Xlabel, fontsize=font['size'])
    Ax.set_ylabel(Ylabel, fontsize=font['size'])
    Ax.set_xlim(min(Xdata), max(Xdata))    
    Ax.set_xticks(np.linspace(min(Xdata),max(Xdata),7,endpoint=True))
    Ax.tick_params(axis='both', labelsize=font['size'])
    Ax.grid(True)
    fmt = '%.'+str(0)+'f°'     
    xticks = mtick.FormatStrFormatter(fmt)
    plt.gca().xaxis.set_major_formatter(xticks)
    Fig.savefig(Directory+'/'+Figure_name+'.pdf', bbox_inches='tight')
    print('saved: ', Figure_name)
    plt.close(Fig)

def save_this_sweep_plot_as_fig(Figure_name,Xdata_expt,Ydata_expt,Xdata_cii,Ydata_cii,Ylabel,Directory,Limits):
    Xlabel=r'$\mu$'
    Legend=('CII','EXPT')
    
    Axislabel_size=15
    Ticklabel_size=13
    Legend_size=14
#    Axislabel_size=font['size']
#    Ticklabel_size=font['size']
#    Legend_size=font['size']
    Fig = plt.figure()
    Ax = Fig.add_subplot(1,1,1)
    Ax.plot(Xdata_cii,Ydata_cii, 'b-*', label=Legend[0])
    Ax.plot(Xdata_expt,Ydata_expt, 'r-*', label=Legend[1])
    Ax.legend(frameon=False, prop={'size': Legend_size})
    Ax.set_xlabel(Xlabel, fontsize=Axislabel_size)
    Ax.set_ylabel(Ylabel, fontsize=Axislabel_size)
    Ax.set_ylim(Limits[0],Limits[1])
    Ax.set_xlim(0.05, 0.30)    
    Ax.set_xticks(np.linspace(0.05,0.30,6,endpoint=True))
    Ax.tick_params(axis='both', labelsize=Ticklabel_size)
    Ax.grid(True)
    if Figure_name=='COLL' or Figure_name=='LATCYC' or Figure_name=='LONGCYC':
        yticks_values=Ax.get_yticks()
        Ax.set_yticklabels([r"${:.1f}\degree$".format(_) for _ in yticks_values])
    Fig.savefig(Directory+'/'+Figure_name+'.png', bbox_inches='tight')
    print('saved: ', Figure_name)
    plt.close(Fig)

def save_this_sweep_plot_as_fig_DK(Figure_name,Xdata_expt,Ydata_expt,Xdata_cii,Ydata_cii,Ylabel,Directory,Limits):
    Xlabel=r'$\mu$'
    Legend=('CII','EXPT')
    
    import matplotlib.pylab as pl
    import matplotlib
    from matplotlib import rc
    import matplotlib.ticker as mtick
    #rc('text', usetex=True)    
    matplotlib.rcParams['mathtext.fontset'] = 'cm' # 'stix' #'custom'
    matplotlib.rcParams['mathtext.rm'] = 'Bitstream Vera Sans'
    matplotlib.rcParams['mathtext.it'] = 'Bitstream Vera Sans:italic'
    matplotlib.rcParams['mathtext.bf'] = 'Bitstream Vera Sans:bold'
    matplotlib.rcParams['text.latex.preamble'] = [r'\usepackage{txfonts}']
    matplotlib.rcParams['font.family'] = 'serif'#'STIXGeneral'
    matplotlib.rcParams['font.serif'] = ['Times']
    font = {'size'   : 18}    
    matplotlib.rc('font', **font)
    colors = pl.cm.viridis(np.linspace(0,0.80,2))       
    linestyles = ['-', '-.', ':', (0, (5,2,1,2,1,2)), (0, (5, 2, 5, 2, 1, 2)), '-', '--', '-.', ':','-', '--', '-.', ':','-', '--', '-.', ':',""]
    markers = ['x','o','s','^','+','h','x','s','^','+',(6,2,30)]

    Fig = plt.figure()
    Ax = Fig.add_subplot(1,1,1)
    Ax.plot(Xdata_cii,Ydata_cii, color=colors[0], linestyle=linestyles[0], marker=markers[0], label=Legend[0])
    Ax.plot(Xdata_expt,Ydata_expt, color=colors[1], linestyle=linestyles[1], marker=markers[1], label=Legend[1])
    Ax.legend(frameon=True, prop={'size': 16})
    if Figure_name=='COLL': Ax.legend(loc=3)
    Ax.set_xlabel(Xlabel, fontsize=font['size'])
    Ax.set_ylabel(Ylabel, fontsize=font['size'])
    Ax.set_ylim(Limits[0],Limits[1])
    Ax.set_xlim(0.05, 0.30)    
    Ax.set_xticks(np.linspace(0.05,0.30,6,endpoint=True))
    Ax.tick_params(axis='both', labelsize=font['size'])
    Ax.grid(True)
    if Figure_name=='COLL' or Figure_name=='LATCYC' or Figure_name=='LONGCYC':
        yticks_values=Ax.get_yticks()
#        Ax.set_yticklabels([r"${:.1f}^{\circ}$".format(_) for _ in yticks_values])
        fmt = '%.'+str(1)+'f°'     
        yticks = mtick.FormatStrFormatter(fmt)
        plt.gca().yaxis.set_major_formatter(yticks)
    Fig.savefig(Directory+'/'+Figure_name+'.pdf', bbox_inches='tight')
    print('saved: ', Figure_name)
    plt.close(Fig)
    
def xy_plot_widgets_all_lines(Fig,Ax,Title,Xdata,Ydata,Legend,Xlabel,Limits):
    f = interp1d(Xdata, Ydata, kind='cubic')
    Xdata_smooth = np.linspace(min(Xdata), max(Xdata), 3*len(Xdata))
    Ydata_smooth = f(Xdata_smooth)
    
    line, = Ax.plot(Xdata_smooth, Ydata_smooth, '-', label=Legend, visible=False)
    Ax.set_title(Title, fontsize=9,fontweight='bold',y=1.0) 
    #Ax.legend()
    if Xlabel=='\Psi':    
        Ax.set_xlabel(Xlabel,fontweight='bold')
        Ax.set_xlim(0.0, 360.0)    #This needs to be changed if output of a non-azimuthal quantity is being plotted
        Ax.set_xticks([0,45,90,135,180,225,270,315,360])
    elif Xlabel=='r/R':
        Ax.set_xlabel(Xlabel,fontweight='bold')
        Ax.set_xlim(0.0, 1.0)    #This needs to be changed if output of a non-azimuthal quantity is being plotted
        Ax.set_xticks(np.linspace(0.0,1.0,5,endpoint=True))            
    Ax.xaxis.grid(True)
    if Limits and Limits[0]!=Limits[1]: 
        #Limits=[math.floor(Limits[0]/50)*50,math.ceil(Limits[1]/50)*50]
        Ax.set_ylim(Limits[0], Limits[1])      #if there are entries in Limits and the entries are not equal (if they are equal an warning is thrown)
        Ax.set_yticks(np.linspace(Limits[0],Limits[1],5,endpoint=True))
    #plt.show()    
    return line


def save_this_subplot_as_fig_2(Figure_name,Xdata,Ydata,Limits,Directory,Ylabel):
    Axislabel_size=17
    Ticklabel_size=13
    Fig = plt.figure()
    Ax = Fig.add_subplot(1,1,1)
    Xlabel=r'$\psi$'
    f = interp1d(Xdata, Ydata, kind='cubic')
    Xdata_smooth = np.linspace(min(Xdata), max(Xdata), 3*len(Xdata))
    Ydata_smooth = f(Xdata_smooth)    
    Ax.plot(Xdata_smooth,Ydata_smooth)
    Ax.set_xlabel(Xlabel, fontsize=Axislabel_size)
    Ax.set_ylabel(Ylabel, fontsize=Axislabel_size)
    Ax.set_xlim(min(Xdata), max(Xdata))    
    xticks=np.linspace(min(Xdata),max(Xdata),7,endpoint=True).tolist()
    xticklabels=[str("{:.0f}".format(tick))+r"$\degree$" for tick in xticks]
    Ax.set_xticks(np.linspace(min(Xdata),max(Xdata),7,endpoint=True))
    Ax.set_xticklabels(xticklabels)
    yticks=Ax.get_yticks(minor=False)
    yticklabels=[str("{:.1f}".format(tick)) for tick in yticks]
    if '[deg]' in  Ylabel:            
        yticklabels=[ticklabel+r"$\degree$" for ticklabel in yticklabels] #Adding degrees symbol to the Z-axis ticks        
        Ylabel=Ylabel.replace(' [deg]','')    #removing '[deg]' from Z-axis label
        Ax.set_yticklabels(yticklabels)  
        Ax.set_ylabel(Ylabel, fontsize=Axislabel_size)
    if 'MINUS_BASELINE' in Directory: Ax.set_ylabel(r'$\Delta$'+Ylabel, labelpad=18)                    #Adding a delta symbol to the label if the plot corrresponds to a delta quantity
    Ax.tick_params(axis='both', labelsize=Ticklabel_size)
    Fig.savefig(Directory+'/'+Figure_name+'.png', bbox_inches='tight')
    print('saved: ', Figure_name)
    plt.close(Fig)

def save_as_fig_together(Ax,Xdata,Ydata,Label):
    f = interp1d(Xdata, Ydata, kind='cubic')
    Xdata_smooth = np.linspace(min(Xdata), max(Xdata), 3*len(Xdata))
    Ydata_smooth = f(Xdata_smooth)    
    if Label=='Baseline':
        Ax.plot(Xdata_smooth,Ydata_smooth,'--k',label=Label)
    else:
        Ax.plot(Xdata_smooth,Ydata_smooth,label=Label)
    Ax.set_xlim(min(Xdata), min(Xdata)) 
    xticks=np.linspace(min(Xdata),max(Xdata),7,endpoint=True).tolist()
    xticklabels=[str("{:.0f}".format(tick))+r"$\degree$" for tick in xticks]
    Ax.set_xticks(np.linspace(min(Xdata),max(Xdata),7,endpoint=True))
    Ax.set_xticklabels(xticklabels)


def TEF_deflection_profile(Ax,Xdata,Ydata,Label,Color,Fontsize_dict):

    Ax.plot(Xdata,Ydata,color=Color)    
    # Ax.yaxis.set_rotate_label(False)
    Ax.legend(frameon=False, prop={'size': Fontsize_dict['Legend_size']})    
    Ax.set_xlim(min(Xdata), max(Xdata))    
    xticks=np.linspace(min(Xdata),max(Xdata),5,endpoint=True).tolist()
    xticklabels=[str("{:.0f}".format(tick))+r"$^\circ$" for tick in xticks]
    Ax.set_xticks(xticks)
    Ax.set_xticklabels(xticklabels)
    Ax.set_ylim(-5,10)
    yticks=Ax.get_yticks(minor=False)
    yticklabels=[str("{:.0f}".format(tick))+r"$^\circ$" for tick in yticks]
    Ax.set_yticklabels(yticklabels)  
    Ax.tick_params(axis='both', labelsize=Fontsize_dict['Ticklabel_size'])    
    Ax.set_xlabel(r'$\psi$', fontsize=Fontsize_dict['Axislabel_size'])
    Ax.set_ylabel(r'$\delta$', fontsize=Fontsize_dict['Axislabel_size'])

    Ax.grid(True)

def tecplot_together(Ax, Xdata, Ydata, Linestyl, Legend):
    Ax.plot(Xdata,Ydata, Linestyl,label=Legend)

def tecplot_separately(Directory, Figure_name, Xdata, Ydata, Linestyl, Legend, Xlabel, Ylabel, Limits_dict):
    Fig = plt.figure()
    Ax = Fig.add_subplot(1,1,1)
    Ax.plot(Xdata,Ydata,Linestyl,label=Legend)
    Ax.legend(frameon=False)
    Ax.set_xlabel(Xlabel)
    Ax.set_ylabel(Ylabel)
    if Limits_dict['X']: Ax.set_xlim(Limits_dict['X'][0], Limits_dict['X'][1])  
    if Limits_dict['Y']: Ax.set_ylim(Limits_dict['Y'][0], Limits_dict['Y'][1])
    #Ax.set_xticks(np.linspace(min(Xdata),max(Xdata),7,endpoint=True))    
    Fig.savefig(Directory+'/'+Figure_name+'.pdf', bbox_inches='tight')
    print('saved figure '+ Figure_name+'.pdf')











































































































