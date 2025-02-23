#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 09:03:31 2019

@author: SumeetKumar

To do
--------

dict_to_bin_save_file does a similar thing as this file. Perhaps there is 
neat way to merge the two and perform slightly different tasks based on if the 
file needs to be saved as text or binary.
"""
###########################################################################################################################################
def add_helpful_header_in_text_file(write_to_file,header_string):
    '''
    Adds filler text to the text file to make the text data more (human) readable 
    
    Parameters
    ----------
    write_to_file : file object
        text file where data is being written to 

    header_string : str
        filler text to be written to file                    

    '''
    write_to_file.write('----------------------------------------------------------------------------------------------------------'+'\n')
    write_to_file.write('\t\t\t\t '+header_string)
    write_to_file.write('\n'+'----------------------------------------------------------------------------------------------------------'+'\n')    

###########################################################################################################################################
###########################################################################################################################################
def patchfile(filepath_to_patchfile,patchfile_all_data_dict):
    """
    Converts patch file dict to a text file 
    
    Parameters
    ----------
    filepath_to_patchfile : str
        file path to the binary patchfile 

    patchfile_all_data_dict : dict
        dictionary containing all the patchfile data                    

    
    """
    filepath_to_textfile=filepath_to_patchfile.split('.dat')[0]+'_text.txt'    #writing text file in same folder as patchfile
    
    with open(filepath_to_textfile,'w') as f_write:

        ####    writing 'data upto format string' data    ####
        add_helpful_header_in_text_file(f_write,'Information upto Format String')   
        for comment_text, value in patchfile_all_data_dict['data upto format string'].items():
            f_write.write(str(value)+'\t #'+comment_text+'\n')    
        
        ####    writing 'header info' and 'zones data' data    ####        
        if patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==1:
     
            add_helpful_header_in_text_file(f_write,'Header Information')
            for i in range(patchfile_all_data_dict['data upto format string']['number of zones']):    
                for comment_text, value in patchfile_all_data_dict['header info'].items():            
                    f_write.write(str(value[i])+'\t #'+comment_text+'\n')                         #Note: zone dimensions written including square brackets
            
            add_helpful_header_in_text_file(f_write,'Zones Data')
            for patch_name in patchfile_all_data_dict['header info']['patch names']:
                #f_write.write(patch_name+'\n\n')
                for patch_coord_name,patch_coord_data in patchfile_all_data_dict['zones data'][patch_name].items():
                    f_write.write(patch_coord_name+'\n')
                    for data_entry in patch_coord_data[0]:  #only one time step info is available
                        f_write.write(str(data_entry)+'\t')        
                    f_write.write('\n\n')
        
        elif patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2:
    
            add_helpful_header_in_text_file(f_write,'Header Information')
            for i in range(patchfile_all_data_dict['data upto format string']['number of zones']):    
                f_write.write(patchfile_all_data_dict['header info']['patch names'][i]+'\t #'+'patch names'+'\n')
                f_write.write(str(patchfile_all_data_dict['header info']['time period'])+'\t #'+'time period'+'\n')
                f_write.write(str(patchfile_all_data_dict['header info']['number of time steps'])+'\t #'+'number of time steps'+'\n')
                f_write.write(str(patchfile_all_data_dict['header info']['grid size'][i])+'\t #'+'grid size'+'\n')    #zone dimensions written including square brackets
            
            add_helpful_header_in_text_file(f_write,'Zones Data')            
            for ts_k_idx,ts_k in enumerate(patchfile_all_data_dict['header info']['time steps or keys']):  #iterating through the number of time steps
                for patch_name in patchfile_all_data_dict['header info']['patch names']: 
                    f_write.write('---------------------'+'\n')
                    f_write.write(str(ts_k)+'\n')
                    f_write.write('---------------------'+'\n')
                    #f_write.write(patch_name+'\n\n')
                    for patch_coord_name,patch_coord_data in patchfile_all_data_dict['zones data'][patch_name].items():
                        f_write.write(patch_coord_name+'\n')
                        for data_entry in patch_coord_data[ts_k_idx]:    #writing data corresponding to all patch surfaces one time step at a time
                            f_write.write(str(data_entry)+'\t')     
                        f_write.write('\n')
                    f_write.write('\n\n')
                    
        elif patchfile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==3:
    
            add_helpful_header_in_text_file(f_write,'Header Information')
            for i in range(patchfile_all_data_dict['data upto format string']['number of zones']):    
                f_write.write(patchfile_all_data_dict['header info']['patch names'][i]+'\t #'+'patch names'+'\n')
                f_write.write(str(patchfile_all_data_dict['header info']['number of time steps'])+'\t #'+'number of time steps'+'\n')
                f_write.write(str(patchfile_all_data_dict['header info']['grid size'][i])+'\t #'+'grid size'+'\n')    #zone dimensions written including square brackets
            
            add_helpful_header_in_text_file(f_write,'Zones Data')            
            for ts_k_idx,ts_k in enumerate(patchfile_all_data_dict['header info']['time steps or keys']):  #iterating through the number of time steps
                for patch_name in patchfile_all_data_dict['header info']['patch names']: 
                    f_write.write('---------------------'+'\n')
                    f_write.write(str(ts_k)+'\n')
                    f_write.write('---------------------'+'\n')
                    #f_write.write(patch_name+'\n\n')
                    for patch_coord_name,patch_coord_data in patchfile_all_data_dict['zones data'][patch_name].items():
                        f_write.write(patch_coord_name+'\n')
                        for data_entry in patch_coord_data[ts_k_idx]:    #writing data corresponding to all patch surfaces one time step at a time
                            f_write.write(str(data_entry)+'\t')     
                        f_write.write('\n')
                    f_write.write('\n\n')
    print('Patch data file dict has been saved as a text file')


###########################################################################################################################################
###########################################################################################################################################
def funcdatafile(filepath_to_funcdatafile,funcdatafile_all_data_dict):
    """
    Converts functional data file dict to a text file 
    
    Parameters
    ----------
    filepath_to_funcdatafile : str
        file path to the binary functional data file 

    funcdatafile_all_data_dict : dict
        dictionary containing all the funcdatafile data                    

    """
    filepath_to_textfile=filepath_to_funcdatafile.split('.dat')[0]+'_text.txt'    #writing text file in same folder as fundatafile

    print('esdklfjasdf')
    with open(filepath_to_textfile,'w') as f_write:

        ####    writing 'data upto format string' data    ####
        add_helpful_header_in_text_file(f_write,'Information upto Format String')
        for comment_text, value in funcdatafile_all_data_dict['data upto format string'].items():
            f_write.write(str(value)+'\t #'+comment_text+'\n')    
    
        ####    writing 'zone specification' data    ####
        add_helpful_header_in_text_file(f_write,'Zone Specification')
        for comment_text, value in funcdatafile_all_data_dict['zone specification'].items():
            f_write.write(str(value)+'\t #'+comment_text+'\n')    
    
        ####    writing 'header info' and 'zones data' data    ####
        if funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==1:
            
            add_helpful_header_in_text_file(f_write,'Header Information')
            for i in range(funcdatafile_all_data_dict['zone specification']['number of zones with data']):    
                for comment_text, value in funcdatafile_all_data_dict['header info'].items():            
                    f_write.write(str(value[i])+'\t #'+comment_text+'\n')                         #zone dimensions written including square brackets
            
            add_helpful_header_in_text_file(f_write,'Zones Data')
            for loading_patch_name in funcdatafile_all_data_dict['header info']['patch names']:
                for loading_surface_vector_name,loading_surface_vector_data in funcdatafile_all_data_dict['zones data'][loading_patch_name].items():
                    f_write.write(loading_surface_vector_name+'\n')    #writing the patch name and the quantity being written down below
                    for data_entry in loading_surface_vector_data[0]:   #only one time step info is available 
                        f_write.write(str(data_entry[0])+'\n')    #writing the data in plot3d format for a particular zone at the 0th time step
                    f_write.write('\n\n')
                                
        elif funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==2: 
    
            add_helpful_header_in_text_file(f_write,'Header Information')
            for i in range(funcdatafile_all_data_dict['zone specification']['number of zones with data']):    
                f_write.write(funcdatafile_all_data_dict['header info']['patch names'][i]+'\t #'+'patch names'+'\n')
                f_write.write(str(funcdatafile_all_data_dict['header info']['time period'])+'\t #'+'time period'+'\n')
                f_write.write(str(funcdatafile_all_data_dict['header info']['number of time steps'])+'\t #'+'number of time steps'+'\n')
                f_write.write(str(funcdatafile_all_data_dict['header info']['grid size'][i])+'\t #'+'grid size'+'\n')    #zone dimensions written including square brackets
            
            add_helpful_header_in_text_file(f_write,'Zones Data')            
            for ts_k_idx,ts_k in enumerate(funcdatafile_all_data_dict['header info']['time steps or keys']):  #iterating through the number of time steps
                for loading_patch_name in funcdatafile_all_data_dict['header info']['patch names']:                
                    f_write.write('---------------------'+'\n')
                    f_write.write(str(ts_k)+'\n')
                    f_write.write('---------------------'+'\n')
                    for loading_surface_vector_name,loading_surface_vector_data in funcdatafile_all_data_dict['zones data'][loading_patch_name].items():
                        f_write.write(loading_surface_vector_name+'\n')    #writing the patch name and the quantity being written down below
                        for data_entry in loading_surface_vector_data[ts_k_idx]:    #writing data corresponding to all loading surfaces one time step at a time
                            f_write.write(str(data_entry)+'\t')    #writing the data in plot3d format for a particular zone at the above time step
                        f_write.write('\n')
                    f_write.write('\n\n')
    
        elif funcdatafile_all_data_dict['data upto format string']['constant/periodic/aperiodic/mtf']==3:
            
            add_helpful_header_in_text_file(f_write,'Header Information')
            for i in range(funcdatafile_all_data_dict['zone specification']['number of zones with data']):    
                f_write.write(funcdatafile_all_data_dict['header info']['patch names'][i]+'\t #'+'patch names'+'\n')
                f_write.write(str(funcdatafile_all_data_dict['header info']['number of time steps'])+'\t #'+'number of time steps'+'\n')
                f_write.write(str(funcdatafile_all_data_dict['header info']['grid size'][i])+'\t #'+'grid size'+'\n')    #zone dimensions written including square brackets
            
            add_helpful_header_in_text_file(f_write,'Zones Data')            
            for ts_k_idx,ts_k in enumerate(funcdatafile_all_data_dict['header info']['time steps or keys']):  #iterating through the number of time steps
                for loading_patch_name in funcdatafile_all_data_dict['header info']['patch names']:                
                    f_write.write('---------------------'+'\n')
                    f_write.write(str(ts_k)+'\n')
                    f_write.write('---------------------'+'\n')
                    for loading_surface_vector_name,loading_surface_vector_data in funcdatafile_all_data_dict['zones data'][loading_patch_name].items():
                        f_write.write(loading_surface_vector_name+'\n')    #writing the patch name and the quantity being written down below
                        for data_entry in loading_surface_vector_data[ts_k_idx]:    #writing data corresponding to all loading surfaces one time step at a time
                            f_write.write(str(data_entry)+'\t')    #writing the data in plot3d format for a particular zone at the above time step
                        f_write.write('\n')
                    f_write.write('\n\n')
    
    print('Functional data file dict has been saved as text file')


###########################################################################################################################################
###########################################################################################################################################
if __name__ == "__main__":     
    
    num_patchdata_zones = 5
    func_filename = '1994_Run15_5_hover_FishBAC_PetersUnsteady_BladePrecone(rotating)_funcdataBlade1_aperiodic.dat'
    patch_filename = '1994_Run15_5_hover_FishBAC_PetersUnsteady_BladePrecone(rotating)_patchdataBlade1_aperiodic.dat'
    # directry = '/home/HT/ge56beh/Work/Python/HeliNoise/Data/Diss_runs/2_simple_hemisphere_aperiodic/1994_Run15_5_hover_FishBAC_PetersUnsteady/1994_Run15_5_hover_FishBAC_PetersUnsteady/blade_data'
    directry = '/home/HT/ge56beh/Work/Python/HeliNoise/Data/Diss_runs/1_simple_aperiodic/1994_Run15_5_hover_FishBAC_PetersUnsteady/1994_Run15_5_hover_FishBAC_PetersUnsteady/blade_data'

    import bin_to_dict as bin_to_dict
    patchfile_all_data_dict = bin_to_dict.patchfile(f'{directry}/{patch_filename}')
    funcfile_all_data_dict = bin_to_dict.funcdatafile(f'{directry}/{func_filename}',num_patchdata_zones)
    # patchfile(f'{directry}/{patch_filename}',patchfile_all_data_dict)
    funcdatafile(f'{directry}/{func_filename}',funcfile_all_data_dict)