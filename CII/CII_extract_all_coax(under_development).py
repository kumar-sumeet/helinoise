#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 12:29:12 2019

@author: ge56beh
"""
import numpy as np
import re
import math
import pandas as pd
import time
import sys

# from extract_get_hubloads import get_hubloads
# from extract_get_bladeloads import get_bladeloads
# from extract_get_positionSenData import get_positionSenData
# from extract_get_aeroSenData import get_aeroSenData

def extract_data_singleline(file,search_str,split_str,index,extract_type):
    while True:
        line = file.readline()
        if search_str in line:    
            if extract_type=='int':
                return int(line.split(split_str)[index])
            elif extract_type=='float':
                return float(line.split(split_str)[index])
            elif extract_type=='string':
                return str(line.split(split_str)[index])
        else:
            continue

def get_aeroSenData(f,rotor,nb,TIME_STEP,M_HARM,PANEL_MIDPOINT,OPPOST,AERODYNAMIC_SENSORS_QUANT,print_read_statements):    
    while True:     
        #####   Extracting blade angle of attack distribution over the azimuth    #####
        ALPHA=np.zeros((TIME_STEP[4]+1,len(PANEL_MIDPOINT)))
        AERO_SENSORS_QUANT_DEFINITION = []
        if OPPOST:    search_txt = ['RTREX '+rotor.split()[-1]+' WING '+str(nb)+' ANGLE OF ATTACK','RTREX'+rotor.split()[-1]+'WING'+str(nb)+'SENSOR']       #if post trim is carried out then extracting the corresponding aerodynamic data (note: both with and without post-trim data are printed out in CII output)
        else:    search_txt = [rotor+' WING '+str(nb)+' ANGLE OF ATTACK',rotor+'WING'+str(nb)+'SENSOR']
        while True:
            line = f.readline()
            if search_txt[0] in line:
                x=0
                while True:           
                    line = f.readline()
                    if 'TIME HISTORY' in line:
                        AoA=[]
                        for w in range(0,1+TIME_STEP[4]):
                            line = f.readline()
                            aoa=[]
                            if x<int(len(PANEL_MIDPOINT)/6):
                                aoa=line.split()[3:]
                            else:
                                aoa=line.split()[3:-1]                      
                            aoa=[float(i) for i in aoa]    
                            AoA.append(aoa)
                        if x<int(len(PANEL_MIDPOINT)/6):
                            ALPHA[:,x*6:x*6+len(aoa)]=np.asarray(AoA)
                            x=x+1
                            continue
                        else:
                            ALPHA[:,x*6:]=np.asarray(AoA)                    
                    else:
                        continue
                    break
            else:
                continue
            break        
        #ALPHA = np.delete(ALPHA, (np.size(ALPHA,0)-1), axis=0)
        #####   Extracting all other sensors data distribution over the azimuth    #####
        SENSORS_DATA=np.zeros((TIME_STEP[4]+1,len(PANEL_MIDPOINT),len(AERODYNAMIC_SENSORS_QUANT)))
        SENSORS_DATA_HARMONICS={'mean':np.zeros((1,len(PANEL_MIDPOINT),len(AERODYNAMIC_SENSORS_QUANT))),
                                'cosine':np.zeros((M_HARM[4],len(PANEL_MIDPOINT),len(AERODYNAMIC_SENSORS_QUANT))),
                                'sine':np.zeros((M_HARM[4],len(PANEL_MIDPOINT),len(AERODYNAMIC_SENSORS_QUANT))),
                                }
        SENSORS_DATA_DICT={}
        SENSORS_DATA_DICT_HARMONICS={'mean':{},'cosine':{},'sine':{}}
        SENSORS_DATA_DF_DICT={}
        z=0
        while True:
            line = f.readline()        
            if ''.join([search_txt[1],str(z+1)]) in line.replace(" ",""):
                x=0
        
                while True:
                    line = f.readline()
                    if 'QUANTITY DEFINITION:' in line:
                        AERO_SENSORS_QUANT_DEFINITION.append((line.split(':')[-1]).strip())               
                        break
        
                while True:
                    line = f.readline()
                    if 'TIME HISTORY' in line:
                        Sensors_data=[]    #getting the time-domain data 
                        for w in range(0,1+TIME_STEP[4]):
                            line = f.readline()
                            sensors_data=[]
                            if x<int(len(PANEL_MIDPOINT)/6):
                                sensors_data=line.split()[3:]
                            else:
                                sensors_data=line.split()[3:-1]
                            sensors_data=[float(i) for i in sensors_data]
                            Sensors_data.append(sensors_data)        
    
                        Sensors_data_harm={'mean':[],'cosine':[],'sine':[]}    #getting the harmonics data
                        line = f.readline()
                        line = f.readline()
                        sensors_data_harm_mean=[]
                        if x<int(len(PANEL_MIDPOINT)/6):
                            sensors_data_harm_mean=[float(i) for i in line.split()[1:]]
                        else:
                            sensors_data_harm_mean=[float(i) for i in line.split()[1:-1]]
                        Sensors_data_harm['mean'].append(sensors_data_harm_mean)     
                        for w in range(0,M_HARM[4]):
                            line = f.readline()
                            sensors_data_harm_cosine, sensors_data_harm_sine = [], []
                            if x<int(len(PANEL_MIDPOINT)/6):
                                sensors_data_harm_cosine=[float(i) for i in line.split()[2:]]
                                line = f.readline()
                                sensors_data_harm_sine=[float(i) for i in line.split()[2:]]
                            else:
                                sensors_data_harm_cosine=[float(i) for i in line.split()[2:-1]]
                                line = f.readline()
                                sensors_data_harm_sine=[float(i) for i in line.split()[2:-1]]                                        
                            Sensors_data_harm['cosine'].append(sensors_data_harm_cosine)
                            Sensors_data_harm['sine'].append(sensors_data_harm_sine)
                        if x<int(len(PANEL_MIDPOINT)/6):
                            SENSORS_DATA[:,x*6:x*6+len(sensors_data),z]=np.asarray(Sensors_data)
                            for hrm in SENSORS_DATA_HARMONICS:
                                SENSORS_DATA_HARMONICS[hrm][:,x*6:x*6+len(sensors_data),z]=np.asarray(Sensors_data_harm[hrm])
                            x=x+1
                            continue
                        else:
                            SENSORS_DATA[:,x*6:,z]=np.asarray(Sensors_data)      
                            for hrm in SENSORS_DATA_HARMONICS:
                                SENSORS_DATA_HARMONICS[hrm][:,x*6:,z]=np.asarray(Sensors_data_harm[hrm])
                    else:
                        continue
                    break
                SENSORS_DATA_DICT[AERO_SENSORS_QUANT_DEFINITION[z]]=SENSORS_DATA[:,:,z]
                for hrm in SENSORS_DATA_HARMONICS:                
                    SENSORS_DATA_DICT_HARMONICS[hrm][AERO_SENSORS_QUANT_DEFINITION[z]]=SENSORS_DATA_HARMONICS[hrm][:,:,z]
                SENSORS_DATA_DF_DICT[AERO_SENSORS_QUANT_DEFINITION[z]]=\
                                 pd.DataFrame(data=SENSORS_DATA[:,:,z],index=[360*ts/TIME_STEP[4] for ts in list(range(TIME_STEP[4]+1))],columns=PANEL_MIDPOINT)
                z=z+1
                if z<len(AERODYNAMIC_SENSORS_QUANT):
                    continue
            else:
                continue
            break
        if print_read_statements: print('read file till aero sensors')
        return ALPHA,SENSORS_DATA,SENSORS_DATA_DICT,SENSORS_DATA_HARMONICS,SENSORS_DATA_DF_DICT,SENSORS_DATA_DICT_HARMONICS,AERO_SENSORS_QUANT_DEFINITION
    
def get_positionSenData(f,rotor,nb,TIME_STEP,M_HARM,SENSOR_STATION_BCFDP,SENSOR_STATION_BP,print_read_statements):    
    while True: 
        line = f.readline()        
        # 2D matrix of pitch distribution: rows --> azimuth, column --> position sensor station        
        PITCH=np.zeros((TIME_STEP[3]+1,len(SENSOR_STATION_BP)))     
        SENSOR_DATA_CFD_POS=np.zeros((TIME_STEP[3]+1,6,len(SENSOR_STATION_BCFDP)))
        SENSOR_DATA_CFD_POS_HARMONICS={'mean':np.zeros((1,6,len(SENSOR_STATION_BCFDP))),
                                      'cosine':np.zeros((M_HARM[3],6,len(SENSOR_STATION_BCFDP))),
                                      'sine':np.zeros((M_HARM[3],6,len(SENSOR_STATION_BCFDP)))}
        MEAN_PITCH,PJOINT_HISTORY = [],[]
        TRIM_CONTROLS = {}
        bp_idx=0
        bcfdp_idx=0
        while True:
            line = f.readline()        
            if ''.join([rotor+' BLADE '+str(nb)+' POS ',SENSOR_STATION_BP[bp_idx]]) in line:  
                # print(rotor+' BLADE '+str(nb)+' POS ',SENSOR_STATION_BP[bp_idx])
                while True:
                    line = f.readline()
                    if 'TIME HISTORY' in line:
                        line = f.readline()
                        MEAN_PITCH.append(float(line.split()[3]))
                    else:
                        continue
                    break
                line = f.readline()
                line = f.readline()
                line = f.readline()
                line = f.readline()
                Pitch=[]
                for x in range(0,1+TIME_STEP[3]):
                    line = f.readline()
                    Pitch.append(float(line.split()[-2]))       
                PITCH[:,bp_idx]=np.asarray(Pitch)    
                if bp_idx<len(SENSOR_STATION_BP)-1 or bcfdp_idx<len(SENSOR_STATION_BCFDP)-1:
                    bp_idx=bp_idx+1
                    if bp_idx==len(SENSOR_STATION_BP):    bp_idx=bp_idx-1
                    continue
            elif rotor+' BLADE '+str(nb)+' POS  PJOINT' in line:   
                # print(rotor+' BLADE '+str(nb)+' POS  PJOINT')
                while True:
                    line = f.readline()
                    if 'TIME HISTORY' in line:
                        line = f.readline()
                        MEAN_PITCH.append(float(line.split()[-1]))
                    else:
                        continue
                    break
                line = f.readline()
                line = f.readline()
                line = f.readline()
                line = f.readline()
                Pitch=[]
                for x in range(0,1+TIME_STEP[3]):
                    line = f.readline()
                    Pitch.append(float(line.split()[-1]))
                    PJOINT_HISTORY.append(float(line.split()[-1]))
                PITCH[:,bp_idx]=np.asarray(Pitch)    
                if 'HARMONICS' in f.readline():                                    #This is executed once the 'TIME HISTORY (AZIMUTH IN DEG)' of the PJOINT has been iterated thru 
                    TRIM_CONTROLS['PJOINT']=[]
                    line=f.readline()
                    TRIM_CONTROLS['PJOINT'].append(float(line.split()[-1]))
                    line=f.readline()
                    TRIM_CONTROLS['PJOINT'].append(float(line.split()[-1]))
                    line=f.readline()
                    TRIM_CONTROLS['PJOINT'].append(float(line.split()[-1]))
                if bp_idx<len(SENSOR_STATION_BP)-1 or bcfdp_idx<len(SENSOR_STATION_BCFDP)-1:
                    bp_idx=bp_idx+1
                    continue
            elif ''.join([rotor+' BLADE '+str(nb)+' CFD ',SENSOR_STATION_BCFDP[bcfdp_idx]]) in line:  
                # print(f'{rotor} BLADE {nb} CFD {SENSOR_STATION_BCFDP[bcfdp_idx]}')
                while True:
                    line = f.readline()
                    if 'TIME HISTORY (AZIMUTH IN DEG)' in line:
                        pass
                    else:
                        continue
                    break
                Pos_rad_station=[]
                for x in range(0,1+TIME_STEP[3]):
                    line = f.readline()
                    inst_pos_rad_station=[]
                    for pos_quant in line.split()[3:]:
                        inst_pos_rad_station.append(float(pos_quant))
                    Pos_rad_station.append(inst_pos_rad_station)
                SENSOR_DATA_CFD_POS[:,:,bcfdp_idx]=np.asarray(Pos_rad_station)   
                
                line = f.readline()
                Pos_disp_euler_ang_harmonics={'mean':[],'cosine':[],'sine':[]}
    
                pos_disp_euler_ang_harmonics_mean=[]
                for y in range(0,M_HARM[3]):                
                    pos_disp_euler_ang_harmonics_cosine=[]
                    pos_disp_euler_ang_harmonics_sine=[]                
                    if pos_disp_euler_ang_harmonics_mean:    #since mean values appear only once
                        pass
                    else:
                        line=f.readline()
                        for t in line.split()[1:]:
                            try:
                                pos_disp_euler_ang_harmonics_mean.append(float(t))
                            except ValueError:
                                    pass     
                        Pos_disp_euler_ang_harmonics['mean'] = pos_disp_euler_ang_harmonics_mean
                    line=f.readline()    
                    for t in line.split()[2:]:
                        try:
                            pos_disp_euler_ang_harmonics_cosine.append(float(t))
                        except ValueError:
                                pass
                    line=f.readline()
                    for t in line.split()[2:]:
                        try:
                            pos_disp_euler_ang_harmonics_sine.append(float(t))
                        except ValueError:
                                pass
                    
                    Pos_disp_euler_ang_harmonics['cosine'].append(pos_disp_euler_ang_harmonics_cosine)
                    Pos_disp_euler_ang_harmonics['sine'].append(pos_disp_euler_ang_harmonics_sine)
                
                SENSOR_DATA_CFD_POS_HARMONICS['mean'][:,:,bcfdp_idx] = np.array(Pos_disp_euler_ang_harmonics['mean'])
                SENSOR_DATA_CFD_POS_HARMONICS['cosine'][:,:,bcfdp_idx] = np.array(Pos_disp_euler_ang_harmonics['cosine'])
                SENSOR_DATA_CFD_POS_HARMONICS['sine'][:,:,bcfdp_idx] = np.array(Pos_disp_euler_ang_harmonics['sine'])
                
                if bcfdp_idx<len(SENSOR_STATION_BCFDP)-1 or bp_idx<len(SENSOR_STATION_BP)-1:
                    bcfdp_idx=bcfdp_idx+1
                    continue
            else:
                continue
            break
        
        if print_read_statements: print('read file till position sensors')
        return PJOINT_HISTORY,PITCH,SENSOR_DATA_CFD_POS,SENSOR_DATA_CFD_POS_HARMONICS,TRIM_CONTROLS['PJOINT']

def get_bladeloads(f,rotor,nb,TIME_STEP,M_HARM,SENSOR_STATION_BL,print_read_statements):
    while True: 
        line = f.readline()        

        # 2D matrix of loads distribution: rows --> azimuth, column --> loads sensor station
        TORSION = np.zeros((TIME_STEP[2]+1,len(SENSOR_STATION_BL)))
        FLAP_BENDING = np.zeros((TIME_STEP[2]+1,len(SENSOR_STATION_BL)))
        LAG_BENDING = np.zeros((TIME_STEP[2]+1,len(SENSOR_STATION_BL)))
        AXIAL_FORCE = np.zeros((TIME_STEP[2]+1,len(SENSOR_STATION_BL)))
        CHORD_FORCE =  np.zeros((TIME_STEP[2]+1,len(SENSOR_STATION_BL)))
        NORM_FORCE = np.zeros((TIME_STEP[2]+1,len(SENSOR_STATION_BL)))
        BLADELOADS=np.zeros((TIME_STEP[2]+1,6,len(SENSOR_STATION_BL)))
        BLADELOADS_OSCILLATORY=np.zeros((TIME_STEP[2]+1,6,len(SENSOR_STATION_BL)))
        BLADELOADS_HARMONICS=np.zeros((M_HARM[2],6,len(SENSOR_STATION_BL)))
        MEAN_LOADS,HALF_PEAK_TO_PEAK = {},{}
            
        
        order_of_loads=['Torsion','Flap','Lag','Axial','Chord','Norm']
        for load_type in order_of_loads: 
            MEAN_LOADS[load_type]=[]
            HALF_PEAK_TO_PEAK[load_type]=[]
        z=0
        while SENSOR_STATION_BL:
            line = f.readline()        
            if ''.join([rotor+' BLADE '+str(nb)+' LOAD ',SENSOR_STATION_BL[z]]) in line:
                mean_loads=[]
                while True:
                    line = f.readline()
                    if 'MEAN' in line:
                        mean_loads=line.split()[1:]
                    else:
                        continue
                    break
                mean_loads=[float(i) for i in mean_loads]
                for load_type,mean_load in zip(order_of_loads,mean_loads): 
                    MEAN_LOADS[load_type].append(mean_load)
                line = f.readline()
                line = f.readline()
                line = f.readline()
                half_p_to_p_loads=line.split()[2:]        
                half_p_to_p_loads=[float(i) for i in half_p_to_p_loads]
                for load_type,hptop_load in zip(order_of_loads,half_p_to_p_loads): 
                    HALF_PEAK_TO_PEAK[load_type].append(hptop_load)
                line = f.readline()
                Bladeloads=[]
                Bladeloads_osc=[]
                for x in range(0,1+TIME_STEP[2]):
                    line = f.readline()
                    bladeloads=[]
                    bladeloads_osc=[]
                    for t in line.split()[3:]:
                        try:
                            bladeloads.append(float(t))
                        except ValueError:
                                pass
                    bladeloads_osc=[bladeloads[i]-mean_loads[i] for i in range(len(bladeloads))]
                    Bladeloads.append(bladeloads)
                    Bladeloads_osc.append(bladeloads_osc)            
                Bladeloads_arr=np.asarray(Bladeloads)
                Bladeloads_osc_arr=np.asarray(Bladeloads_osc)
                                              
                line=f.readline()
                line=f.readline()
                Bladeloads_harmonics=[]
                for y in range(0,M_HARM[2]):
                    line=f.readline()
                    bladeloads_harmonics_cosine=[]
                    bladeloads_harmonics_sine=[]
                    bladeloads_harmonics=[]
                    for t in line.split()[2:]:
                        try:
                            bladeloads_harmonics_cosine.append(float(t))
                        except ValueError:
                                pass
                    line=f.readline()
                    for t in line.split()[2:]:
                        try:
                            bladeloads_harmonics_sine.append(float(t))
                        except ValueError:
                                pass
                    bladeloads_harmonics=[math.sqrt(bladeloads_harmonics_cosine[m]*bladeloads_harmonics_cosine[m]+bladeloads_harmonics_sine[m]*bladeloads_harmonics_sine[m]) for m in range(0,len(bladeloads_harmonics_sine))]        
                    Bladeloads_harmonics.append(bladeloads_harmonics)        
                Bladeloads_harmonics_arr=np.asarray(Bladeloads_harmonics)
                    
                z=z+1
                BLADELOADS[:,:,z-1]=Bladeloads_arr
                BLADELOADS_OSCILLATORY[:,:,z-1]=Bladeloads_osc_arr
                TORSION[:,z-1]=Bladeloads_arr[:,0]
                FLAP_BENDING[:,z-1]=Bladeloads_arr[:,1]
                LAG_BENDING[:,z-1]=Bladeloads_arr[:,2]
                AXIAL_FORCE[:,z-1]=Bladeloads_arr[:,3]
                CHORD_FORCE[:,z-1]=Bladeloads_arr[:,4]
                NORM_FORCE[:,z-1]=Bladeloads_arr[:,5]
                
                BLADELOADS_HARMONICS[:,:,z-1]=Bladeloads_harmonics_arr
        
                if z<len(SENSOR_STATION_BL):
                    continue
            else:
                continue
            break
        if print_read_statements: print('read CII file till bladeloads sensors')
        
        return BLADELOADS,BLADELOADS_OSCILLATORY,BLADELOADS_HARMONICS,MEAN_LOADS,HALF_PEAK_TO_PEAK
               
def get_hubloads(f,rotor,nb,TIME_STEP,M_HARM,print_read_statements):    
    while True: 
        line = f.readline()
        if rotor+' NONROTATING HUB FORCE' in line:
            while True:
                line = f.readline()
                if 'TIME HISTORY (AZIMUTH IN DEG)' in line:   
                    #Saving azimuthal history of hub forces
                    up,aft,right=[],[],[]
                    for x in range(0,1+TIME_STEP[0]):
                        line = f.readline()     
                        aft.append(float(line.split()[3]))
                        right.append(float(line.split()[4]))
                        up.append(float(line.split()[5]))
                    line = f.readline()
                    line = f.readline()
                    #Saving harmonics of hub forces
                    up_harm,aft_harm,right_harm=[],[],[]
                    up_harm_cosine,aft_harm_cosine,right_harm_cosine=[],[],[]
                    up_harm_sine,aft_harm_sine,right_harm_sine=[],[],[]
                    for y in range(0,M_HARM[0]):
                        line=f.readline()
                        hubloads_harmonics_cosine=[]
                        hubloads_harmonics_sine=[]
                        hubloads_harmonics=[]
                        for t in line.split()[2:]:
                            try:
                                hubloads_harmonics_cosine.append(float(t))
                            except ValueError:
                                    pass
                        line=f.readline()
                        for t in line.split()[2:]:
                            try:
                                hubloads_harmonics_sine.append(float(t))
                            except ValueError:
                                    pass
                        hubloads_harmonics=[math.sqrt(hubloads_harmonics_cosine[m]*hubloads_harmonics_cosine[m]+hubloads_harmonics_sine[m]*hubloads_harmonics_sine[m]) for m in range(0,len(hubloads_harmonics_sine))]        
                        aft_harm.append(hubloads_harmonics[0])
                        aft_harm_cosine.append(hubloads_harmonics_cosine[0])
                        aft_harm_sine.append(hubloads_harmonics_sine[0])                        
                        right_harm.append(hubloads_harmonics[1])        
                        right_harm_cosine.append(hubloads_harmonics_cosine[1])
                        right_harm_sine.append(hubloads_harmonics_sine[1])
                        up_harm.append(hubloads_harmonics[2])
                        up_harm_cosine.append(hubloads_harmonics_cosine[2])
                        up_harm_sine.append(hubloads_harmonics_sine[2])
                    NONROT_HUB_FORCE={'UP':up,'RIGHT':right,'AFT':aft}
                    NONROT_HUB_FORCE_HARM={'UP':up_harm,'RIGHT':right_harm,'AFT':aft_harm}
                    NONROT_HUB_FORCE_HARM_COSINE={'UP':up_harm_cosine,'RIGHT':right_harm_cosine,'AFT':aft_harm_cosine}
                    NONROT_HUB_FORCE_HARM_SINE={'UP':up_harm_sine,'RIGHT':right_harm_sine,'AFT':aft_harm_sine}
                else:
                    continue
                break
        else:
            continue
        break
    
    while True:
        line = f.readline()        
        if rotor+' NONROTATING HUB MOMENT' in line:
            while True:
                line = f.readline()
                if 'TIME HISTORY (AZIMUTH IN DEG)' in line:    
                    roll,pitch,yaw=[],[],[]
                    for x in range(0,1+TIME_STEP[0]):
                        line = f.readline()
                        roll.append(float(line.split()[3]))
                        pitch.append(float(line.split()[4]))
                        yaw.append(float(line.split()[5]))
                    line = f.readline()
                    line = f.readline()
                    roll_harm,pitch_harm,yaw_harm=[],[],[]
                    roll_harm_cosine,pitch_harm_cosine,yaw_harm_cosine=[],[],[]
                    roll_harm_sine,pitch_harm_sine,yaw_harm_sine=[],[],[]
                    for y in range(0,M_HARM[0]):
                        line=f.readline()
                        hubmoments_harmonics_cosine=[]
                        hubmoments_harmonics_sine=[]
                        hubmoments_harmonics=[]
                        for t in line.split()[2:]:
                            try:
                                hubmoments_harmonics_cosine.append(float(t))
                            except ValueError:
                                    pass
                        line=f.readline()
                        for t in line.split()[2:]:
                            try:
                                hubmoments_harmonics_sine.append(float(t))
                            except ValueError:
                                    pass
                        hubmoments_harmonics=[math.sqrt(hubmoments_harmonics_cosine[m]*hubmoments_harmonics_cosine[m]+hubmoments_harmonics_sine[m]*hubmoments_harmonics_sine[m]) for m in range(0,len(hubmoments_harmonics_sine))]        
                        roll_harm.append(hubmoments_harmonics[0])
                        roll_harm_cosine.append(hubmoments_harmonics_cosine[0])
                        roll_harm_sine.append(hubmoments_harmonics_sine[0])
                        pitch_harm.append(hubmoments_harmonics[1])
                        pitch_harm_cosine.append(hubmoments_harmonics_cosine[1])
                        pitch_harm_sine.append(hubmoments_harmonics_sine[1])
                        yaw_harm.append(hubmoments_harmonics[2])  
                        yaw_harm_cosine.append(hubmoments_harmonics_cosine[2])
                        yaw_harm_sine.append(hubmoments_harmonics_sine[2])
                        
                    NONROT_HUB_MOM={'ROLL':roll, 'PITCH':pitch, 'YAW':yaw}
                    NONROT_HUB_MOM_HARM={'ROLL':roll_harm, 'PITCH':pitch_harm, 'YAW':yaw_harm}
                    NONROT_HUB_MOM_HARM_COSINE={'ROLL':roll_harm_cosine, 'PITCH':pitch_harm_cosine, 'YAW':yaw_harm_cosine}
                    NONROT_HUB_MOM_HARM_SINE={'ROLL':roll_harm_sine, 'PITCH':pitch_harm_sine, 'YAW':yaw_harm_sine}
                    
                    HUBLOADS = {'NONROT_HUB_FORCE':NONROT_HUB_FORCE,'NONROT_HUB_FORCE_HARM':NONROT_HUB_FORCE_HARM,'NONROT_HUB_FORCE_HARM_COSINE':NONROT_HUB_FORCE_HARM_COSINE,
                                     'NONROT_HUB_FORCE_HARM_SINE':NONROT_HUB_FORCE_HARM_SINE,'NONROT_HUB_MOM':NONROT_HUB_MOM,'NONROT_HUB_MOM_HARM':NONROT_HUB_MOM_HARM,
                                     'NONROT_HUB_MOM_HARM_COSINE':NONROT_HUB_MOM_HARM_COSINE,'NONROT_HUB_MOM_HARM_SINE':NONROT_HUB_MOM_HARM_SINE}
                else:
                    continue
                break                        
        else:
            continue
        break
    while True:
        line = f.readline()        
        if rotor+' BLADE '+str(nb)+' ROOT FORCE' in line:
            while True:
                line = f.readline()
                if 'TIME HISTORY (AZIMUTH IN DEG)' in line:   
                    #Saving azimuthal history of blade root forces
                    up,aft,right=[],[],[]
                    for x in range(0,1+TIME_STEP[0]):
                        line = f.readline()     
                        aft.append(float(line.split()[3]))
                        right.append(float(line.split()[4]))
                        up.append(float(line.split()[5]))
                    line = f.readline()
                    line = f.readline()
                    #Saving harmonics of hub forces
                    up_harm,aft_harm,right_harm=[],[],[]
                    up_harm_cosine,aft_harm_cosine,right_harm_cosine=[],[],[]
                    up_harm_sine,aft_harm_sine,right_harm_sine=[],[],[]
                    for y in range(0,M_HARM[0]):
                        line=f.readline()
                        blade_root_loads_harmonics_cosine=[]
                        blade_root_loads_harmonics_sine=[]
                        blade_root_loads_harmonics=[]
                        for t in line.split()[2:]:
                            try:
                                blade_root_loads_harmonics_cosine.append(float(t))
                            except ValueError:
                                    pass
                        line=f.readline()
                        for t in line.split()[2:]:
                            try:
                                blade_root_loads_harmonics_sine.append(float(t))
                            except ValueError:
                                    pass
                        blade_root_loads_harmonics=[math.sqrt(blade_root_loads_harmonics_cosine[m]*blade_root_loads_harmonics_cosine[m]+blade_root_loads_harmonics_sine[m]*blade_root_loads_harmonics_sine[m]) for m in range(0,len(blade_root_loads_harmonics_sine))]        
                        aft_harm.append(blade_root_loads_harmonics[0])
                        aft_harm_cosine.append(blade_root_loads_harmonics_cosine[0])
                        aft_harm_sine.append(blade_root_loads_harmonics_sine[0])                        
                        right_harm.append(blade_root_loads_harmonics[1])        
                        right_harm_cosine.append(blade_root_loads_harmonics_cosine[1])
                        right_harm_sine.append(blade_root_loads_harmonics_sine[1])
                        up_harm.append(blade_root_loads_harmonics[2])
                        up_harm_cosine.append(blade_root_loads_harmonics_cosine[2])
                        up_harm_sine.append(blade_root_loads_harmonics_sine[2])
                    ROT_BLADE_ROOT_FORCE={'UP':up,'RIGHT':right,'AFT':aft}
                    ROT_BLADE_ROOT_FORCE_HARM={'UP':up_harm,'RIGHT':right_harm,'AFT':aft_harm}
                    ROT_BLADE_ROOT_FORCE_HARM_COSINE={'UP':up_harm_cosine,'RIGHT':right_harm_cosine,'AFT':aft_harm_cosine}
                    ROT_BLADE_ROOT_FORCE_HARM_SINE={'UP':up_harm_sine,'RIGHT':right_harm_sine,'AFT':aft_harm_sine}
                else:
                    continue
                break
        else:
            continue
        break
        
    while True:
        line = f.readline()        
        if rotor+' BLADE '+str(nb)+' ROOT MOMENT' in line:
            while True:
                line = f.readline()
                if 'TIME HISTORY (AZIMUTH IN DEG)' in line:    
                    flapwise,twist,chordwise=[],[],[]
                    for x in range(0,1+TIME_STEP[0]):
                        line = f.readline()
                        flapwise.append(float(line.split()[3]))
                        twist.append(float(line.split()[4]))
                        chordwise.append(float(line.split()[5]))
                    line = f.readline()
                    line = f.readline()
                                        
                    flapwise_harm,twist_harm,chordwise_harm=[],[],[]
                    flapwise_harm_cosine,twist_harm_cosine,chordwise_harm_cosine=[],[],[]
                    flapwise_harm_sine,twist_harm_sine,chordwise_harm_sine=[],[],[]
                    for y in range(0,M_HARM[0]):
                        line=f.readline()
                        blade_root_moments_harmonics_cosine=[]
                        blade_root_moments_harmonics_sine=[]
                        blade_root_moments_harmonics=[]
                        for t in line.split()[2:]:
                            try:
                                blade_root_moments_harmonics_cosine.append(float(t))
                            except ValueError:
                                    pass
                        line=f.readline()
                        for t in line.split()[2:]:
                            try:
                                blade_root_moments_harmonics_sine.append(float(t))
                            except ValueError:
                                    pass
                        blade_root_moments_harmonics=[math.sqrt(blade_root_moments_harmonics_cosine[m]*blade_root_moments_harmonics_cosine[m]+blade_root_moments_harmonics_sine[m]*blade_root_moments_harmonics_sine[m]) for m in range(0,len(blade_root_moments_harmonics_sine))]        
                        flapwise_harm.append(blade_root_moments_harmonics[0])
                        flapwise_harm_cosine.append(blade_root_moments_harmonics_cosine[0])
                        flapwise_harm_sine.append(blade_root_moments_harmonics_sine[0])
                        twist_harm.append(blade_root_moments_harmonics[1])
                        twist_harm_cosine.append(blade_root_moments_harmonics_cosine[1])
                        twist_harm_sine.append(blade_root_moments_harmonics_sine[1])
                        chordwise_harm.append(blade_root_moments_harmonics[2])  
                        chordwise_harm_cosine.append(blade_root_moments_harmonics_cosine[2])
                        chordwise_harm_sine.append(blade_root_moments_harmonics_sine[2])
                        
                    ROT_BLADE_ROOT_MOM={'FLAPWISE':flapwise, 'TWIST':twist, 'CHORDWISE':chordwise}
                    ROT_BLADE_ROOT_MOM_HARM={'FLAPWISE':flapwise_harm, 'TWIST':twist_harm, 'CHORDWISE':chordwise_harm}
                    ROT_BLADE_ROOT_MOM_HARM_COSINE={'FLAPWISE':flapwise_harm_cosine, 'TWIST':twist_harm_cosine, 'CHORDWISE':chordwise_harm_cosine}
                    ROT_BLADE_ROOT_MOM_HARM_SINE={'FLAPWISE':flapwise_harm_sine, 'TWIST':twist_harm_sine, 'CHORDWISE':chordwise_harm_sine}
                    BLADE_ROOT_LOADS={'ROT_BLADE_ROOT_FORCE':ROT_BLADE_ROOT_FORCE,'ROT_BLADE_ROOT_FORCE_HARM':ROT_BLADE_ROOT_FORCE_HARM,'ROT_BLADE_ROOT_FORCE_HARM_COSINE':ROT_BLADE_ROOT_FORCE_HARM_COSINE,
                              'ROT_BLADE_ROOT_FORCE_HARM_SINE':ROT_BLADE_ROOT_FORCE_HARM_SINE,'ROT_BLADE_ROOT_MOM':ROT_BLADE_ROOT_MOM,'ROT_BLADE_ROOT_MOM_HARM':ROT_BLADE_ROOT_MOM_HARM,
                              'ROT_BLADE_ROOT_MOM_HARM_COSINE':ROT_BLADE_ROOT_MOM_HARM_COSINE,'ROT_BLADE_ROOT_MOM_HARM_SINE':ROT_BLADE_ROOT_MOM_HARM_SINE}
                else:
                    continue
                break                        
        else:
            continue
        break
    
                ###############################################################################
                ##############         Extracting control loads data          #################
                ###############################################################################
    CONTROL_LOADS={}
    while True:
        line = f.readline()        
        if rotor+' PITCH LINK '+str(nb)+' FORCE' in line:
            while True:
                line = f.readline()
                if 'TIME HISTORY' in line:
                    line = f.readline()
                    CONTROL_LOADS['MEAN']=float(line.split()[-1])
                    line = f.readline()
                    line = f.readline()
                    line = f.readline()
                    CONTROL_LOADS['PEAK-TO-PEAK']=float(line.split()[-1])
                else:
                    continue
                break
        else:
            continue
        break
    if print_read_statements: print('read CII file till control load sensors')    
    return HUBLOADS,BLADE_ROOT_LOADS,CONTROL_LOADS

def cii_extract_all_coax(filepath,print_read_statements = False,pointer_loc=0):
    
    file = open(filepath,'r')
    file_content = file.read()    
    NCASES_run = int( file_content.count(130*'*')/2) # reading NCASES this way because not all cases might have finished running
    file.close()

    #print_read_statements used for debugging
    with open(filepath, 'r') as f:
        f.seek(pointer_loc)
        NCASES=extract_data_singleline(f,'NCASES',None,-1,'int')
        
        rotors_list = []
        while True:
            line = f.readline()            
            check = re.search('ROTOR [0-9]', line) # temp fix for rotorcraft with max 9 rotors
            if check is not None:
                rotors_list.append(check.group())
            if 130*'*' in line:
                pass
            else:
                continue
            break
        
        rotors_list = list(set(rotors_list))
        rotors_list.sort()
        Nrotors = len(rotors_list)
        cii_all_data_dict = {}
        for case in range(1,NCASES_run+1,1):
                    ##################################################################################
                    #########       Getting some basic data based on input information       #########
                    ##################################################################################    
            
            RADIUS,NB={},{}
            for rotor in rotors_list:               
                RADIUS[rotor]=extract_data_singleline(f,'RADIUS (M)',None,3,'float')
                NB[rotor]=extract_data_singleline(f,'NUMBER OF BLADES',None,4,'int')
                
            # DELTA_PSI=extract_data_singleline(f,'AZIMUTH INCREMENT (DEG)','=',2,'float')
            
            OPPOST = bool(extract_data_singleline(f,'OPPOST','=',-1,'int'))        

            TIME_STEP,M_HARM={},{}
            for rotor in rotors_list:    
                TIME_STEP[rotor],M_HARM[rotor]=[],[]
                while True:
                    line = f.readline()
                    if 'HUB AND BLADE SENSORS' in line:
                        line = f.readline()
                        line = f.readline()
                        for x in range(0,6):
                            line = f.readline()
                            time_step=re.search('TIME =(.*) M', line)
                            TIME_STEP[rotor].append(int(time_step.group(1)))
                            no_harmonics=line.split()[-1]
                            M_HARM[rotor].append(int(no_harmonics))
                    else:
                        continue
                    break
    
            ASHAFT={}
            while True:
                line = f.readline()
                if 'ASHAFT' in line:
                        all_rotor_data=line.split('=')[-1]   
                        ashaft_list = all_rotor_data.split()
                        ashaft_list = [float(tilt) for tilt in ashaft_list]
                        ASHAFT = dict(zip(rotors_list,ashaft_list))
                else:
                    continue
                break
            
            #####   Extracting pitch bearing location    #####
            
            ROTATE,EPITCH,OPTEF,EHTEF,NRPOS = {},{},{},{},{}
            SENSOR_STATION_BP={}
            OPCFD,NRCFD,SENSOR_STATION_BCFDP={},{},{}
            SENSOR_STATION_BL={}
            for rotor in rotors_list:   
                ROTATE[rotor]=extract_data_singleline(f,'ROTATE',None,-1,'int')
                EPITCH[rotor]="{:.4f}".format(extract_data_singleline(f,'EPITCH',None,-1,'float'))
                OPTEF[rotor]=extract_data_singleline(f,'OPTEF =',None,-1,'int')
                SENSOR_STATION_BP[rotor]=[]
                SENSOR_STATION_BCFDP[rotor]=[]
                SENSOR_STATION_BL[rotor]=[]
                
                if OPTEF[rotor]:
                    print('OPTEF value is ', OPTEF[rotor])
                    pass                                        #currently the coax rotor doesn't have any active mechanism so thcode here is missing            
                    EHTEF[rotor]=None
                else:
                    EHTEF[rotor]=None
                #####   Extracting data corresponding to blade position sensors    #####   
                #Entries are stored as string and not float since exact matching of station with text in output file is required to extract further data 
                while True:
                    line = f.readline()
                    if 'NRPOS' in line:
                        NRPOS[rotor] = int(line.split()[-1])
                        if NRPOS[rotor]>1:
                            line = f.readline()
                            for t in line.split()[4:]:
                                try:
                                    SENSOR_STATION_BP[rotor].append("{:.4f}".format(float(t)))     #extract blade position sensor station upto 4 decimal places
                                except ValueError:
                                    pass
                            while len(SENSOR_STATION_BP[rotor])<NRPOS[rotor]:
                                line = f.readline()
                                for t in line.split():
                                    try:
                                        SENSOR_STATION_BP[rotor].append("{:.4f}".format(float(t)))     #extract blade position sensor station upto 4 decimal places
                                    except ValueError:
                                        pass                 
                    else:
                        continue
                    SENSOR_STATION_BP[rotor].append('1.0000')                  #position sensor data corresponding to EPITCH is output even if data there is not desired (i.e. the entry was not explicitly made to see the output there)
                    SENSOR_STATION_BP[rotor].append(str(EPITCH[rotor]))               #position sensor data corresponding to EPITCH is output even if data there is not desired
                    SENSOR_STATION_BP[rotor] = list(set(SENSOR_STATION_BP[rotor]))    #removing redundant entries that might arise
                    SENSOR_STATION_BP[rotor].sort()  
                    break
             
            #####   Extracting data corresponding to blade CFD position sensors    #####  
                OPCFD[rotor]=extract_data_singleline(f,'OPCFD',None,-1,'int')
                if OPCFD[rotor]:
                    while True:
                        line = f.readline()
                        NRCFD[rotor] = extract_data_singleline(f,'NRCFD',None,-1,'int')
                        if NRCFD[rotor]>1:
                            line = f.readline()
                            for t in line.split()[4:]:
                                try:
                                    SENSOR_STATION_BCFDP[rotor].append("{:.5f}".format(float(t)))     #extract blade position sensor station upto 5 decimal places
                                except ValueError:
                                    pass
                            while len(SENSOR_STATION_BCFDP[rotor])<NRCFD[rotor]:
                                line = f.readline()
                                for t in line.split():
                                    try:
                                        SENSOR_STATION_BCFDP[rotor].append("{:.5f}".format(float(t)))     #extract blade position sensor station upto 5 decimal places
                                    except ValueError:
                                        pass                 
                        else:
                            continue
                        break
                else:
                    NRCFD[rotor]=None                               
                #####   Extracting data corresponding to blade loads sensors    #####                   
                while True:
                    line = f.readline()
                    if 'BLADE LOADS SENSORS' in line:
                        line = f.readline()
                        no_of_sensors=int(line.split("=")[1])
                        line = f.readline()
                        line = f.readline()
                        for x in range(0,no_of_sensors):
                            line = f.readline()
                            last="{:.3f}".format(float(line.split()[-1]))
                            SENSOR_STATION_BL[rotor].append(last)            
                    else:
                        continue
                    break

            NPANEL,REDGE,PANEL_MIDPOINT={},{},{}
            AERODYNAMIC_SENSORS_QUANT={}
            for rotor in rotors_list:  
                REDGE[rotor] = []
                PANEL_MIDPOINT[rotor] = []
                AERODYNAMIC_SENSORS_QUANT[rotor] = []
            #####   Extracting data corresponding to aerodynamic panel locations    #####
                while True:
                    line = f.readline()
                    if 'NPANEL' in line:
                        NPANEL[rotor] = int(line.split()[-1]) 
                        next_line=f.readline()
                        next_line=f.readline()
                        for x in range(0,NPANEL[rotor]):
                            next_line=f.readline()
                            REDGE[rotor].append(float(next_line.split()[1]))
                            PANEL_MIDPOINT[rotor].append(float(next_line.split()[3]))
                    else:
                        continue
                    break           
                #####   Extracting data corresponding to aerodynamic sensors    #####
                while True:
                    line = f.readline()
                    if 'AERODYNAMIC SENSORS' in line:
                        line = f.readline()
                        no_of_sensors=int(line.split()[-1])
                        line = f.readline()
                        line = f.readline()
                        for x in range(0,no_of_sensors):
                            line = f.readline()           
                            AERODYNAMIC_SENSORS_QUANT[rotor].append(int(line.split()[3]))            
                    else:
                        continue
                    break
            
            if print_read_statements: print('read CII file till  trim analysis')
        ######################################################################################################################################################################
        ########################################################           Extracting information after trim analysis           ###############################################
        ###################################################################################################################################################################### 
        
        
                    ##########################################################################################################
                    ##############         Extracting oncoming flow velocities in different formats          #################
                    ##########################################################################################################
            SPEED={}
            TRIM_CONTROLS={}
            while True:
                line = f.readline()
                if 'VELOCITY (KNOTS)' in line:
                    SPEED['VELOCITY (KNOTS)']=float(line.split()[-1])
                    line = f.readline()
                    SPEED['V/(OMEGA*R)']=float(line.split()[-1])
                    line = f.readline()
                    SPEED['MACH NUMBER']=float(line.split()[-1])
                    line = f.readline()
                    SPEED['VELOCITY (M/SEC)']=float(line.split()[-1])
                    SPEED['OMEGA (RAD/SEC)']=float(line.split()[-1])
                    line = f.readline()            
                else:
                    continue
                break
        
                    ################################################################################
                    ##############         Extracting PILOT CONTROL input          #################
                    ################################################################################    
            while True:
                line = f.readline()
                if 'PILOT CONTROL (DEG)' in line:
                    TRIM_CONTROLS['PILOT_INPUT']=[]
                    line = f.readline()
                    TRIM_CONTROLS['PILOT_INPUT'].append(float(line.split()[2]))
                    line = f.readline()
                    TRIM_CONTROLS['PILOT_INPUT'].append(float(line.split()[3]))
                    line = f.readline()
                    TRIM_CONTROLS['PILOT_INPUT'].append(float(line.split()[3]))
                else:
                    continue
                break
            
            
            TRIM_CONTROLS_PRIMARY = {} 
            for rotor in rotors_list:
                TRIM_CONTROLS_PRIMARY[rotor]=[]
                while True:
                    line = f.readline()
                    if 'PRIMARY CONTROLS (DEG)' in line:                        
                        line = f.readline()
                        TRIM_CONTROLS_PRIMARY[rotor].append(float(line.split()[2]))
                        line = f.readline()
                        TRIM_CONTROLS_PRIMARY[rotor].append(float(line.split()[3]))
                        line = f.readline()
                        TRIM_CONTROLS_PRIMARY[rotor].append(float(line.split()[3]))
                    else:
                        continue
                    break                               
                    #############################################################################################
                    ##############         Extracting overall rotor forces and moments          #################
                    #############################################################################################

            ROTOR_FORCES_AND_MOMENTS_ALL,ROTOR_POWER_ALL,SIGMA,ROTOR_RPM = {},{},{},{}  
            for rotor in rotors_list:
                ROTOR_FORCES_AND_MOMENTS_ALL[rotor]=[]
                ROTOR_POWER_ALL[rotor]=[]
                while True:
                    line = f.readline()
                    if 'ROTOR FORCES AND MOMENTS' in line:
                        line = f.readline()
                        for x in range (0,20):
                            line = f.readline()
                            force_moment=[] 
                            i=0
                            for t in line.split():
                                if i<3:
                                    try:
                                        force_moment.append(float(t))                      #add only three columns of float values and ignore the rows with a fourth float entry (that way a rectangular matrix is possible) 
                                        i=i+1
                                    except ValueError:
                                        pass
                                else: break
                            if not force_moment:
                                pass
                            else:
                                ROTOR_FORCES_AND_MOMENTS_ALL[rotor].append(force_moment)                
                    else:
                        continue
                    break
                ROTOR_FORCES_AND_MOMENTS_ALL[rotor]=np.asarray(ROTOR_FORCES_AND_MOMENTS_ALL[rotor])
            
                    ##############         Extracting reference rotor RPM          #################
            
                while True:
                    line = f.readline()
                    if 'REFERENCE ROTATIONAL SPEED OMEGA' in line:
                        ROTOR_RPM[rotor] = float(re.search('REFERENCE ROTATIONAL SPEED OMEGA =(.*) RPM', line).group(1))
                    else:
                        continue
                    break
            
                        ################################################################################
                        ##############         Extracting overall rotor power          #################
                        ################################################################################    
                while True:
                    line = f.readline()
                    if 'ROTOR POWER' in line:
                        for x in range (0,16):
                            line = f.readline()
                            power=[] 
                            for t in line.split():
                                try:
                                    power.append(float(t))
                                except ValueError:
                                    pass
                            if not power:
                                pass
                            else:
                                ROTOR_POWER_ALL[rotor].append(power)                
                    else:
                        continue
                    break
                ROTOR_POWER=ROTOR_POWER_ALL[rotor][0][2]
                ROTOR_POWER_ALL[rotor]=np.asarray(ROTOR_POWER_ALL[rotor])
        
                #####    rotor solidity   #####
                while True:
                    line = f.readline()
                    if 'SOLIDITY RATIO SIGMA' in line:
                        SIGMA[rotor] = float(re.search('SOLIDITY RATIO SIGMA =(.*),',line).group(1))
                        break
                    else:
                        continue
        
        
                    ##############         Extracting hub loads sensor data          #################                    
            HUBLOADS={}
                    ##############         Extracting blade root loads sensor data          #################
            BLADE_ROOT_LOADS, CONTROL_LOADS ={},{}
                    ##############       Extracting blade loads sensor data          #################
            TORSION,FLAP_BENDING,LAG_BENDING,AXIAL_FORCE,CHORD_FORCE,NORM_FORCE = {},{},{},{},{},{}
            BLADELOADS,BLADELOADS_OSCILLATORY,BLADELOADS_HARMONICS = {},{},{}
            MEAN_LOADS,HALF_PEAK_TO_PEAK = {},{}
                    ##########           Extracting blade position sensors data            ###########
            PITCH,PJOINT_HISTORY, SENSOR_DATA_CFD_POS, SENSOR_DATA_CFD_POS_HARMONICS = {},{},{},{}
                    ###########           Extracting aerodynamic sensors data            #############
            ALPHA,SENSORS_DATA,SENSORS_DATA_HARMONICS = {},{},{}
            SENSORS_DATA_DICT,SENSORS_DATA_DICT_HARMONICS,SENSORS_DATA_DF_DICT = {},{},{}    
            AERO_SENSORS_QUANT_DEFINITION = {}
            
            for rotor in rotors_list:
                HUBLOADS[rotor],BLADE_ROOT_LOADS[rotor], CONTROL_LOADS[rotor] = get_hubloads(f,rotor,NB[rotor],TIME_STEP[rotor],M_HARM[rotor],print_read_statements)
                BLADELOADS[rotor],BLADELOADS_OSCILLATORY[rotor],BLADELOADS_HARMONICS[rotor],MEAN_LOADS[rotor],HALF_PEAK_TO_PEAK[rotor] = get_bladeloads(f,rotor,NB[rotor],TIME_STEP[rotor],                         
                                                                                                                                                        M_HARM[rotor],SENSOR_STATION_BL[rotor],
                                                                                                                                                        print_read_statements)
                PJOINT_HISTORY[rotor],PITCH[rotor],SENSOR_DATA_CFD_POS[rotor],SENSOR_DATA_CFD_POS_HARMONICS[rotor],trim_pjoint = get_positionSenData(f,rotor,NB[rotor],TIME_STEP[rotor],                         
                                                                                                      M_HARM[rotor],SENSOR_STATION_BCFDP[rotor],
                                                                                                      SENSOR_STATION_BP[rotor],print_read_statements)
                if OPPOST:
                    continue
                else:            
                    ALPHA[rotor],SENSORS_DATA[rotor],SENSORS_DATA_DICT[rotor],SENSORS_DATA_HARMONICS[rotor],SENSORS_DATA_DF_DICT[rotor], SENSORS_DATA_DICT_HARMONICS[rotor], AERO_SENSORS_QUANT_DEFINITION[rotor]  = get_aeroSenData(f,rotor,NB[rotor],TIME_STEP[rotor],M_HARM[rotor],
                                                                                                                                                                       PANEL_MIDPOINT[rotor],OPPOST,AERODYNAMIC_SENSORS_QUANT[rotor],
                                                                                                                                                                       print_read_statements)
            if OPPOST:
                for rotor in rotors_list:
                    ALPHA[rotor],SENSORS_DATA[rotor],SENSORS_DATA_DICT[rotor],SENSORS_DATA_HARMONICS[rotor],SENSORS_DATA_DF_DICT[rotor], SENSORS_DATA_DICT_HARMONICS[rotor], AERO_SENSORS_QUANT_DEFINITION[rotor]  = get_aeroSenData(f,rotor,NB[rotor],TIME_STEP[rotor],M_HARM[rotor],
                                                                                                                                                                       PANEL_MIDPOINT[rotor],OPPOST,AERODYNAMIC_SENSORS_QUANT[rotor],
                                                                                                                                                                       print_read_statements)
            TRIM_CONTROLS.update({'PJOINT':trim_pjoint})                
            POINTER_LOC=f.tell()
            
            # reach the end of case
            while True:
                line = f.readline()
                if 130*'*' in line:
                    pass
                else:
                    continue
                break
            
            rotor_data_dict = {'ROTOR(S)_DATA':{}}
            for rotor in rotors_list:                
                rotor_data_dict['ROTOR(S)_DATA'].update({rotor:{'filename':filepath.split('/')[-1],
                                                'RADIUS':RADIUS[rotor],'Nb':NB[rotor],'TIME_STEP':TIME_STEP[rotor],'ASHAFT':ASHAFT[rotor],'ROTATE':ROTATE[rotor],'EPITCH':EPITCH[rotor],
                                                'OPTEF':OPTEF[rotor],'EHTEF':EHTEF[rotor],
                                                'SENSOR_STATION_BCFDP':SENSOR_STATION_BCFDP[rotor],'SENSOR_STATION_BP':SENSOR_STATION_BP[rotor],'SENSOR_STATION_BL':SENSOR_STATION_BL[rotor],
                                                'NPANEL':NPANEL[rotor],'REDGE':REDGE[rotor],'PANEL_MIDPOINT':PANEL_MIDPOINT[rotor],
                                                'AERODYNAMIC_SENSORS_QUANT':AERODYNAMIC_SENSORS_QUANT[rotor],
                                                'TRIM_CONTROLS_PRIMARY':TRIM_CONTROLS_PRIMARY[rotor],
                                                'ROTOR_POWER_ALL':ROTOR_POWER_ALL[rotor],'ROTOR_FORCES_AND_MOMENTS_ALL':ROTOR_FORCES_AND_MOMENTS_ALL,
                                                'SIGMA':SIGMA[rotor],'ROTOR_RPM':ROTOR_RPM[rotor],
                                                'HUBLOADS':HUBLOADS[rotor],'BLADE_ROOT_LOADS':BLADE_ROOT_LOADS[rotor],'CONTROL_LOADS':CONTROL_LOADS[rotor],'MEAN_LOADS':MEAN_LOADS[rotor],
                                                'HALF_PEAK_TO_PEAK':HALF_PEAK_TO_PEAK[rotor],'BLADELOADS':BLADELOADS[rotor],
                                                'BLADELOADS_OSCILLATORY':BLADELOADS_OSCILLATORY[rotor],'BLADELOADS_HARMONICS':BLADELOADS_HARMONICS[rotor],'PITCH':PITCH[rotor],
                                                'PJOINT_HISTORY':PJOINT_HISTORY[rotor],'SENSOR_DATA_CFD_POS':SENSOR_DATA_CFD_POS[rotor],'SENSOR_DATA_CFD_POS_HARMONICS':SENSOR_DATA_CFD_POS_HARMONICS[rotor],
                                                'ALPHA':ALPHA[rotor],'AERO_SENSORS_QUANT_DEFINITION':AERO_SENSORS_QUANT_DEFINITION[rotor],
                                                'SENSORS_DATA':SENSORS_DATA[rotor],'SENSORS_DATA_DICT':SENSORS_DATA_DICT[rotor],'SENSORS_DATA_DF_DICT':SENSORS_DATA_DF_DICT[rotor],
                                                'SENSORS_DATA_HARMONICS':SENSORS_DATA_HARMONICS[rotor],'SENSORS_DATA_DICT_HARMONICS':SENSORS_DATA_DICT_HARMONICS[rotor],
                                                'POINTER_LOC':POINTER_LOC}})
            rotor_data_dict.update({'AIRCRAFT':{'SPEED':SPEED,'TRIM_CONTROLS':TRIM_CONTROLS}})
            if print_read_statements: print('read everything from file',filepath.split('/')[-1],' for case ', case)

            cii_all_data_dict.update({case:rotor_data_dict})

    return cii_all_data_dict


