#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 09:03:31 2019

@author: ge56beh
"""
"""
accepts patchfile data filepath to convert binary data to text format and returns a dictionary of all the converted data

"""
import numpy as np
import sys

###########################################################################################################################################
def patchfile(patchdata_input_dict,node_pos_arr_dict,norm_pos_arr_dict,time_steps_or_keys):                                          
    """


    Generates the patch data dict based on node and normals data obtained using
    SONATA 
    
    Parameters
    ----------
    patchdata_input_dict : dict
        contains all relevant input for patch file input for PSU WOPWOP
    node_pos_arr_dict : dict
        contains patch names as 'keys' and the position vectors of the nodes as 
        'values' 
    norm_pos_arr_dict : dict
        contains patch names as 'keys' and the normal vectors at the nodes as 
        'values' 
    time_steps_or_keys : str
        WOPWOP feature 

    Returns
    ----------
    patchfile_all_data_dict : dict
        dictionary with self-explanatory organization of all patch file data

    """        

    zones_data_dict={}
    node_pos_plot3d_dict, norm_pos_plot3d_dict = {},{}
    for patch_name in node_pos_arr_dict:    #patch_name are same in node_pos_arr_dict and norm_pos_arr_dict
        zones_data_dict[patch_name]={}    
        node_pos_plot3d_dict[patch_name]={'X':[],'Y':[],'Z':[]}
        norm_pos_plot3d_dict[patch_name]={'X':[],'Y':[],'Z':[]}
        for time_dim_idx in range(node_pos_arr_dict[patch_name].shape[-1]):
            node_pos_plot3d_dict[patch_name]['X'].append((-node_pos_arr_dict[patch_name][:,:,1,time_dim_idx]).flatten().tolist())
            node_pos_plot3d_dict[patch_name]['Y'].append(node_pos_arr_dict[patch_name][:,:,0,time_dim_idx].flatten().tolist())
            node_pos_plot3d_dict[patch_name]['Z'].append(node_pos_arr_dict[patch_name][:,:,2,time_dim_idx].flatten().tolist())
            
            norm_pos_plot3d_dict[patch_name]['X'].append((-norm_pos_arr_dict[patch_name][:,:,1,time_dim_idx]).flatten().tolist())
            norm_pos_plot3d_dict[patch_name]['Y'].append(norm_pos_arr_dict[patch_name][:,:,0,time_dim_idx].flatten().tolist())
            norm_pos_plot3d_dict[patch_name]['Z'].append(norm_pos_arr_dict[patch_name][:,:,2,time_dim_idx].flatten().tolist())

        for direction in ['X','Y','Z']:
            zones_data_dict[patch_name][patch_name+' '+direction+' node data']=node_pos_plot3d_dict[patch_name][direction]
        for direction in ['X','Y','Z']:
            zones_data_dict[patch_name][patch_name+' '+direction+' normal data']=norm_pos_plot3d_dict[patch_name][direction]            
        

    if len(patchdata_input_dict['units'])>32:         sys.exit("ERROR::::    WOPWOP file construction error \n              'units' in patch data more than 32 bytes")
    if len(patchdata_input_dict['comments'])>1024:    sys.exit("ERROR::::    WOPWOP file construction error \n              'comments' in patch data more than 1024 bytes")
        
    patchfile_all_data_dict={'data upto format string':{'magic number':42,
                                                      'version':1,
                                                      'number':0,
                                                      'units':patchdata_input_dict['units'], 
                                                      'comments':patchdata_input_dict['comments'],    #len of the str should not exceed 1024   
                                                      '1->geometry file/-1->node subset geometry file':1,
                                                      'number of zones':len(node_pos_arr_dict),
                                                      'structured/unstructured':patchdata_input_dict['grid'],    
                                                      'constant/periodic/aperiodic/mtf':patchdata_input_dict['periodicity'],    #whether the patch should be constant/periodic gets decided whether the size of 4th dimension of arr is greater than 1
                                                      'normal vectors node-centered/face-centered':patchdata_input_dict['normal_vecs'],
                                                      'single precision/double precision':1,
                                                      'iblank':0,
                                                      'future use':0},
                            'header info':{'patch names':[patch_name for patch_name in node_pos_arr_dict],
                                           'grid size': [[np.size(arr,1),np.size(arr,0)] for _,arr in node_pos_arr_dict.items()]},
                            'zones data':zones_data_dict
                            }
    #adding additional 'header info' data in case of periodic patch file
    if patchdata_input_dict['periodicity']==1:
        pass
    
    elif patchdata_input_dict['periodicity']==2:
        patchfile_all_data_dict['header info']['time period']=patchdata_input_dict['time period']
        patchfile_all_data_dict['header info']['number of time steps']=patchdata_input_dict['number of time steps']
        patchfile_all_data_dict['header info']['time steps or keys']=patchdata_input_dict[time_steps_or_keys]
    
    elif patchdata_input_dict['periodicity']==3:
        print("patchdata_input_dict['periodicity']==3   functionality is a work in progress")
            
    return patchfile_all_data_dict


###########################################################################################################################################
###########################################################################################################################################
def funcdatafile(funcdatafile_input_dict,loading_dict,time_steps_or_keys):                                          
    """
    
    
    Generates the patch data dict based on node and normals data obtained using
    the relevant SONATA packages
    Note: the data in node_pos_arr_dict,norm_pos_arr_dict is in SONATA 
    coordinates and needs to be converted to WOPWOP coordinates
    
    Parameters
    ----------
    funcdatafile_input_dict : dict
        Contains details necessary to create the functional data file 
    loading_dict : dict
        contains loading along each direction correspodning to each patch 
    time_steps_or_keys : str
        WOPWOP feature 

    Returns
    ----------
    funcdatafile_all_data_dict : dict
        dictionary with self-explanatory organization of all data within
        the functional file

    """
        
    zones_loading_data={}
    patch_namelst=[]
    patch_gridsize=[]
    for surface,loading_info in loading_dict.items():
        if loading_info:  
            zones_loading_data[surface]=loading_info 
            patch_namelst.append(surface)
            for key,loadinglst in loading_info.items():
                patch_gridsize.append([1,len(loadinglst[0])])
                break    #getting grid info from just one input (the rest are expected to be the same)
    
    zones_with_data=[1+list(loading_dict.keys()).index(zone) for zone in zones_loading_data]

#    #making some compatibitly checks    
#    if len(zones_loading_data)!=len(zones_with_data):
#        sys.exit()
#    for zone_no in zones_with_data:
#        sys.exit()

    if len(funcdatafile_input_dict['comments'])>1024:    sys.exit("ERROR::::    WOPWOP file construction error \n              'comments' in functional data more than 1024 bytes")  
    
    funcdatafile_all_data_dict={'data upto format string':{'magic number':42,
                                                           'version':1,
                                                           'number':0,
                                                           'comments':funcdatafile_input_dict['comments'],   #len of the str should not exceed 1024
                                                           'number to indicate this is a functional data file':2,
                                                           'number of zones':len(loading_dict),    
                                                           'structured/unstructured':funcdatafile_input_dict['grid'],
                                                           'constant/periodic/aperiodic/mtf':funcdatafile_input_dict['periodicity'],
                                                           'normal vectors node-centered/face-centered':funcdatafile_input_dict['normal_vecs'],
                                                           'surface pressure(GAUGE PRESSURE!!)/surface loading vector/flow parameters':funcdatafile_input_dict['aero_data'],
                                                           'stationary ground-fixed frame/rotating ground-fixed frame/patch-fixed frame':funcdatafile_input_dict['frame'],
                                                           'single precision/double precision':1,
                                                           'future use 1':0,
                                                           'future use 2':0},
                                'zone specification':{'number of zones with data':len(zones_loading_data),
                                                      'zones with data':zones_with_data},
                                'header info':{'patch names':patch_namelst,
                                               'grid size': patch_gridsize},   
                                'zones data':zones_loading_data
                                }

    if funcdatafile_input_dict['periodicity']==1:
        pass    #the above funcdatafile_all_data_dict suffices
    
    elif funcdatafile_input_dict['periodicity']==2:
        funcdatafile_all_data_dict['header info']['time period']=funcdatafile_input_dict['time period']
        funcdatafile_all_data_dict['header info']['number of time steps']=funcdatafile_input_dict['number of time steps']
        funcdatafile_all_data_dict['header info']['time steps or keys']=funcdatafile_input_dict[time_steps_or_keys]
        
    elif funcdatafile_input_dict['periodicity']==3:
        funcdatafile_all_data_dict['header info']['number of time steps']=funcdatafile_input_dict['number of time steps']
        #not tested
           
    return funcdatafile_all_data_dict


###########################################################################################################################################
###########################################################################################################################################
