#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:11:43 2020

@author: ge56beh
"""

import pickle
import numpy as np
import tecplot as tp
import concurrent.futures

case=1
rotors_list=['ROTOR 1','ROTOR 2']
#cii_filename = 'carmen_L3_900rpm_COLL8_windsweep_CMX_0_highres_rigidblade_DPOS5_DCFD5'
cii_filename='carmen_L3_900rpm_COLL8_windsweep_CMX_0_highres_rigidblade'
#cii_filename='carmen_L3_900rpm_COLL8_windsweep_CMX_0_highres'
def gen_plt(blade_no):    
    node_pos_arr_dict = pickle.load( open( f"../{cii_filename}_node_pos_arr_dict_case{case}_{rotor}_blade{blade_no}.p", "rb" ) )
    norm_pos_arr_dict = pickle.load( open( f"../{cii_filename}_norm_pos_arr_dict_case{case}_{rotor}_blade{blade_no}.p", "rb" ) )
    
    for key in node_pos_arr_dict:    
        no_timesteps = np.shape(node_pos_arr_dict[key])[-1]
        break
    T = 0.0667 # time period needs to be entered
    time_steps =  np.linspace(0,T,no_timesteps)    
    surf_list =list(node_pos_arr_dict.keys())
    with tp.session.suspend():
        
        tp.new_layout()
        frame = tp.active_frame()
        dataset = frame.dataset
        for coord in ['x','y','z','x_normal','y_normal','z_normal']:
            dataset.add_variable(coord)
        zones={}
            
        for t_idx, t in enumerate(time_steps):
                    
            print(t_idx)
            for surf,node_arr in node_pos_arr_dict.items():
                
                norm_arr = norm_pos_arr_dict[surf]
                
    
                
    #            if surf!='lifting-line':
    #                continue
                ord_zone_tup = (np.size(node_arr,axis=1),np.size(node_arr,axis=0),1)
                zones[surf+str(t)] = dataset.add_ordered_zone(surf+'_'+"{:5.4f}".format(t), 
                                                             ord_zone_tup, 
                                                             solution_time=t, 
    #                                                         strand_id=1+surf_list.index(surf))
                                                             strand_id=1)
                # visualize in Camrad frame
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
    #            frame.add_text('$\psi=$'+"{:3.0f}".format(360*t/T), position=(80, 80), size=10)
#        frame.add_latex(r'$\psi=$'+"{:3.0f}".format(360*t/T), position=(80, 80), size=10)
    
    #variables_to_save = [dataset.variable(var) for var in dataset.variable_names]
    #print(dataset.variable_names)
    #print(dataset.zone_names)
    #print(dataset.solution_times)
    #zone_to_save = [dataset.zone(z) for z in dataset.zone_names]
    tp.data.save_tecplot_plt(f'{cii_filename}_case{case}_{rotor}_blade{blade_no}.plt'.format(blade_no), 
                             dataset=dataset)                                      #saves all the data added above to the dataset                   
                            # variables=variables_to_save, 
                            # zones=zone_to_save)

for rotor in rotors_list:
    blade_no_lst = [1,2]
    executor = concurrent.futures.ProcessPoolExecutor()
    executor.map(gen_plt,blade_no_lst)

