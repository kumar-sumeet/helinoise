#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 09:03:31 2019

@author: ge56beh
"""
import numpy as np
import struct as struct
import os

###############################################################################################################################################################
def chunk_convtobin_writetofile(f,p_loc_old,d,s,dt):                           
    '''
    secondary function to carry out the conversion to binary for data chunkwise
    
    Parameters
    ----------
    f : file object
        where the information in data chunk is written to
    p_loc_old : int
        location of pointer till where the data has been written to binary file  
        at the beginning of the function call
    d : str/int
        data chunk
    s : int
        binary size over which data chunk is written in file                    
    dt : str
        data type 

    Returns
    -------
    p_loc_new : int
        location of pointer till where the data has been written to binary file
        at the end of the function call
        
    '''
    f.seek(p_loc_old)    
    p_loc_new = p_loc_old+s

    if dt=='signed-int':
        f.write(d.to_bytes(s,byteorder='little',signed=True))
        return p_loc_new

    if dt=='int':
        f.write(d.to_bytes(s,byteorder='little',signed=False))     
        return p_loc_new

    elif dt=='float':
        f.write(struct.pack('f',d))
        return p_loc_new

    elif dt=='string':
        bin_string=d.encode(encoding='utf-8')
        if len(bin_string)>s:                #
            raise ValueError(dt,' comment larger than ',str(s),' bytes \n THIS WILL RESULT IN ERROR WHEN RUNNING WOPWOP!!!! \n Error occured while writing to ',f.name)
            
        elif len(bin_string)<=s:
            d_new=d.ljust(s)
            bin_string_new=d_new.encode(encoding='utf-8')
            f.write(bin_string_new)
        return p_loc_new

    elif dt=='ascii':
        if len(d)>s:            
            raise ValueError(dt,' comment larger than ',str(s),' bytes \n THIS WILL RESULT IN ERROR WHEN RUNNING WOPWOP!!!! \n Error occured while writing to ',f.name)
        elif len(d)<=s:
            d_new=d.ljust(s)
            f.write(d_new)
        return p_loc_new

###############################################################################################################################################################    
def patchfile(filepath_to_patchfile,patchfile_all_data_dict,size_check=False):
    '''
    accepts patch file filepath and the dictionary of all text data in that 
    file and saves it in WOPWOP-relevant binary format 
    
    Parameters
    ----------
    filepath_to_patchfile : str
        file path to the binary patchfile 

    patchfile_all_data_dict : dict
        dictionary containing all the patchfile data                    


    Notes
    -----
    - Functionality for unstructured grid data has not yet been added since all examples files use structured data
    '''

    data_type=['signed-int','signed-int','signed-int','string','ascii','int','int','int','int','int','int','int','int']
    size=[4,4,4,32,1024,4,4,4,4,4,4,4,4]

    with open(filepath_to_patchfile,'wb') as f_write:                                        #open file to write in binary format
        pointer_loc=0                                                              #determines location of the cursor while writing the file
        
        ####    writing 'data upto format string' data    ####
        for index,key in enumerate(patchfile_all_data_dict['data upto format string']):
            data_chunk=patchfile_all_data_dict['data upto format string'][key]
            pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,data_chunk,size[index],data_type[index])    #returns the new pointer location after writing the data to file
        
        binfilesize = 1100   #at this point the file size is 1100 bytes    
        ####    writing 'header info' data    ####
        for index,patch_name in enumerate(patchfile_all_data_dict['header info']['patch names']): 
            pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,patch_name,32,'string')    
            binfilesize = binfilesize+32
            
            if patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==1:                    
                dim1=patchfile_all_data_dict['header info']['grid size'][index][0]                    #1st dimension
                pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,dim1,4,'int')                        
                dim2=patchfile_all_data_dict['header info']['grid size'][index][1]                    #2nd dimension
                pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,dim2,4,'int')                        
                binfilesize = binfilesize+4+4
                
            elif patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2: 
                time_period=patchfile_all_data_dict['header info']['time period']              #time period
                pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,time_period,4,'float')
                time_steps=patchfile_all_data_dict['header info']['number of time steps']                #time steps
                pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,time_steps,4,'int')
                dim1=patchfile_all_data_dict['header info']['grid size'][index][0]                    #1st dimension
                pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,dim1,4,'int')                        
                dim2=patchfile_all_data_dict['header info']['grid size'][index][1]                    #2nd dimension
                pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,dim2,4,'int')                        
                binfilesize = binfilesize+4+4+4+4
                
            elif patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==3:
                pass
        
            elif patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==4:
                pass
    
        ####    writing 'zones data' data    ####
        if patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==1: 
            for patch_name in patchfile_all_data_dict['header info']['patch names']:
                for patch_coord_name,patch_coord_data in patchfile_all_data_dict['zones data'][patch_name].items():
                    for data_entry in patch_coord_data[0]:  #only one time step info is available 
                        pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,data_entry,4,'float')
                        binfilesize = binfilesize+4
    
        elif patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2:                 
             
                for ts_k_idx,ts_k in enumerate(patchfile_all_data_dict['header info']['time steps or keys']):  #iterating through the number of time steps
                    
                    for patch_name in patchfile_all_data_dict['header info']['patch names']:
                        
                        pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,ts_k,4,'float')
                        binfilesize = binfilesize+4
                        for patch_coord_name,patch_coord_data in patchfile_all_data_dict['zones data'][patch_name].items():
                            for data_entry in patch_coord_data[ts_k_idx]:    #writing data corresponding to all patch surfaces one time step at a time
                                pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,data_entry,4,'float')    
                                binfilesize = binfilesize+4

    if size_check:
        print('pointer location till where patchfile binary data was written----------->',pointer_loc)
    #    size_arr=np.array(size)
    #    binaryfilesize=sum(size_arr)+40*len(patchfile_all_data_dict['header info']['patch names'])
    #    print('expected size of the binary patchfile based on patchfile_all_data_dict-->', )
        #secondary check
        print('file size (secondary check) -------------------------------------------->',os.stat(filepath_to_patchfile).st_size)
        print('file size (tertiary check) --------------------------------------------->',binfilesize)
    # print('patch data converted to binary saved to file!!!!!!!')

###############################################################################################################################################################
def funcdatafile(filepath_to_funcdatafile,funcdatafile_all_data_dict,num_patchdata_zones,size_check=False):
    '''
    accepts functional data filepath and the dictionary of all data and saves it in WOPWOP-relevant binary format 
    
    Parameters
    ----------
    filepath_to_funcdatafile : str
        file path to the binary funcdatafile 

    funcdatafile_all_data_dict : dict
        dictionary containing all the funcdatafile data                    
    
    num_patchdata_zones : int
        number of zones for which data is provided in the patch file

    *considering 'zone specification data' to be 'signed-int' even though this is not explicitly stated in the manual
    writing time stepping from just one surface
    add function/equation to calculate bytes from the dictionary data as well (for secondary check that all the data was indeed written to binary file)
    '''
    
    data_type=['signed-int','signed-int','signed-int','ascii','int','int','int','int','int','int','int','int','int','int']
    size=[4,4,4,1024,4,4,4,4,4,4,4,4,4,4]

    with open(filepath_to_funcdatafile,'wb') as f_write:                              #open file to write in binary format
        pointer_loc=0                                                              #determines location of the cursor while writing the file (initial value 0 implies it starts writing from the begininng of the file)
        
        ####    writing 'data upto format string' data    ####
        for index,key in enumerate(funcdatafile_all_data_dict['data upto format string']):
            data_chunk=funcdatafile_all_data_dict['data upto format string'][key]
            pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,data_chunk,size[index],data_type[index])    #returns the new pointer location after writing the data to file
            
        ####    writing 'zone specification' data    ####
        data_chunk = funcdatafile_all_data_dict['zone specification']['number of zones with data']
        pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,data_chunk,4,'signed-int')    
    
        #Raise error if the number of zones in the file are not same as in geometry file (consistency check)
        if funcdatafile_all_data_dict['data upto format string']['number of zones']!=num_patchdata_zones:
            raise ValueError('Number of zone entries in Functional data not the same as in Patch data')
    
        for zone_no in funcdatafile_all_data_dict['zone specification']['zones with data']:
            pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,zone_no,4,'signed-int')
    
        ####    writing 'header info' data    ####        
        for index,loading_surface_name in enumerate(funcdatafile_all_data_dict['header info']['patch names']): 
            pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,loading_surface_name,32,'string')    
        
            if funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==1:                    
                dim1=funcdatafile_all_data_dict['header info']['grid size'][index][0]                    #1st dimension
                pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,dim1,4,'int')                        
                dim2=funcdatafile_all_data_dict['header info']['grid size'][index][1]                    #2nd dimension
                pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,dim2,4,'int')                        
        
            elif funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2: 
                time_period=funcdatafile_all_data_dict['header info']['time period']              #time period
                pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,time_period,4,'float')
                no_time_steps=funcdatafile_all_data_dict['header info']['number of time steps']                #time steps
                pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,no_time_steps,4,'int')
                dim1=funcdatafile_all_data_dict['header info']['grid size'][index][0]                    #1st dimension
                pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,dim1,4,'int')                        
                dim2=funcdatafile_all_data_dict['header info']['grid size'][index][1]                    #2nd dimension
                pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,dim2,4,'int')                        
                
            elif funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==3:
                pass
        
            elif funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==4:
                pass
        
    #Functionality for unstructured grid data has not yet been added since all examples files use structured data
    #Functionality for periodic geometry data has not yet been added since all examples files use constant data
    #Maybe adding periodic geometry data feature is just a matter of adding a time loop at the outermost location        
        
        
    #    keys=np.arange(0,funcdatafile_all_data_dict['header info']['number of time steps'][0],1,dtype='float')
    ##    for idx,key in enumerate(keys):
    #    for ts_k_idx,ts_k in enumerate(keys):
    #        for loading_surface_name in funcdatafile_all_data_dict['header info']['patch names']:
    #            pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,funcdatafile_all_data_dict['header info']['time steps'][loading_surface_name][ts_k_idx],4,'float')
    #            #pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,key,4,'float')
    #            for loading_surface_vector_name,loading_surface_vector_data in funcdatafile_all_data_dict['zones data'][loading_surface_name].items():
    #                for data_entry in loading_surface_vector_data[idx]:
    #                    pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,data_entry,4,'float')
    
        ####    writing 'zones data' data    ####
        if funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==1:
            for loading_patch_name in funcdatafile_all_data_dict['header info']['patch names']:
                for loading_patch_vector_name,loading_patch_vector_data in funcdatafile_all_data_dict['zones data'][loading_patch_name].items():
                    for data_entry in loading_patch_vector_data[0]:   #only one time step info is available 
                        pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,data_entry,4,'float')
            
        elif funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2:        
            for ts_k_idx,ts_k in enumerate(funcdatafile_all_data_dict['header info']['time steps or keys']):  #iterating through the number of time steps
                
                
                for loading_patch_name in funcdatafile_all_data_dict['header info']['patch names']:
                    pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,ts_k,4,'float')
                    for loading_patch_vector_name,loading_patch_vector_data in funcdatafile_all_data_dict['zones data'][loading_patch_name].items():
                        for data_entry in loading_patch_vector_data[ts_k_idx]:    #writing data corresponding to all loading surfaces one time step at a time
                            pointer_loc=chunk_convtobin_writetofile(f_write,pointer_loc,data_entry,4,'float')
            
     
    if size_check:
        print('pointer location till where Functional binary data file was written----------->',pointer_loc)
    #    size_arr=np.array(size)
    #    binaryfilesize=sum(size_arr)+40*len(patchfile_all_data_dict['header info']['patch names'])
    #    print('expected size of the binary patchfile based on patchfile_all_data_dict-->', )
        #secondary check
        print('file size (secondary check) -------------------------------------------------->',os.stat(filepath_to_funcdatafile).st_size)
    
    # print('Functional data converted to binary and saved to file!!!!!!!')


