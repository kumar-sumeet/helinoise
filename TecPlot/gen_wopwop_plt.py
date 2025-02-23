#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:11:43 2020

@author: SumeetKumar
"""

import pickle
import numpy as np
import tecplot as tp
from concurrent.futures import ProcessPoolExecutor as Pool
from itertools import repeat
import os
from functools import partial

def sonataToCIIframe(arr,t_idx):
    """
    the deformed blade coordinates have been generated in SONATA frame i.e.
    x along blade span and y towards LE. This function transforms that to CII 
    blade frame where y axis is along span and x is towards TE

    """
    # Camrad blade frame
    x = -arr[:,:,1,t_idx]
    y = arr[:,:,0,t_idx]
    z = arr[:,:,2,t_idx]
    
    return x, y, z
    
def sonataToDymframe(arr,t_idx):
    # Dymore blade frame
    x = arr[:,:,0,t_idx]
    y = arr[:,:,1,t_idx]
    z = arr[:,:,2,t_idx]
    
    return x, y, z
 
    
def get_plt(pltdatadict):
    """
    post blade discretization converts blade nodes and normals, obtained using 
    SONATA, to *plt format for easy verification by viewing the blade 
    deformation in TecPlot over one time period         

    Parameters
    -------
    blade_no : int
        reference blade number based on CAMRAD II, blade_no=4 referes to blade 
        at 0 azimuth angle at t=0
    T : float
        time period of rotor revolution
        
    Returns
    -------
    None

    ToDo
    -------
    -display azimuth in *.plt file 
    """            
    
    
    solver = pltdatadict['solver']
    disp_or_pos = pltdatadict['disp_or_pos']
    directry = pltdatadict['directry']
    filename = pltdatadict['filename']
    T = pltdatadict['T']
    blade_no = pltdatadict['blade_no']
    dataframename = pltdatadict['dataframename']
    delta_t = pltdatadict['delta_t']
    node_pos_arr_dict = pltdatadict['node_pos_arr_dict']
    norm_pos_arr_dict = pltdatadict['norm_pos_arr_dict']
    loading_dict = pltdatadict['loading_dict']

    for key in node_pos_arr_dict:    
        no_timesteps = np.shape(node_pos_arr_dict[key])[-1]
        break
    
    if disp_or_pos=='disp':
        time_steps_motion =  np.linspace(0,T,no_timesteps)  #fix this later same as for 'pos'
    elif disp_or_pos == 'pos':
        time_steps_motion = pltdatadict['time_steps_motion']
        
    with tp.session.suspend():
        
        tp.new_layout()
        frametp = tp.active_frame()
        dataset = frametp.dataset
        for var in ['x','y','z','x_normal','y_normal','z_normal','Fx','Fy','Fz']:
            dataset.add_variable(var)
        zones={}
            
        for t_idx, t in enumerate(time_steps_motion):
            print('time step-->',t_idx,f' of {no_timesteps}' )
            for surf,node_arr in node_pos_arr_dict.items():
                
                norm_arr = norm_pos_arr_dict[surf]
                # if surf!='lifting-line':    #just get the lifting-line
                #     continue
                ord_zone_tup = (np.size(node_arr,axis=1),np.size(node_arr,axis=0),1)
                zones[surf+str(t)] = dataset.add_ordered_zone(surf+'_'+"{:5.4f}".format(t), 
                                                             ord_zone_tup, 
                                                             solution_time=t, 
                                                             strand_id=1)

                if solver == 'CII':
                    x_val, y_val, z_val = sonataToCIIframe(node_arr,t_idx)
                    x_val_normal, y_val_normal, z_val_normal = sonataToCIIframe(norm_arr,t_idx)
                
                elif solver == 'Dymore':
                    x_val, y_val, z_val = sonataToDymframe(node_arr,t_idx)
                    x_val_normal, y_val_normal, z_val_normal = sonataToDymframe(norm_arr,t_idx)
    
                zones[surf+str(t)].values('x')[:]=x_val.ravel()
                zones[surf+str(t)].values('y')[:]=y_val.ravel()
                zones[surf+str(t)].values('z')[:]=z_val.ravel()
                zones[surf+str(t)].values('x_normal')[:]=x_val_normal.ravel()
                zones[surf+str(t)].values('y_normal')[:]=y_val_normal.ravel()
                zones[surf+str(t)].values('z_normal')[:]=z_val_normal.ravel()
                
                if surf in ['inboard tip','outboard tip']:
                    continue
                
                for ax in ['X','Y','Z']:
                    f_ax = loading_dict['lifting-line'][f'lifting-line {ax} loading vector'][t_idx,:] #(no of radial discretizations,)
                    f_ax = np.repeat(f_ax,x_val.shape[1]) #(no of radial discretizations,chordwise discretizations)
                    zones[surf+str(t)].values(f'F{ax}')[:]=f_ax.ravel()                
                
#                azimuth=(90*blade_no)+(360*t/T)
#                macr_str=f"""$!AttachText 
#                  AnchorPos
#                    {{
#                    X = 53.08578008059873
#                    Y = 66.21761658031089
#                    }}
#                  TextShape
#                    {{
#                    IsBold = No
#                    }}
#                  Text = 'Azimuth={azimuth:.1f} deg'"""
#                tp.macro.execute_command(macr_str)
            
    tp.data.save_tecplot_plt(f"{directry}/{filename}_{dataframename}_Blade_{blade_no}_surfaceload.plt", 
                             dataset=dataset)                                      #saves all the data added above to the dataset                   

    with tp.session.suspend():
        
        tp.new_layout()
        frametp = tp.active_frame()
        dataset = frametp.dataset
        for var in ['x','y','z','x_normal','y_normal','z_normal','Fx','Fy','Fz']:
            dataset.add_variable(var)
        zones={}
            
        for t_idx, t in enumerate(time_steps_motion):
            print('time step-->',t_idx,f' of {no_timesteps}' )
            for surf,node_arr in node_pos_arr_dict.items():
                
                norm_arr = norm_pos_arr_dict[surf]
                # if surf!='lifting-line':    #just get the lifting-line
                #     continue
                ord_zone_tup = (np.size(node_arr,axis=1),np.size(node_arr,axis=0),1)
                zones[surf+str(t)] = dataset.add_ordered_zone(surf+'_'+"{:5.4f}".format(t), 
                                                             ord_zone_tup, 
                                                             solution_time=t, 
                                                             strand_id=1)

                if solver == 'CII':
                    x_val, y_val, z_val = sonataToCIIframe(node_arr,t_idx)
                    x_val_normal, y_val_normal, z_val_normal = sonataToCIIframe(norm_arr,t_idx)
                
                elif solver == 'Dymore':
                    x_val, y_val, z_val = sonataToDymframe(node_arr,t_idx)
                    x_val_normal, y_val_normal, z_val_normal = sonataToDymframe(norm_arr,t_idx)
    
                zones[surf+str(t)].values('x')[:]=x_val.ravel()
                zones[surf+str(t)].values('y')[:]=y_val.ravel()
                zones[surf+str(t)].values('z')[:]=z_val.ravel()
                zones[surf+str(t)].values('x_normal')[:]=x_val_normal.ravel()
                zones[surf+str(t)].values('y_normal')[:]=y_val_normal.ravel()
                zones[surf+str(t)].values('z_normal')[:]=z_val_normal.ravel()
                
                if surf in ['inboard tip','outboard tip']:
                    continue
                
                if surf!='lifting-line':    #just get the lifting-line
                    continue
                for ax in ['X','Y','Z']:
                    f_ax = loading_dict['lifting-line'][f'lifting-line {ax} loading vector'][t_idx,:] #(no of radial discretizations,)
                    f_ax = np.repeat(f_ax,x_val.shape[1]) #(no of radial discretizations,chordwise discretizations)
                    zones[surf+str(t)].values(f'F{ax}')[:]=f_ax.ravel()                
                
#                azimuth=(90*blade_no)+(360*t/T)
#                macr_str=f"""$!AttachText 
#                  AnchorPos
#                    {{
#                    X = 53.08578008059873
#                    Y = 66.21761658031089
#                    }}
#                  TextShape
#                    {{
#                    IsBold = No
#                    }}
#                  Text = 'Azimuth={azimuth:.1f} deg'"""
#                tp.macro.execute_command(macr_str)
            
    tp.data.save_tecplot_plt(f"{directry}/{filename}_{dataframename}_Blade_{blade_no}_LLvectorload.plt", 
                             dataset=dataset)                                      #saves all the data added above to the dataset                   

    print(f"... {blade_no} finished")
     
if __name__ == "__main__":     
    
    # T=0.14117 #Bo 105
    # Nb=4
    # filename = '1994_Run42_7_FishBAC_PetersUnsteady'
    # partial_get_plt = partial(get_plt,filename,T)                  
    # # generate *.plt files     
    # with Pool(4) as p:
    #     p.map(partial_get_plt,np.arange(1,Nb+1,1))
    
    # directry = '../Data/Diss_runs/1_simple_periodic/wing_rectangular_static/wing_rectangular_static/'
    # directry = '../Data/Diss_runs/1_simple_periodic/wing_rectangular_pitching/wing_rectangular_pitching/'
    # directry = '../Data/Diss_runs/1_simple_periodic/wing_elliptical_pitching/wing_elliptical_pitching/'
    directry = '../Data/Diss_runs/2_simple_sphere_periodic/H1/H1/'
    filename = 'pltdatadict.p'
    pltdatadict = pickle.load( open( f'{directry}/{filename}', "rb" ) )
    get_plt(pltdatadict)
