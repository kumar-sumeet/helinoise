#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:11:43 2020

@author: SumeetKumar
"""

import pickle
import numpy as np
import tecplot as tp
from multiprocessing import Pool
from itertools import repeat
import os
from functools import partial

def get_plt(T,blade_no):
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
    
    print(f'*.p  to *.plt :: Blade {blade_no}...')
    
    node_pos_arr_dict = pickle.load( open( os.path.dirname(os.path.dirname(__file__))+"/node_pos_arr_dict_{0}.p".format(blade_no), "rb" ) )
    norm_pos_arr_dict = pickle.load( open( os.path.dirname(os.path.dirname(__file__))+"/norm_pos_arr_dict_{0}.p".format(blade_no), "rb" ) )
    
    for key in node_pos_arr_dict:    
        no_timesteps = np.shape(node_pos_arr_dict[key])[-1]
        break
    
    time_steps =  np.linspace(0,T,no_timesteps) 
    
    with tp.session.suspend():
        
        tp.new_layout()
        frame = tp.active_frame()
        dataset = frame.dataset
        for var in ['x','y','z','x_normal','y_normal','z_normal']:
            dataset.add_variable(var)
        zones={}
            
        for t_idx, t in enumerate(time_steps):
                    
#            print('time step-->',t_idx,f' of {no_timesteps}' )
            for surf,node_arr in node_pos_arr_dict.items():
                
                norm_arr = norm_pos_arr_dict[surf]
#                if surf!='lifting-line':    #just get the lifting-line
#                    continue
                ord_zone_tup = (np.size(node_arr,axis=1),np.size(node_arr,axis=0),1)
                zones[surf+str(t)] = dataset.add_ordered_zone(surf+'_'+"{:5.4f}".format(t), 
                                                             ord_zone_tup, 
                                                             solution_time=t, 
                                                             strand_id=1)
#                 visualize in Camrad frame
                x_val = -node_arr[:,:,1,t_idx]
                y_val = node_arr[:,:,0,t_idx]
                z_val = node_arr[:,:,2,t_idx]
                x_val_normal = -norm_arr[:,:,1,t_idx]
                y_val_normal = norm_arr[:,:,0,t_idx]
                z_val_normal = norm_arr[:,:,2,t_idx]
    
                zones[surf+str(t)].values('x')[:]=x_val.ravel()
                zones[surf+str(t)].values('y')[:]=y_val.ravel()
                zones[surf+str(t)].values('z')[:]=z_val.ravel()
                zones[surf+str(t)].values('x_normal')[:]=x_val_normal.ravel()
                zones[surf+str(t)].values('y_normal')[:]=y_val_normal.ravel()
                zones[surf+str(t)].values('z_normal')[:]=z_val_normal.ravel()
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
    tp.data.save_tecplot_plt(os.path.dirname(os.path.dirname(__file__))+'/Blade_{0}.plt'.format(blade_no), 
                             dataset=dataset)                                      #saves all the data added above to the dataset                   
    print(f'... {blade_no} finished')
    
if __name__ == "__main__":     
    
    T=0.14117 #Bo 105
    Nb=4
    
    partial_get_plt = partial(get_plt,T)                  
    # generate *.plt files     
    with Pool(4) as p:
        p.map(partial_get_plt,np.arange(1,Nb+1,1))
    
    
    
