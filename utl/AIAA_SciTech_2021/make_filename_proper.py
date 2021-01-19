#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 18:48:40 2020

@author: ge56beh
"""

import os
import sys

# Data_dir = '/home/HT/ge56beh/Work/AIAA_scitech_data/CII_new/0.35'
# ALL_FILE_PATHS=[]                                                              #List of complete file paths to each '.out' file
# ALL_FILE_NAMES=[]
# for _, _, allfilenames in os.walk(Data_dir):
#     for filename in allfilenames:
#         if ".out" in filename:
#             filename=filename.split('.out')[0]
#             tmp=['0.000' if x=='0.0' else x for x in filename.split('_')]
#             filename_new = '_'.join(k for k in tmp)
#             ALL_FILE_PATHS.append(Data_dir+'/'+filename_new+'.out')                 #List of file paths
#             ALL_FILE_NAMES.append(filename_new)
#             os.rename(Data_dir+'/'+filename+'.out', ALL_FILE_PATHS[-1])

Data_dir = '/home/HT/ge56beh/Work/Python/Acoustics/Data/CII/Camrad_files/ibc_cases/mu30_-76'
ALL_FILE_PATHS=[]                                                              #List of complete file paths to each '.out' file
ALL_FILE_NAMES=[]
for _, _, allfilenames in os.walk(Data_dir):
    for filename in allfilenames:
        if ".out" in filename:
            filename=filename.split('.out')[0]
            tmp=['0.000' if x=='0.0' else x for x in filename.split('_')[6:]]
            custom=[format('%05.1f' % float(filename.split('_')[5]))] 
            filename_new = '_'.join(k for k in filename.split('_')[:5]+custom+tmp)            
            ALL_FILE_PATHS.append(Data_dir+'/'+filename_new+'.out')                 #List of file paths
            ALL_FILE_NAMES.append(filename_new)
            os.rename(Data_dir+'/'+filename+'.out', ALL_FILE_PATHS[-1])
            # sys.exit()
            