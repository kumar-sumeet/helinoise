#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 16:55:29 2019

@author: ge56beh
"""
# Standard library imports
from collections import OrderedDict 
import numpy as np
import matplotlib.pyplot as plt
import pickle
import math
from scipy.interpolate import interp1d
import concurrent.futures

# Local application imports
import sys
# sys.path.append('./CII')
from CII import CII_extract_all_coax
sys.path.append('./FishBAConator')
from FishBAConator import master_morphing
# from morphing_main import create_fishbac_deformation
from SONATA.classBlade import Blade
from PSU_WOPWOP import create_data_dict,save_dict_as_txtfile,dict_to_bin_save_file,bin_to_dict
# from PSU_WOPWOP.classRotor import Rotor
###############################################################################
'''
-surface, patch and patch_name have been interchangeably used throughout the this entire framework of WOPWOP to refer to the same entity
-


'''
######################################################################
######################    Input data    ##############################
######################################################################

               
                

##############################    SONATA    ###################################
filepath_SONATA_yml = './SONATA/UTAustin_VR12.yml'
blade_name = 'UT Austin coax rotor'
# filepath_SONATA_yml = './SONATA/Bo_105.yml'
# blade_name = 'Bo 105'

##############################    CII    ######################################
# cii_filepath = './CII/Camrad_files/best_cases_journal_paper/0.750_0.300_1.960_000.0_0.000_355.0_0.980_0.0_0.0_0.0_0.0_0.0_0.0_highresAero.out'
# cii_dir = './CII/Camrad_files/best_cases_journal_paper/'
# cii_filename = '0.700_0.400_3.100_322.0_3.530_267.0_1.116_0.0_0.0_0.0_0.0_0.0_0.0_highresAero.out'

# cii_dir = './CII/Camrad_files/best_cases_journal_paper/'
# cii_filename = 'baseline_highresAero.out'

# CII_output_data_dict=CII_extract_all.cii_extract_all(cii_dir+cii_filename)     #extracting all relevant data from the CII output file as a dict  


###########################
# cii_dir = '/home/HT/ge56beh/Work/High-mu_flettner_input_studi_Jakob/jobs_forward_flight/'
cii_dir = '/home/HT/ge56beh/Work/High-mu_flettner_input_studi_Jakob/jobs_hover_single_rotor/'
# # cii_filename = 'carmen_L3_900rpm_COLL8_mu_0_5_CMXsweep_abCMX0_highres.out'
# cii_filename = 'carmen_L3_900rpm_COLL8_windsweep_CMX_0_highres_rigidblade.out'
# cii_filename = 'carmen_L3_900rpm_COLL8_windsweep_CMX_0_highres.out'
###########################
# cii_dir = '/home/HT/ge56beh/Work/High-mu_flettner_input_studi_Jakob/jobs_forward_flight_inertial_fram_DPOS_DCFD/'
# cii_filename = 'carmen_L3_900rpm_COLL8_mu_0_5_CMXsweep_abCMX0_highres.out'
# cii_filename = 'carmen_L3_900rpm_COLL8_windsweep_CMX_0_highres_rigidblade_DPOS5_DCFD5.out'
# cii_filename = 'carmen_L3_900rpm_BL_010.out'
# cii_filename = 'carmen_900rpm_coll_6.out'
cii_filename = 'carmen_1200rpm_coll_10.out'
############################
filepath = cii_dir+cii_filename
file = open(filepath,'r')
file_content = file.read()    
NCASES_run = int( file_content.count(130*'*')/2) # reading NCASES this way because not all cases might have finished running
file.close()

# pickle.dump(CII_extract_all_coax.cii_extract_all_coax(filepath,NCASES_run), open(f'{cii_filename}.p', 'wb' ) )

CII_output_data_dict_all_cases = CII_extract_all_coax.cii_extract_all_coax(filepath,NCASES_run)     #extracting all relevant data from the CII output file as a dict  
case = 1

def get_blade_patch_funcdata_files(blade_no):
    print('Processing Blade {0}...'.format(blade_no))
    deformation_CII_blade['Blade_{0}'.format(blade_no)] = np.zeros((deformation_CII.shape))
    for psi_idx, psi in enumerate(np.linspace(0,2*np.pi,no_motion_time_steps,endpoint=True)):
        # for mean,c,s in zip(deformation_CII_frame_harm['mean'],deformation_CII_frame_harm['cosine'],deformation_CII_frame_harm['sine']):
            deformation_CII_blade['Blade_{0}'.format(blade_no)][psi_idx,:,:] = deformation_mean_harm
            for harm,(c,s) in enumerate(zip(deformation_cosine_harm,deformation_sine_harm),1):
                deformation_CII_blade['Blade_{0}'.format(blade_no)][psi_idx,:,:] += c*math.cos(harm*(psi+blade_no*2*np.pi/Nb)) \
                                                                                    +s*math.sin(harm*(psi+blade_no*2*np.pi/Nb))
    
    fishbac_deflection = np.zeros_like(time_steps_aero)
    if CII_output_data_dict['OPTEF']:    
        cii_tef_input = CII_output_data_dict['IBC_HHC_INPUT']['TEF_INPUT']
        if 'Cosine' in cii_tef_input:
            for n,(delta_c,delta_s) in enumerate(zip(cii_tef_input['Cosine'],cii_tef_input['Sine']),1):
                # print(delta_c,delta_s)
                fishbac_deflection = fishbac_deflection \
                                     +delta_c*np.cos(n*(2*np.pi*time_steps_aero/time_period+blade_no*2*np.pi/Nb)) \
                                     +delta_s*np.sin(n*(2*np.pi*time_steps_aero/time_period+blade_no*2*np.pi/Nb))
        if 'Mean' in cii_tef_input:
            fishbac_deflection = fishbac_deflection+cii_tef_input['Mean']
    
    
    if np.any(fishbac_deflection):
        active_section = CII_output_data_dict['EHTEF']
        for idx,deflection in enumerate(fishbac_deflection): 
            fishbac_coordinate, _, _ = morphing_main.create_fishbac_deformation(deflection_level = deflection)
            if idx ==0:
                fishbac_coordinates =np.expand_dims(fishbac_coordinate,axis=2)            
            else:
                fishbac_coordinates = np.dstack((fishbac_coordinates,fishbac_coordinate))
    else:
        fishbac_coordinates = None
        active_section = []
            
    # plt.plot((180/np.pi)*np.linspace(0,2*np.pi,no_motion_time_steps,endpoint=True),fishbac_deflection,label=str(blade_no))
    # plt.grid()
    # plt.legend()
    # plt.xlabel(r'$\psi$')
    # plt.ylabel('Tip deflection of morphing section as chord % (1=0.02c deflection)')
    ############################################################################################
    #####################    Generate patch data using SONATA    ###############################
    ############################################################################################
    
    blade = Blade(name=blade_name, filename = filepath_SONATA_yml)    #reading all blade design data from *.yml file to 'Blade' object    
    if periodicity_patch==1:    
        # "deformation" info for just one time step so that the returned node_pos_arr_dict 
        # and norm_pos_arr_dict have only unit length in the fourth dimension for rigid profiles       
        deformedblade_CII_Bframe=np.zeros((CII_output_data_dict['SENSOR_DATA_CFD_POS'][0:1,:,:].shape))                                                                         
    elif periodicity_patch==2: 
        # CFD position sensor data from camrad Bframe: displacement --> m, angles --> deg 
        deformedblade_CII_Bframe = np.concatenate((Radius*deformation_CII_blade['Blade_{0}'.format(blade_no)][:,0:3,:],
                                                  (np.pi/180)*deformation_CII_blade['Blade_{0}'.format(blade_no)][:,3:6,:]),
                                                  axis=1)  
    #calling SONATA functionality to get node position vectors of discretized blade surface and normals at those nodes
    radial_res_dist, node_pos_arr_dict, norm_pos_arr_dict = blade.blade_gen_wopwop_mesh(radial_res_CII, 
                                                                                       surfaces_dict, 
                                                                                       deformedblade_CII_Bframe, 
                                                                                       nbpoints = 100,
                                                                                       dist_curvature = 0.0001,
                                                                                       fishbac_spantr = fishbac_spantr,
                                                                                       active_section = active_section,
                                                                                       fishbac_coordinates = fishbac_coordinates,
                                                                                       rotate = rotate)        
    
    # use of tecplot recommended for visualisation instead of this SONATA feature
    # blade1.blade_post_3dtopo(flag_lft=False, flag_wopwop=True)    
    ###########################################################################
    ##################    Organize and save patchfile    ######################
    ###########################################################################
    print(' ######################################################## \n ##### Details corresponding to patch data handling ##### \n ########################################################')
    patchfile_all_data_dict = create_data_dict.patchfile(patchdata_input_dict,node_pos_arr_dict,norm_pos_arr_dict,time_steps_or_keys)   
    filepath_to_patchfile_blade = directory_to_bin_patchfile+'/'+cii_filename.split('.out')[0]+f'_case{case}_{rotor}_blade{blade_no}_patchdata_{periodicity_def[periodicity_loading]}.dat'
    dict_to_bin_save_file.patchfile(filepath_to_patchfile_blade,patchfile_all_data_dict)                                               #converts the patchfile_all_data_dict data to a binary WOPWOP-input patch file 
    save_dict_as_txtfile.patchfile(filepath_to_patchfile_blade,bin_to_dict.patchfile(filepath_to_patchfile_blade))                       #converts the saved bin patchfile to text file to check if everthing was done right
        
    #################################################################################################
    ###################    Generate loading data (based on CII output)   ############################
    ################################################################################################# 
    loading_dict.update({'Blade_{0}'.format(blade_no):{}})
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

        loading_dict['Blade_{0}'.format(blade_no)].update({surf:loading_vecs_dict})
    
    ##############################################################################
    ##################    Organize and save funcdatafile    ######################
    ##############################################################################
    Num_zones_patchdatafile = patchfile_all_data_dict['data upto format string']['number of zones']                                                                                         #based on the string, the corresponding value from CII_info will be used to before data of each zone
    print(' ############################################################# \n ##### Details corresponding to functional data handling ##### \n #############################################################')
    funcdatafile_all_data_dict=create_data_dict.funcdatafile(funcdatafile_input_dict,loading_dict['Blade_{0}'.format(blade_no)],time_steps_or_keys)                          #generates functional data file and returns a dictionary of all the data 
    filepath_to_funcdatafile_blade = directory_to_bin_funcdatafile+'/'+cii_filename.split('.out')[0]+f'_case{case}_{rotor}_blade{blade_no}_funcdata_{periodicity_def[periodicity_loading]}.dat'
    dict_to_bin_save_file.funcdatafile(filepath_to_funcdatafile_blade,funcdatafile_all_data_dict,Num_zones_patchdatafile)                                  #converts the funcdatafile_all_data_dict data to a binary WOPWOP-input functional data file 
    save_dict_as_txtfile.funcdatafile(filepath_to_funcdatafile_blade,bin_to_dict.funcdatafile(filepath_to_funcdatafile_blade,Num_zones_patchdatafile))       #converts the saved bin funcdatafile to text file to check if everthing was done right
    
    #####################################################################################################################################################################################################
    pickle.dump( node_pos_arr_dict, open( cii_filename.split('.out')[0]+f'_node_pos_arr_dict_case{case}_{rotor}_blade{blade_no}.p', 'wb' ) )
    pickle.dump( norm_pos_arr_dict, open( cii_filename.split('.out')[0]+f'_norm_pos_arr_dict_case{case}_{rotor}_blade{blade_no}.p', 'wb' ) )

for rotor, CII_output_data_dict in CII_output_data_dict_all_cases[case]['ROTOR(S)_DATA'].items():
    print(f'Processing {rotor}...')
    Radius = CII_output_data_dict['RADIUS']
    time_period = 60/CII_output_data_dict['ROTOR_RPM']         
    no_aero_time_steps = 1+CII_output_data_dict['TIME_STEP'][4]     #number of time steps in the airloads sensors info
    time_steps_aero = np.linspace(0,time_period,no_aero_time_steps)                                  
    no_motion_time_steps = 1+CII_output_data_dict['TIME_STEP'][3]     #number of time steps in the position sensors info
    if no_aero_time_steps!=no_motion_time_steps: raise ValueError    # these need to be equal for wopwop to work
    time_steps_motion = np.linspace(0,time_period,no_motion_time_steps)                                  
    
    radial_res_CII = np.array([float(station) for station in CII_output_data_dict['SENSOR_STATION_BCFDP']])
    deformation_CII=CII_output_data_dict['SENSOR_DATA_CFD_POS']
    deformation_CII_frame_harm = CII_output_data_dict['SENSOR_DATA_CFD_POS_HARMONICS']
    fishbac_spantr = 0.02    # fishbac spanwise transition as percentage of radius
    
    #############################    Patchfile ####################################
    directory_to_bin_patchfile='./PSU_WOPWOP/PSU_WOPWOP_new'
    periodicity_patch=2   #'constant/periodic/aperiodic/mtf'
    surfaces_dict = {'lifting_surfaces':['upper surface','lower surface'],
                     'end_surfaces':['inboard tip','outboard tip'],
                     'compact_surfaces':['lifting-line']}
    patchdata_input_dict ={
                           'units':'Pa',                                           #len of the str should not exceed 32
                           'comments':b'Patch data file containing geometry information of Bo 105',    #len of the str should not exceed 1024 
                           'grid':1,                                               #'structured/unstructured'
                           'periodicity':periodicity_patch,                                        #'constant/periodic/aperiodic/mtf'
                           'normal_vecs':1,                                        #'normal vectors node-centered/face-centered'
                           'time period':time_period, 
                           'number of time steps':no_motion_time_steps,
                           'time steps':time_steps_motion,
                           'keys':np.arange(0,no_motion_time_steps,1.) 
                          }    
    
    #############################    Funcdatafile #################################
    directory_to_bin_funcdatafile='./PSU_WOPWOP/PSU_WOPWOP_new'
    time_steps_or_keys = 'keys'
    loading_type = 2     #'surface pressure(GAUGE PRESSURE!!)/surface loading vector/flow parameters'
    periodicity_loading=2   #'constant/periodic/aperiodic/mtf'
    loading_frame = 1       #'stationary ground-fixed frame/rotating ground-fixed frame/patch-fixed frame'
    periodicity_def = {1:'constant',2:'periodic',3:'aperiodic',4:'mtf'}
    funcdatafile_input_dict = {
                               'comments':b'Functional data file containing CII (lifting line) loading information of Bo 105',   #len of the str should not exceed 1024
                               'grid':1,            #'structured/unstructured'
                               'periodicity':periodicity_loading,         
                               'normal_vecs':1,     #'normal vectors node-centered/face-centered'
                               'aero_data':loading_type,     
                               'frame':loading_frame, 
                               'time period':time_period, 
                               'number of time steps':no_aero_time_steps,
                               'time steps':time_steps_aero,
                               'keys':np.arange(0,no_aero_time_steps,1) 
                              }
    deformation_CII_blade = {}
    deformation_mean_harm = np.squeeze(deformation_CII_frame_harm['mean'])
    deformation_cosine_harm = deformation_CII_frame_harm['cosine']
    deformation_sine_harm = deformation_CII_frame_harm['sine']
    
    loading_dict = OrderedDict()
    
    # blade = Blade(name=blade_name, filename = filepath_SONATA_yml)    #reading all blade design data from *.yml file to 'Blade' object
    # rotor1 = Rotor(blade,no_blades,blade_zimuth)
    # Nb = CII_output_data_dict['Nb']
    rotate = CII_output_data_dict['ROTATE']
    # get_blade_patch_funcdata_files(1)
    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     Nb = CII_output_data_dict['Nb']
    #     executor.map(get_blade_patch_funcdata_files,np.arange(1,Nb+1,1))
    Nb = CII_output_data_dict['Nb']
    
    executor=concurrent.futures.ProcessPoolExecutor()     
    executor.map(get_blade_patch_funcdata_files,np.arange(1,Nb+1,1))
    
    
    