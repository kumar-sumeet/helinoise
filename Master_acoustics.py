"""
This is the main script that starts processes that generate the binary input 
surface and loading for acoustic analysis using PSU-WOPWOP. 

Note: 'surface', 'patch' and 'patch_name' have been interchangeably used 
throughout this entire toolchain to refer to the same entity. CII refers to 
CAMRAD II.
"""

import numpy as np
from multiprocessing import Pool
import os
import sys
from functools import partial
import pickle

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/SONATA')
from HeliNoise.CII import CII_extract_all
from HeliNoise.utl import crawler
from HeliNoise.PSU_WOPWOP.generate_blade import patch_file,loading_file
from HeliNoise.TecPlot.gen_wopwop_plt import get_plt

def generate_files(CII_output_data_dict,concurrency=True,generate_plt=False):    
    """
    All the input information relevant to acoustic analysis is organised here.
    For e.g. for rigid blade analysis `patchdata_input_dict['periodicity']` can
    be set as 1 irrespective of whether CII solution output is based on elastic 
    blade.
    
    Parameters
    ----------
    CII_output_data_dict : dict
        contains all relevant CII solution output in a dict format for one rotor
    generate_plt : bool, optional
        set to `True` to generate *.plt files corresponding to each blade to 
        view the blade geometry for debugging/veryfication purposes. Pytecplot 
        installation is required for this. The default is `False`.
    
    To-do
    -----
    concurrency : bool, optional
        set to `False`to generate files for each blade sequentially, otherwise
        multiprocessing is used
   
    """
    time_period = 2*(np.pi)/CII_output_data_dict['SPEED']['OMEGA (RAD/SEC)']            
    no_aero_time_steps = 1+CII_output_data_dict['TIME_STEP'][4]                # number of time steps in the airloads sensors info
    time_steps_aero = np.linspace(0,time_period,no_aero_time_steps)                                  
    no_motion_time_steps = 1+CII_output_data_dict['TIME_STEP'][3]              # number of time steps in the position sensors info
    if no_aero_time_steps!=no_motion_time_steps: raise ValueError              # these need to be equal for wopwop to work
    time_steps_motion = np.linspace(0,time_period,no_motion_time_steps)                                  
    
    misc_dict = {
                'fishbac_spantr' : 0.02,                                       # active camber blade spanwise transition as percentage of radius
                'surfaces_dict' : {
                                   'lifting_surfaces':['upper surface',
                                                       'lower surface'],
                                   'end_surfaces':['inboard tip',
                                                   'outboard tip'],
                                   'compact_surfaces':['lifting-line']
                                   },
                'time_steps_or_keys' : 'keys',    # wopwop feature 
                'directory_to_bin_patchfile' : directory_to_bin_patchfile,
                'directory_to_bin_funcdatafile' : directory_to_bin_funcdatafile,
                'filepath_SONATA_yml' : filepath_SONATA_yml,
                'generate_plt' : generate_plt,
                'periodicity_def' : {1:'constant',2:'periodic',3:'aperiodic',4:'mtf'}
                }
    
    #############################    Patchfile ################################
    patchdata_input_dict ={
                           'units':'Pa',                                       # len of the str should not exceed 32 bytes
                           'comments':b'''Patch data file containing geometry 
                                          information of Bo 105''',            # len of the str should not exceed 1024 bytes
                           'grid':1,                                           # 'structured/unstructured'
                           'periodicity':2,                                    # 'constant/periodic/aperiodic/mtf'
                           'normal_vecs':1,                                    # 'normal vectors node-centered/face-centered'
                           'time period':time_period, 
                           'number of time steps':no_motion_time_steps,
                           'time steps':time_steps_motion,
                           'keys':np.arange(0,no_motion_time_steps,1.) 
                          }    
    
    #############################    Funcdatafile #############################
    funcdatafile_input_dict = {
                               'comments':b'''Functional data file containing CII
                                            (lifting line) loading information 
                                            of Bo 105''',                      #len of the str should not exceed 1024 bytes
                               'grid':1,                                       #'structured/unstructured'
                               'periodicity':2,                                #'constant/periodic/aperiodic/mtf'         
                               'normal_vecs':1,                                #'normal vectors node-centered/face-centered'
                               'aero_data':2,                                  #'surface pressure(GAUGE PRESSURE!!)/surface loading vector/flow parameters'   
                               'frame':1,                                      #'stationary ground-fixed frame/rotating ground-fixed frame/patch-fixed frame'
                               'time period':time_period, 
                               'number of time steps':no_aero_time_steps,
                               'time steps':time_steps_aero,
                               'keys':np.arange(0,no_aero_time_steps,1) 
                              }

    Nb = CII_output_data_dict['Nb']
    
    # patch_file(patchdata_input_dict,CII_output_data_dict,misc_dict,1)
    # multiprocessing is used for speed-up, however this messes up output to
    # the terminal a bit (each statement from SONATA gets printed 'Nb' times)     
    partial_patch_file=partial(patch_file,patchdata_input_dict,
                                CII_output_data_dict,misc_dict)
    with Pool(Nb) as p:
        p.map(partial_patch_file,np.arange(1,Nb+1,1))
    partial_loading_file=partial(loading_file,patchdata_input_dict,
                                  funcdatafile_input_dict,CII_output_data_dict,
                                  misc_dict)
    with Pool(Nb) as p:
        p.map(partial_loading_file,np.arange(1,Nb+1,1))
    
    if generate_plt: 
        partial_get_plt = partial(get_plt,time_period)
        with Pool(Nb) as p:
            p.map(partial_get_plt,np.arange(1,Nb+1,1))

if __name__=='__main__':
    ##############################    SONATA    ###############################
    filepath_SONATA_yml = './SONATA/Bo_105.yml'
    ########################    WOPWOP Files    ###############################
    directory_to_bin_patchfile = './'
    directory_to_bin_funcdatafile = './'
    ##############################    CII    ##################################
    # cii_dir = '/home/HT/ge56beh/Work/Python/Data_SciTech_2021/CII/Parameter_study/1P/0.00/'
    # cii_filename = '0.700_0.400_0.000_330.0_2.000_0.000_0.000_0.000_0.000_0.000_0.000_0.000_0.000.out'
       
    # CII_output_data_dict = CII_extract_all.cii_extract_all(cii_dir+cii_filename) 
    # pickle.dump( CII_output_data_dict, open( 'sample_CII_output_data_dict.p', 'wb' ) )
    CII_output_data_dict = pickle.load( open( f'sample_CII_output_data_dict.p', "rb" ) )    

    generate_files(CII_output_data_dict,concurrency=True,generate_plt=True)










































































































































