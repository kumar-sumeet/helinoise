#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 11:08:31 2020

@author: ge56beh
"""
import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from utl import crawler

# Data_dir = '/home/HT/ge56beh/Work/AIAA_scitech_data/CII_1P'
Data_dir = '/home/HT/ge56beh/Work/Python/Acoustics/Data/CII/Camrad_files/ibc_cases'
All_filepath_dict,All_filenames_dict = crawler.get_files_info(Data_dir)

Unreliable_files={}
for mu,filenames in All_filenames_dict.items():  
    Unreliable_files[mu]=[]
    print(mu)
    for idx,filename in enumerate(filenames):
        filename_lst=[]
        for a in filename.split('_'):
            if a=='0.0': a='0.000'
            filename_lst.append(a)
        filename_new='_'.join(filename_lst)       
        os.rename(f'{Data_dir}/{mu}/{filename}.out', f'{Data_dir}/{mu}/{filename_new}.out')
        
        with open(f'{Data_dir}/{mu}/{filename_new}.out', 'r') as f:
            if 'RESULTS UNRELIABLE' in f.read(): 
                print(filename_new)
                Unreliable_files[mu].append(filename_new)
                os.rename(f'{Data_dir}/{mu}/{filename_new}.out', f'{Data_dir}/{mu}/{filename_new}.notrel')
        