#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 15:41:40 2020

@author: ge56beh
"""
import numpy as np
import itertools
import matplotlib.pyplot as plt
#plt.ioff()
import matplotlib.gridspec as gridspec
import operator
import mpl_toolkits.mplot3d#The IDE says that this is not being explicitly used but not importing this module does not recognise projection='3d' and throws an error

import polar,xy,bar,wireframe 

#Function returns dictionaries of figures, axes and all data corresponding to each subplot plotted after click

def plot_all(filename,data_dict,DATA_EXTRACTED_BASELINE,QUANTITIES_TO_BE_PLOTTED,PLOT_LIMITS,PLOT_LIMITS_DELTA,DISPLAY_SETTINGS,CLICK_FIG_DETAILS):
    #Data corresponding to Bo-105 only
    Linear_twist=-8
    Radius=4.912        

####################################################################################################
####    Extracting general information presumed to be same for 'CLICK_FILENAME' and Baseline    ####
####################################################################################################
    TIME_STEP = data_dict['TIME_STEP']                
    EPITCH = float(data_dict['EPITCH'])
    SENSOR_STATION_BL = data_dict['SENSOR_STATION_BL']
    AERODYNAMIC_SENSORS_QUANT = data_dict['AERODYNAMIC_SENSORS_QUANT']
    SENSOR_STATION_BP = data_dict['SENSOR_STATION_BP']
    SENSOR_STATION_AERO = ['PANEL_MIDPOINT']
    PSI_HL = (np.arange(0,360+360.0/TIME_STEP[3],360.0/TIME_STEP[0])).tolist()
    PSI_BP = (np.arange(0,360+360.0/TIME_STEP[3],360.0/TIME_STEP[3])).tolist()
    PSI_BL = (np.arange(0,360+360.0/TIME_STEP[2],360.0/TIME_STEP[2])).tolist()
    PSI_AERO = (np.arange(0,360+360.0/TIME_STEP[4],360.0/TIME_STEP[4])).tolist()
    BLADELOADS_ORDER = ['TORSION','FLAP','LAG','AXIAL','CHORD','NORM']

########################################################################################    
####    Getting data corresponding to 'CLICK_FILENAME' stored in 'ALL_DATA_DICT'    ####
########################################################################################
    if DISPLAY_SETTINGS[0]:
        BLADELOADS=data_dict['BLADELOADS_OSCILLATORY']
    else:
        BLADELOADS=data_dict['BLADELOADS']     
        
    BLADELOADS_HARMONICS = data_dict['BLADELOADS_HARMONICS']
    PITCH = data_dict['PITCH']
    PJOINT_HISTORY = data_dict['PJOINT_HISTORY']
    SENSOR_DATA_AERO = data_dict['SENSORS_DATA']
    SPEED = data_dict['SPEED']
    TRIM_CONTROLS = data_dict['TRIM_CONTROLS']
    ROTOR_POWER_ALL = data_dict['ROTOR_POWER_ALL']
    ROTOR_FORCES_AND_MOMENTS_ALL = data_dict['ROTOR_FORCES_AND_MOMENTS_ALL']
    DATA_HUBLOADS = data_dict['HUBLOADS']
    
####    Evaulating blade twist    ####
    RIGID_BLADE_PITCH_POLAR=np.zeros((len(PSI_BP),len(SENSOR_STATION_BP)))
    ELASTIC_BLADE_PITCH_POLAR=PITCH
    for i in range(0,len(SENSOR_STATION_BP)):
        if float(SENSOR_STATION_BP[i])>=EPITCH:                #Twisting starts from the pitch bearing 
            for j in range(0,len(PSI_BP)):
                RIGID_BLADE_PITCH_POLAR[j][i]=PJOINT_HISTORY[j]+(Linear_twist*(Radius-EPITCH)/Radius)*(float(SENSOR_STATION_BP[i])-EPITCH)    
    ELASTIC_TWIST=ELASTIC_BLADE_PITCH_POLAR-RIGID_BLADE_PITCH_POLAR
    SENSOR_POS_DICT={'RIGID_BLADE_PITCH_POLAR':RIGID_BLADE_PITCH_POLAR,'ELASTIC_BLADE_PITCH_POLAR':ELASTIC_BLADE_PITCH_POLAR,'ELASTIC_TWIST':ELASTIC_TWIST}
    
######################################################################################################################################## 
####    Getting data corresponding to DATA_EXTRACTED_BASELINE assuming that input file parameters are the same as filename    ####
######################################################################################################################################## 
    if DISPLAY_SETTINGS[0]:
        BLADELOADS_BASELINE=DATA_EXTRACTED_BASELINE['BLADELOADS_OSCILLATORY']
    else:
        BLADELOADS_BASELINE=DATA_EXTRACTED_BASELINE['BLADELOADS']
    BLADELOADS_HARMONICS_BASELINE=DATA_EXTRACTED_BASELINE['BLADELOADS_HARMONICS']
    PITCH_BASELINE=DATA_EXTRACTED_BASELINE['PITCH']
    PJOINT_HISTORY_BASELINE=DATA_EXTRACTED_BASELINE['PJOINT_HISTORY']
    SENSOR_DATA_AERO_BASELINE=DATA_EXTRACTED_BASELINE['SENSORS_DATA']
    ROTOR_POWER_ALL_BASELINE=DATA_EXTRACTED_BASELINE['ROTOR_POWER_ALL']
    ROTOR_FORCES_AND_MOMENTS_ALL_BASELINE=DATA_EXTRACTED_BASELINE['ROTOR_FORCES_AND_MOMENTS_ALL']
    SPEED_BASELINE=DATA_EXTRACTED_BASELINE['SPEED']
    TRIM_CONTROLS_BASELINE = DATA_EXTRACTED_BASELINE['TRIM_CONTROLS']
    DATA_HUBLOADS_BASELINE = DATA_EXTRACTED_BASELINE['HUBLOADS']                    

####    Evaulating baseline blade twist    ####
    RIGID_BLADE_PITCH_POLAR_BASELINE=np.zeros((len(PSI_BP),len(SENSOR_STATION_BP)))
    ELASTIC_BLADE_PITCH_POLAR_BASELINE=PITCH_BASELINE
    for i in range(0,len(SENSOR_STATION_BP)):
        if float(SENSOR_STATION_BP[i])>=EPITCH:
            for j in range(0,len(PSI_BP)):
                RIGID_BLADE_PITCH_POLAR_BASELINE[j][i]=PJOINT_HISTORY_BASELINE[j]+(Linear_twist*(Radius-EPITCH)/Radius)*(float(SENSOR_STATION_BP[i])-EPITCH)    
    ELASTIC_TWIST_BASELINE=ELASTIC_BLADE_PITCH_POLAR_BASELINE-RIGID_BLADE_PITCH_POLAR_BASELINE
    SENSOR_POS_DICT_BASELINE={'RIGID_BLADE_PITCH_POLAR':RIGID_BLADE_PITCH_POLAR_BASELINE,'ELASTIC_BLADE_PITCH_POLAR':ELASTIC_BLADE_PITCH_POLAR_BASELINE,'ELASTIC_TWIST':ELASTIC_TWIST_BASELINE}
    SENSOR_POS_DICT_DELTA={'RIGID_BLADE_PITCH_POLAR':RIGID_BLADE_PITCH_POLAR-RIGID_BLADE_PITCH_POLAR_BASELINE,
                           'ELASTIC_BLADE_PITCH_POLAR':ELASTIC_BLADE_PITCH_POLAR-ELASTIC_BLADE_PITCH_POLAR_BASELINE,
                           'ELASTIC_TWIST':ELASTIC_TWIST-ELASTIC_TWIST_BASELINE}
##################################################################################################################
####    Creating a dictionary of figures, axes, grids and output data for figures to be plotted post click    ####
##################################################################################################################    
    All_possible_figs_post_click={filename:DISPLAY_SETTINGS[1],'BASELINE':DISPLAY_SETTINGS[3],filename+'_MINUS_BASELINE':DISPLAY_SETTINGS[2]}
    FIG={}
    GS={}
    AX={}
    DATA_PLOTTED_POST_CLICK={}
    DATA_EXTRACTED_FOR_WIDGETS_PLOT={}
    DATA_WIDGETS_COMMON={}
    for figurename in All_possible_figs_post_click:
        if All_possible_figs_post_click[figurename]:
            FIG[figurename]=plt.figure(num=figurename,figsize=CLICK_FIG_DETAILS[0])            
            GS[figurename]=gridspec.GridSpec(CLICK_FIG_DETAILS[1], CLICK_FIG_DETAILS[2], figure=FIG[figurename])
            AX[figurename]=[]
            DATA_PLOTTED_POST_CLICK[figurename]={}                               #Nested dictionary to return all data plotted in each figure that gets generated post-click      
            DATA_EXTRACTED_FOR_WIDGETS_PLOT[figurename]={}
            DATA_WIDGETS_COMMON[figurename]={}

    print('adhsfudzsfzdaszfuasdzofzsdouzfsoud')
    print(FIG.keys())
    l=-1
    Operators=[operator.add, operator.sub, operator.mul, operator.truediv]    
    for KEY, VALUE in QUANTITIES_TO_BE_PLOTTED.items():
        
        if KEY != 'ADDITIONAL_DATA':    
            for figurename in FIG:    DATA_EXTRACTED_FOR_WIDGETS_PLOT[figurename][KEY],DATA_WIDGETS_COMMON[figurename][KEY]={},{}

                
                          ########################################################################################              
                          ####           Printing the XY/Bar plots corresponding to HUBLOAD_SENSORS           ####  
                          ######################################################################################## 
        if KEY=='HUBLOAD_SENSORS':
            for figurename in FIG: DATA_PLOTTED_POST_CLICK[figurename][KEY]={}   #Creating empty nested dictionary to save data
            
            if VALUE:
                for Key, Value in VALUE.items():    #'Key' here refers to 'NONROT_HUB(_*)' in Plot_from_click_HUBLOAD_SENSORS
                    if Value:                       #if there exist elements in the list corresponding to the value associated with 'Key'
                        for figurename in FIG: 
                            DATA_PLOTTED_POST_CLICK[figurename][KEY][Key]={}
                            
                        for quantity in Value:      #iterating thru the elements in the list
                            
                            Fig_title=KEY+'-'+quantity
                            Legend=[]
                            l+=1
                            if l>=CLICK_FIG_DETAILS[1]*CLICK_FIG_DETAILS[2]:                              #Checking if the grid is full of plots already or not (if it is then further plotting is stopped and the grid size needs to be increased)  
                                for figurename in FIG:    GS[figurename].tight_layout(FIG[figurename])        #Ensures no subplots overlap
                                print('WARNING: It seems you are seeking to plot more results than the grid size allows for. Increase the grid size (using \'Click_grid_rows\' and \'Click_grid_columns\' to see all results!!')
                                return FIG,AX,DATA_PLOTTED_POST_CLICK,DATA_EXTRACTED_FOR_WIDGETS_PLOT,DATA_WIDGETS_COMMON
                                
                            if 'HARM' in Key:
                                Ylabel='Magnitude'
                                Xlabel='Harmonics'                            
                                indices=np.arange(1,1+len(DATA_HUBLOADS[Key][quantity]))
                                Xticklabels=tuple([str(i)+'P' for i in indices])    #Assuming that the baseline and all the other files have the same number of harmonics data in the output files
                                Data_hubloads_delta_harmonics=[data_click_filename-data_baseline for (data_click_filename,data_baseline) in zip(DATA_HUBLOADS[Key][quantity],DATA_HUBLOADS_BASELINE[Key][quantity])]
                                Hubload_harmonics={filename:DATA_HUBLOADS[Key][quantity],filename+'_MINUS_BASELINE':Data_hubloads_delta_harmonics,'BASELINE':DATA_HUBLOADS_BASELINE[Key][quantity]}            
                                for figurename in FIG:
                                    DATA_PLOTTED_POST_CLICK[figurename][KEY][Key]={}
                                    AX[figurename].append(FIG[figurename].add_subplot(GS[figurename][l]))
                                    bar.bar_plot(FIG[figurename],AX[figurename][l],Fig_title,Hubload_harmonics[figurename],Legend,Xlabel,Ylabel,Xticklabels)
                                    DATA_PLOTTED_POST_CLICK[figurename][KEY][Key][quantity]=Hubload_harmonics[figurename]
                            else:
                                Xlabel='${\psi}$'
                                Ylabel=KEY+'-'+quantity
                                Data_hubloads_delta=[data_click_filename-data_baseline for (data_click_filename,data_baseline) in zip(DATA_HUBLOADS[Key][quantity],DATA_HUBLOADS_BASELINE[Key][quantity])]
                                Hubload={filename:DATA_HUBLOADS[Key][quantity],filename+'_MINUS_BASELINE':Data_hubloads_delta,'BASELINE':DATA_HUBLOADS_BASELINE[Key][quantity]}            
                                for figurename in FIG:
                                    AX[figurename].append(FIG[figurename].add_subplot(GS[figurename][l]))
                                    Limits=[]
                                    if Key in PLOT_LIMITS and quantity in PLOT_LIMITS[Key]: Limits=PLOT_LIMITS[Key][quantity][0:2]
                                    if Key in PLOT_LIMITS_DELTA and quantity in PLOT_LIMITS[Key] and figurename==filename+'_MINUS_BASELINE': Limits=PLOT_LIMITS[Key][quantity][0:2]
                                    xy.xy_plot(FIG[figurename],AX[figurename][l],Fig_title,PSI_HL,Hubload[figurename],Legend,Xlabel,Ylabel,Limits)
                                    DATA_PLOTTED_POST_CLICK[figurename][KEY][Key][quantity]=Hubload[figurename]

                          ########################################################################################              
                          ####        Printing the XY/Bar plots corresponding to BLADELOAD_SENSORS            ####  
                          ######################################################################################## 
        if KEY=='LOAD_SENSORS':
            for figurename in FIG: DATA_PLOTTED_POST_CLICK[figurename][KEY]={}
                
            for key in VALUE:                
                if VALUE[key]:                                                 #Checking if there are any bladeload sensors to plot
                    for figurename in FIG: 
                        DATA_PLOTTED_POST_CLICK[figurename][KEY][key]={}
                        if DISPLAY_SETTINGS[4]:DATA_PLOTTED_POST_CLICK[figurename][KEY][key+'Harmonics']={}
                    if not DISPLAY_SETTINGS[4] and not DISPLAY_SETTINGS[5]:                           #if both 'Plot_BL_individually' and 'Plot_BL_harmonics' are set to False  
                        l=l+1
                        if l>=CLICK_FIG_DETAILS[1]*CLICK_FIG_DETAILS[2]:                              #Checking if the grid is full of plots already or not (if it is then further plotting is stopped and the grid size needs to be increased)  
                            for figurename in FIG:    GS[figurename].tight_layout(FIG[figurename])        #Ensures no subplots overlap
                            print('WARNING: It seems you are seeking to plot more results than the grid size allows for. Increase the grid size (using \'Click_grid_rows\' and \'Click_grid_columns\' to see all results!!')
                            return FIG,AX,DATA_PLOTTED_POST_CLICK,DATA_EXTRACTED_FOR_WIDGETS_PLOT,DATA_WIDGETS_COMMON
                            
                    for sensor_station in VALUE[key]:                        
                        if DISPLAY_SETTINGS[4] or DISPLAY_SETTINGS[5]:                                #if either 'Plot_BL_individually' are 'Plot_BL_harmonics' are set to True  
                            l=l+1
                            if l>=CLICK_FIG_DETAILS[1]*CLICK_FIG_DETAILS[2]:                              #Checking if the grid is full of plots already or not (if it is then further plotting is stopped and the grid size needs to be increased)  
                                for figurename in FIG:    GS[figurename].tight_layout(FIG[figurename])        #Ensures no subplots overlap
                                print('WARNING: It seems you are seeking to plot more results than the grid size allows for. Increase the grid size (using \'Click_grid_rows\' and \'Click_grid_columns\' to see all results!!')
                                return FIG,AX,DATA_PLOTTED_POST_CLICK,DATA_EXTRACTED_FOR_WIDGETS_PLOT,DATA_WIDGETS_COMMON
                            
                        if sensor_station in SENSOR_STATION_BL:
                            Legend=sensor_station+'R'
                            Xlabel='${\psi}$'
                            Ylabel=key
                            column_index=BLADELOADS_ORDER.index(key)
                            slice_index=SENSOR_STATION_BL.index(sensor_station)
                            BLADELOADS_EXTRACT=BLADELOADS[:,column_index:1+column_index,slice_index:slice_index+1].tolist()
                            BLADELOADS_EXTRACT_BASELINE=BLADELOADS_BASELINE[:,column_index:1+column_index,slice_index:slice_index+1].tolist()
                            BLADELOADS_EXTRACT=list(itertools.chain.from_iterable(BLADELOADS_EXTRACT))
                            BLADELOADS_EXTRACT=list(itertools.chain.from_iterable(BLADELOADS_EXTRACT))
                            BLADELOADS_EXTRACT_BASELINE=list(itertools.chain.from_iterable(BLADELOADS_EXTRACT_BASELINE))
                            BLADELOADS_EXTRACT_BASELINE=list(itertools.chain.from_iterable(BLADELOADS_EXTRACT_BASELINE))
                            BLADELOADS_EXTRACT_DELTA=(np.array(BLADELOADS_EXTRACT)-np.array(BLADELOADS_EXTRACT_BASELINE)).tolist()
                            BLADELOADS_EXTRACTED_ALL={filename:BLADELOADS_EXTRACT,filename+'_MINUS_BASELINE':BLADELOADS_EXTRACT_DELTA,'BASELINE':BLADELOADS_EXTRACT_BASELINE}                           
                            for figurename in FIG:
                                AX[figurename].append(FIG[figurename].add_subplot(GS[figurename][l]))
                                Limits=[]
                                if key in PLOT_LIMITS: Limits=PLOT_LIMITS[key][0:2]
                                if key in PLOT_LIMITS_DELTA and figurename==filename+'_MINUS_BASELINE': Limits=PLOT_LIMITS_DELTA[key][0:2]
                                xy.xy_plot(FIG[figurename],AX[figurename][l],key,PSI_BL,BLADELOADS_EXTRACTED_ALL[figurename],Legend,Xlabel,Ylabel,Limits)
                                DATA_PLOTTED_POST_CLICK[figurename][KEY][key][sensor_station]=BLADELOADS_EXTRACTED_ALL[figurename]
                            
                            BLADELOADS_HARMONICS_EXTRACT=BLADELOADS_HARMONICS[:,column_index:1+column_index,slice_index:slice_index+1].tolist()
                            BLADELOADS_HARMONICS_EXTRACT_BASELINE=BLADELOADS_HARMONICS_BASELINE[:,column_index:1+column_index,slice_index:slice_index+1].tolist()
                            BLADELOADS_HARMONICS_EXTRACT=list(itertools.chain.from_iterable(BLADELOADS_HARMONICS_EXTRACT))
                            BLADELOADS_HARMONICS_EXTRACT=list(itertools.chain.from_iterable(BLADELOADS_HARMONICS_EXTRACT))
                            BLADELOADS_HARMONICS_EXTRACT_BASELINE=list(itertools.chain.from_iterable(BLADELOADS_HARMONICS_EXTRACT_BASELINE))
                            BLADELOADS_HARMONICS_EXTRACT_BASELINE=list(itertools.chain.from_iterable(BLADELOADS_HARMONICS_EXTRACT_BASELINE))
                            BLADELOADS_HARMONICS_EXTRACT_DELTA=(np.array(BLADELOADS_HARMONICS_EXTRACT)-np.array(BLADELOADS_HARMONICS_EXTRACT_BASELINE)).tolist()
                            BLADELOADS_HARMONICS_EXTRACTED_ALL={filename:BLADELOADS_HARMONICS_EXTRACT,filename+'_MINUS_BASELINE':BLADELOADS_HARMONICS_EXTRACT_DELTA,'BASELINE':BLADELOADS_HARMONICS_EXTRACT_BASELINE}                           
                            if DISPLAY_SETTINGS[4]:                            #if harmonic content of bladeloads is desired   
                                indices=np.arange(1,1+len(BLADELOADS_HARMONICS_EXTRACT))
                                Xticklabels=tuple([str(i)+'P' for i in indices])    #Assuming that the baseline and all the other files have the same number of harmonics data in the output files
                                l=l+1
                                if l>=CLICK_FIG_DETAILS[1]*CLICK_FIG_DETAILS[2]:                              #Checking if the grid is full of plots already or not (if it is then further plotting is stopped and the grid size needs to be increased)  
                                    for figurename in FIG:    GS[figurename].tight_layout(FIG[figurename])        #Ensures no subplots overlap
                                    print('WARNING: It seems you are seeking to plot more results than the grid size allows for. Increase the grid size (using \'Click_grid_rows\' and \'Click_grid_columns\' to see all results!!')
                                    return FIG,AX,DATA_PLOTTED_POST_CLICK,DATA_EXTRACTED_FOR_WIDGETS_PLOT,DATA_WIDGETS_COMMON
                                for figurename in FIG:
                                    Xlabel='Harmonics'
                                    Ylabel='Magnitude'
                                    AX[figurename].append(FIG[figurename].add_subplot(GS[figurename][l]))
                                    bar.bar_plot(FIG[figurename],AX[figurename][l],key,BLADELOADS_HARMONICS_EXTRACTED_ALL[figurename],Legend,Ylabel,Xlabel,Xticklabels)
                                    DATA_PLOTTED_POST_CLICK[figurename][KEY][key+'Harmonics'][sensor_station]=BLADELOADS_HARMONICS_EXTRACTED_ALL[figurename]                                
                        else:
                            print('ERROR:: ',KEY,'OUTPUT FOR',key,' AT ',VALUE[key]+'R','IS NOT AVAILABLE IN OUTPUT FILE')            
            BLADELOADS_ALL={filename:BLADELOADS,filename+'_MINUS_BASELINE':BLADELOADS-BLADELOADS_BASELINE,'BASELINE':BLADELOADS_BASELINE}                           
            for figurename in FIG:
                for type_of_load in BLADELOADS_ORDER:
                    column_index=BLADELOADS_ORDER.index(type_of_load)
                    DATA_EXTRACTED_FOR_WIDGETS_PLOT[figurename][KEY][type_of_load]=np.squeeze(BLADELOADS_ALL[figurename][:,column_index:1+column_index,:],axis=(1,))                           
                DATA_WIDGETS_COMMON[figurename][KEY]['SENSOR_STATIONS']=[float(station) for station in SENSOR_STATION_BL] 
                DATA_WIDGETS_COMMON[figurename][KEY]['PSI']=PSI_BL
                
                          #########################################################################################             
                          ####    Printing the polar plots corresponding to Plot_from_click_POSITION_SENSORS   ####  
                          #########################################################################################
        if KEY=='POSITION_SENSORS':
            for figurename in FIG:    DATA_PLOTTED_POST_CLICK[figurename][KEY]={}
            for key in VALUE:
                if VALUE[key]:
                    
                    ####    Plotting the polar plots    ####
                    l=l+1
                    if l>=CLICK_FIG_DETAILS[1]*CLICK_FIG_DETAILS[2]:                              #Checking if the grid is full of plots already or not (if it is then further plotting is stopped and the grid size needs to be increased)  
                        for figurename in FIG:    GS[figurename].tight_layout(FIG[figurename])        #Ensures no subplots overlap
                        print('WARNING: It seems you are seeking to plot more results than the grid size allows for. Increase the grid size (using \'Click_grid_rows\' and \'Click_grid_columns\' to see all results!!')
                        return FIG,AX,DATA_PLOTTED_POST_CLICK,DATA_EXTRACTED_FOR_WIDGETS_PLOT,DATA_WIDGETS_COMMON
                    SENSOR_POS_DATA_EXTRACTED_ALL={filename:SENSOR_POS_DICT,filename+'_MINUS_BASELINE':SENSOR_POS_DICT_DELTA,'BASELINE':SENSOR_POS_DICT_BASELINE}
                    for figurename in FIG:
                        DATA_PLOTTED_POST_CLICK[figurename][KEY][key]={}
                        AX[figurename].append(FIG[figurename].add_subplot(GS[figurename][l],projection='polar'))
                        Limits,Tick_details=[],[]
                        if key in PLOT_LIMITS: Limits,Tick_details=PLOT_LIMITS[key][0:2],PLOT_LIMITS[key][2:3]
                        if key in PLOT_LIMITS_DELTA and figurename==filename+'_MINUS_BASELINE': Limits,Tick_details=PLOT_LIMITS_DELTA[key][0:2],PLOT_LIMITS_DELTA[key][2:3]
                        # print(figurename)
                        # print(FIG[figurename],'\n')
                        # print(AX[figurename][l],'\n')
                        # print(key,'\n')
                        # print(PSI_BP,'\n',SENSOR_STATION_BP,'\n')
                        # print(SENSOR_POS_DATA_EXTRACTED_ALL[figurename][key],'\n',Limits,'\n',Tick_details)
                        polar.pcolormesh_plot(FIG[figurename],AX[figurename][l],key,PSI_BP,SENSOR_STATION_BP,SENSOR_POS_DATA_EXTRACTED_ALL[figurename][key],Limits,Tick_details)
                        DATA_PLOTTED_POST_CLICK[figurename][KEY][key]['Xdata']=PSI_BP
                        DATA_PLOTTED_POST_CLICK[figurename][KEY][key]['Ydata']=SENSOR_STATION_BP
                        DATA_PLOTTED_POST_CLICK[figurename][KEY][key]['Zdata']=SENSOR_POS_DATA_EXTRACTED_ALL[figurename][key]
                        DATA_EXTRACTED_FOR_WIDGETS_PLOT[figurename][KEY][key]=SENSOR_POS_DATA_EXTRACTED_ALL[figurename][key]

                    ####    Plotting the wireplots    ####    
                    if DISPLAY_SETTINGS[6]:                                    #if Display_wireplots_also=True 
                        l=l+1
                        if l>=CLICK_FIG_DETAILS[1]*CLICK_FIG_DETAILS[2]:                              #Checking if the grid is full of plots already or not (if it is then further plotting is stopped and the grid size needs to be increased)  
                            for figurename in FIG:    GS[figurename].tight_layout(FIG[figurename])        #Ensures no subplots overlap
                            print('WARNING: It seems you are seeking to plot more results than the grid size allows for. Increase the grid size (using \'Click_grid_rows\' and \'Click_grid_columns\' to see all results!!')
                            return FIG,AX,DATA_PLOTTED_POST_CLICK,DATA_EXTRACTED_FOR_WIDGETS_PLOT,DATA_WIDGETS_COMMON
                        for figurename in FIG:
                            AX[figurename].append(FIG[figurename].add_subplot(GS[figurename][l],projection='3d'))
                            Limits=[]
                            if key in PLOT_LIMITS: Limits=PLOT_LIMITS[key][0:2]
                            if key in PLOT_LIMITS_DELTA and figurename==filename+'_MINUS_BASELINE': Limits=PLOT_LIMITS_DELTA[key][0:2]
                            wireframe.wireframe_plot(FIG[figurename],AX[figurename][l],key,PSI_BP,[float(station)for station in SENSOR_STATION_BP],SENSOR_POS_DATA_EXTRACTED_ALL[figurename][key],Limits)
            for figurename in FIG:                                
                DATA_WIDGETS_COMMON[figurename][KEY]['SENSOR_STATIONS']=[float(station) for station in SENSOR_STATION_BP] 
                DATA_WIDGETS_COMMON[figurename][KEY]['PSI']=PSI_BP
                
                          ######################################################################################              
                          ####    Printing the polar plots corresponding to Plot_from_click_AERO_SENSORS    ####  
                          ###################################################################################### 
        if KEY=='AERO_SENSORS':
            for figurename in FIG:    DATA_PLOTTED_POST_CLICK[figurename][KEY]={}
            for key in VALUE:
                if VALUE[key]:   #if values in Plot_from_click_AERO_SENSORS consist of non-empty lists then execute
                    l=l+1
                    if l>=CLICK_FIG_DETAILS[1]*CLICK_FIG_DETAILS[2]:                              #Checking if the grid is full of plots already or not (if it is then further plotting is stopped and the grid size needs to be increased)  
                        for figurename in FIG:    GS[figurename].tight_layout(FIG[figurename])        #Ensures no subplots overlap
                        print('WARNING: It seems you are seeking to plot more results than the grid size allows for. Increase the grid size (using \'Click_grid_rows\' and \'Click_grid_columns\' to see all results!!')
                        return FIG,AX,DATA_PLOTTED_POST_CLICK,DATA_EXTRACTED_FOR_WIDGETS_PLOT,DATA_WIDGETS_COMMON
                    skip=0
                    QUANTITY=np.zeros((len(PSI_AERO),len(SENSOR_STATION_AERO)))
                    QUANTITY_BASELINE=np.zeros((len(PSI_AERO),len(SENSOR_STATION_AERO)))
                    for quant in VALUE[key]:
                        quant_input="{:.2f}".format(float(quant))
                        intpart=int(quant_input.split('.')[0])
                        decimalparts=[int(d) for d in quant_input.split('.')[1]]
                        decimalpart_first=decimalparts[0]
                        decimalpart_second=decimalparts[1]                       
                        if intpart in AERODYNAMIC_SENSORS_QUANT:
                            quant_index=decimalpart_second+(AERODYNAMIC_SENSORS_QUANT.index(intpart))
                            QUANTITY=Operators[decimalpart_first](QUANTITY,np.squeeze(SENSOR_DATA_AERO[:,:,quant_index:quant_index+1], axis=(2,)))
                            QUANTITY_BASELINE=Operators[decimalpart_first](QUANTITY_BASELINE,np.squeeze(SENSOR_DATA_AERO_BASELINE[:,:,quant_index:quant_index+1], axis=(2,)))
                        elif intpart==0:
                            r, _ = np.meshgrid(SENSOR_STATION_AERO,PSI_AERO)
                            QUANTITY=Operators[decimalpart_first](QUANTITY,r)
                            QUANTITY_BASELINE=Operators[decimalpart_first](QUANTITY_BASELINE,r)
                        else:
                            print('Error: The sensor quant',intpart,' you are trying to display is not there in the output file')
                            skip=1                    
                    if key=='ALPHA': 
                        QUANTITY=(180/3.14)*QUANTITY       #Converting angle to degrees
                        QUANTITY_BASELINE=(180/3.14)*QUANTITY_BASELINE
                    if key=='FLAP_DEFLECTION_ANGLE':   #Additionally converting MCC to degrees format
                        QUANTITY= (180/3.14)*(np.arctan((180/3.14)*QUANTITY*2/25))
                        QUANTITY_BASELINE=(180/3.14)*(np.arctan((180/3.14)*QUANTITY_BASELINE*2/25))
                    if skip==1:
                        pass
                    else:
                        QUANTITY_EXTRACTED_ALL={filename:QUANTITY,filename+'_MINUS_BASELINE':QUANTITY-QUANTITY_BASELINE,'BASELINE':QUANTITY_BASELINE}
                        for figurename in FIG:
                            DATA_PLOTTED_POST_CLICK[figurename][KEY][key]={}
                            AX[figurename].append(FIG[figurename].add_subplot(GS[figurename][l],projection='polar'))
                            Limits,Tick_details=[],[]
                            if key in PLOT_LIMITS: Limits,Tick_details=PLOT_LIMITS[key][0:2],PLOT_LIMITS[key][2:3]
                            if key in PLOT_LIMITS_DELTA and figurename==filename+'_MINUS_BASELINE': Limits,Tick_details=PLOT_LIMITS_DELTA[key][0:2],PLOT_LIMITS_DELTA[key][2:3]
                            polar.pcolormesh_plot(FIG[figurename],AX[figurename][l],key,PSI_AERO,SENSOR_STATION_AERO,QUANTITY_EXTRACTED_ALL[figurename],Limits,Tick_details)
                            DATA_PLOTTED_POST_CLICK[figurename][KEY][key]['Xdata']=PSI_AERO
                            DATA_PLOTTED_POST_CLICK[figurename][KEY][key]['Ydata']=SENSOR_STATION_AERO
                            DATA_PLOTTED_POST_CLICK[figurename][KEY][key]['Zdata']=QUANTITY_EXTRACTED_ALL[figurename]
                            DATA_EXTRACTED_FOR_WIDGETS_PLOT[figurename][KEY][key]=QUANTITY_EXTRACTED_ALL[figurename]    
                    ####    Plotting the wireplots    ####    
                    if DISPLAY_SETTINGS[6]:                                    #if Display_wireplots_also=True 
                        l=l+1
                        if l>=CLICK_FIG_DETAILS[1]*CLICK_FIG_DETAILS[2]:                              #Checking if the grid is full of plots already or not (if it is then further plotting is stopped and the grid size needs to be increased)  
                            for figurename in FIG:    GS[figurename].tight_layout(FIG[figurename])        #Ensures no subplots overlap
                            print('WARNING: It seems you are seeking to plot more results than the grid size allows for. Increase the grid size (using \'Click_grid_rows\' and \'Click_grid_columns\' to see all results!!')
                            return FIG,AX,DATA_PLOTTED_POST_CLICK,DATA_EXTRACTED_FOR_WIDGETS_PLOT,DATA_WIDGETS_COMMON
                        for figurename in FIG:
                            AX[figurename].append(FIG[figurename].add_subplot(GS[figurename][l],projection='3d'))
                            Limits=[]
                            if key in PLOT_LIMITS: Limits=PLOT_LIMITS[key][0:2]
                            if key in PLOT_LIMITS_DELTA and figurename==filename+'_MINUS_BASELINE': Limits=PLOT_LIMITS_DELTA[key][0:2]
                            wireframe.wireframe_plot(FIG[figurename],AX[figurename][l],key,PSI_AERO,SENSOR_STATION_AERO,QUANTITY_EXTRACTED_ALL[figurename],Limits)
            for figurename in FIG:                                
                DATA_WIDGETS_COMMON[figurename][KEY]['SENSOR_STATIONS']=SENSOR_STATION_AERO
                DATA_WIDGETS_COMMON[figurename][KEY]['PSI']=PSI_AERO

                  ####################################################################################################             
                  ####    Any additional desired data (not included in above formats) can be plotted thru this    ####  
                  #################################################################################################### 
        if KEY=='ADDITIONAL_DATA':
            for figurename in FIG: DATA_PLOTTED_POST_CLICK[figurename][KEY]={}
            for Key, Value in VALUE.items():
                if Key=='TRIM_CONTROLS' and Value:     #if the Key is 'TRIM CONTROLS' and there is something in the 'value' associated with (NOTE that this also plots the L/D) 
                    l=l+1
                    if l>=CLICK_FIG_DETAILS[1]*CLICK_FIG_DETAILS[2]:                              #Checking if the grid is full of plots already or not (if it is then further plotting is stopped and the grid size needs to be increased)  
                        for figurename in FIG:    GS[figurename].tight_layout(FIG[figurename])        #Ensures no subplots overlap
                        print('WARNING: It seems you are seeking to plot more results than the grid size allows for. Increase the grid size (using \'Click_grid_rows\' and \'Click_grid_columns\' to see all results!!')
                        return FIG,AX,DATA_PLOTTED_POST_CLICK,DATA_EXTRACTED_FOR_WIDGETS_PLOT,DATA_WIDGETS_COMMON
                    L_by_D=float(SPEED[3]*ROTOR_FORCES_AND_MOMENTS_ALL[12,2]/(ROTOR_POWER_ALL[2,3]))
                    L_by_D_BASELINE=float(SPEED_BASELINE[3]*ROTOR_FORCES_AND_MOMENTS_ALL_BASELINE[12,2]/(ROTOR_POWER_ALL_BASELINE[2,3]))
                    if Value[0]=='PJOINT':
                        TRIM_CONTROLS_AND_LbyD_EXTRACTED_CLICK_FILENAME=TRIM_CONTROLS[Value[0]]
                        TRIM_CONTROLS_AND_LbyD_EXTRACTED_BASELINE=TRIM_CONTROLS_BASELINE[Value[0]]
                    elif Value[0]=='PILOT_INPUT':
                        TRIM_CONTROLS_AND_LbyD_EXTRACTED_CLICK_FILENAME=[TRIM_CONTROLS[Value[0]][0]]       #Collective retains the sign
                        TRIM_CONTROLS_AND_LbyD_EXTRACTED_CLICK_FILENAME.append(-TRIM_CONTROLS[Value[0]][1])#Cyclic angles have opposite sign convention
                        TRIM_CONTROLS_AND_LbyD_EXTRACTED_CLICK_FILENAME.append(-TRIM_CONTROLS[Value[0]][2])
                        TRIM_CONTROLS_AND_LbyD_EXTRACTED_BASELINE=[TRIM_CONTROLS_BASELINE[Value[0]][0]]
                        TRIM_CONTROLS_AND_LbyD_EXTRACTED_BASELINE.append(-TRIM_CONTROLS_BASELINE[Value[0]][1])
                        TRIM_CONTROLS_AND_LbyD_EXTRACTED_BASELINE.append(-TRIM_CONTROLS_BASELINE[Value[0]][2])
                    TRIM_CONTROLS_AND_LbyD_EXTRACTED_CLICK_FILENAME.append(L_by_D)
                    TRIM_CONTROLS_AND_LbyD_EXTRACTED_BASELINE.append(L_by_D_BASELINE)
                    TRIM_CONTROLS_AND_LbyD_EXTRACTED_DELTA=[TRIM_CONTROLS_AND_LbyD_EXTRACTED_CLICK_FILENAME[k]-TRIM_CONTROLS_AND_LbyD_EXTRACTED_BASELINE[k] for k in range(0,len(TRIM_CONTROLS_AND_LbyD_EXTRACTED_CLICK_FILENAME))]
                    TRIM_CONTROLS_AND_LbyD_EXTRACTED_ALL={filename:TRIM_CONTROLS_AND_LbyD_EXTRACTED_CLICK_FILENAME,filename+'_MINUS_BASELINE':TRIM_CONTROLS_AND_LbyD_EXTRACTED_DELTA,'BASELINE':TRIM_CONTROLS_AND_LbyD_EXTRACTED_BASELINE}                           
                    Legend='CII'
                    Ylabel='Magnitude'
                    Xlabel=''
                    for figurename in FIG:
                        Xticklabels=[r'$\theta_{0}$',r'$\theta_{1c}$',r'$\theta_{1s}$','L/D']
                        AX[figurename].append(FIG[figurename].add_subplot(GS[figurename][l]))
                        tuple(Xticklabels)
                        bar.bar_plot(FIG[figurename],AX[figurename][l],'TRIM_ANGLES_and_LbyD',TRIM_CONTROLS_AND_LbyD_EXTRACTED_ALL[figurename],Legend,Ylabel,Xlabel,Xticklabels)
                        DATA_PLOTTED_POST_CLICK[figurename][KEY][Key+'and_L_by_D']=TRIM_CONTROLS_AND_LbyD_EXTRACTED_ALL[figurename] 
                if Key=='PJOINT_HISTORY' and Value:     #if the Key is 'PJOINT_HISTORY' and the value is True 
                    for figurename in FIG: DATA_PLOTTED_POST_CLICK[figurename][KEY][Key]={}
                    l=l+1
                    if l>=CLICK_FIG_DETAILS[1]*CLICK_FIG_DETAILS[2]:                              #Checking if the grid is full of plots already or not (if it is then further plotting is stopped and the grid size needs to be increased)  
                        for figurename in FIG:    GS[figurename].tight_layout(FIG[figurename])        #Ensures no subplots overlap
                        print('WARNING: It seems you are seeking to plot more results than the grid size allows for. Increase the grid size (using \'Click_grid_rows\' and \'Click_grid_columns\' to see all results!!')
                        return FIG,AX,DATA_PLOTTED_POST_CLICK,DATA_EXTRACTED_FOR_WIDGETS_PLOT,DATA_WIDGETS_COMMON
                    
                    PJOINT_HISTORY_EXTRACTED_CLICK_FILENAME=PJOINT_HISTORY
                    PJOINT_HISTORY_EXTRACTED_BASELINE=PJOINT_HISTORY_BASELINE
                    PJOINT_HISTORY_EXTRACTED_DELTA=[theta-theta_baseline for (theta,theta_baseline) in zip(PJOINT_HISTORY,PJOINT_HISTORY_BASELINE)]
                    PJOINT_HISTORY_EXTRACTED_ALL={filename:PJOINT_HISTORY_EXTRACTED_CLICK_FILENAME,filename+'_MINUS_BASELINE':PJOINT_HISTORY_EXTRACTED_DELTA,'BASELINE':PJOINT_HISTORY_EXTRACTED_BASELINE}                           
                    Legend='CII'
                    Ylabel='Pitch [deg]'
                    Xlabel=r'$\psi$'
                    for figurename in FIG:
                        AX[figurename].append(FIG[figurename].add_subplot(GS[figurename][l]))
                        Limits=[]
                        if Key in PLOT_LIMITS: Limits=PLOT_LIMITS[Key][0:2]
                        if Key in PLOT_LIMITS_DELTA and figurename==filename+'_MINUS_BASELINE': Limits=PLOT_LIMITS_DELTA[Key][0:2]
                        xy.xy_plot(FIG[figurename],AX[figurename][l],Key,PSI_BP,PJOINT_HISTORY_EXTRACTED_ALL[figurename],Legend,Xlabel,Ylabel,Limits)
                        DATA_PLOTTED_POST_CLICK[figurename][KEY][Key]['Xdata']=PSI_BP
                        DATA_PLOTTED_POST_CLICK[figurename][KEY][Key]['Ydata']=PJOINT_HISTORY_EXTRACTED_ALL[figurename]
                if Key=='FLAP_DEFLECTION_ANGLE' and Value:  #Quick and dirty, extracting data from info acquired thru AERO_SENSORS
                    for figurename in FIG: DATA_PLOTTED_POST_CLICK[figurename][KEY][Key]={}
                    l=l+1
                    if l>=CLICK_FIG_DETAILS[1]*CLICK_FIG_DETAILS[2]:                              #Checking if the grid is full of plots already or not (if it is then further plotting is stopped and the grid size needs to be increased)  
                        for figurename in FIG:    GS[figurename].tight_layout(FIG[figurename])        #Ensures no subplots overlap
                        print('WARNING: It seems you are seeking to plot more results than the grid size allows for. Increase the grid size (using \'Click_grid_rows\' and \'Click_grid_columns\' to see all results!!')
                        return FIG,AX,DATA_PLOTTED_POST_CLICK,DATA_EXTRACTED_FOR_WIDGETS_PLOT,DATA_WIDGETS_COMMON

                    Legend='CII'
                    Ylabel=r'$\delta$'
                    Xlabel=r'$\psi$'
                    for figurename in FIG:
                        flap_location_index=0
                    
                        for i in range(0,len(DATA_PLOTTED_POST_CLICK[figurename]['AERO_SENSORS'][Key]['Ydata'])):
                            if DATA_PLOTTED_POST_CLICK[figurename]['AERO_SENSORS'][Key]['Zdata'][0,i]!=0:
                                flap_location_index=i
                                break      

                        AX[figurename].append(FIG[figurename].add_subplot(GS[figurename][l]))
                        Limits=[]
                        if Key in PLOT_LIMITS: Limits=PLOT_LIMITS[Key][0:2]
                        if Key in PLOT_LIMITS_DELTA and figurename==filename+'_MINUS_BASELINE': Limits=PLOT_LIMITS_DELTA[Key][0:2]
                        Xdata=DATA_PLOTTED_POST_CLICK[figurename]['AERO_SENSORS'][Key]['Xdata']
                        Ydata=DATA_PLOTTED_POST_CLICK[figurename]['AERO_SENSORS'][Key]['Zdata'][:,flap_location_index]
                        xy.xy_plot(FIG[figurename],AX[figurename][l],Key,Xdata,Ydata,Legend,Xlabel,Ylabel,Limits)
                        DATA_PLOTTED_POST_CLICK[figurename][KEY][Key]['Xdata']=Xdata
                        DATA_PLOTTED_POST_CLICK[figurename][KEY][Key]['Ydata']=Ydata
                    
    for figurename in FIG:    
        GS[figurename].tight_layout(FIG[figurename])        #Ensures no subplots overlap
    return FIG,AX,DATA_PLOTTED_POST_CLICK,DATA_EXTRACTED_FOR_WIDGETS_PLOT,DATA_WIDGETS_COMMON
            
