#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 10:03:48 2020

@author: ge56beh
"""

import numpy as np
import pickle
from collections import OrderedDict 
import math
from scipy.interpolate import interp1d
import os

from SONATA.classBlade import Blade
from SONATA.classAirfoil import Airfoil
from HeliNoise.SONATA import classBlade_attr_replace
from HeliNoise.SONATA import classAirfoil_attr_replace
from HeliNoise.FishBAConator import sabre_morphing
from HeliNoise.PSU_WOPWOP import (create_data_dict,
                                 save_dict_as_txtfile,
                                 dict_to_bin_save_file,
                                 bin_to_dict,)

def patch_file(patchdata_input_dict,CII_output_data_dict,misc_dict,blade_no):
    """
    
    
    Parameters
    ----------
    patchdata_input_dict : dict
        contains all relevant input for patch file input for PSU WOPWOP
    CII_output_data_dict : dict
        contains the necessary relevant solution output from CII output file        
    misc_dict : dict
        contains other miscellaneous input parameters that can be set from the 
        `Master_acoustics.py` script 
    blade_no : int
        blade reference number used to identify blade for which discretization 
        is generated. CII convention followed where last blade is at 0 azimuth, 
        for e.g. blade 4 is at 0 azimuth at initial time for Bo 105 
 
    Returns
    -------
    None.

    """
    
    print(f'PatchFiles :: Processing Blade {blade_no}...')
    
    periodicity_def = misc_dict['periodicity_def']
    periodicity_patch = patchdata_input_dict['periodicity']

    time_period = 2*(np.pi)/CII_output_data_dict['SPEED']['OMEGA (RAD/SEC)']
    radius = CII_output_data_dict['RADIUS']
    no_motion_time_steps = 1+CII_output_data_dict['TIME_STEP'][3]
    no_aero_time_steps = 1+CII_output_data_dict['TIME_STEP'][4]
    
    # get blade elastic deformation
    deformation_CII_frame_harm = CII_output_data_dict['SENSOR_DATA_CFD_POS_HARMONICS']
    deformation_mean_harm = np.squeeze(deformation_CII_frame_harm['mean'])
    deformation_cosine_harm = deformation_CII_frame_harm['cosine']
    deformation_sine_harm = deformation_CII_frame_harm['sine']
        
    deformation_CII_blade = np.zeros((CII_output_data_dict['SENSOR_DATA_CFD_POS'].shape))
    for psi_idx, psi in enumerate(np.linspace(0,2*np.pi,no_motion_time_steps,endpoint=True)):
        deformation_CII_blade[psi_idx,:,:] = deformation_mean_harm
        for harm,(c,s) in enumerate(zip(deformation_cosine_harm,deformation_sine_harm),1):
            deformation_CII_blade[psi_idx,:,:] += c*math.cos(harm*(psi+blade_no*np.pi/2)) \
                                                  +s*math.sin(harm*(psi+blade_no*np.pi/2))
    
    if periodicity_patch==1:   
        # "deformation" info for just one time step so that the returned node_pos_arr_dict 
        # and norm_pos_arr_dict have only unit length in the fourth dimension for rigid profiles       
        deformedblade_CII_Bframe=np.zeros((CII_output_data_dict['SENSOR_DATA_CFD_POS'][0:1,:,:].shape))                                                                         
    elif periodicity_patch==2: 
        # CFD position sensor data from CII Bframe: displacement --> m, angles --> deg 
        deformedblade_CII_Bframe = np.concatenate((radius*deformation_CII_blade[:,0:3,:],
                                                  (np.pi/180)*deformation_CII_blade[:,3:6,:]),
                                                  axis=1)           
    radial_res_CII = np.array([float(station) for station in CII_output_data_dict['SENSOR_STATION_BCFDP']])
    
    # get 2D chordwise profile morphing
    if CII_output_data_dict['OPTEF']:   
        fishbac_coordinates,active_section = sabre_morphing.morphing_section(blade_no,CII_output_data_dict)        
    else:
        fishbac_coordinates = None
        active_section = []
            
    # using SONATA to get blade surface discretization
    blade = Blade(filename = misc_dict['filepath_SONATA_yml'], ref_axes_format=0, ontology=0)    #reading all blade design data from *.yml file to 'Blade' object        
    Blade.blade_gen_wopwop_mesh = classBlade_attr_replace.blade_gen_wopwop_mesh
    # Blade.blade_post_3dtopo= classBlade_attr_replace.blade_post_3dtopo    
    Airfoil.gen_wopwop_dist = classAirfoil_attr_replace.gen_wopwop_dist                              
    #calling SONATA functionality to get node position vectors of discretized blade surface and normals at those nodes
    radial_res_dist, node_pos_arr_dict, norm_pos_arr_dict = blade.blade_gen_wopwop_mesh(radial_res_CII, 
                                                                                       misc_dict['surfaces_dict'], 
                                                                                       deformedblade_CII_Bframe, 
                                                                                       nbpoints = 100,
                                                                                       dist_curvature = 0.0001,
                                                                                       fishbac_spantr = misc_dict['fishbac_spantr'],
                                                                                       active_section = active_section,
                                                                                       fishbac_coordinates = fishbac_coordinates)        
    
    # Organize and save patchfile        
    patchfile_all_data_dict = create_data_dict.patchfile(patchdata_input_dict,
                                                         node_pos_arr_dict,
                                                         norm_pos_arr_dict,
                                                         misc_dict['time_steps_or_keys'])   
    filepath_to_patchfile_blade = misc_dict['directory_to_bin_patchfile']\
                                  +CII_output_data_dict['filename'].split('.out')[0] \
                                  +'_patchdataBlade'+str(blade_no) \
                                  +'_'+periodicity_def[periodicity_patch]+'.dat'
    dict_to_bin_save_file.patchfile(filepath_to_patchfile_blade,patchfile_all_data_dict)    #converts the patchfile_all_data_dict data to a binary WOPWOP-input patch file 
    # save_dict_as_txtfile.patchfile(filepath_to_patchfile_blade,bin_to_dict.patchfile(filepath_to_patchfile_blade))    #converts the saved bin patchfile to text file to check if everthing was done right
    
    pickle.dump( radial_res_dist, open( f'radial_res_dist_{blade_no}.p', 'wb' ) )
    pickle.dump( patchfile_all_data_dict, open( f'patchfile_all_data_dict_{blade_no}.p', 'wb' ) )
    print(f'...finished {blade_no} :: PatchFiles')
    if misc_dict['generate_plt']:
        pickle.dump( node_pos_arr_dict, open( f'node_pos_arr_dict_{blade_no}.p', 'wb' ) )
        pickle.dump( norm_pos_arr_dict, open( f'norm_pos_arr_dict_{blade_no}.p', 'wb' ) )

def loading_file(patchfile_all_data_dict,funcdatafile_input_dict,CII_output_data_dict,misc_dict,blade_no):
    """
    

    Parameters
    ----------
    patchdata_input_dict : dict
        contains all relevant input for patch file input for PSU WOPWOP
    funcdatafile_input_dict : dict
        contains all relevant input for loading file input for PSU WOPWOP
    CII_output_data_dict : dict
        contains the necessary relevant solution output from CII output file        
    misc_dict : dict
        contains other miscellaneous input parameters that can be set from the 
        `Master_acoustics.py` script 
    blade_no : int
        blade reference number used to identify blade for which discretization 
        is generated. CII convention followed where last blade is at 0 azimuth, 
        for e.g. blade 4 is at 0 azimuth at initial time for Bo 105 
 
    Returns
    -------
    None.

    """
    
    print(f'LoadingFiles :: Processing Blade {blade_no}...')

    radial_res_dist = pickle.load( open( f'radial_res_dist_{blade_no}.p', "rb" ) )
    os.remove(f'radial_res_dist_{blade_no}.p')
    patchfile_all_data_dict = pickle.load( open( f'patchfile_all_data_dict_{blade_no}.p', "rb" ) )
    os.remove(f'patchfile_all_data_dict_{blade_no}.p')
    
    surfaces_dict = misc_dict['surfaces_dict']
    periodicity_def = misc_dict['periodicity_def']
    periodicity_loading = funcdatafile_input_dict['periodicity']
    no_aero_time_steps = 1+CII_output_data_dict['TIME_STEP'][4]
    radial_res_CII = np.array([float(station) for station in CII_output_data_dict['SENSOR_STATION_BCFDP']])
    
    
    # Generate loading data (based on CII output)        
    loading_dict = OrderedDict()
    for surf in patchfile_all_data_dict['header info']['patch names']:  # temp construct, needs to be fixed later        
        loading_vecs_dict={}
        if surf == surfaces_dict['compact_surfaces'][0]:            
            for load_direction in ['X','Y','Z']:
                loading_vecs_CII_arr = np.zeros((no_aero_time_steps,len(radial_res_CII[1:-1])))
                loading_harm_mean = CII_output_data_dict['SENSORS_DATA_DICT_HARMONICS']['mean']['SECTION FORCE; '+load_direction+' COMPONENT, WING PLANE AXES']
                loading_harm_cosine = CII_output_data_dict['SENSORS_DATA_DICT_HARMONICS']['cosine']['SECTION FORCE; '+load_direction+' COMPONENT, WING PLANE AXES']
                loading_harm_sine = CII_output_data_dict['SENSORS_DATA_DICT_HARMONICS']['sine']['SECTION FORCE; '+load_direction+' COMPONENT, WING PLANE AXES']                
                for psi_idx, psi in enumerate(np.linspace(0,2*np.pi,no_aero_time_steps,endpoint=True)):
                    loading_vecs_CII_arr[psi_idx,:] = loading_harm_mean
                    for harm,(c,s) in enumerate(zip(loading_harm_cosine,loading_harm_sine),1):
                        loading_vecs_CII_arr[psi_idx,:] += c*math.cos(harm*(psi+blade_no*np.pi/2)) \
                                                           +s*math.sin(harm*(psi+blade_no*np.pi/2))
                # adding zero load column vector data for the blade tips (aero loading data is at the panel midpoints)
                # loading_vecs_arr = np.hstack((np.zeros((loading_vecs_CII_arr.shape[0],1)),loading_vecs_CII_arr,np.zeros((loading_vecs_CII_arr.shape[0],1))))    
                # adding non-zero load column vector data for the blade tips (aero loading data is at the panel midpoints)
                loading_vecs_arr = np.hstack((loading_vecs_CII_arr[:,0,np.newaxis],loading_vecs_CII_arr,loading_vecs_CII_arr[:,-1,np.newaxis]))    
                f_loading_interp = interp1d(radial_res_CII,loading_vecs_arr,kind='linear', axis=1)        
                loading_vecs_arr_newres = f_loading_interp(radial_res_dist)
                loading_vecs_dict[surf+' '+load_direction+' loading vector'] = loading_vecs_arr_newres

        loading_dict.update({surf:loading_vecs_dict})
         
    # Organize and save funcdatafile    
    Num_zones_patchdatafile = patchfile_all_data_dict['data upto format string']['number of zones']                                                                                         #based on the string, the corresponding value from CII_info will be used to before data of each zone
    funcdatafile_all_data_dict=create_data_dict.funcdatafile(funcdatafile_input_dict,
                                                             loading_dict,
                                                             misc_dict['time_steps_or_keys'])   #generates functional data file and returns a dictionary of all the data 
    filepath_to_funcdatafile_blade = misc_dict['directory_to_bin_funcdatafile'] \
                                    +CII_output_data_dict['filename'].split('.out')[0] \
                                    +'_funcdataBlade'+str(blade_no) \
                                    +'_'+periodicity_def[periodicity_loading]+'.dat'
    dict_to_bin_save_file.funcdatafile(filepath_to_funcdatafile_blade,funcdatafile_all_data_dict,Num_zones_patchdatafile)                                  #converts the funcdatafile_all_data_dict data to a binary WOPWOP-input functional data file 
    # save_dict_as_txtfile.funcdatafile(filepath_to_funcdatafile_blade,bin_to_dict.funcdatafile(filepath_to_funcdatafile_blade,Num_zones_patchdatafile))       #converts the saved bin funcdatafile to text file to check if everthing was done right
    print(f'...finished {blade_no} :: LoadingFiles')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    