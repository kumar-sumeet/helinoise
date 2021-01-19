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

def cii_extract_all(filename,pointer_loc=0):
    print_read_statements = False     #used for debugging
    with open(filename, 'r') as f:
        f.seek(pointer_loc)
        REDGE = []
        PANEL_MIDPOINT = []
        SENSOR_STATION_BL=[]                                                       #radial stations where blade loads output is obtained
        SENSOR_STATION_BP=[]                                                       #radial stations where blade poistion output is obtained
        SENSOR_STATION_BCFDP=[]                                                    #radial stations where blade CFD poistion output is obtained
        TIME_STEP=[]
        M_HARM=[]
        OPTEF=0
        EHTEF=[0,0]    
        MEAN_LOADS={}
        HALF_PEAK_TO_PEAK={}
        PJOINT_HISTORY=[]
        MEAN_PITCH = []
        AERODYNAMIC_SENSORS_QUANT=[]                                               #QUANT value of the different sensors for which output is available
        AERO_SENSORS_QUANT_DEFINITION=[]
        TRIM_CONTROLS={}                                                           #Dictionary to save trim angles from pilot input and those actually observed on the blade from PJOINT (the two will be different when the pitch link is flexible) 
        SPEED={}                                                                   #dictionary of some of rotor(craft) operating conditions 
        ROTOR_FORCES_AND_MOMENTS_ALL=[]                                            #Array of overall rotor forces and moment             
        ROTOR_POWER_ALL=[]                                                         #Array of values of different types of rotor power 
        HUBLOADS={}                                                                #Dictionary containing all info regarding hubloads 
                    ##################################################################################
                    #########       Getting some basic data based on input information       #########
                    ##################################################################################    
        while True:
            line = f.readline()
            if 'RADIUS (M)' in line:
                RADIUS=float(line.split()[3])
            else:
                continue
            break
    
        while True:
            line = f.readline()
            if 'NUMBER OF BLADES' in line:
                Nb=int(line.split()[4])
            else:
                continue
            break
   
    
        while True:
            line = f.readline()
            if 'AZIMUTH INCREMENT (DEG)' in line:
                DELTA_PSI=line.split("=")[2]
                DELTA_PSI=float(DELTA_PSI)
            else:
                continue
            break
    
        while True:
            line = f.readline()
            if 'OPPOST' in line:
                OPPOST=bool(int(line.split('=')[-1]))
            else:
                continue
            break
        
        while True:
            line = f.readline()
            if 'HUB AND BLADE SENSORS' in line:
                line = f.readline()
                line = f.readline()
                for x in range(0,6):
                    line = f.readline()
                    time_step=re.search('TIME =(.*) M', line)
                    TIME_STEP.append(int(time_step.group(1)))
                    no_harmonics=line.split()[-1]
                    M_HARM.append(int(no_harmonics))
            else:
                continue
            break

        while True:
            line = f.readline()
            if 'ASHAFT' in line:
                ASHAFT = float(line.split('=')[-1])
            else:
                continue
            break
    
        #####   Extracting pitch bearing location    #####
        while True:
            line = f.readline()
            if 'EPITCH' in line:
                EPITCH="{:.4f}".format(float(line.split()[-1]))
            else:
                continue
            break
    
        #####   Extracting TEF location    #####
        while True:
            line = f.readline()
            if 'OPTEF =' in line:
                OPTEF="{:.0f}".format(float(line.split()[-1]))
            else:
                continue
            break
        
        if OPTEF:
            while True:
                line = f.readline()
                if 'EHTEF =' in line:
                    EHTEF=[float(line.split()[3]), float(line.split()[4])]
                else:
                    continue
                break
        
        #####   Extracting data corresponding to blade position sensors    #####   
        #Entries are stored as string and not float since exact matching of station with text in output file is required to extract further data 
        while True:
            line = f.readline()
            if 'NRPOS' in line:
                NRPOS = int(line.split()[-1])
                if NRPOS>1:
                    line = f.readline()
                    for t in line.split()[4:]:
                        try:
                            SENSOR_STATION_BP.append("{:.4f}".format(float(t)))     #extract blade position sensor station upto 4 decimal places
                        except ValueError:
                            pass
                    while len(SENSOR_STATION_BP)<NRPOS:
                        line = f.readline()
                        for t in line.split():
                            try:
                                SENSOR_STATION_BP.append("{:.4f}".format(float(t)))     #extract blade position sensor station upto 4 decimal places
                            except ValueError:
                                pass                 
            else:
                continue
            SENSOR_STATION_BP.append('1.0000')                  #position sensor data corresponding to EPITCH is output even if data there is not desired (i.e. the entry was not explicitly made to see the output there)
            SENSOR_STATION_BP.append(str(EPITCH))               #position sensor data corresponding to EPITCH is output even if data there is not desired
            SENSOR_STATION_BP = list(set(SENSOR_STATION_BP))    #removing redundant entries that might arise
            SENSOR_STATION_BP.sort()  
            break
        
        if print_read_statements: print('read CII file till blade position sensor stations')
         
        
        #####   Extracting data corresponding to blade CFD position sensors    #####   
        while True:
            line = f.readline()
            if 'OPCFD =' in line:
                OPCFD="{:.0f}".format(float(line.split()[-1]))
            else:
                continue
            break

        while True:
            line = f.readline()
            if 'NRCFD' in line:
                NRCFD = int(line.split()[-1])
                if NRCFD>1:
                    line = f.readline()
                    for t in line.split()[4:]:
                        try:
                            SENSOR_STATION_BCFDP.append("{:.5f}".format(float(t)))     #extract blade position sensor station upto 5 decimal places
                        except ValueError:
                            pass
                    while len(SENSOR_STATION_BCFDP)<NRCFD:
                        line = f.readline()
                        for t in line.split():
                            try:
                                SENSOR_STATION_BCFDP.append("{:.5f}".format(float(t)))     #extract blade position sensor station upto 5 decimal places
                            except ValueError:
                                pass                 
            else:
                continue
            break
    
        
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
                    SENSOR_STATION_BL.append(last)            
                    #SENSOR_STATION_BL.append(float(split_line[-1]))
            else:
                continue
            break
        if print_read_statements: print('read CII file till bloadeload sensor locations')
        
        #####   Extracting data corresponding to aerodynamic panel locations    #####
        while True:
            line = f.readline()
            if 'NPANEL' in line:
                NPANEL = int(line.split()[-1]) 
                next_line=f.readline()
                next_line=f.readline()
                for x in range(0,NPANEL):
                    next_line=f.readline()
                    REDGE.append(float(next_line.split()[1]))
                    PANEL_MIDPOINT.append(float(next_line.split()[3]))
            else:
                continue
            break   
    
        if print_read_statements: print('read CII file till aeropanel locations')
        
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
                    AERODYNAMIC_SENSORS_QUANT.append(int(line.split()[3]))            
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
        while True:
            line = f.readline()
            if 'VELOCITY (KNOTS)' in line:
                SPEED['VELOCITY (KNOTS)']=float(line.split()[3])
                line = f.readline()
                SPEED['V/(OMEGA*R)']=float(line.split()[2])
                line = f.readline()
                SPEED['MACH NUMBER']=float(line.split()[3])
                line = f.readline()
                SPEED['VELOCITY (M/SEC)']=float(line.split()[3])
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
    
                ##########################################################################################
                ##############         Extracting HIGHER HARMONIC CONTROL input          #################
                ##########################################################################################   
    
        IBC_HHC_INPUT={'ROT_FRAME_INPUT':{},'TEF_INPUT':{}}  
        while True:
            line = f.readline()
            if 'HIGHER HARMONIC CONTROL' in line:
                line = f.readline()
                temp=line.split('ROTATING FRAME    =   ')[-1]
                ROT_FRAME_INPUT_HARMONICS_NUMBER=int(temp.split('      TE FLAP =   ')[0])
                TEF_INPUT_HARMONICS_NUMBER=int(temp.split('      TE FLAP =   ')[-1])
                line = f.readline()
                TEF_mean_1 = float(line.split()[8])
                if ROT_FRAME_INPUT_HARMONICS_NUMBER!=0:                
                    IBC_HHC_INPUT['ROT_FRAME_INPUT']['Cosine']=[]
                    IBC_HHC_INPUT['ROT_FRAME_INPUT']['Sine']=[]
                    while True:
                        line=f.readline()
                        if 'HIGHER HARMONIC CONTROL, ROTATING FRAME PITCH' in line:
                            line=f.readline()
                            for _ in range(0,ROT_FRAME_INPUT_HARMONICS_NUMBER):
                                line=f.readline()
                                IBC_HHC_INPUT['ROT_FRAME_INPUT']['Cosine'].append(float(line.split()[4]))
                                IBC_HHC_INPUT['ROT_FRAME_INPUT']['Sine'].append(float(line.split()[7]))
                        else:
                            continue                    
                        break
                IBC_HHC_INPUT['TEF_INPUT']['Mean']=TEF_mean_1
                if TEF_INPUT_HARMONICS_NUMBER!=0:
                    IBC_HHC_INPUT['TEF_INPUT']['Cosine']=[]
                    IBC_HHC_INPUT['TEF_INPUT']['Sine']=[]
                    
                    while True:
                        line=f.readline()
                        if 'HIGHER HARMONIC CONTROL, TRAILING EDGE FLAP 1' in line:
                            line=f.readline()
                            TEF_mean_2=float(line.split()[-1])                                          
                            IBC_HHC_INPUT['TEF_INPUT']['Mean']=TEF_mean_1+TEF_mean_2                    #Adding the two possible ways mnean deflection entry can be given 
                            for _ in range(0,TEF_INPUT_HARMONICS_NUMBER):
                                line=f.readline()
                                IBC_HHC_INPUT['TEF_INPUT']['Cosine'].append(float(line.split()[4]))
                                IBC_HHC_INPUT['TEF_INPUT']['Sine'].append(float(line.split()[7]))
                        else:
                            continue                    
                        break
            else:
                continue
            break
                
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
    
                #############################################################################################
                ##############         Extracting overall rotor forces and moments          #################
                #############################################################################################
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
                        ROTOR_FORCES_AND_MOMENTS_ALL.append(force_moment)                
            else:
                continue
            break
        ROTOR_FORCES_AND_MOMENTS_ALL=np.asarray(ROTOR_FORCES_AND_MOMENTS_ALL)
    
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
                        ROTOR_POWER_ALL.append(power)                
            else:
                continue
            break
        ROTOR_POWER=ROTOR_POWER_ALL[0][2]
        ROTOR_POWER_ALL=np.asarray(ROTOR_POWER_ALL)

        #####    rotor solidity   #####
        while True:
            line = f.readline()
            if 'SOLIDITY RATIO SIGMA' in line:
                SIGMA = float(re.search('SOLIDITY RATIO SIGMA =(.*),',line).group(1))
                break
            else:
                continue
            
                
    
        if print_read_statements: print('read CII file till position sensors')
    
                ##################################################################################
                ##############         Extracting hub loads sensor data          #################
                ##################################################################################
        while True:
            line = f.readline()        
            if 'ROTOR 1 NONROTATING HUB FORCE' in line:
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
            if 'ROTOR 1 NONROTATING HUB MOMENT' in line:
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
                        HUBLOADS={'NONROT_HUB_FORCE':NONROT_HUB_FORCE,'NONROT_HUB_FORCE_HARM':NONROT_HUB_FORCE_HARM,'NONROT_HUB_FORCE_HARM_COSINE':NONROT_HUB_FORCE_HARM_COSINE,
                                  'NONROT_HUB_FORCE_HARM_SINE':NONROT_HUB_FORCE_HARM_SINE,'NONROT_HUB_MOM':NONROT_HUB_MOM,'NONROT_HUB_MOM_HARM':NONROT_HUB_MOM_HARM,
                                  'NONROT_HUB_MOM_HARM_COSINE':NONROT_HUB_MOM_HARM_COSINE,'NONROT_HUB_MOM_HARM_SINE':NONROT_HUB_MOM_HARM_SINE}
                    else:
                        continue
                    break                        
            else:
                continue
            break
    
    
                #########################################################################################
                ##############         Extracting blade root loads sensor data          #################
                #########################################################################################
        while True:
            line = f.readline()        
            if 'ROTOR 1 BLADE 4 ROOT FORCE' in line:
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
            if 'ROTOR 1 BLADE 4 ROOT MOMENT' in line:
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
            if 'ROTOR 1 PITCH LINK 4 FORCE' in line:
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
                    
    
    
        if print_read_statements: print('read CII file till bladeloads sensors')
    
    
                ##################################################################################
                ##############       Extracting blade loads sensor data          #################
                ##################################################################################           
        # 2D matrix of loads distribution: rows --> azimuth, column --> loads sensor station
        TORSION=FLAP_BENDING=LAG_BENDING=AXIAL_FORCE=CHORD_FORCE=NORM_FORCE=np.zeros((TIME_STEP[2]+1,len(SENSOR_STATION_BL)))
        BLADELOADS=np.zeros((TIME_STEP[2]+1,6,len(SENSOR_STATION_BL)))
        BLADELOADS_OSCILLATORY=np.zeros((TIME_STEP[2]+1,6,len(SENSOR_STATION_BL)))
        BLADELOADS_HARMONICS=np.zeros((M_HARM[2],6,len(SENSOR_STATION_BL)))
        order_of_loads=['Torsion','Flap','Lag','Axial','Chord','Norm']
        for load_type in order_of_loads: 
            MEAN_LOADS[load_type]=[]
            HALF_PEAK_TO_PEAK[load_type]=[]
        z=0
        while True:
            line = f.readline()        
            if ''.join(['ROTOR 1 BLADE 4 LOAD ',SENSOR_STATION_BL[z]]) in line:
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
    
        if print_read_statements: print('read CII file till position sensors')
    
                ##################################################################################
                ##########           Extracting blade position sensors data            ###########
                ##################################################################################
        # 2D matrix of pitch distribution: rows --> azimuth, column --> position sensor station        
        PITCH=np.zeros((TIME_STEP[3]+1,len(SENSOR_STATION_BP)))     
        SENSOR_DATA_CFD_POS=np.zeros((TIME_STEP[3]+1,6,len(SENSOR_STATION_BCFDP)))
        SENSOR_DATA_CFD_POS_HARMONICS={'mean':np.zeros((1,6,len(SENSOR_STATION_BCFDP))),
                                      'cosine':np.zeros((M_HARM[3],6,len(SENSOR_STATION_BCFDP))),
                                      'sine':np.zeros((M_HARM[3],6,len(SENSOR_STATION_BCFDP)))}
        bp_idx=0
        bcfdp_idx=0
        while True:
            line = f.readline()        
            if ''.join(['ROTOR 1 BLADE 4 POS ',SENSOR_STATION_BP[bp_idx]]) in line:  
                
                while True:
                    line = f.readline()
                    if 'MEAN' in line:
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
            elif 'ROTOR 1 BLADE 4 POS  PJOINT' in line:
    
                while True:
                    line = f.readline()
                    if 'MEAN' in line:
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
            elif ''.join(['ROTOR 1 BLADE 4 CFD ',SENSOR_STATION_BCFDP[bcfdp_idx]]) in line:        
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
        
        if print_read_statements: print('read file till aero sensors')
                ##################################################################################
                ###########           Extracting aerodynamic sensors data            #############
                ##################################################################################
        
        #####   Extracting blade angle of attack distribution over the azimuth    #####
        ALPHA=np.zeros((TIME_STEP[4]+1,len(PANEL_MIDPOINT)))
        
        # if post trim is carried out then extracting the corresponding aerodynamic data 
        # (note: both with and without post-trim data are printed out in CII output)
        if OPPOST:    search_txt = ['RTREX 1 WING 4 ANGLE OF ATTACK','RTREX1WING4SENSOR']       
        else:    search_txt = ['ROTOR 1 WING 4 ANGLE OF ATTACK','ROTOR1WING4SENSOR']
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
        AZIMUTH=np.arange(0.0,360.0+DELTA_PSI,DELTA_PSI)               
        
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
        POINTER_LOC=f.tell()
        if print_read_statements: print('read everything from file',filename.split('/')[-1])

    return {'filename':filename.split('/')[-1],
            'RADIUS':RADIUS,'Nb':Nb,'DELTA_PSI':DELTA_PSI,'TIME_STEP':TIME_STEP,'ASHAFT':ASHAFT,'EPITCH':EPITCH,
            'OPTEF':OPTEF,'EHTEF':EHTEF,
            'SENSOR_STATION_BCFDP':SENSOR_STATION_BCFDP,'SENSOR_STATION_BP':SENSOR_STATION_BP,'SENSOR_STATION_BL':SENSOR_STATION_BL,
            'NPANEL':NPANEL,'REDGE':REDGE,'PANEL_MIDPOINT':PANEL_MIDPOINT,
            'AERODYNAMIC_SENSORS_QUANT':AERODYNAMIC_SENSORS_QUANT,'SPEED':SPEED,'TRIM_CONTROLS':TRIM_CONTROLS,'IBC_HHC_INPUT':IBC_HHC_INPUT,
            'ROTOR_FORCES_AND_MOMENTS_ALL':ROTOR_FORCES_AND_MOMENTS_ALL,'ROTOR_POWER':ROTOR_POWER,'ROTOR_POWER_ALL':ROTOR_POWER_ALL,
            'SIGMA':SIGMA,
            'HUBLOADS':HUBLOADS,'BLADE_ROOT_LOADS':BLADE_ROOT_LOADS,'CONTROL_LOADS':CONTROL_LOADS,'MEAN_LOADS':MEAN_LOADS,
            'HALF_PEAK_TO_PEAK':HALF_PEAK_TO_PEAK,'BLADELOADS':BLADELOADS,
            'BLADELOADS_OSCILLATORY':BLADELOADS_OSCILLATORY,'BLADELOADS_HARMONICS':BLADELOADS_HARMONICS,'MEAN_PITCH':MEAN_PITCH,'PITCH':PITCH,
            'PJOINT_HISTORY':PJOINT_HISTORY,'SENSOR_DATA_CFD_POS':SENSOR_DATA_CFD_POS,'SENSOR_DATA_CFD_POS_HARMONICS':SENSOR_DATA_CFD_POS_HARMONICS,
            'ALPHA':ALPHA,'AZIMUTH':AZIMUTH,'AERO_SENSORS_QUANT_DEFINITION':AERO_SENSORS_QUANT_DEFINITION,
            'SENSORS_DATA':SENSORS_DATA,'SENSORS_DATA_DICT':SENSORS_DATA_DICT,'SENSORS_DATA_DF_DICT':SENSORS_DATA_DF_DICT,
            'SENSORS_DATA_HARMONICS':SENSORS_DATA_HARMONICS,'SENSORS_DATA_DICT_HARMONICS':SENSORS_DATA_DICT_HARMONICS,
            'POINTER_LOC':POINTER_LOC}

               
                