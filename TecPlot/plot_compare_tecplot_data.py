#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 08:37:37 2020

@author: sumeetkumar
"""

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

from HeliNoise.utl import tecplot

dir_dict = {
            'Baseline':'./PSU_WOPWOP/PSU_WOPWOP_new/baseline_hartstyl/baseline_hartstyl/',
            'Highres':'./PSU_WOPWOP/PSU_WOPWOP_new/baseline_highresAero_hartstyl/baseline_highresAero_hartstyl/',
            }



#quantities=['Thickness']                                                       #noise components available in *.tec files 
quantities=['Thickness','Loading','Total']
plot_together=True                                                             #plot all quantities in one plot
frequency_in_bpf = True
time_in_azimuth = False

#### leave expty for default limits to plots
lim_p_dict = {'X':[0.0,0.1412/4],'Y':[-2.0,1.5]}
lim_spl_dict ={'X':[0,50],'Y':[-40,90]}
fontsize_dict={'Axislabel_size':10,'Ticklabel_size':10,'Legend_size':9}
###############################################################################

rot_freq_hz = 4*7.083349897247894   #Bo 105 BPF                               #used to non-dimensionalize the acoustics frequencies 
#rot_freq_hz = 4*109.028/(2*np.pi)   #HART II BPF                              #used to non-dimensionalize the acoustics frequencies 
#rot_freq_hz = 3*30.04796/(2*np.pi)   #case1, case5
#rot_freq_hz = 109.028/(2*np.pi)   #case2 BPF

for idx,quantity in enumerate(quantities,1):
    Fig_p = plt.figure(figsize=(2.913,1.897))
    Ax_p = Fig_p.add_subplot(1,1,1)
    Data_OASPLdBA = []
    for label,directory in dir_dict.items():
        print(label)
        filename_pressure=directory+'pressure.tec'
        filename_OASPLdBA=directory+'OASPLdBA.tec'
        
        Data_pressure = tecplot.read_tecfile(filename_pressure)
        Data_OASPLdBA.append(tecplot.read_tecfile_OASPLdB(filename_OASPLdBA)[0])
        
        if time_in_azimuth:
            xdata_p=Data_pressure[:,0]     #this needs to be modified
            xlabel_p = 'Rotor azimuth (deg)'
        else:
            xdata_p=Data_pressure[:,0] 
            xlabel_p = 'Time (s)'
        ydata_p=Data_pressure[:,idx]
        ylabel_p = 'Acoustic pressure (Pa)'

        Ax_p.plot(xdata_p,ydata_p,label=label)
        
    Ax_p.legend(frameon=False, prop={'size': fontsize_dict['Legend_size']})
    
#    Ax_p.set_xlim(min(xdata_p), max(xdata_p)) 
    Ax_p.set_xlim(lim_p_dict['X'][0], lim_p_dict['X'][1]) 
    Ax_p.set_ylim(lim_p_dict['Y'][0], lim_p_dict['Y'][1]) 
    Ax_p.set_xlabel(xlabel_p,fontsize=fontsize_dict['Axislabel_size'])
    Ax_p.set_ylabel(ylabel_p,fontsize=fontsize_dict['Axislabel_size'])
    Ax_p.tick_params(axis='both', labelsize=fontsize_dict['Ticklabel_size'])
    Ax_p.grid(axis='both')
    

#    Fig_p.savefig('./PSU_WOPWOP/PSU-WOPWOP_new'+'/'+quantity+'_Pressure.pdf', bbox_inches='tight')
#    print('saved pdf figure')
    Fig_p.savefig('./PSU_WOPWOP/PSU_WOPWOP_new'+'/'+quantity+'_Pressure.png', bbox_inches='tight')
    print('saved png figure')
    

Fig_p_bar = plt.figure(figsize=(4,4))
Ax_p_bar = Fig_p_bar.add_subplot(1,1,1)

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        Ax_p_bar.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


x = np.arange(len(quantities))
width = 0.05
Data_OASPLdBA_arr = np.asarray(Data_OASPLdBA)
for idx,label in enumerate(dir_dict):
    Ax_p_bar.bar(x+(idx-0.5*(len(dir_dict.keys())-1))*width,  Data_OASPLdBA_arr[idx,1:4], width, label=label)
        

#Ax_p_bar.bar(x-1.5*width,  Data_OASPLdBA_arr[0,1:4], width, label='Baseline')
#Ax_p_bar.bar(x - 0.5*width, Data_OASPLdBA_arr[1,1:4], width, label='1P')
#Ax_p_bar.bar(x + 0.5*width,  Data_OASPLdBA_arr[2,1:4], width, label='2P')
#Ax_p_bar.bar(x + 1.5*width, Data_OASPLdBA_arr[3,1:4], width, label='1P+2P')


# Add some text for labels, title and custom x-axis tick labels, etc.
Ax_p_bar.set_ylabel('OASPL (dBA)')
Ax_p_bar.set_xticks(x)
Ax_p_bar.set_xticklabels(quantities)
Ax_p_bar.legend()
#Ax_p_bar.set_xlim(lim_p_dict['X'][0], lim_p_dict['X'][1]) 
Ax_p_bar.set_ylim(40, 80) 
Fig_p_bar.savefig('./PSU_WOPWOP/PSU_WOPWOP_new'+'/'+'_OASPL_dBA.png', bbox_inches='tight')
print('saved png bar figure')
