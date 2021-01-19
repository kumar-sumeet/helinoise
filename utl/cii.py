#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions to manipulate data, obtained from CII output file, into alternative
meaningful quantities
"""
import math
import numpy as np

def vib_power(all_data_dict, nondim=False, nondim_data={'m0':8.22,'Omega':44.5,'R':4.912}):
    """
    Extract/separate  vibration loads and power results from CII output data 
    and return as dictionary.
    
    Parameters
    ----------
    all_data_dict : dict
        [x,y,z] position in blade reference coordinates
    nondim_data : dict
        dict used for non-dimensionalizing blade vibration loads. 'm0' is 
        average blade mass, 'Omega' is rotor angular speed in rad/s and 'R'
    nondim : bool
        chord length
    
    Returns
    ---------
    Vib_power_dict : dict
        
        
    Todo 
    --------- 
       
    """
    
    if nondim:
        force_non_dim=1/(nondim_data['m0']*nondim_data['Omega']*nondim_data['R']*nondim_data['R'])
        moment_non_dim=1/(nondim_data['m0']*nondim_data['Omega']*nondim_data['R']*nondim_data['R']*nondim_data['R'])
    else:
        force_non_dim=1
        moment_non_dim=1
        
    J_baseline=math.sqrt(6)

    Vib_power_dict={}
    for subdir, data_dict in all_data_dict.items():
        Vib_power_dict[subdir]={}
        for filename,cii_output in data_dict.items():
            Vib_power_dict[subdir][filename]={'CP':cii_output['ROTOR_POWER_ALL'][0][0],
                                              'CPS':cii_output['ROTOR_POWER_ALL'][0][1],
                                              'P':cii_output['ROTOR_POWER'],
                                              'Fx':force_non_dim*cii_output['HUBLOADS']['NONROT_HUB_FORCE_HARM']['AFT'][3],
                                              'Fy':force_non_dim*cii_output['HUBLOADS']['NONROT_HUB_FORCE_HARM']['RIGHT'][3],
                                              'Fz':force_non_dim*cii_output['HUBLOADS']['NONROT_HUB_FORCE_HARM']['UP'][3],
                                              'Mx':moment_non_dim*cii_output['HUBLOADS']['NONROT_HUB_MOM_HARM']['ROLL'][3],
                                              'My':moment_non_dim*cii_output['HUBLOADS']['NONROT_HUB_MOM_HARM']['PITCH'][3],
                                              'Mz':moment_non_dim*cii_output['HUBLOADS']['NONROT_HUB_MOM_HARM']['YAW'][3],
                                              'Mx_cosine':moment_non_dim*cii_output['HUBLOADS']['NONROT_HUB_MOM_HARM_COSINE']['ROLL'][3],
                                              'Mx_sine':moment_non_dim*cii_output['HUBLOADS']['NONROT_HUB_MOM_HARM_SINE']['ROLL'][3],
                                              'My_cosine':moment_non_dim*cii_output['HUBLOADS']['NONROT_HUB_MOM_HARM_COSINE']['PITCH'][3],
                                              'My_sine':moment_non_dim*cii_output['HUBLOADS']['NONROT_HUB_MOM_HARM_SINE']['PITCH'][3],
                                              'Mz_cosine':moment_non_dim*cii_output['HUBLOADS']['NONROT_HUB_MOM_HARM_COSINE']['YAW'][3],
                                              'Mz_sine':moment_non_dim*cii_output['HUBLOADS']['NONROT_HUB_MOM_HARM_SINE']['YAW'][3]
                                              }
            
        baseline_dict = Vib_power_dict[subdir]['Baseline']
        
        for filename,cii_output in data_dict.items():
            tmp_dict = Vib_power_dict[subdir][filename]
            Vib_power_dict[subdir][filename].update({
                                                  'In_plane_Hub_Shear':math.sqrt(math.pow((tmp_dict['Fx']),2)+math.pow((tmp_dict['Fy']),2)),
                                                  'In_plane_Hub_Moment': math.sqrt(math.pow((tmp_dict['Mx']),2)+math.pow((tmp_dict['My']),2))
                                                      })
        for filename,cii_output in data_dict.items():
            tmp_dict = Vib_power_dict[subdir][filename]
            Vib_power_dict[subdir][filename].update({
                                                  'J':((tmp_dict['Fx']/baseline_dict['Fx'])**2+(tmp_dict['Fy']/baseline_dict['Fy'])**2+(tmp_dict['Fz']/baseline_dict['Fz'])**2+\
                                                       (tmp_dict['Mx']/baseline_dict['Mx'])**2+(tmp_dict['My']/baseline_dict['My'])**2+(tmp_dict['Mz']/baseline_dict['Mz'])**2)**0.5
                                                      })
        keys=[key for key in Vib_power_dict[subdir][filename].keys()]
        for filename,cii_output in data_dict.items():
            tmp_dict = Vib_power_dict[subdir][filename]
            for key in keys:
                Vib_power_dict[subdir][filename][f'delta_{key}%']=(tmp_dict[key]-Vib_power_dict[subdir]['Baseline'][key])*100/Vib_power_dict[subdir]['Baseline'][key]
    
    return Vib_power_dict

def get_tef_deflection(CII_data_dict):
    Azimuth = np.arange(0,360+360.0/100,360.0/100)
    # DEFLECTION_PROFILE={}
    # for filename in All_data_dict:
    # if 'Baseline' in filename: continue         #Dont calculate the baseline TEF deflection profile 
    #These entries are in terms of MCC
    Cosine_amp = CII_data_dict['IBC_HHC_INPUT']['TEF_INPUT']['Cosine']
    Sine_amp = CII_data_dict['IBC_HHC_INPUT']['TEF_INPUT']['Sine']
    Mean_amp = CII_data_dict['IBC_HHC_INPUT']['TEF_INPUT']['Mean']
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
        # DEFLECTION_PROFILE[filename] = Deflection_profile     
    
    return Azimuth, Deflection_profile
    