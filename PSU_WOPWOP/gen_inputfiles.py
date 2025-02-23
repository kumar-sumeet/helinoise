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
from HeliNoise.TecPlot.gen_wopwop_plt import get_plt
from HeliNoise.utl import dym

def gen_inputfiles(patchdata_input_dict,funcdatafile_input_dict,aug_data_dict,misc_dict,dataframename,rotate,blade_no):
    
    T = 2*(np.pi)/aug_data_dict['SPEED']['OMEGA (RAD/SEC)']
    # dataframename = aug_data_dict['dataframename']
    solver = aug_data_dict['solver']
    delta_t = aug_data_dict['delta_t']
    directry = misc_dict['directory_to_bin_patchfile']
    periodicity_def = misc_dict['periodicity_def']
    generate_plt = misc_dict['generate_plt']
    periodicity_patch = patchdata_input_dict['periodicity']
    filename = aug_data_dict['filename']
    no_motion_time_steps = patchdata_input_dict['number of time steps']
    time_steps_motion = patchdata_input_dict['time steps']

    patchfile_all_data_dict, sonataout_dict = patchfile(patchdata_input_dict,aug_data_dict,misc_dict,dataframename,rotate,blade_no)
    loadingfile(patchfile_all_data_dict,funcdatafile_input_dict,sonataout_dict['radial_res_dist'],aug_data_dict,misc_dict,dataframename,blade_no)
        
    #not very clean, fix it later
    periodicity_loading = funcdatafile_input_dict['periodicity']
    no_aero_time_steps = funcdatafile_input_dict['number of time steps']
    if aug_data_dict['solver']=='CII':
        loading_dict = get_loadingCII(aug_data_dict,patchfile_all_data_dict,
                                      sonataout_dict['radial_res_dist'],
                                      misc_dict['surfaces_dict'],blade_no)
    elif aug_data_dict['solver']=='Dymore':
        loading_dict = get_loadingDym(aug_data_dict,patchfile_all_data_dict,
                                      periodicity_loading,sonataout_dict['radial_res_dist'],
                                      misc_dict['surfaces_dict'],
                                      blade_no,no_aero_time_steps,
                                      dataframename)
                                     # 'BladePrecone(rotating)')
                                     #'BladeHub(rotating)')
                                     # 'Wing(non-pitching)')

    if generate_plt:
        pltdatadict = {'solver': solver,#adding solver info to be used for generating plt files later
                     'disp_or_pos': aug_data_dict['disp_or_pos'],
                     'directry':directry,
                     'filename':filename,
                     'T': T,
                     'blade_no': blade_no,
                     'dataframename':dataframename,
                     'delta_t': delta_t,
                     'no_motion_time_steps': no_motion_time_steps, #remove it, this is not needed
                     'time_steps_motion': time_steps_motion,
                     'node_pos_arr_dict':sonataout_dict['node_pos_arr_dict'],
                     'norm_pos_arr_dict':sonataout_dict['norm_pos_arr_dict'],
                     'loading_dict': loading_dict
                            }
        # pickle.dump( pltdatadict, open( f'{directry}/pltdatadict_blade{blade_no}_{dataframename}.p', 'wb' ) )
        get_plt(pltdatadict)
    
    
    
def get_deformedbladeCII(aug_data_dict,periodicity_patch,blade_no):
    
    radius = aug_data_dict['RADIUS']
    no_motion_time_steps = 1+aug_data_dict['TIME_STEP'][3]

    # get blade elastic deformation
    deformation_CII_frame_harm = aug_data_dict['SENSOR_DATA_CFD_POS_HARMONICS']
    deformation_mean_harm = np.squeeze(deformation_CII_frame_harm['mean'])
    deformation_cosine_harm = deformation_CII_frame_harm['cosine']
    deformation_sine_harm = deformation_CII_frame_harm['sine']
        
    deformation_CII_blade = np.zeros((aug_data_dict['SENSOR_DATA_CFD_POS'].shape))
    for psi_idx, psi in enumerate(np.linspace(0,2*np.pi,no_motion_time_steps,endpoint=True)):
        deformation_CII_blade[psi_idx,:,:] = deformation_mean_harm
        for harm,(c,s) in enumerate(zip(deformation_cosine_harm,deformation_sine_harm),1):
            deformation_CII_blade[psi_idx,:,:] += c*math.cos(harm*(psi+blade_no*np.pi/2)) \
                                                  +s*math.sin(harm*(psi+blade_no*np.pi/2))

    if periodicity_patch==1:   
        # "deformation" info for just one time step so that the returned node_pos_arr_dict 
        # and norm_pos_arr_dict have only unit length in the fourth dimension for rigid profiles       
        deformedblade_CII_Bframe=np.zeros((aug_data_dict['SENSOR_DATA_CFD_POS'][0:1,:,:].shape))                                                                         
    elif periodicity_patch==2: 
        # CFD position sensor data from CII Bframe: displacement --> m, angles --> deg 
        deformedblade_CII_Bframe = np.concatenate((radius*deformation_CII_blade[:,0:3,:],
                                                  (np.pi/180)*deformation_CII_blade[:,3:6,:]),
                                                  axis=1)           
        
    radial_res = np.array([float(station) for station in aug_data_dict['SENSOR_STATION_BCFDP']])

    # get 2D chordwise profile morphing
    if aug_data_dict['OPTEF']:   
        fishbac_coordinates,active_section = sabre_morphing.morphing_section(blade_no,aug_data_dict)        
    else:
        fishbac_coordinates = None
        active_section = []
    
    return radial_res, deformedblade_CII_Bframe, fishbac_coordinates,active_section

def get_deformedbladeDym(aug_data_dict,periodicity_patch,blade_no,no_motion_time_steps,dataframename):
    
    # no_motion_time_steps = len(aug_data_dict['time_steps_motion'])
        
    if aug_data_dict['disp_or_pos'] == 'pos':
        # dataframename = aug_data_dict['dataframename']
        if periodicity_patch == 1:
            deformedblade_Dym = aug_data_dict[f'LL_Pos_{dataframename}'][f'Blade0{blade_no}'][-1:,:,:]       
        elif periodicity_patch == 2:
            deformedblade_Dym = aug_data_dict[f'LL_Pos_{dataframename}'][f'Blade0{blade_no}'][-no_motion_time_steps:,:,:]       
        elif periodicity_patch == 3:
            deformedblade_Dym = aug_data_dict[f'LL_Pos_{dataframename}'][f'Blade0{blade_no}'][-no_motion_time_steps:,:,:]       #last 26s worth of data  
        elif periodicity_patch == 4:
            pass
    elif aug_data_dict['disp_or_pos'] == 'disp':
        deformedblade_Dym = aug_data_dict[f'LL_DISPLACEMENTS'][f'Blade0{blade_no}']       
        
        
    radial_res = np.array([float(station) for station in aug_data_dict['LL_STATIONS']])

    # get 2D chordwise profile morphing
    if np.any(aug_data_dict['fishbac_deflection']):   #if there is a non-zero FishBAC deflection
        fishbac_coordinates, active_section = sabre_morphing.morphing_section(blade_no,
                                                                              aug_data_dict,
                                                                              no_motion_time_steps)        
    else:
        fishbac_coordinates = None
        active_section = []
    
    return radial_res, deformedblade_Dym, fishbac_coordinates, active_section
    
    

def patchfile(patchdata_input_dict,aug_data_dict,misc_dict,dataframename,rotate,blade_no):
    """
    
    
    Parameters
    ----------
    patchdata_input_dict : dict
        contains all relevant input for patch file input for PSU WOPWOP
    aug_data_dict : dict
        contains all relevant comprehensive analysis solution (CII/Dymore) 
        output in a dict format for one rotor
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
    
    print(f'PatchFiles :: Processing Blade/Wing {blade_no}...')
    
    T = 2*(np.pi)/aug_data_dict['SPEED']['OMEGA (RAD/SEC)']
    # dataframename = aug_data_dict['dataframename']
    solver = aug_data_dict['solver']
    delta_t = aug_data_dict['delta_t']
    directry = misc_dict['directory_to_bin_patchfile']
    debug = misc_dict['debug']
    periodicity_def = misc_dict['periodicity_def']
    generate_plt = misc_dict['generate_plt']
    periodicity_patch = patchdata_input_dict['periodicity']
    filename = aug_data_dict['filename']
    no_motion_time_steps = patchdata_input_dict['number of time steps']
    if aug_data_dict['solver']=='CII':
        radial_res, deformedblade_data, fishbac_coordinates, active_section = get_deformedbladeCII(aug_data_dict,periodicity_patch,blade_no)
    if aug_data_dict['solver']=='Dymore':
        radial_res, deformedblade_data, fishbac_coordinates, active_section = get_deformedbladeDym(aug_data_dict,
                                                                                                   periodicity_patch,
                                                                                                   blade_no,
                                                                                                   no_motion_time_steps,
                                                                                                   dataframename)
            
    # print('radial_res', radial_res)
    # using SONATA to get blade surface discretization
    blade = Blade(filename = misc_dict['filepath_SONATA_yml'], ref_axes_format=0, ontology=0)    #reading all blade design data from *.yml file to 'Blade' object        
    Blade.blade_gen_wopwop_mesh = classBlade_attr_replace.blade_gen_wopwop_mesh
    # Blade.blade_post_3dtopo= classBlade_attr_replace.blade_post_3dtopo    
    Airfoil.gen_wopwop_dist = classAirfoil_attr_replace.gen_wopwop_dist          


    if aug_data_dict['grid_res']==0:    #coarse res
         nbpoints = 3 
    elif aug_data_dict['grid_res']==1:    #medium res
         nbpoints = 10 
    elif aug_data_dict['grid_res']==2:    #fine res
         nbpoints = 50 

    #calling SONATA functionality to get node position vectors of discretized blade surface and normals at those nodes
    radial_res_dist, node_pos_arr_dict, norm_pos_arr_dict = blade.blade_gen_wopwop_mesh(radial_res, 
                                                                                       misc_dict['surfaces_dict'], 
                                                                                       deformedblade_data, 
                                                                                       nbpoints,
                                                                                       fishbac_spantr = misc_dict['fishbac_spantr'],
                                                                                       active_section = active_section,
                                                                                       rotate=rotate,
                                                                                       fishbac_coordinates = fishbac_coordinates,
                                                                                       solver = aug_data_dict['solver'],
                                                                                       disp_or_pos = aug_data_dict['disp_or_pos'])        
    
    #making dymore data strictly periodic (removing small deviations from cycle-to-cycle)
    if aug_data_dict['solver']=='Dymore' and periodicity_patch==2 and misc_dict['smoothdata']:
        print('Making Dym nodes/norm data periodic')
        node_pos_arr_dict = dym.make_node_norm_periodic(node_pos_arr_dict)
        norm_pos_arr_dict = dym.make_node_norm_periodic(norm_pos_arr_dict)
        
    print('######################################################')

    sonataout_dict = {'radial_res_dist': radial_res_dist, 
                      'node_pos_arr_dict': node_pos_arr_dict,
                      'norm_pos_arr_dict': norm_pos_arr_dict}

    # Organize and save patchfile        
    patchfile_all_data_dict = create_data_dict.patchfile(patchdata_input_dict,
                                                         node_pos_arr_dict,
                                                         norm_pos_arr_dict,
                                                         misc_dict['time_steps_or_keys'])   
    dirtosave_dat = f"{directry}/blade_data"
    try:
        os.makedirs(dirtosave_dat)
    except FileExistsError:
        pass                # directory already exists                   
    filepath_to_patchfile_blade = f"{dirtosave_dat}/{filename}_{dataframename}_patchdataBlade{str(blade_no)}"\
                                  +'_'+periodicity_def[periodicity_patch]+'.dat'
    if debug:
        dict_to_bin_save_file.patchfile(filepath_to_patchfile_blade,patchfile_all_data_dict,size_check=True)    #converts the patchfile_all_data_dict data to a binary WOPWOP-input patch file 
        save_dict_as_txtfile.patchfile(filepath_to_patchfile_blade,
                                       bin_to_dict.patchfile(filepath_to_patchfile_blade,
                                                             size_check=True))    #converts the saved bin patchfile to text file to check if everthing was done right
    else:
        dict_to_bin_save_file.patchfile(filepath_to_patchfile_blade,patchfile_all_data_dict)    #converts the patchfile_all_data_dict data to a binary WOPWOP-input patch file 

    
    return patchfile_all_data_dict, sonataout_dict

def get_loadingCII(aug_data_dict,patchfile_all_data_dict,radial_res_dist,surfaces_dict,blade_no):

    no_aero_time_steps = 1+aug_data_dict['TIME_STEP'][4]
    radial_res = np.array([float(station) for station in aug_data_dict['SENSOR_STATION_BCFDP']])

    # Generate loading data from CII output
    loading_dict = OrderedDict()
    for surf in patchfile_all_data_dict['header info']['patch names']:  # temp construct, needs to be fixed later        
        loading_vecs_dict={}
        if surf == surfaces_dict['compact_surfaces'][0]:            
            for load_direction in ['X','Y','Z']:
                loading_vecs_CII_arr = np.zeros((no_aero_time_steps,len(radial_res[1:-1])))
                loading_harm_mean = aug_data_dict['SENSORS_DATA_DICT_HARMONICS']['mean']['SECTION FORCE; '+load_direction+' COMPONENT, WING PLANE AXES']
                loading_harm_cosine = aug_data_dict['SENSORS_DATA_DICT_HARMONICS']['cosine']['SECTION FORCE; '+load_direction+' COMPONENT, WING PLANE AXES']
                loading_harm_sine = aug_data_dict['SENSORS_DATA_DICT_HARMONICS']['sine']['SECTION FORCE; '+load_direction+' COMPONENT, WING PLANE AXES']                
                for psi_idx, psi in enumerate(np.linspace(0,2*np.pi,no_aero_time_steps,endpoint=True)):
                    loading_vecs_CII_arr[psi_idx,:] = loading_harm_mean
                    for harm,(c,s) in enumerate(zip(loading_harm_cosine,loading_harm_sine),1):
                        loading_vecs_CII_arr[psi_idx,:] += c*math.cos(harm*(psi+blade_no*np.pi/2)) \
                                                           +s*math.sin(harm*(psi+blade_no*np.pi/2))
                # adding zero load column vector data for the blade tips (aero loading data is at the panel midpoints)
                # loading_vecs_arr = np.hstack((np.zeros((loading_vecs_CII_arr.shape[0],1)),loading_vecs_CII_arr,np.zeros((loading_vecs_CII_arr.shape[0],1))))    
                # adding non-zero load column vector data for the blade tips (aero loading data is at the panel midpoints)
                loading_vecs_arr = np.hstack((loading_vecs_CII_arr[:,0,np.newaxis],loading_vecs_CII_arr,loading_vecs_CII_arr[:,-1,np.newaxis]))    
                f_loading_interp = interp1d(radial_res,loading_vecs_arr,kind='linear', axis=1)        
                loading_vecs_arr_newres = f_loading_interp(radial_res_dist)
                loading_vecs_dict[surf+' '+load_direction+' loading vector'] = loading_vecs_arr_newres

        loading_dict.update({surf:loading_vecs_dict})
        
    return loading_dict


def get_loadingDym(aug_data_dict,patchfile_all_data_dict,periodicity_loading,
                   radial_res_dist,surfaces_dict,blade_no,no_aero_time_steps,dataframename):


    # no_aero_time_steps = len(aug_data_dict['no_aero_time_steps'])
    
    radial_res = np.array([float(station) for station in aug_data_dict['LL_STATIONS']])
    # dataframename = aug_data_dict['dataframename']
    if periodicity_loading == 1:
        loading_arr = aug_data_dict[f'LL_AstLoad_{dataframename}'][f'Blade0{blade_no}'][-1:,:,:]       
    elif periodicity_loading == 2:
        loading_arr = aug_data_dict[f'LL_AstLoad_{dataframename}'][f'Blade0{blade_no}'][-no_aero_time_steps:,:,:] 
        print(np.shape(loading_arr))
        loading_arr[-1,:,:] = loading_arr[0,:,:]   #ensuring periodicity
    elif periodicity_loading == 3:
        loading_arr = aug_data_dict[f'LL_AstLoad_{dataframename}'][f'Blade0{blade_no}'][-no_aero_time_steps:,:,:]       
    elif periodicity_loading == 4:
        pass

    # Generate loading data from Dym output
    loading_dict = OrderedDict()
    for surf in patchfile_all_data_dict['header info']['patch names']:  # temp construct, needs to be fixed later        
        loading_vecs_dict={}
        if surf == surfaces_dict['compact_surfaces'][0]:            
            for idx,load_direction in enumerate(['X','Y','Z']): 
                loading_arr_direction = loading_arr[:,idx,:]
                f_loading_interp = interp1d(radial_res,loading_arr_direction,kind='linear', axis=1)        
                loadingnewres_arr = f_loading_interp(radial_res_dist)
                loading_vecs_dict[surf+' '+load_direction+' loading vector'] = loadingnewres_arr

        loading_dict.update({surf:loading_vecs_dict})
       
    return loading_dict


def loadingfile(patchfile_all_data_dict,funcdatafile_input_dict,radial_res_dist,aug_data_dict,misc_dict,dataframename,blade_no):
    """
    

    Parameters
    ----------
    patchdata_input_dict : dict
        contains all relevant input for patch file input for PSU WOPWOP
    funcdatafile_input_dict : dict
        contains all relevant input for loading file input for PSU WOPWOP
    aug_data_dict : dict
        contains all relevant comprehensive analysis solution (CII/Dymore) 
        output in a dict format for one rotor
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
    
    print(f'LoadingFiles :: Processing Blade/Wing {blade_no}...')

    directry = misc_dict['directory_to_bin_funcdatafile']
    # dataframename = aug_data_dict['dataframename']
    filename = aug_data_dict['filename']
    debug = misc_dict['debug']
    surfaces_dict = misc_dict['surfaces_dict']
    periodicity_def = misc_dict['periodicity_def']
    periodicity_loading = funcdatafile_input_dict['periodicity']
    no_aero_time_steps = funcdatafile_input_dict['number of time steps']
    
    if aug_data_dict['solver']=='CII':
        loading_dict = get_loadingCII(aug_data_dict,patchfile_all_data_dict,
                                      radial_res_dist,
                                      surfaces_dict,blade_no)
    elif aug_data_dict['solver']=='Dymore':
        # loading_arr, loading_dict = get_loadingDym(aug_data_dict,patchfile_all_data_dict,
        #                               periodicity_loading,radial_res_dist,
        #                               surfaces_dict,blade_no,no_aero_time_steps,dataframename)
        loading_dict = get_loadingDym(aug_data_dict,patchfile_all_data_dict,
                                      periodicity_loading,radial_res_dist,
                                      surfaces_dict,blade_no,no_aero_time_steps,dataframename)
    
    #making dymore data strictly periodic (removing small deviations from cycle-to-cycle)
    if aug_data_dict['solver']=='Dymore' and periodicity_loading==2 and misc_dict['smoothdata']:
        print('Making Dym loading data periodic')
        loading_dict = dym.make_loading_periodic(loading_dict)
    
    # Organize and save funcdatafile    
    Num_zones_patchdatafile = patchfile_all_data_dict['data upto format string']['number of zones']                                                                                         #based on the string, the corresponding value from CII_info will be used to before data of each zone
    funcdatafile_all_data_dict = create_data_dict.funcdatafile(funcdatafile_input_dict,
                                                             loading_dict,
                                                             misc_dict['time_steps_or_keys'])   #generates functional data file and returns a dictionary of all the data 
    dirtosave_dat = f"{directry}/blade_data"
    try:
        os.makedirs(dirtosave_dat)
    except FileExistsError:
        pass                # directory already exists                   
    filepath_to_funcdatafile_blade = f"{dirtosave_dat}/{filename}_{dataframename}_funcdataBlade{str(blade_no)}"\
                                    +'_'+periodicity_def[periodicity_loading]+'.dat'
    if debug:
        dict_to_bin_save_file.funcdatafile(filepath_to_funcdatafile_blade,
                                           funcdatafile_all_data_dict,
                                           Num_zones_patchdatafile,
                                           size_check=True)                                  #converts the funcdatafile_all_data_dict data to a binary WOPWOP-input functional data file 
        save_dict_as_txtfile.funcdatafile(filepath_to_funcdatafile_blade,
                                          bin_to_dict.funcdatafile(filepath_to_funcdatafile_blade,
                                                                   Num_zones_patchdatafile,
                                                                   size_check=True))       #converts the saved bin funcdatafile to text file to check if everthing was done right
    else:
        dict_to_bin_save_file.funcdatafile(filepath_to_funcdatafile_blade,
                                           funcdatafile_all_data_dict,
                                           Num_zones_patchdatafile)                                  #converts the funcdatafile_all_data_dict data to a binary WOPWOP-input functional data file 
        
    
    # return loading_arr    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    