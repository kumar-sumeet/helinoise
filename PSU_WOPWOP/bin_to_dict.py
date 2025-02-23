#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 09:03:31 2019

@author: SumeetKumar
"""
from collections import OrderedDict 
import struct as struct
import os
import sys

###########################################################################################################################################
def data_extract_func(read_from_file,pointer_location,read_chunk,extract_type):       
    '''
    Reads a chunk of data from binary data file and converts it to appropriate format 
    
    Parameters
    ----------
    read_from_file : file object
        text file where data is being read from 

    pointer_location : int
        location within file where data is to be read 

    read_chunk : int
        size of data (in bytes) to be read                   

    extract_type : str
        expected data type of the extracted chunk of binary data                  

    Returns
    ----------
    pointer_location_new : int
        new location where the next chunk of data should be written
    
    decoded_bin_chunk : 
        data converted from binary format
        

    '''

    read_from_file.seek(pointer_location)
    extract_bin_text=read_from_file.read(read_chunk)
    
    if extract_type=='int' or extract_type=='signed-int':
        decoded_bin_chunk=int(int.from_bytes(extract_bin_text,byteorder='little', signed=True))    #not sure if this is True even for 'int', either way the value seems to be the same
        pointer_location_new=pointer_location+read_chunk
        
    elif extract_type=='float':
        [float_text]=struct.unpack('f',extract_bin_text)
        decoded_bin_chunk=float_text
        
        pointer_location_new=pointer_location+read_chunk
    elif extract_type=='string':
        decoded_bin_chunk=extract_bin_text.decode(encoding='utf-8')
        pointer_location_new=pointer_location+read_chunk
        
    elif extract_type=='ascii':
        decoded_bin_chunk=extract_bin_text
        pointer_location_new=pointer_location+read_chunk

    return pointer_location_new,decoded_bin_chunk


###########################################################################################################################################
###########################################################################################################################################
def patchfile(filepath_to_patchfile,size_check=False):                                          
    """
    Converts binary data in patch file to appropriate (human) readable format 
    and returns it as dictionary 
    
    Parameters
    ----------
    filepath_to_patchfile : str
        complete filepath of the binary patch file

    Returns
    ----------
    patchfile_all_data_dict : dict
        dictionary with self-explanatory organization of all patch file data
          
    TO-DO
    ----------
    #Functionality for unstructured grid data has not yet been added since all examples files use structured data
    #Functionality for periodic geometry data has aeen added but needs to be rigorously tested
    #extracting iblank data feature needs to be added
    """

    patchfile_all_data_dict=OrderedDict({'data upto format string':{},'header info':{},'zones data':{}}) 
    
    with open(filepath_to_patchfile,'rb') as f_read:                                #open file to read in binary format
        pointer_loc=0                                                              #determines location of the cursor while reading the file
        
        ######################################################################################################################   
        ####    Extracting binary data and storing it as text in patchfile_all_data_dict upto the 'Format String' data    ####
        ######################################################################################################################
        data_type=['signed-int','signed-int','signed-int','string','ascii','int','int','int','int','int','int','int','int']
        size=[4,4,4,32,1024,4,4,4,4,4,4,4,4]
        infotext_for_textfile=['magic number','version','number','units','comments','1->geometry file/-1->node subset geometry file','number of zones',\
                           'structured/unstructured','constant/periodic/aperiodic/mtf','normal vectors node-centered/face-centered',\
                           'single precision/double precision','iblank','future use']
    
        for index,(dt,s) in enumerate(zip(data_type,size)):  
            pointer_loc,patchfile_all_data_dict['data upto format string'][infotext_for_textfile[index]]=data_extract_func(f_read,pointer_loc,s,dt)    #patch name
    
        #############################################        
        ####    Extracting header information    ####
        #############################################
        if patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==1:
            patchfile_all_data_dict['header info']={'patch names':[],'grid size':[]}
        elif patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2:    
            patchfile_all_data_dict['header info']={'patch names':[],'grid size':[],'time steps or keys':[]}
        elif patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==3:
            patchfile_all_data_dict['header info']={'patch names':[],'grid size':[],'time steps or keys':[]}
    
        for _ in range(0,patchfile_all_data_dict['data upto format string']['number of zones']): 
            pointer_loc,text=data_extract_func(f_read,pointer_loc,32,'string')    
            patchfile_all_data_dict['header info']['patch names'].append(text.strip())     #removing extra spaces from the string (since it can be shorter than the allocated 32 bytes) 
        
            if patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2: 
                pointer_loc,t_period=data_extract_func(f_read,pointer_loc,4,'float')                  #time period
                patchfile_all_data_dict['header info']['time period']=t_period
                pointer_loc,no_t_steps=data_extract_func(f_read,pointer_loc,4,'int')                  #time steps
                patchfile_all_data_dict['header info']['number of time steps']=no_t_steps              
                
            elif patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==3:
                pointer_loc,no_t_steps=data_extract_func(f_read,pointer_loc,4,'int')                  #time steps
                patchfile_all_data_dict['header info']['number of time steps']=no_t_steps              
        
            elif patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==4:
                print('Functionality corresponding to patchfile_all_data_dict[data upto format string][constant/periodic/aperiodic/mtf]=4 has not been created yet')
                sys.exit()
    
            pointer_loc,dim1=data_extract_func(f_read,pointer_loc,4,'int')                        #1st dimension
            pointer_loc,dim2=data_extract_func(f_read,pointer_loc,4,'int')                        #2nd dimension
            patchfile_all_data_dict['header info']['grid size'].append([dim1,dim2])
            
        #################################################################################################
        ####    Extracting zones data based on format string data and header info collected above    ####
        #################################################################################################
        coordinates=['X','Y','Z']
    
        while True:
                     
            #read the time_step_or_key info and move pointer_loc back since iteration happens in the loop below as well
            if patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2 or \
               patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==3:
                pointer_loc,time_step_or_key=data_extract_func(f_read,pointer_loc,4,'float')
                patchfile_all_data_dict['header info']['time steps or keys'].append(time_step_or_key)
                pointer_loc=pointer_loc-4   
            
            for idx,patch_name in enumerate(patchfile_all_data_dict['header info']['patch names']):
    
                #read the time_step_or_key info but don't do anything about it
                if patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2 or \
                   patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==3:
                    pointer_loc,time_step_or_key=data_extract_func(f_read,pointer_loc,4,'float')
                
                #do this for the first time_step_or_key only
                if patch_name not in patchfile_all_data_dict['zones data']:
                    patchfile_all_data_dict['zones data'][patch_name]={}
                
                #getting the number of nodes or nomrals vectors
                if patchfile_all_data_dict['data upto format string']['normal vectors node-centered/face-centered']==2 or \
                   patchfile_all_data_dict['data upto format string']['normal vectors node-centered/face-centered']==3:    #not sure about this (this seems to be true only for unstructured example formats provided in the manual)               
                    num_node_vecs=patchfile_all_data_dict['header info']['grid size'][idx][0]
                    num_norm_vecs=patchfile_all_data_dict['header info']['grid size'][idx][1]
                else:                                   
                    num_node_vecs=patchfile_all_data_dict['header info']['grid size'][idx][0]*patchfile_all_data_dict['header info']['grid size'][idx][1]
                    num_norm_vecs=num_node_vecs                
                
                #iterating through the number of nodes along each direction
                for direction in coordinates:                                                            #extracting node data       
                    node_lst_name = patch_name+' '+direction+' node data' 
                    if node_lst_name in patchfile_all_data_dict['zones data'][patch_name]:
                        pass
                    else:
                        patchfile_all_data_dict['zones data'][patch_name][node_lst_name]=[]              #create this list only for first time step
                    node_lst = []
                    for _ in range(num_node_vecs):
                        pointer_loc,node_coord_val=data_extract_func(f_read,pointer_loc,4,'float')       #extracting node data along 'direction' corrdinate grid point by grid point
                        node_lst.append(node_coord_val)                                                  #compiling it all into a list       
                    patchfile_all_data_dict['zones data'][patch_name][node_lst_name].append(node_lst)
                
                #iterating through the number of normals along each direction
                for direction in coordinates:                                                             #extracting normal data      
                    normal_lst_name = patch_name+' '+direction+' normal data'
                    if normal_lst_name in patchfile_all_data_dict['zones data'][patch_name]:
                        pass
                    else:
                        patchfile_all_data_dict['zones data'][patch_name][normal_lst_name]=[]                        #create this list only for first time step  
                    normal_lst = []
                    for _ in range(num_norm_vecs):
                        pointer_loc,norm_coord_val=data_extract_func(f_read,pointer_loc,4,'float')       #extracting node data along 'direction' corrdinate grid point by grid point
                        normal_lst.append(norm_coord_val)                                                #compiling it all into a list 
                    patchfile_all_data_dict['zones data'][patch_name][normal_lst_name].append(normal_lst)
        #        #extracting iblank data (currently works only for structured grid)
        #        if patchfile_all_data_dict['data upto format string']['iblank']==1:                                             
        #            patchfile_all_data_dict['zones data'][patch_name+' iblank data']=[]
        #            for _ in range(num_norm_vecs):
        #                pointer_loc,norm_coord_val=data_extract_func(f_read,pointer_loc,4,'float')
        #                patchfile_all_data_dict['zones data'][patch_name+' iblank data'].append(norm_coord_val)
    
            if patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==1:
                break   #breaks the while loop after just reading one set of data
                
            if patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2 or \
               patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==3:
                if len(patchfile_all_data_dict['header info']['time steps or keys'])<patchfile_all_data_dict['header info']['number of time steps']:        #just checking for the last patch from the iteration above (so assumes that all the patches have same number of time steps)
                    continue
                else:
                    break    #breaks the while loop after data from all the time steps has been extracted               

    
    ##############################################################################################
    ####    Checking if there is additional binary text left in the binary file to convert    ####
    ##############################################################################################
    if size_check:
        print('bin_to_dict: pointer location till where patchfile data was read--------------------->' ,pointer_loc)
        with open(filepath_to_patchfile,'rb') as f_check:
            for _ in f_check: pass            
            pointer_loc_check=f_check.tell()
        print('bin_to_dict: pointer location till where patchfile data is available----------------->' ,pointer_loc_check)
        #secondary check
        print('bin_to_dict: binary file size (secondary check) ------------------------------------->',os.stat(filepath_to_patchfile).st_size)
               
    return patchfile_all_data_dict

        
###########################################################################################################################################
###########################################################################################################################################
def funcdatafile(filepath_to_funcdatafile,num_patchdata_zones,size_check=False):            
    """
    Converts binary data in functional data file to appropriate (human) 
    readable format and returns it as dictionary 
    
    Parameters
    ----------
    filepath_to_funcdatafile : str
        complete filepath of the binary patch file

    num_patchdata_zones : int
        number of zones for which data is provided in the patch file
    
    Returns
    ----------
    funcdatafile_all_data_dict : dict
        dictionary with self-explanatory organization of all functional file data
          
    TO-DO
    ----------
    #Functionality for unstructured grid data has not yet been added since all examples files use structured data
    #The current construct is for all loading data with the same number of time steps 
    (not sure if it is even worth it to expand here since it would be imperative to have the source code to be really sure what's going on!!!)
    #extracting iblank data feature needs to be added
    """
    
    funcdatafile_all_data_dict=OrderedDict({'data upto format string':{},'zone specification':{},'header info':{},'zones data':{}}) 

    with open(filepath_to_funcdatafile,'rb') as f_read:                             #open file to read in binary format
        pointer_loc=0                                                              #determines location of the cursor while reading the file
    
        #######################################################################################################################
        ####    Extracting binary data and storing it as text in funcdatafile_all_data_dict upto the format string data    ####
        #######################################################################################################################
        data_type=['signed-int','signed-int','signed-int','ascii','int','int','int','int','int','int','int','int','int','int']
        size=[4,4,4,1024,4,4,4,4,4,4,4,4,4,4]
        infotext_for_textfile=['magic number','version','number','comments','number to indicate this is a functional data file','number of zones',\
                           'structured/unstructured','constant/periodic/aperiodic/mtf','normal vectors node-centered/face-centered',\
                           'surface pressure(GAUGE PRESSURE!!)/surface loading vector/flow parameters','stationary ground-fixed frame/rotating ground-fixed frame/patch-fixed frame',\
                           'single precision/double precision','future use 1','future use 2']
        for index,(dt,s) in enumerate(zip(data_type,size)):       
            pointer_loc,funcdatafile_all_data_dict['data upto format string'][infotext_for_textfile[index]]=data_extract_func(f_read,pointer_loc,s,dt)
    
        #Raise error if the number of zones in the file are not same as in geometry file (consistency check)
        if funcdatafile_all_data_dict['data upto format string']['number of zones']!=num_patchdata_zones:
            sys.exit('ERROR :: Number of zone entries in Functional data file not the same as in Patch data file')
    
        ##################################################
        ####    Extracting zone specification data    ####
        ##################################################
        pointer_loc,funcdatafile_all_data_dict['zone specification']['number of zones with data']=data_extract_func(f_read,pointer_loc,4,'int')  
        
        funcdatafile_all_data_dict['zone specification']['zones with data']=[]
        for i in range(funcdatafile_all_data_dict['zone specification']['number of zones with data']):        
            pointer_loc,text=data_extract_func(f_read,pointer_loc,4,'int')  
            funcdatafile_all_data_dict['zone specification']['zones with data'].append(text)
    
        #############################################        
        ####    Extracting header information    ####
        #############################################
        if funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==1:
            funcdatafile_all_data_dict['header info']={'patch names':[],'grid size':[]}                     #since 'funcdatafile_all_data_dict' is an Ordered dict, the order of keys is important
        elif funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2:    
            funcdatafile_all_data_dict['header info']={'patch names':[],'grid size':[],'time steps or keys':[]}
        elif funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==3:
            funcdatafile_all_data_dict['header info']={'patch names':[],'number of time steps':[],'grid size':[],'time steps or keys':[]}
            
        for _ in range(funcdatafile_all_data_dict['zone specification']['number of zones with data']): 
            pointer_loc,text=data_extract_func(f_read,pointer_loc,32,'string')     
            funcdatafile_all_data_dict['header info']['patch names'].append(text.strip())             #removing extra spaces from the string (since it can be shorter than the allocated 32 bytes) 
            
            if funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2:       
                pointer_loc,t_period=data_extract_func(f_read,pointer_loc,4,'float')
                funcdatafile_all_data_dict['header info']['time period'] = t_period            #time period
                pointer_loc,no_t_steps=data_extract_func(f_read,pointer_loc,4,'int')
                funcdatafile_all_data_dict['header info']['number of time steps'] = no_t_steps  #number of time steps  
        
            elif funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==3:
                pointer_loc,no_t_steps=data_extract_func(f_read,pointer_loc,4,'int')
                funcdatafile_all_data_dict['header info']['number of time steps'] = no_t_steps  #number of time steps  
        
            elif funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==4:
                print('Functionality corresponding to funcdatafile_all_data_dict[data upto format string][constant/periodic/aperiodic/mtf]=3 has not been created yet')
                pass
    
            pointer_loc,dim1=data_extract_func(f_read,pointer_loc,4,'int')                        #1st dimension
            pointer_loc,dim2=data_extract_func(f_read,pointer_loc,4,'int')                        #2nd dimension 
            funcdatafile_all_data_dict['header info']['grid size'].append([dim1,dim2])
                
        #################################################################################################
        ####    Extracting zones data based on format string data and header info collected above    ####
        #################################################################################################
        
        coordinates=['X','Y','Z']
        
        while True:
    
            #read the time_step_or_key info and move pointer_loc back since iteration happens in the loop below as well
            if funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2 or funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==3:
                pointer_loc,time_step_or_key=data_extract_func(f_read,pointer_loc,4,'float')
                funcdatafile_all_data_dict['header info']['time steps or keys'].append(time_step_or_key)
                pointer_loc=pointer_loc-4   
            
            for indx,patch_name_with_data in enumerate(funcdatafile_all_data_dict['header info']['patch names']): 
    
                #read the time_step_or_key info but don't do anything about it
                if funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2 or funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==3:
                    pointer_loc,time_step_or_key=data_extract_func(f_read,pointer_loc,4,'float')
                    
                #read the time_step_or_key info but don't do anything about it    
                if patch_name_with_data not in funcdatafile_all_data_dict['zones data']:    
                    funcdatafile_all_data_dict['zones data'][patch_name_with_data]={}
    
                if funcdatafile_all_data_dict['data upto format string']['normal vectors node-centered/face-centered']==2:               
                    num_node_vecs=funcdatafile_all_data_dict['header info']['grid size'][indx][0]
                    num_norm_vecs=funcdatafile_all_data_dict['header info']['grid size'][indx][1]
                else:                                   
                    num_node_vecs=funcdatafile_all_data_dict['header info']['grid size'][indx][0]*funcdatafile_all_data_dict['header info']['grid size'][indx][1]
                    num_norm_vecs=num_node_vecs                
                            
                if funcdatafile_all_data_dict['data upto format string']['surface pressure(GAUGE PRESSURE!!)/surface loading vector/flow parameters']==1:    #extracting pressure data at nodes or faces  
                    if patch_name_with_data+' pressure data' in funcdatafile_all_data_dict['zones data'][patch_name_with_data]:
                        pass
                    else:
                        funcdatafile_all_data_dict['zones data'][patch_name_with_data][patch_name_with_data+' pressure data']=[]                             #create this list only for first time step
                    list_pressure_data=[]
                    for _ in range(num_norm_vecs):
                        pointer_loc,text=data_extract_func(f_read,pointer_loc,4,'float')
                        list_pressure_data.append(text)
                    funcdatafile_all_data_dict['zones data'][patch_name_with_data][patch_name_with_data+' pressure data'].append(list_pressure_data)
    
                
                if funcdatafile_all_data_dict['data upto format string']['surface pressure(GAUGE PRESSURE!!)/surface loading vector/flow parameters']==2:    #extracting loading vector data at nodes or faces  
                    for direction in coordinates:                                                                                                            #extracting it along all directions
                        if patch_name_with_data+' '+direction+' loading vector data' in funcdatafile_all_data_dict['zones data'][patch_name_with_data]:
                            pass
                        else:
                            funcdatafile_all_data_dict['zones data'][patch_name_with_data][patch_name_with_data+' '+direction+' loading vector data']=[]     #create this list only for first time step
                        loading_vector_list=[]
                        for _ in range(num_norm_vecs):
                            pointer_loc,text=data_extract_func(f_read,pointer_loc,4,'float')  
                            loading_vector_list.append(text)
                        funcdatafile_all_data_dict['zones data'][patch_name_with_data][patch_name_with_data+' '+direction+' loading vector data'].append(loading_vector_list)
        
                if funcdatafile_all_data_dict['data upto format string']['surface pressure(GAUGE PRESSURE!!)/surface loading vector/flow parameters']==3:    #extracting flow data at nodes or faces  
                    if patch_name_with_data+' densities data' in funcdatafile_all_data_dict['zones data'][patch_name_with_data]:
                        pass
                    else:
                        funcdatafile_all_data_dict['zones data'][patch_name_with_data][patch_name_with_data+' densities data']=[]                            #create this list only for first time step
                    density_list=[]
                    for _ in range(num_norm_vecs):                                                                                                           #extracting density data at all nodes/faces
                        pointer_loc,text=data_extract_func(f_read,pointer_loc,4,'float')    
                        density_list.append(text)
                    funcdatafile_all_data_dict['zones data'][patch_name_with_data][patch_name_with_data+' densities data'].append(density_list)
                    for direction in coordinates:                                                                                                            #extracting momentum vector data at all nodes/faces
                        if patch_name_with_data+' '+direction+' momentum vector data' in funcdatafile_all_data_dict['zones data'][patch_name_with_data]:
                            pass
                        else:
                            funcdatafile_all_data_dict['zones data'][patch_name_with_data][patch_name_with_data+' '+direction+' momentum vector data']=[]    #create this list only for first time step
                        momentum_vector_list=[]
                        for _ in range(num_norm_vecs):
                            pointer_loc,text=data_extract_func(f_read,pointer_loc,4,'float')
                            momentum_vector_list.append(text)
                        funcdatafile_all_data_dict['zones data'][patch_name_with_data][patch_name_with_data+' '+direction+' momentum vector data'].append(momentum_vector_list)
                    if patch_name_with_data+' perturbation pressure data' in funcdatafile_all_data_dict['zones data'][patch_name_with_data]:
                        pass
                    else:
                        funcdatafile_all_data_dict['zones data'][patch_name_with_data][patch_name_with_data+' perturbation pressure data']=[]                #create this list only for first time step
                    perturbation_pressure_list=[]
                    for _ in range(num_norm_vecs):                                                                                                           #extracting perturbation pressure data at all nodes/faces
                        pointer_loc,text=data_extract_func(f_read,pointer_loc,4,'float')
                        perturbation_pressure_list.append(text)
                    funcdatafile_all_data_dict['zones data'][patch_name_with_data][patch_name_with_data+' perturbation pressure data'].append(perturbation_pressure_list)
           
            if funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==1:
                break   #breaks the while loop after just reading one set of data
            if funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2 or funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==3:
                if len(funcdatafile_all_data_dict['header info']['time steps or keys'])<funcdatafile_all_data_dict['header info']['number of time steps']:        #just checking for the last patch from the iteration above (so assumes that all the patches have same number of time steps)
                    continue
                else:
                    break    #breaks the while loop after data from all the time steps has been extracted               
    

    ##############################################################################################
    ####    Checking if there is additional binary text left in the binary file to convert    ####
    ##############################################################################################
    if size_check:
        print('bin_to_dict: pointer location till where functional datafile data was read----------------->' ,pointer_loc)
        with open(filepath_to_funcdatafile,'rb') as f_check:
            for _ in f_check: pass            
            pointer_loc_check=f_check.tell()
        print('bin_to_dict: pointer location till where functional datafile data is available------------->' ,pointer_loc_check)    
        print('bin_to_dict: file size (secondary check) -------------------------------------------------->',os.stat(filepath_to_funcdatafile).st_size)    #secondary check

    return funcdatafile_all_data_dict

if __name__ == "__main__":     
    
    num_patchdata_zones = 5
    func_filename = '1994_Run15_5_hover_FishBAC_PetersUnsteady_BladePrecone(rotating)_funcdataBlade1_aperiodic.dat'
    patch_filename = '1994_Run15_5_hover_FishBAC_PetersUnsteady_BladePrecone(rotating)_patchdataBlade1_aperiodic.dat'
    # directry = '/home/HT/ge56beh/Work/Python/HeliNoise/Data/Diss_runs/2_simple_hemisphere_aperiodic/1994_Run15_5_hover_FishBAC_PetersUnsteady/1994_Run15_5_hover_FishBAC_PetersUnsteady/blade_data'
    directry = '/home/HT/ge56beh/Work/Python/HeliNoise/Data/Diss_runs/1_simple_aperiodic/1994_Run15_5_hover_FishBAC_PetersUnsteady/1994_Run15_5_hover_FishBAC_PetersUnsteady/blade_data'

    patchfile_all_data_dict = patchfile(f'{directry}/{patch_filename}')
    funcfile_all_data_dict = funcdatafile(f'{directry}/{func_filename}',num_patchdata_zones)
    
    
    
    