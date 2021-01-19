#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:05:32 2020

@author: ge56beh
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import pathlib
from shutil import copy
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+'/SONATA'))
from HeliNoise.CII import CII_extract_all
from HeliNoise.utl import crawler
from HeliNoise.plot import make_pretty

def wopwop(Dir_CII_data,Dir_wopwop_data,cases_prototype_filepath,namelist_prototype_filepath):
      for subdir,filenames in All_filenames_dict.items():
        pathlib.Path(Dir_wopwop_data+'/'+subdir).mkdir(parents=True, exist_ok=True) 
        for filename in filenames:
            pathlib.Path(f'{Dir_wopwop_data}/{subdir}/{filename}').mkdir(parents=True, exist_ok=True)
            copy(cases_prototype_filepath, f'{Dir_wopwop_data}/{subdir}/{filename}')            
            with open(f'{Dir_wopwop_data}/{subdir}/{filename}/cases.nam', 'r') as f:    lines=f.readlines()
            lines[1]=f"globalFolderName='./{filename}/'\n"
            lines[2]=f"caseNameFile='./{filename}.nam'\n"
            with open(f'{Dir_wopwop_data}/{subdir}/{filename}/cases.nam', 'w') as f:    
                for line in lines:    f.write(line)                
                
            pathlib.Path(f'{Dir_wopwop_data}/{subdir}/{filename}/{filename}').mkdir(parents=True, exist_ok=True)
            pathlib.Path(f'{Dir_wopwop_data}/{subdir}/{filename}/{filename}/blade_data').mkdir(parents=True, exist_ok=True)
            copy(namelist_prototype_filepath, f'{Dir_wopwop_data}/{subdir}/{filename}/{filename}')
            os.rename(f'{Dir_wopwop_data}/{subdir}/{filename}/{filename}/_.nam', f'{Dir_wopwop_data}/{subdir}/{filename}/{filename}/{filename}.nam')
            with open(f'{Dir_wopwop_data}/{subdir}/{filename}/{filename}/{filename}.nam', 'r') as f:    lines=f.readlines()
            lines[64]=f"			VH = -{All_data_dict[subdir][filename]['SPEED']['VELOCITY (M/SEC)']},0.0,0.0"
            lines[81]=f"  anglevalue     = {(np.pi/180)*All_data_dict[subdir][filename]['ASHAFT']:.4f}\n"
            lines[94]=f"  patchGeometryFile= './blade_data/{filename}_patchdataBlade1_periodic.dat'\n"
            lines[95]=f"  patchLoadingFile= './blade_data/{filename}_funcdataBlade1_periodic.dat'\n"
            lines[102]=f"  patchGeometryFile= './blade_data/{filename}_patchdataBlade2_periodic.dat'\n"
            lines[103]=f"  patchLoadingFile= './blade_data/{filename}_funcdataBlade2_periodic.dat'\n"
            lines[115]=f"  patchGeometryFile= './blade_data/{filename}_patchdataBlade3_periodic.dat'\n"
            lines[116]=f"  patchLoadingFile= './blade_data/{filename}_funcdataBlade3_periodic.dat'\n"
            lines[128]=f"  patchGeometryFile= './blade_data/{filename}_patchdataBlade4_periodic.dat'\n"
            lines[129]=f"  patchLoadingFile= './blade_data/{filename}_funcdataBlade4_periodic.dat'\n"
            with open(f'{Dir_wopwop_data}/{subdir}/{filename}/{filename}/{filename}.nam', 'w') as f:    
                for line in lines:    f.write(line)                                

if __name__=='__main__':
    freq='2P'
    Dir_CII_data = f'/home/HT/ge56beh/Work/Python/Data_SciTech_2021/CII/Parameter_study/{freq}'
    Dir_wopwop_data = f'/home/HT/ge56beh/Work/Python/Data_SciTech_2021/PSU_WOPWOP/Parameter_study/{freq}/out_of_plane'
    cases_prototype_filepath = f'{Dir_wopwop_data}/cases.nam'
    namelist_prototype_filepath = f'{Dir_wopwop_data}/_.nam'
    # Dir_CII_data = '/home/HT/ge56beh/Work/Python/Acoustics/Data/CII/Camrad_files/bvi'
    # Dir_wopwop_data = '/home/HT/ge56beh/Work/Python/Acoustics/Data/PSU_WOPWOP/PSU_WOPWOP_new/BVI_SingleObserver_validation'
    # cases_prototype_filepath = '/home/HT/ge56beh/Work/Python/Acoustics/Data/PSU_WOPWOP/PSU_WOPWOP_new/BVI_SingleObserver_validation/cases.nam'
    # namelist_prototype_filepath = '/home/HT/ge56beh/Work/Python/Acoustics/Data/PSU_WOPWOP/PSU_WOPWOP_new/BVI_SingleObserver_validation/_.nam'
    # Dir_CII_data = '/home/HT/ge56beh/Work/Python/Acoustics/Data/CII/Camrad_files/best_cases_journal_paper/highres_out'
    # Dir_wopwop_data = '/home/HT/ge56beh/Work/Python/Acoustics/Data/PSU_WOPWOP/PSU_WOPWOP_new/best_cases_journal_paper'
    # cases_prototype_filepath = '/home/HT/ge56beh/Work/Python/Acoustics/Data/PSU_WOPWOP/PSU_WOPWOP_new/best_cases_journal_paper/cases.nam'
    # namelist_prototype_filepath = '/home/HT/ge56beh/Work/Python/Acoustics/Data/PSU_WOPWOP/PSU_WOPWOP_new/best_cases_journal_paper/_.nam'
    
    All_filepath_dict,All_filenames_dict = crawler.get_files_info(Dir_CII_data)
    All_data_dict = crawler.get_cii_output(Dir_CII_data,All_filepath_dict,All_filenames_dict,Read_pckl=True)
    wopwop(All_data_dict,Dir_wopwop_data,cases_prototype_filepath,namelist_prototype_filepath)
