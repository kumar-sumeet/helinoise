#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 19:45:17 2020

@author: sumeetkumar
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import numpy as np
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from HeliNoise.CII import CII_extract_all
from HeliNoise.plot import make_pretty, plot_details, XY_plot
plt.rcParams.update(make_pretty.set_font_settings('AIAA_SciTech'))


Filepaths_dict = {
                  'Baseline':'../../Data_SciTech_2021/CII/Camrad_files/best_cases_journal_paper/baseline_highresAero.out',
                  '1P':'../../Data_SciTech_2021/CII/Camrad_files/best_cases_journal_paper/0.700_0.400_3.160_278.0_2.440_0.0_0.0_0.0_0.0_0.0_0.0_0.0_0.0.out',
                  '2P':'../../Data_SciTech_2021/CII/Camrad_files/best_cases_journal_paper/0.750_0.300_1.960_000.0_0.000_355.0_0.980_0.0_0.0_0.0_0.0_0.0_0.0.out',
                  '1P+2P':'../../Data_SciTech_2021/CII/Camrad_files/best_cases_journal_paper/0.700_0.400_3.100_322.0_3.530_267.0_1.116_0.0_0.0_0.0_0.0_0.0_0.0.out',
                  }

Dir_save_plots='./'
Fig_name='TEF_profiles'
Fontsize_dict={'Axislabel_size':15,'Ticklabel_size':13,'Legend_size':14}
Pack_TEF_harm_together=True # plot the bars packed together without empty spaces

bar_width=0.1

COLORS = plot_details.get_colors_lst() 
COLORS_dim = plot_details.get_dimcolors_lst()

All_CII_data_dict = {}
for file_key, filepath in Filepaths_dict.items():
    All_CII_data_dict[file_key] = CII_extract_all.cii_extract_all(filepath)

Fig_TEF = plt.figure(figsize=(10,3.5))
Gs_TEF = gridspec.GridSpec(1, 2, figure=Fig_TEF)
Ax_TEF_profile = Fig_TEF.add_subplot(Gs_TEF[0])
Ax_TEF_harm = Fig_TEF.add_subplot(Gs_TEF[1])
Deflection_profile_harm,Deflection_profile_harm_together,Deflection_profile_harm_all={},{},{}

COLORS_DICT={}
index_examp=6
COLORS=COLORS[:index_examp]+COLORS_dim[index_examp-1:]
for color_index,filename in enumerate(All_CII_data_dict):    
    COLORS_DICT[filename]=COLORS[color_index]
TEF_input_harmonics_labels=[r'$A_{0P}$',r'$A_{1P}$',r'$A_{2P}$']
Azimuth = np.arange(0,360+360.0/100,360.0/100)
count=0
Xdata_tef_together=np.arange(1,7).tolist()
for filename in All_CII_data_dict:
    if 'Baseline' in filename: continue         #Dont calculate the Baseline TEF deflection profile 
    #These entries are in terms of MCC
    Cosine_amp = All_CII_data_dict[filename]['IBC_HHC_INPUT']['TEF_INPUT']['Cosine']
    Sine_amp = All_CII_data_dict[filename]['IBC_HHC_INPUT']['TEF_INPUT']['Sine']
    Mean_amp = All_CII_data_dict[filename]['IBC_HHC_INPUT']['TEF_INPUT']['Mean']
    #Converting to degrees
    Cosine_amp_deg = [(180/3.14)*(np.arctan(cos_value*2/25)) for cos_value in Cosine_amp]
    Sine_amp_deg = [(180/3.14)*(np.arctan(sin_value*2/25)) for sin_value in Sine_amp]
    Mean_amp_deg = (180/3.14)*(np.arctan(Mean_amp*2/25))
    Deflection_profile = Azimuth*0
    Deflection_profile = Deflection_profile+Mean_amp_deg    
    freq = 1
    for sin_value_deg, cos_value_deg in zip(Sine_amp_deg,Cosine_amp_deg):
        Deflection_profile = Deflection_profile + cos_value_deg*np.cos(freq*((np.pi)/180)*Azimuth) + sin_value_deg*np.sin(freq*(np.pi/180)*Azimuth)
        freq = freq+1
    labl=filename

    XY_plot.TEF_deflection_profile(Ax_TEF_profile,Azimuth,Deflection_profile,labl,COLORS_DICT[filename],Fontsize_dict)


####    Plotting the harmonics of active control input
    Deflection_profile_harm[filename]={'MEAN':Mean_amp_deg}
    Deflection_profile_harm_all[filename]=[Mean_amp_deg]
    #harm=1
    for cos,sin,harm_str in zip(Cosine_amp_deg,Sine_amp_deg,TEF_input_harmonics_labels):
        Deflection_profile_harm[filename][harm_str]=(cos*cos+sin*sin)**0.5
        Deflection_profile_harm_all[filename].append((cos*cos+sin*sin)**0.5)
        #harm+=1

    ylabel='Active Control Input'
    xlabel='Harmonics'

    for bar_no,harm_str in enumerate(TEF_input_harmonics_labels,1):
        Deflection_profile_harm_together[harm_str]={}
        for filename in Deflection_profile_harm:
            if harm_str in Deflection_profile_harm[filename] and Deflection_profile_harm[filename][harm_str]!=0:       #Only plotting the non-zero harmonics
                Deflection_profile_harm_together[harm_str][filename]=Deflection_profile_harm[filename][harm_str]
        xdata=np.arange(bar_no,bar_no+len(Deflection_profile_harm_together[harm_str])*bar_width,bar_width)

  
    ydata=Deflection_profile_harm_all[filename]
    shift_minor=bar_width*count
    xdata=np.arange(1+shift_minor,1+len(ydata)).tolist()

    if Pack_TEF_harm_together:
        ydata_new,xdata_new=[],[]
        for index, value in enumerate(ydata): 
            if value==0.0: continue 
            else: 
                ydata_new.append(value)
                xdata_new.append(Xdata_tef_together[index])
        Xdata_tef_together_remain=list(set(Xdata_tef_together)-set(xdata_new))
        Xdata_tef_together=Xdata_tef_together_remain+[bar_width+coord for coord in xdata_new]
        Xdata_tef_together.sort()
        Ax_TEF_harm.bar(xdata_new, ydata_new, bar_width,color=COLORS_DICT[filename],label=labl,zorder=3) 
    else:   
        Ax_TEF_harm.bar(xdata, ydata, bar_width,color=COLORS_DICT[filename],label=labl) 
        count+=1
        Ax_TEF_harm.set_xticks(np.arange(1+ (len(All_CII_data_dict)-2)*bar_width / 2,1+len(TEF_input_harmonics_labels)))
        Ax_TEF_harm.set_xticklabels(TEF_input_harmonics_labels, pad=10)

if Pack_TEF_harm_together:
    Ax_TEF_harm.set_xticks(np.array(Xdata_tef_together)-0.5*(np.array(Xdata_tef_together)-np.arange(1,1+len(Xdata_tef_together)))-0.5*bar_width)
    Ax_TEF_harm.set_xticklabels(TEF_input_harmonics_labels)
    
Ax_TEF_harm.set_xlabel(xlabel, fontsize=Fontsize_dict['Axislabel_size'])    
# Ax_TEF_harm.set_ylabel(ylabel, fontsize=Fontsize_dict['Axislabel_size'])    
Ax_TEF_harm.tick_params(axis='x', which='major', pad=10)
Ax_TEF_harm.set_xlim(0.5,3.5)
Ax_TEF_harm.set_ylim(0,5)
Ax_TEF_harm.grid(zorder=0)
yticks=Ax_TEF_harm.get_yticks(minor=False)
Ax_TEF_harm.set_yticklabels([r"${:.0f}^\circ$".format(_) for _ in yticks])
Ax_TEF_harm.tick_params(axis='both', labelsize=Fontsize_dict['Ticklabel_size'])
Legends_all=Ax_TEF_harm.legend(frameon=False, prop={'size': Fontsize_dict['Legend_size']},loc='center left',bbox_to_anchor=(1.1, 0.5))        
    
for legnd in Legends_all.get_texts()[index_examp-1:]:    legnd.set_color('gray')
    
Gs_TEF.tight_layout(Fig_TEF)        #Ensures no subplots overlap
Fig_TEF.savefig(f'{Dir_save_plots}/{Fig_name}.pdf', bbox_inches='tight')

print('saved: ', 'TEF deflection profiles and harmonics')
