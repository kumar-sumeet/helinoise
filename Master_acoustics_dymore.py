"""
This is the main script that starts processes that generate the binary input 
surface and loading for acoustic analysis using PSU-WOPWOP. 

Note: 'surface', 'patch' and 'patch_name' have been interchangeably used 
throughout this entire toolchain to refer to the same entity. CII refers to 
CAMRAD II.
"""

import numpy as np
from concurrent.futures import ProcessPoolExecutor as Pool
import os
import sys
from functools import partial
import pickle
import time
import itertools
import glob
import subprocess
from shutil import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/SONATA')
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/HeliNoise/TecPlot')
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/HeliNoise/TecPlot/macros')
from HeliNoise.CII import CII_extract_all
from HeliNoise.utl import crawler
from HeliNoise.PSU_WOPWOP.gen_inputfiles import gen_inputfiles
from HeliNoise.PSU_WOPWOP import crawler_create_files

# from HeliNoise.TecPlot.gen_wopwop_plt import get_plt
from HeliNoise.TecPlot import animatemp4, ParallelImageCreator
from HeliNoise.TecPlot.macros import rotor as macros_rotor
import initialise

def generate_files(aug_data_dict,dataframename,concurrency=True,generate_plt=True):    
    """
    All the input information relevant to acoustic analysis is organised here.
    For e.g. for rigid blade analysis `patchdata_input_dict['periodicity']` can
    be set as 1 irrespective of whether CII solution output is based on elastic 
    blade.
    
    Parameters
    ----------
    aug_data_dict : dict
        contains all relevant comprehensive analysis solution (CII/Dymore) 
        output in a dict format for one rotor
    generate_plt : bool, optional
        set to `True` to generate *.plt files corresponding to each blade to 
        view the blade geometry for debugging/veryfication purposes. The 
        default is `False`. Pytecplot installation is required for this.
    
    To-do
    -----
    concurrency : bool, optional
        set to `False`to generate files for each blade sequentially, otherwise
        multiprocessing is used
   
    """
    
    cycles = 1 #number of periodic cylces in periodic data (use to circumvent issue of dym data not being STRICTLY periodic)
    time_period = cycles*2*(np.pi)/aug_data_dict['SPEED']['OMEGA (RAD/SEC)']            
    time_steps_aero = aug_data_dict['time_steps_aero']                                  
    time_steps_motion = aug_data_dict['time_steps_motion']     
    TIME_STEPS = cycles*aug_data_dict['TIME_STEP'][0]  
    
    print(f'time_period={time_period}')
    print(f'time_steps_aero={time_steps_aero}')
    print(f'TIME_STEPS={TIME_STEPS}')
    # print(f'time_period={time_period}')
    periodicOraperiodic = aug_data_dict['periodicOraperiodic']    
    if periodicOraperiodic=='periodic':
        periodicity = 2
    elif periodicOraperiodic=='aperiodic':
        periodicity = 3
    elif periodicOraperiodic=='constant':
        periodicity = 1
        
    # periodicity = 2
    if periodicity==2:
        time_steps_or_keys = 'keys' #following output when using time steps for periodic data
                                    #ERROR: The timestep in the surface file does not match that in the loading file
        time_steps_motion = time_steps_motion[-(TIME_STEPS+1):]                         
        time_steps_aero = time_steps_aero[-(TIME_STEPS+1):]                         
    elif periodicity==3:
        time_steps_or_keys = 'time steps'
        time_steps_motion = time_steps_motion[:]         #last 26s = 16575 steps, last 11s = 7013 steps                
        time_steps_aero = time_steps_aero[:]       
    elif periodicity==1:
        time_steps_or_keys = ''
        time_steps_motion = []
        time_steps_aero = []                  

    no_motion_time_steps = len(time_steps_motion)
    no_aero_time_steps = len(time_steps_aero)

    if no_aero_time_steps!=no_motion_time_steps: raise ValueError              # these need to be equal for wopwop to work
    directry = aug_data_dict['directry']
    misc_dict = {
                'debug':False, #print out extra info that might be relevant for debugging HeliNoise (run for only 1 blade)
                'fishbac_spantr' : 0.02,                                       # active camber blade spanwise transition as percentage of radius
                'surfaces_dict' : {
                                   'lifting_surfaces':['upper surface',
                                                       'lower surface'],
                                    'end_surfaces':['inboard tip','outboard tip'],
                                   'compact_surfaces':['lifting-line']
                                   },
                'time_steps_or_keys' : time_steps_or_keys,    # wopwop feature 
                'directory_to_bin_patchfile' : directry,
                'directory_to_bin_funcdatafile' : directry,
                'filepath_SONATA_yml' : aug_data_dict['filepath_SONATA_yml'],
                'generate_plt' : generate_plt,
                'periodicity_def' : {1:'constant',2:'periodic',3:'aperiodic',4:'mtf'},
                'smoothdata': False, #smooth out periodic dymore data (only works for bladeprecone(rotating))
                }
    
    #############################    Patchfile ################################
    patchdata_input_dict ={
                           'units':'Pa',                                       # len of the str should not exceed 32 bytes
                           'comments':b'''Patch data file containing geometry 
                                          information of Bo 105''',            # len of the str should not exceed 1024 bytes
                           'grid':1,                                           # 'structured/unstructured'
                           'periodicity':periodicity,                                    # 'constant/periodic/aperiodic/mtf'
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
                               'periodicity':periodicity,                                #'constant/periodic/aperiodic/mtf'         
                               'normal_vecs':1,                                #'normal vectors node-centered/face-centered'
                               'aero_data':2,                                  #'surface pressure(GAUGE PRESSURE!!)/surface loading vector/flow parameters'   
#caution when using this parameter
                               'frame':3,                                      #'stationary ground-fixed frame/rotating ground-fixed frame/patch-fixed frame'
                               'time period':time_period, 
                               'number of time steps':no_aero_time_steps,
                               'time steps':time_steps_aero,
                               'keys':np.arange(0,no_aero_time_steps,1) 
                              }

    Nb = aug_data_dict['Nb']
    rotate=1 #default anti-clockwise rotation
    # pickle.dump( aug_data_dict, open( f'{directry}/aug_data_dict.p', 'wb' ) )
    # multiprocessing is used for speed-up, however this messes up output to
    # the terminal a bit (each statement from SONATA gets printed 'Nb' times)     
    partial_gen_inputfiles=partial(gen_inputfiles,patchdata_input_dict,
                                    funcdatafile_input_dict,
                                aug_data_dict,misc_dict,dataframename,rotate)
    #since using multiple cylces data to get 1 period worth of noise, this is throwing an error
    # with Pool(Nb) as p:
    #     p.map(partial_gen_inputfiles,np.arange(1,Nb+1,1))
    # partial_gen_inputfiles(f'1R1')
    if 'UTAustin' in aug_data_dict['filepath_SONATA_yml']:#this case needs to be handled differently
        if 'Bladedstacked' in aug_data_dict['filename'] or 'Bladedccr' in aug_data_dict['filename']:
            for bladeOrwing in np.arange(1,Nb+1,1):
                partial_gen_inputfiles(f'{bladeOrwing}R1')
        elif 'stacked' in aug_data_dict['filename']:
            for ridx,nb in enumerate(Nb):
                for bladeOrwing in np.arange(1,nb+1,1):
                    partial_gen_inputfiles(f'{bladeOrwing}R{ridx+1}')
        elif 'ccr' in aug_data_dict['filename']:
            # for ridx,nb in enumerate(Nb):
            #     if ridx == 0: #upper rotor rotates anti-clockwise
            #         rotate=1
            #         partial_gen_inputfiles=partial(gen_inputfiles,patchdata_input_dict,
            #                                         funcdatafile_input_dict,
            #                                     aug_data_dict,misc_dict,dataframename,rotate)
            #     elif ridx == 1: #lower rotor rotates clockwise
            #         rotate=-1
            #         partial_gen_inputfiles=partial(gen_inputfiles,patchdata_input_dict,
            #                                         funcdatafile_input_dict,
            #                                     aug_data_dict,misc_dict,dataframename,rotate)
            #     for bladeOrwing in np.arange(1,nb+1,1):
            #         print(f'{bladeOrwing}R{ridx+1}')
            #         partial_gen_inputfiles(f'{bladeOrwing}R{ridx+1}')
            with Pool(4) as p: #hard-coded for now
                p.map(partial_gen_inputfiles,['1R1','2R1','1R2','2R2'])
            
    else:        
        # for bladeOrwing in np.arange(1,Nb+1,1):
        # for bladeOrwing in np.arange(1,2,1): #use this for debugging
            # partial_gen_inputfiles(bladeOrwing)
        with Pool(Nb) as p:
            p.map(partial_gen_inputfiles,np.arange(1,Nb+1,1))
            
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
#animation for blade motion (code taken from https://github.com/Tecplot/handyscripts/blob/master/python/ParallelImageCreator.py)

import multiprocessing
import atexit
import tecplot as tp
def initialize_process(layout_file):
    atexit.register(tp.session.stop)
    tp.macro.execute_command("$!FileConfig LoadOnDemand { UNLOADSTRATEGY = MinimizeMemoryUse }")
    tp.load_layout(layout_file)
def save_image(args):
    solution_time, width, supersample, image_file = args
    tp.active_frame().plot().solution_time = solution_time
    tp.export.save_png(image_file, width=width, supersample=supersample)
    return image_file
def animatemp4_multiprocess(directry, basename, animation_dict):
    layoutfile = f"{directry}/{basename}.lay"
    numprocs = multiprocessing.cpu_count()
    imagewidth = animation_dict['imagewidth']
    supersamplefactor = animation_dict['supersamplefactor']
    endtime = animation_dict['endtime']

    tp.new_layout()
    tp.load_layout(layoutfile)
    solution_times = tp.active_frame().dataset.solution_times
    tp.session.stop()
    multiprocessing.set_start_method('spawn', force=True)

    # Set up the pool with initializing function and associated arguments
    pool = multiprocessing.Pool(processes=numprocs,
                                initializer=initialize_process,
                                initargs=(layoutfile,))
    try:
        job_args = []
        for i, solution_time in enumerate(solution_times):
            if solution_time > endtime: 
                break 
            image_file = f'{directry}/{basename}_' + "%06d.png" % (i)
            job_args.append((solution_time, imagewidth, supersamplefactor, image_file))
        image_files = pool.map(save_image, job_args)
    finally:
        pool.close()
        pool.join()
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
def start_gen_files( SONATA_ymlfilepath, coarse_fine, periodicOraperiodic, generate_plt, datadir_mdl_filename_dataframename):
    """
    

    Parameters
    ----------
    grid_res : int
        decides whether the geometry generated has a fine descretization or a 
        low res discretization over the chord. Set to 2 to make geometry look 
        smooth. Set to 0 for debug purposes or fast execution of script.
        (Radial discretization of geometry based on res used in comprehensive 
         analysis result in output_data_dict)
    periodicOraperiodic : str
        'aperiodic' or 'periodic'
    maindir_filename_dataframename : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    datadir = datadir_mdl_filename_dataframename[0]
    mdl = datadir_mdl_filename_dataframename[1]
    filename = datadir_mdl_filename_dataframename[2]
    dataframename = datadir_mdl_filename_dataframename[3]
    directry = f'{datadir}/{mdl}/{filename}/{filename}'
    output_data_dict = pickle.load( open( f'{directry}/{filename}.p', "rb" ) )
    aug_data_dict = output_data_dict.copy()
    aug_data_dict['disp_or_pos'] = 'pos'
    aug_data_dict['filename'] = filename
    aug_data_dict['filepath_SONATA_yml'] = SONATA_ymlfilepath
    aug_data_dict['grid_res'] = coarse_fine
    aug_data_dict['directry'] = directry    #unclean to add this here; fix later
    aug_data_dict['periodicOraperiodic'] = periodicOraperiodic
    generate_files(aug_data_dict,dataframename,generate_plt=generate_plt)
    
def runwopwop(datadir_mdl_filename):
    datadir = datadir_mdl_filename[0]
    mdl = datadir_mdl_filename[1]
    filename = datadir_mdl_filename[2]
    os.chdir(f'{datadir}/{mdl}/{filename}')
    subprocess.run('/HTOpt/psu_wopwop/wopwop_v3.4.3/wopwop3_serial')
    
if __name__=='__main__':
    starttime = time.time()

    wopwop_datapath = './Data' 
    periodicOraperiodic = 'periodic' #aperiodic or periodic
    coarse_fine = 2 #chordwise discretization, 0 -> coarse, 1->medium, 2-> fine
    generate_plt = True
    runcase =  [
            'bo105_complex',
             ]
    runcase_dict = { 'hartii': 0,   'bo105_simple':1,  'bo105_simple_fromhartii':2,
                    'bo105_simple_fromhartiiquicktrim':3,
                    'bo105_complex':4, 'uh60a':5, 'test':6, 'wingAnsell':7,
                    'wingelliptical':8, 'wing2D':9, 'wingCOARSE':10,
                    'utaustin_2bladedstacked': 11, 'utaustin_4bladedstacked':12, 
                    'utaustin_stacked':13, 'utaustin_2bladedccr':14,
                    'utaustin_4bladedccr':15,'utaustin_ccr':16,
                    }
    idx0 = runcase_dict[runcase[-1]]
    print(runcase[-1])
    mdls, SONATA_ymlfilepaths, dataframenamess, filenamess, wopwopoutdirss = initialise.runsetup(wopwop_datapath,periodicOraperiodic)
    mdl, SONATA_ymlfilepath, dataframenames, filenames, wopwopoutdirs = mdls[idx0:idx0+1], SONATA_ymlfilepaths[idx0], dataframenamess[idx0], filenamess[idx0], wopwopoutdirss[idx0]

    datadir_mdl_filename_dataframename = list(itertools.product(wopwopoutdirs,mdl,filenames,dataframenames))

    # for ddir_mdl_file_dfn in datadir_mdl_filename_dataframename:
    #     start_gen_files(SONATA_ymlfilepath, coarse_fine, periodicOraperiodic,generate_plt, ddir_mdl_file_dfn)    

    #note that *.dat wopwop input files in multiple frames can be obtained using
    #this script but 'frame' entry in funcdatafile_input_dict needs to be changed accordingly
    partial_parallel_genfiles=partial(start_gen_files,SONATA_ymlfilepath, coarse_fine, periodicOraperiodic, generate_plt)
    with Pool(4) as p:
        p.map(partial_parallel_genfiles,datadir_mdl_filename_dataframename)       
            # pickle.dump( output_data_dict, open( 'sample_CII_output_data_dict.p', 'wb' ) )
    
    
    # output_data_dict = pickle.load( open( 'sample_CII_output_data_dict.p', "rb" ) )    
    # # output_data_dict['Nb'] = 1
    # # pickle.dump( output_data_dict, open( 'sample_CII_output_data_dict.p', 'wb' ) )
    # generate_files(output_data_dict,concurrency=True,generate_plt=True)

