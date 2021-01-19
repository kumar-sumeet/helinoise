#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:13:09 2020

@author: ge56beh
"""
import os
import subprocess
import sys

def wopwop(Dir_wopwop_data,All_filenames_dict):
    for subdir,filenames in All_filenames_dict.items():
        # if subdir not in ['0.00','0.15','0.25','0.35']: continue
        for filename in filenames:
            print(subdir,'---',filename)
            # if filename =='0.700_0.400_0.000_240.0_1.500_0.000_0.000_0.000_0.000_0.000_0.000_0.000_0.000': print('found it!!!!')
            # sys.exit
            if os.path.isfile(f'{Dir_wopwop_data}/{subdir}/{filename}/{filename}/OASPLdBA.tec'): continue 
            os.chdir(f'{Dir_wopwop_data}/{subdir}/{filename}')
            subprocess.run('/HTOpt/psu_wopwop/wopwop_v3.4.3/wopwop3_serial')
            
if __name__=='__main__':
    # Dir_wopwop_data = '/home/HT/ge56beh/Work/AIAA_scitech_data/PSU_WOPWOP'
    # Dir_wopwop_data = '/home/HT/ge56beh/Work/Python/Acoustics/PSU_WOPWOP/PSU_WOPWOP_new/SingleObserver_50m'
    # Dir_wopwop_data = '/home/HT/ge56beh/Work/Python/Acoustics/PSU_WOPWOP/PSU_WOPWOP_new/SingleObserver_150m'
    # Dir_wopwop_data = '/home/HT/ge56beh/Work/Python/Acoustics/Data/PSU_WOPWOP/PSU_WOPWOP_new/BVI_SingleObserver_validation'
    Dir_wopwop_data = '/home/HT/ge56beh/Work/AIAA_scitech_data/PSU_WOPWOP/2P/out_of_plane'
    All_filenames_dict={}
        
    for subdir in next(os.walk(Dir_wopwop_data))[1]:
        All_filenames_dict[subdir]=next(os.walk(os.path.join(Dir_wopwop_data,subdir)))[1]

    wopwop(Dir_wopwop_data,All_filenames_dict)
