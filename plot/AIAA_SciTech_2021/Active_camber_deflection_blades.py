#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:55:35 2020

@author: ge56beh
"""
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sys
sys.path.append('./CII')
import CII_extract_all
sys.path.append('./plot')

cii_filepath = './PSU_WOPWOP/PSU-WOPWOP_new/baseline/Camrad_files/Best_cases_journal_paper/0.700_0.400_3.100_322.0_3.530_267.0_1.116_0.0_0.0_0.0_0.0_0.0_0.0_highresAero.out'
CII_output_data_dict=CII_extract_all.cii_extract_all(cii_filepath)                                                               #extracting all relevant data from the CII output file as a dict


time_period = 2*(np.pi)/CII_output_data_dict['SPEED']['OMEGA (RAD/SEC)']            
no_aero_time_steps = 1+CII_output_data_dict['TIME_STEP'][4]     #number of time steps in the airloads sensors info
time_steps_aero = np.linspace(0,time_period,no_aero_time_steps)                                  
no_motion_time_steps = 1+CII_output_data_dict['TIME_STEP'][3]     #number of time steps in the position sensors info

Fig_TEF = plt.figure(figsize=(18,10))
Gs_TEF = gridspec.GridSpec(2, 2, figure=Fig_TEF)
Ax = [Fig_TEF.add_subplot(gstef) for gstef in Gs_TEF]

for blade_no in [1,2,3,4]:
    fishbac_deflection = np.zeros_like(time_steps_aero)
    fishbac_deflection_cosine = np.zeros_like(time_steps_aero)
    fishbac_deflection_sine = np.zeros_like(time_steps_aero)
    # print(fishbac_deflection)
    if CII_output_data_dict['OPTEF']:    
        cii_tef_input = CII_output_data_dict['IBC_HHC_INPUT']['TEF_INPUT']
        if 'Cosine' in cii_tef_input:
            # print('blade no =', blade_no)
            for n,(delta_c,delta_s) in enumerate(zip(cii_tef_input['Cosine'],cii_tef_input['Sine']),1):
                print(n)
                print(delta_c,delta_s)
                fishbac_deflection_cosine += delta_c*np.cos(n*(2*np.pi*time_steps_aero/time_period+blade_no*np.pi/2))
                fishbac_deflection_sine += delta_s*np.sin(n*(2*np.pi*time_steps_aero/time_period+blade_no*np.pi/2))
                fishbac_deflection +=fishbac_deflection_cosine+fishbac_deflection_sine
                
        if 'Mean' in cii_tef_input:
            
            # print('blade no =', blade_no)
            # print(cii_tef_input['Mean'])
            # print('\n')
            fishbac_deflection += cii_tef_input['Mean']
            # print(fishbac_deflection)
    # time.sleep(10)
    Ax[0].plot((180/np.pi)*np.linspace(0,2*np.pi,no_motion_time_steps,endpoint=True),fishbac_deflection,label=str(blade_no))
    Ax[1].plot((180/np.pi)*np.linspace(0,2*np.pi,no_motion_time_steps,endpoint=True),fishbac_deflection_cosine,label=str(blade_no))
    Ax[2].plot((180/np.pi)*np.linspace(0,2*np.pi,no_motion_time_steps,endpoint=True),fishbac_deflection_sine,label=str(blade_no))

for ax in Ax:
    ax.grid()
    ax.legend()