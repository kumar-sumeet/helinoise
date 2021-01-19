#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 12:10:44 2020

@author: SumeetKumar
"""

import matplotlib.pyplot as plt
plt.ioff()
# plt.style.use('seaborn')
import os
import numpy as np
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from utl import crawler,cii
from plot import make_pretty, plot_details
# plt.rcParams.update(make_pretty.set_font_settings('AIAA_scitech'))

##############################################################################################################################################################################################################################################################################
####################################    Necessary input information    #######################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################
DesignVar_list=['R','DELTA-R','DELTA-MIN','PHI-1P','A-1P','PHI-2P','A-2P']#,'PHI-3P','A-3P','PHI-4P','A-4P','PHI-5P','A-5P'] #There need to be atleast 3 variables here
Data_dir = '/home/HT/ge56beh/Work/Python/Acoustics/Data/CII/Camrad_files/ibc_cases'
All_filepath_dict,All_filenames_dict = crawler.get_files_info(Data_dir)
All_data_dict,DesignVar_ranges_dict = crawler.get_cii_output(Data_dir,All_filepath_dict,All_filenames_dict,Read_pckl=True,DesignVar=DesignVar_list)    
Vib_power_dict = cii.vib_power(All_data_dict)

Default_set_of_values=['0.700','0.400','0.000','000.0','0.000','0.000','0.000','0.000','0.000','0.000','0.000','0.000','0.000']
# Default_set_of_values=['0.700','0.400','0.000','000.0','0.000','000.0','0.000','0.000','0.000','0.000','0.000','0.000','0.000']

Var_1='A-2P'    #this variable is kept constant for one sweep of VAR_2; name based on that used in Design_variables
Var_2='PHI-2P'    #sweep variable
Var_3=['delta_Mz%','delta_Fz%','delta_In_plane_Hub_Shear%','delta_In_plane_Hub_Moment%' ]           #Z-axis; 

Limits={'J':[0,10],'J_Mz':[0,10],
        'CP':[0.0003,0.00055],'mu':[0,0.4],
        'delta_CP%':[-10,20],'delta_J%':[-100,400],
        'delta_Mz%':[-70,70],'delta_Fz%':[-70,70],'delta_In_plane_Hub_Shear%':[-70,70],'delta_In_plane_Hub_Moment%':[-70,70],
        'PHI-1P':[0,360],'PHI-2P':[0,360],
        'Torsion':[-300,400],'Flap':[],'Lag':[],'Axial':[],'Chord':[],'Norm':[-400,450],
        'Delta_Torsion':[-250,150],'Delta_Flap':[],'Delta_Lag':[],'Delta_Axial':[],'Delta_Chord':[],'Delta_Norm':[]}
YLimits_fig={'fig5':[-50,70],'fig6':[-80,20],'fig13':[-100,300],'fig16':[-737.56,1844],'fig20':[-50,200],'fig21':[-40,40]}
XLimits_fig={'fig5':[0,360],'fig6':[0,3.0],'fig13':[0,250],'fig16':[-1106,1475],'fig20':[0,360],'fig21':[0,3]}
Ticks_number={'delta_CP%':7,'delta_J%':6,'PHI-2P':7,'PHI-1P':7}
LABELS = plot_details.get_labels_dict()
LIMITS = plot_details.get_limits_dict()
COLORS = plot_details.get_colors_lst() 

COLORS=['blue','red','green','darkorange','limegreen','gold','gray','dimgray','dodgerblue','limegreen','teal','burlywood', 'plum', 'lightblue', 'peru','greenyellow'] # CHOOSE FROM THIS LIST obtained from--> https://matplotlib.org/gallery/color/named_colors.html
LIMITS_percent={'CP':[-4,10],'Fx':[],'Fy':[],'Fz':[],'Mx':[],'My':[],'Mz':[],'In-plane Hub Moment': [],'In-plane Hub Shear':[],'J':[-100,300],'J_abs':[],'J_Mz':[]}

All_plots_data_dict={}

Axislabel_size=21
Ticklabel_size=15
Legend_size=15

label_show=True

# for mu in All_data_dict:
for mu,figname in {'0.10_-2.4':'fig5','0.30_-7.6':'fig13','0.10_4.0':'fig20'}.items():    
    
    
    for _,amp in enumerate(DesignVar_ranges_dict[mu][Var_1]):
        Fig=plt.figure(figsize=make_pretty.set_size('AIAA_scitech',fraction=1))
        Ax = Fig.add_subplot(1,1,1)
        if amp!=1.0: continue #this is validation specific
        # if amp not in [0.5,1.0,1.5,2.0,2.5]: continue
                
        filename_set_of_values = Default_set_of_values.copy()
        
        for color_idx,var in enumerate(Var_3):
            filename_set_of_values[DesignVar_list.index(Var_1)]=format(amp,'.3f') 
            phidata=[]
            quantdata=[]
            for phi in DesignVar_ranges_dict[mu][Var_2]:
                filename_set_of_values[DesignVar_list.index(Var_2)]=format('%05.1f' % phi) 
                filename='_'.join(filename_set_of_values)
                if filename_set_of_values==Default_set_of_values: filename='Baseline'
                print('filename-->', filename)
                if filename in Vib_power_dict[mu]: 
                    print('filename-->', filename)
                    phidata.append(phi)
                    quantdata.append(Vib_power_dict[mu][filename][var])
            if phidata:
                phidata.append(360)
                quantdata.append(quantdata[0])
            # if label_show: label=var  
            label=var  
            print('quantdata-->',quantdata)
            Ax.plot(phidata,quantdata,marker='*',color=COLORS[color_idx], linestyle='-',label=label)
        # label_show=False
        # label=None        
        Ax.set_xlabel(LABELS[Var_2]+' ['+r'$\degree$'+']',labelpad=25, fontsize=Axislabel_size)
        Ax.set_ylabel('% Chnage in 4/rev Hub Vibration',labelpad=15, fontsize=Axislabel_size)
        Ax.set_xlim(lim for lim in XLimits_fig[figname])
        Ax.set_ylim(lim for lim in YLimits_fig[figname])
        Ax.grid(True)
        for t in Ax.xaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
        for t in Ax.yaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
        Ax.legend()
        # Fig.savefig(f'{Data_dir}/Figures_vibration/WJ2_{figname}_{amp}deg'+'.png', bbox_inches='tight', facecolor=Fig.get_facecolor(), transparent=True)
        Fig.savefig(f'{Data_dir}/Figures_vibration/WJ2_{figname}_{amp}deg'+'.pdf', bbox_inches='tight', facecolor=Fig.get_facecolor(), transparent=True)
        print('saved: ',f'WJ2_{figname}_{amp}deg')
        plt.close(Fig)


# for mu in All_data_dict:
for mu,figname in {'0.10_-2.4':'fig6','0.10_4.0':'fig21'}.items():          
    Fig=plt.figure(figsize=make_pretty.set_size('AIAA_scitech',fraction=1))
    Ax = Fig.add_subplot(1,1,1)
    for color_idx,var in enumerate(Var_3):        
        filename_set_of_values = Default_set_of_values.copy()
        ampdata=[]
        phi=60
        filename_set_of_values[DesignVar_list.index(Var_2)]=format('%05.1f' % phi) 
        quantdata=[]
        for _,amp in enumerate(DesignVar_ranges_dict[mu][Var_1]):                
            filename_set_of_values[DesignVar_list.index(Var_1)]=format(amp,'.3f') 
            filename='_'.join(filename_set_of_values)
            if filename_set_of_values==Default_set_of_values: filename='Baseline'
            print('filename-->', filename)
            if filename in Vib_power_dict[mu]: 
                print('filename-->', filename)
                ampdata.append(amp)
                quantdata.append(Vib_power_dict[mu][filename][var])
        print('ampdata-->',ampdata)
        print('quantdata-->',quantdata)
        Ax.plot(ampdata,quantdata,marker='*',color=COLORS[color_idx], linestyle='-',label=var)
    Ax.set_xlabel('Amp',labelpad=25, fontsize=Axislabel_size)
    Ax.set_ylabel(LABELS[var],labelpad=15, fontsize=Axislabel_size)
    Ax.set_xlim(lim for lim in XLimits_fig[figname])
    Ax.set_ylim(lim for lim in YLimits_fig[figname])
    Ax.legend()
    Ax.grid(True)
    # Fig.savefig(f'{Data_dir}/Figures_vibration/WJ2_{figname}_{amp}deg'+'.png', bbox_inches='tight', facecolor=Fig.get_facecolor(), transparent=True)
    Fig.savefig(f'{Data_dir}/Figures_vibration/WJ2_{figname}_{phi}deg'+'.pdf', bbox_inches='tight', facecolor=Fig.get_facecolor(), transparent=True)
    print('saved: ',f'WJ2_{figname}_{phi}deg')
    plt.close(Fig)


# for mu in All_data_dict:
for mu,figname in {'0.30_-7.6':'fig16'}.items():    
    Fig=plt.figure(figsize=make_pretty.set_size('AIAA_scitech',fraction=1))
    Ax = Fig.add_subplot(1,1,1)    
    amp=1.0             
    filename_set_of_values = Default_set_of_values.copy()        
    filename_set_of_values[DesignVar_list.index(Var_1)]=format(amp,'.3f') 
    phidata=[]
    quantdata=[]
    for phi in DesignVar_ranges_dict[mu][Var_2]:
        filename_set_of_values[DesignVar_list.index(Var_2)]=format('%05.1f' % phi) 
        filename='_'.join(filename_set_of_values)
        if filename_set_of_values==Default_set_of_values: filename='Baseline'
        print('filename-->', filename)
        if filename in Vib_power_dict[mu]: 
            print('filename-->', filename)
            phidata.append(phi)
            quantdata.append([Vib_power_dict[mu][filename]['My_sine'],Vib_power_dict[mu][filename]['My_cosine']])
    if phidata:
        phidata.append(360)
        quantdata.append(quantdata[0])
    print('quantdata-->',quantdata)
    Ax.plot(np.array(quantdata)[:,0],np.array(quantdata)[:,1],marker='*', linestyle='-')
    Ax.set_xlabel('My_sine',labelpad=25, fontsize=Axislabel_size)
    Ax.set_ylabel('My_cosine',labelpad=15, fontsize=Axislabel_size)
    for t in Ax.xaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
    for t in Ax.yaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
    # Fig.savefig(f'{Data_dir}/Figures_vibration/WJ2_{figname}_{amp}deg'+'.png', bbox_inches='tight', facecolor=Fig.get_facecolor(), transparent=True)
    Ax.set_xlim(lim for lim in XLimits_fig[figname])
    Ax.set_ylim(lim for lim in YLimits_fig[figname])
    Ax.grid(True)
    Fig.savefig(f'{Data_dir}/Figures_vibration/WJ2_{figname}_{amp}deg'+'.pdf', bbox_inches='tight', facecolor=Fig.get_facecolor(), transparent=True)
    print('saved: ',f'WJ2_{figname}_{amp}deg')
    plt.close(Fig)

