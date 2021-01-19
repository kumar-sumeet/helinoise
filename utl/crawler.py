#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Useful functions to gather and assimilate data from a parameteric study spread 
over multiple files across multiple directories
"""
import pickle
import os 

from HeliNoise.CII import CII_extract_all
from HeliNoise.TecPlot import read_wopwop_tecfile

def get_files_info(Data_dir):
    """
    Accepts path to dir containing subdirs and files within them. Returns 
    filepaths/filenames to all files within dir as a dict with subdirs as 
    dict keys and filepaths/filenames as values

    Parameters
    ----------
    Data_dir : str
        filepath to dir containing subdirs with files for analysis

    Returns
    -------
    All_filepath_dict : dict
        DESCRIPTION.
    All_filenames_dict : dict
        DESCRIPTION.

    """
    All_filepath_dict={}                                                              #List of complete file paths to each '.out' file
    All_filenames_dict={}
    dir_=[d for d in os.listdir(Data_dir) if 'pckl' not in d.lower() and 'figure'not in d.lower()]
    dir_.sort()
    for subdir in dir_:
        All_filepath_dict[subdir]=[]
        All_filenames_dict[subdir]=[]
        for _, _, filenames in os.walk(os.path.join(Data_dir,subdir)):
            for filename in filenames:
                if '.out' in filename:
                    All_filepath_dict[subdir].append(os.path.join(Data_dir,subdir,filename))                 #List of file paths
                    All_filenames_dict[subdir].append(filename.split('.out')[0])

    return All_filepath_dict,All_filenames_dict


def get_cii_output(Data_dir,All_filepath_dict,All_filenames_dict,Read_pckl=False,DesignVar=[]):
    if Read_pckl:
        print('NOTE: READING FROM STORED DATA AT ',Data_dir+'/Stored_ALL_DATA_DICT.pckl \n ...')
        with open(Data_dir+'/Stored_ALL_DATA_DICT.pckl', 'rb') as f:
            All_data_dict = pickle.load(f)        
        if DesignVar:
            print('NOTE: READING FROM STORED DESIGN DATA AT ',Data_dir+'/Stored_DESIGN_VARIABLES.pckl \n ...')
            with open(Data_dir+'/Stored_DESIGN_VARIABLES.pckl', 'rb') as g:
                DesignVar_ranges_dict = pickle.load(g)
        print('... done')    
    else:    
        All_data_dict = {}
        DesignVar_ranges_dict={}
        for idx_dir, subdir in enumerate(All_filenames_dict,1): 
            if 'figure' in subdir.lower(): continue    #ignoring the figures folder
            All_data_dict[subdir],DesignVar_ranges_dict[subdir] = {},{ var : [] for var in DesignVar }
            for idx_file, filepath in enumerate(All_filepath_dict[subdir],1):
                filename=All_filenames_dict[subdir][All_filepath_dict[subdir].index(filepath)]
                print('\r READ DIR: ',int(100*idx_dir/len(All_filepath_dict)),'%; READ FILES IN DIR: ',int(100*idx_file/len(All_filepath_dict[subdir])),'% COMPLETE', end='')
                All_data_dict[subdir][filename] = CII_extract_all.cii_extract_all(filepath)  
                if filename=='Baseline': continue
                if DesignVar:                    
                    for idx_var,var in enumerate(DesignVar):
                        DesignVar_ranges_dict[subdir][var].append(float(filename.split('_')[idx_var]))  
                        DesignVar_ranges_dict[subdir][var]=list(set(DesignVar_ranges_dict[subdir][var]))                                #removing all repeatitive entries
                        DesignVar_ranges_dict[subdir][var].sort()

        with open(Data_dir+'/Stored_ALL_DATA_DICT.pckl', 'wb') as f:
            print('\n Pickling data...')
            pickle.dump(All_data_dict, f)        
        if DesignVar:
            with open(Data_dir+'/Stored_DESIGN_VARIABLES.pckl', 'wb') as g:
                pickle.dump(DesignVar_ranges_dict, g)
        print('...done')
    if DesignVar:
        return All_data_dict, DesignVar_ranges_dict 
    else:
        return All_data_dict

def get_wopwop_files_info(Data_dir):
    All_folderpath_dict={}                                                             
    All_foldernames_dict={}
    dir_=[d for d in os.listdir(Data_dir) if 'nam' not in d.lower() and 'pckl' not in d.lower()]
    dir_.sort()
    for subdir in dir_:
        All_folderpath_dict[subdir]=[]
        All_foldernames_dict[subdir]=[]
        for subsubdir in [d for d in os.listdir(os.path.join(Data_dir,subdir))]:
            All_folderpath_dict[subdir].append(os.path.join(Data_dir,subdir,subsubdir,subsubdir))                 
            All_foldernames_dict[subdir].append(subsubdir)

    return All_folderpath_dict,All_foldernames_dict
    
def get_wopwop_output(Data_dir,All_folderpath_dict,All_foldernames_dict,Read_pckl=False,DesignVar=[]):
    if Read_pckl:
        print('NOTE: READING FROM STORED DATA AT ',Data_dir+'/Stored_ALL_DATA_DICT.pckl \n ...')
        with open(Data_dir+'/Stored_ALL_DATA_DICT.pckl', 'rb') as f:
            All_data_dict = pickle.load(f)        
        print('... done')    
    else:    
        All_data_dict = {}
        DesignVar_ranges_dict={}
        for idx_dir, subdir in enumerate(All_foldernames_dict,1): 
            # if subdir not in ['0.00','0.15','0.25','0.35']: continue
            # if 'figure' in subdir.lower(): continue    #ignoring the figures folder
            All_data_dict[subdir],DesignVar_ranges_dict[subdir] = {},{ var : [] for var in DesignVar }
            for idx_folder, folderpath in enumerate(All_folderpath_dict[subdir],1):
                foldername=All_foldernames_dict[subdir][All_folderpath_dict[subdir].index(folderpath)]
                print('\r READ DIR: ',int(100*idx_dir/len(All_folderpath_dict)),'%; READ FILES IN DIR: ',int(100*idx_folder/len(All_folderpath_dict[subdir])),'% COMPLETE', end='')
                All_data_dict[subdir][foldername] = read_wopwop_tecfile.dB(f'{folderpath}/OASPLdBA.tec') 
                # print(read_wopwop_tecfile.dB(f'{folderpath}/OASPLdBA.tec') )
                if foldername=='Baseline': continue
                if DesignVar:                    
                    for idx_var,var in enumerate(DesignVar):
                        DesignVar_ranges_dict[subdir][var].append(float(foldername.split('_')[idx_var]))  
                        DesignVar_ranges_dict[subdir][var]=list(set(DesignVar_ranges_dict[subdir][var]))                                #removing all repeatitive entries
                        DesignVar_ranges_dict[subdir][var].sort()

        with open(Data_dir+'/Stored_ALL_DATA_DICT.pckl', 'wb') as f:
            print('\n Pickling data...')
            pickle.dump(All_data_dict, f)        
        if DesignVar:
            with open(Data_dir+'/Stored_DESIGN_VARIABLES.pckl', 'wb') as g:
                pickle.dump(DesignVar_ranges_dict, g)
        print('...done')
    if DesignVar:
        return All_data_dict, DesignVar_ranges_dict 
    else:
        return All_data_dict
