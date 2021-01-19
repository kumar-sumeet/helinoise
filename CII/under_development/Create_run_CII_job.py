#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:22:49 2019

@author: ge56beh
"""

import time
import os
import os.path
import subprocess
import shutil

def get_num_lic():
    cmd = ['/HTOpt/ansys/17.2/ansys_inc/v172/fluent/bin/lmstat','-a']
    lic_output = subprocess.check_output(cmd)
    lic_output = lic_output.decode("utf-8")
    lic_output = lic_output.split(" ")
    for i, j in enumerate(lic_output):
        if j == 'licenses':
            num_lic = lic_output[i+5]
            break
    return int(num_lic)


def create_new_CII_job(dir_path,copy_from,copy_to,replacement_data_dict):
    '''
    starts the CII calculation by executing the job file 
    
    Parameters
    -------
    copy_from : string
        job filename with all the relevant default entries of parameters
    copy_to : string
        the new job filename with changed parameters
    replacement_data_dict : dict
        dictionary containing the CII variables as keys and corresponding new data (as list) as value of that key 
    dir_path : string
        path to the directory that contains the job files
    
    Returns
    -------

    '''
    shutil.copyfile(dir_path+'/'+copy_from,dir_path+'/'+copy_to)
    f=open(dir_path+'/'+copy_to,'r')
    copied_file_lines=f.readlines()
    new_file_lines=copied_file_lines.copy()
    for param,replace_val in replacement_data_dict.items():
        for index,line in enumerate(copied_file_lines):
            if param in line:
                new_line=param+'='+replace_val+'\n'
                new_file_lines[index]=new_line                
                break
    f.close()
    f=open(dir_path+'/'+copy_to,'w')
    for line in new_file_lines: f.write(line)
    f.close()
    
def run_CII_job(dir_path,jobfile):     
    '''
    starts the CII calculation by executing the job file 
    
    Parameters
    -------
    jobfile : string
        name of the job file that needs to be executed
    dir_path : string
        path to the directory that contains the job file
    
    Returns
    -------

    '''
    os.chdir(dir_path)
    subprocess.Popen(['csh',jobfile],preexec_fn=os.setpgrp)
    print('csh ',jobfile)
    print('CII job file has been executed')
    print('waiting for output file to be ready...')
    
def check_CII_job_finished(filepath):                                   
    '''
    check if the output file is ready (i.e. the simulation has finished) 
    
    Parameters
    -------
    filepath : string
        nondimensional grid location
    
    Returns
    -------

    '''
    while True:
        f=open(filepath)
        read_all=f.readlines()
        if 'ANALYSIS EXIT (END OF PROGRAM)' in read_all[-1]:    #check if the end of the file has this string
            print('CII output file is ready')
            f.close()
            break
        f.close()
        time.sleep(30)    #wait for sometime before again checking to see if the ouput file is ready
        print('...still checking if camrad file has run')

def create_run_CII_job(dir_path,template_jobfilename,new_jobfile_name,replacement_data_dict):
    max_lic = 20
    while True:
        time.sleep(1)    #keep checking after a time delay
        num_lic = 20
        # counting number of available licenses --> comparing with allowed licenses
        try:
            num_lic = get_num_lic()
            print('no of licences is',num_lic)
        except:
            time.sleep(1)
            continue
        if num_lic >= max_lic:
            continue        
        
        print('execution complete till here')
        create_new_CII_job(dir_path,template_jobfilename,new_jobfile_name,replacement_data_dict)
        run_CII_job(dir_path,new_jobfile_name)                                 #start running the camrad job file 
        tmp_string_list=dir_path.split('/')[:-1]
        output_filepath='/'.join(tmp_string_list)+'/output/'+new_jobfile_name.split('.')[0]+'.out'                #output filename same as job filename
        check_CII_job_finished(output_filepath)                                
        break
