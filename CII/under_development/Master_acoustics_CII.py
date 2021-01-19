#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 11:50:55 2019

@author: ge56beh
"""
import numpy as np

import CII_extract_all
import Create_run_CII_job

rad_discr_no=20    #cannot be more than 400 since that is the limit for CII
chord_discr_no=25

Blade_dict={'rad_discr_no':rad_discr_no,\
            'chord_discr_no':chord_discr_no,\
            'elastic':False}

rad_discr_list=list(np.linspace(0.22,1.0,Blade_dict['rad_discr_no']).round(decimals=4))
chord_disc_list=list(np.linspace(0,1.0,Blade_dict['chord_discr_no']).round(decimals=4))

##############################################################################################################################################################################################################################################################################
####################################    Necessary input information    #######################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################
FILEPATH='/home/HT/ge56beh/Work/CII/Acoustics/Manual/output/Baseline_new_1case_rigid_highres.out'
Pointer_loc_base=0                 #Do not change this 

##############################################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################

#Creating a tuple containing all the output extracted from output file of the baseline case
ALL_DATA_DICT = CII_extract_all.cii_extract_all(FILEPATH,Pointer_loc_base)   #Extracting data for the baseline case (single file) only

Dir_path='/home/HT/ge56beh/Work/CII/Acoustics/Auto_generated/jobs'
Template_jobfilename='Baseline_new_1case.lnx'
New_jobfile_name=Template_jobfilename.split('.lnx')[0]+'_r'+str(rad_discr_no)+'.lnx'
Replacement_data_dict={'set name':'\''+New_jobfile_name.split('.lnx')[0]+'\'','NRPOS':str(rad_discr_no)+',','RPOS':str(rad_discr_list)[1:-1]+',','NRCFD':str(rad_discr_no)+',','RCFD':str(rad_discr_list)[1:-1]+','}
#num_lic = Create_run_CII_job.create_run_CII_job(Dir_path,Template_jobfilename,New_jobfile_name,Replacement_data_dict)
print('script successful')