#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
(Single observer)
Accepts path to finished acoustics PSU-WOPWOP files and generates (and saves) 
acoustic pressure and spectrum results
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from HeliNoise.utl import tecplot

def xy_tecplot_separately(Directory, Figure_name, Xdata, Ydata, Linestyl, Legend, Xlabel, Ylabel, Limits_dict):
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
    

################    variables to set prior to execution    ####################

directory='../Data/PSU_WOPWOP/PSU-WOPWOP_new/SingleObserver_50m/below/0.750_0.300_1.960_000.0_0.000_355.0_0.980_0.0_0.0_0.0_0.0_0.0_0.0_highresAero_hartstyl/0.750_0.300_1.960_000.0_0.000_355.0_0.980_0.0_0.0_0.0_0.0_0.0_0.0_highresAero_hartstyl/'
directory='./'
#quantities=['Thickness']                                                       #noise components available in *.tec files 
quantities=['Thickness','Loading','Total']
plot_together=True                                                             #plot all quantities in one plot
frequency_in_bpf = True
time_in_azimuth = False

#### leave expty for default limits to plots
lim_p_dict = {'X':[0.0,0.1412],'Y':[-2.0,1.0]}
lim_spl_dict ={'X':[0,50],'Y':[-40,90]}
fontsize_dict={'Axislabel_size':10,'Ticklabel_size':10,'Legend_size':9}
###############################################################################

rot_freq_hz = 4*7.083349897247894   #Bo 105 BPF                               
#rot_freq_hz = 4*109.028/(2*np.pi)   #HART II BPF                              
#rot_freq_hz = 3*30.04796/(2*np.pi)   #case1, case5
#rot_freq_hz = 109.028/(2*np.pi)   #case2 BPF

filename_pressure=directory+'pressure.tec'
filename_spectrum=directory+'spl_spectrum.tec'

Data_pressure = tecplot.read_tecfile(filename_pressure)
Data_spectrum = tecplot.read_tecfile(filename_spectrum)

if plot_together:
    Fig_p = plt.figure(figsize=(2.913,1.897))
    Ax_p = Fig_p.add_subplot(1,1,1)
    Fig_spl = plt.figure(figsize=(2.913,1.897))
    Ax_spl = Fig_spl.add_subplot(1,1,1)

for idx, quantity in enumerate(quantities,1):

    if time_in_azimuth:
        xdata_p=Data_pressure[:,0]     #this needs to be modified
        xlabel_p = 'Rotor azimuth (deg)'
    else:
        xdata_p=Data_pressure[:,0] 
        xlabel_p = 'Time (s)'
    ydata_p=Data_pressure[:,idx]
    ylabel_p = 'Acoustic pressure (Pa)'
    
    if frequency_in_bpf:
        xdata_spl=Data_spectrum[:,0]/rot_freq_hz    #frequency relative to the BPF 
        xlabel_spl='Frequency (BPF)'
    else:
        xdata_spl=Data_spectrum[:,0]    #absolute frequency in Hz
        xlabel_spl='Frequency (Hz)'
    ydata_spl=Data_spectrum[:,idx]
    ylabel_spl = ' Sound level (dB)'

    legend=quantity
    if plot_together:
        Ax_p.plot(xdata_p,ydata_p,label=legend)
        Ax_spl.plot(xdata_spl,ydata_spl,label=legend)
    else:
        xy_tecplot_separately(directory,quantity+'_pressure',xdata_spl,ydata_spl,'-*',legend, xlabel_spl, ylabel_spl, lim_spl_dict)
        xy_tecplot_separately(directory,quantity+'_spectrum',xdata_p,ydata_p,'-',legend, xlabel_spl, ylabel_spl, lim_p_dict)

if plot_together:    
    Ax_p.legend(frameon=False, prop={'size': fontsize_dict['Legend_size']})
    
#    Ax_p.set_xlim(min(xdata_p), max(xdata_p)) 
    Ax_p.set_xlim(lim_p_dict['X'][0], lim_p_dict['X'][1]) 
    Ax_p.set_ylim(lim_p_dict['Y'][0], lim_p_dict['Y'][1]) 
    Ax_p.set_xlabel(xlabel_p,fontsize=fontsize_dict['Axislabel_size'])
    Ax_p.set_ylabel(ylabel_p,fontsize=fontsize_dict['Axislabel_size'])
    Ax_p.tick_params(axis='both', labelsize=fontsize_dict['Ticklabel_size'])
    Ax_p.grid(axis='both')
    
    Ax_spl.legend(frameon=False, prop={'size': fontsize_dict['Legend_size']})
    Ax_spl.set_xlabel(xlabel_spl,fontsize=fontsize_dict['Axislabel_size'])
    Ax_spl.set_ylabel(ylabel_spl,fontsize=fontsize_dict['Axislabel_size'])
    Ax_spl.set_xlim(lim_spl_dict['X'][0], lim_spl_dict['X'][1]) 
    Ax_spl.set_ylim(lim_spl_dict['Y'][0], lim_spl_dict['Y'][1]) 
    Ax_spl.tick_params(axis='both', labelsize=fontsize_dict['Ticklabel_size'])
    Ax_spl.grid(axis='both')

    Fig_p.savefig(directory+'/Pressure.pdf', bbox_inches='tight')
    print('saved figure Pressure.pdf')
    Fig_spl.savefig(directory+'/Spectrum.pdf', bbox_inches='tight')
    print('saved figure Spectrum.pdf')
    Fig_p.savefig(directory+'/Pressure.png', bbox_inches='tight')
    print('saved figure Pressure.png')
    Fig_spl.savefig(directory+'/Spectrum.png', bbox_inches='tight')
    print('saved figure Spectrum.png')
    

