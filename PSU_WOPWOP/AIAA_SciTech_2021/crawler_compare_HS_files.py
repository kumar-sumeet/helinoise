#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:13:09 2020

@author: ge56beh
"""
import os
import subprocess

def wopwop(Dir_wopwop_data,All_file_names_dict):
    for subdir,filenames in All_file_names_dict.items():
        for filename in filenames:
            print(subdir,'---',filename)
            os.chdir(f'{Dir_wopwop_data}/{subdir}/{filename}')
            subprocess.run('/HTOpt/psu_wopwop/wopwop_v3.4.3/wopwop3_serial')

if __name__=='__main__':
    Dir_CII_data = '/home/HT/ge56beh/Work/AIAA_scitech_data/CII'
    Dir_wopwop_data = '/home/HT/ge56beh/Work/AIAA_scitech_data/PSU_WOPWOP'
    All_file_names_dict={}
    dir_=[d for d in os.listdir(Dir_CII_data) if 'pckl' not in d]
    
    for subdir in dir_:
        All_file_names_dict[subdir]=[]
        for _, _, filenames in os.walk(os.path.join(Dir_CII_data,subdir+'/split_files')):
            for filename in filenames:
                if '.out' in filename:
                    All_file_names_dict[subdir].append(filename.split('.out')[0])
    wopwop(Dir_wopwop_data,All_file_names_dict)
