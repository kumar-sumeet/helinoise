#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 11:33:05 2021

@author: SumeetKumar
"""

import numpy as np

from HeliNoise.FishBAConator import master_morphing

def solverCII(blade_no,CII_output_data_dict):
    time_period = 2*(np.pi)/CII_output_data_dict['SPEED']['OMEGA (RAD/SEC)']
    no_aero_time_steps = 1+CII_output_data_dict['TIME_STEP'][4]
    time_steps_aero = np.linspace(0,time_period,no_aero_time_steps)                                  

    fishbac_deflection = np.zeros_like(time_steps_aero)
    cii_tef_input = CII_output_data_dict['IBC_HHC_INPUT']['TEF_INPUT']
    if 'Cosine' in cii_tef_input:
        for n,(delta_c,delta_s) in enumerate(zip(cii_tef_input['Cosine'],cii_tef_input['Sine']),1):
            fishbac_deflection = fishbac_deflection \
                                 +6*delta_c*np.cos(n*(2*np.pi*time_steps_aero/time_period+blade_no*np.pi/2)) \
                                 +6*delta_s*np.sin(n*(2*np.pi*time_steps_aero/time_period+blade_no*np.pi/2))     #why is this getting multiplied by 6 here???
    if 'Mean' in cii_tef_input:
        fishbac_deflection = fishbac_deflection+cii_tef_input['Mean']
   
    if np.any(fishbac_deflection):
        active_section = CII_output_data_dict['EHTEF']
        for idx,deflection in enumerate(fishbac_deflection): 
            fishbac_coordinate, _, _ = master_morphing.create_fishbac_deformation(deflection_level = deflection)
            if idx ==0:
                fishbac_coordinates =np.expand_dims(fishbac_coordinate,axis=2)            
            else:
                fishbac_coordinates = np.dstack((fishbac_coordinates,fishbac_coordinate))               
    else:
        fishbac_coordinates =None
        active_section = [] 
    
    return fishbac_coordinates, active_section
    
    
def solverDym(blade_no,output_data_dict,no_motion_time_steps):
    fishbac_deflection = output_data_dict['fishbac_deflection'][-no_motion_time_steps:]   
    if np.any(fishbac_deflection):
        for idx,deflection in enumerate(fishbac_deflection): 
            deflection_mcc = deflection*(180/np.pi)*(1/4.5739)    #1MCC = 4.5739 deg
            fishbac_coordinate, _, _ = master_morphing.create_fishbac_deformation(deflection_level = deflection_mcc)
            if idx ==0:
                fishbac_coordinates =np.expand_dims(fishbac_coordinate,axis=2)            
            else:
                fishbac_coordinates = np.dstack((fishbac_coordinates,fishbac_coordinate))               
        active_section = output_data_dict['active_section']
    else:
        fishbac_coordinates =None
        active_section = [] 
    
    return fishbac_coordinates, active_section

    
def morphing_section(blade_no,output_data_dict,no_motion_time_steps):
    """
    takes camber morphing information from TEF deflection representation in CII
    and generates 2D profile coordinates of the morphing sction at each time 
    step of CII solution and returns it. Also returns the spanwise length of 
    morphing section.

    Parameters
    ----------
    blade_no : int
        blade reference number used to identify blade for which time series 
        data of active camber profile coordinates is generated. CII convention
        followed when solver is CII where last blade is at 0 azimuth, for e.g. 
        blade 4 is at 0 azimuth at initial time for Bo 105 
    output_data_dict : dict
        contains the relevant solution output from comprehensive analysis        

    Returns
    -------
    fishbac_coordinates : ndarray or None
        time-history of the coordinates of the 2D profile of the active camber 
        section generated at each time-step. Returns None when no camber 
        actuation takes place
    active_section : list 
        two-element list of blade spanwise coordinates where active morphing 
        section is located. Non-dimensionalized with blade radius. Empty list 
        returned if no camber morphing is occuring.

    """
    
    if output_data_dict['solver']=='CII':
        fishbac_coordinates, active_section = solverCII(blade_no,output_data_dict)
    elif output_data_dict['solver']=='Dymore':
        fishbac_coordinates, active_section = solverDym(blade_no,output_data_dict,no_motion_time_steps)
        
        
    return fishbac_coordinates, active_section
