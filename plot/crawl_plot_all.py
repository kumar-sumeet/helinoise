#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 11:50:55 2019

@author: ge56beh
"""
import matplotlib.pyplot as plt
plt.ioff()
plt.style.use('seaborn')
import os
import pickle
import numpy as np
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from CII import CII_extract_all
from plot import CII_extract_from_click, Polar_plot, Three_D_surface_plot, XY_plot, make_pretty

# plt.rcParams.update(make_pretty.set_font_settings('AIAA_scitech'))
##############################################################################################################################################################################################################################################################################
####################################    Necessary input information    #######################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################
# DIRECTORY_PATH='/home/HT/ge56beh/Work/Python/Acoustics/Data/CII/Camrad_files/bvi/N73_300steps'   #Path to folder that contains ALL the '*.out' files with one case each (NO INTERNAL FOLDER STRUCTURE!!!)
# BASELINE_FILEPATH=DIRECTORY_PATH+'/case5.out'
# Data_dir='/home/HT/ge56beh/Work/AIAA_scitech_data/CII_2P'   #Path to folder that contains ALL the '*.out' files with one case each (NO INTERNAL FOLDER STRUCTURE!!!
# Data_dir='/home/HT/ge56beh/Work/Python/Acoustics/Data/CII/Camrad_files/ibc_cases'   #Path to folder that contains ALL the '*.out' files with one case each (NO INTERNAL FOLDER STRUCTURE!!!
# dir_=[d for d in os.listdir(Data_dir) if 'pckl' not in d.lower() and 'figure'not in d.lower()]
# for d in dir_:
#     if d=='0.00': continue
# DIRECTORY_PATH=f'{Data_dir}/{d}'
# DIRECTORY_PATH='/home/HT/ge56beh/Work/Python/Acoustics/Data/CII/Camrad_files/ibc_cases/0.30_-7.6' 
# BASELINE_FILEPATH=DIRECTORY_PATH+'/Baseline.out'
    
DIRECTORY_PATH='../Data/CII/Camrad_files/best_cases_journal_paper/highres_out'   #Path to folder that contains ALL the '*.out' files with one case each (NO INTERNAL FOLDER STRUCTURE!!!)
BASELINE_FILEPATH=DIRECTORY_PATH+'/baseline_highresAero.out'
# DIRECTORY_PATH='../Data/CII/Camrad_files/best_cases_journal_paper/normalres_out'   #Path to folder that contains ALL the '*.out' files with one case each (NO INTERNAL FOLDER STRUCTURE!!!)
# BASELINE_FILEPATH=DIRECTORY_PATH+'/baseline.out'
# DIRECTORY_PATH='../Data/CII/Camrad_files/mu0.15_diffres/normalres_out'   #Path to folder that contains ALL the '*.out' files with one case each (NO INTERNAL FOLDER STRUCTURE!!!)
# BASELINE_FILEPATH=DIRECTORY_PATH+'/baseline_normalres.out'
# DIRECTORY_PATH='../Data/CII/Camrad_files/mu0.15_diffres/highres_out'   #Path to folder that contains ALL the '*.out' files with one case each (NO INTERNAL FOLDER STRUCTURE!!!)
# BASELINE_FILEPATH=DIRECTORY_PATH+'/baseline_highresAero.out'
# DIRECTORY_PATH='../Data/CII/Camrad_files/mu0.15_diffres/veryhighres_out'   #Path to folder that contains ALL the '*.out' files with one case each (NO INTERNAL FOLDER STRUCTURE!!!)
# BASELINE_FILEPATH=DIRECTORY_PATH+'/baseline_veryhighresAero.out'
# DIRECTORY_PATH='../Data/CII/Camrad_files/best_cases_journal_paper/veryhighres_out'   #Path to folder that contains ALL the '*.out' files with one case each (NO INTERNAL FOLDER STRUCTURE!!!)
# BASELINE_FILEPATH=DIRECTORY_PATH+'/baseline_veryhighresAero.out'
READ_STORED_DATA=False

####################################    Input info corresponding to plots desired after click    #######################################################################################################################################################################################################

#Plot_from_click_HUBLOAD_SENSORS={'NONROT_HUB_FORCE':['UP','AFT','RIGHT'],'NONROT_HUB_FORCE_HARM':['UP','AFT','RIGHT'],'NONROT_HUB_MOM':['ROLL','PITCH','YAW'],'NONROT_HUB_MOM_HARM':['ROLL','PITCH','YAW']}  
Plot_from_click_HUBLOAD_SENSORS={}  
Display_HL_azimuthal=True
Display_HL_harmonics=True
Plot_from_click_BLADELOAD_SENSORS={'TORSION':[],'FLAP':[],'LAG':[],'AXIAL':[],'CHORD':[],'NORM':[]}#Enter radial stations (3 decimal places) at which corresponding bladeload values are desired
Extract_osc_BL=False                #plotted bladeloads for the above sensors (if any) will be with the mean value removed
Plot_BL_individually=True          #plot the bladeloads separately in each subplot
Plot_BL_harmonics=True             #also plot the harmonic contents (in which case each type of bladeload corresponding to each radial location WILL be plotted separately)
Plot_from_click_POSITION_SENSORS={'RIGID_BLADE_PITCH_POLAR':[],'ELASTIC_BLADE_PITCH_POLAR':[],'ELASTIC_TWIST':[]}      #Not congruent with the convention for rest of the sensors but couldn't come up with something better that conformed with a nested dict style!
Plot_from_click_AERO_SENSORS={'WING_FRAME_FORCE_AXIS1':[],'WING_FRAME_FORCE_AXIS2':[82.01],'WING_FRAME_FORCE_AXIS3':[82.02],
                              'FLAP_DEFLECTION_ANGLE':[7.00],'V_IND':[5.00],'CL':[61.00],'CM':[64.00],'CD':[62.00],'P_PROFILE':[93.00],
                              'ALPHA':[25.00],'CL_V_IND_M^2':[61.00,5.20,26.20,26.20],'CL_M^2':[61.00,26.20,26.20],'CM_M^2':[64.00,26.20,26.20],'CD_M^2':[62.00,26.20,26.20],'P_INDUCED':[91.00],          #A quant value of 0 required for radius input; #Enter corresponding aerodynamic sensor QUANT values necessary to calculate the quantity. All entries must be with upto 2  
                              'M':[26.00],'CLbyCD':[61.00,62.30],'R_CL_M^2':[0.00,61.20,26.20,26.20],'R_CM_M^2':[0.00,64.20,26.20,26.20],'R_CD_M^2':[0.00,62.20,26.20,26.20],'P_INDUCED+P_PROFILE':[91.00,93.00]}  #significant digits. First digit is for which operation is being performed on the sensor data corresponding to that quant value. For e.g., 61.00 implies that data associated                                                                                                                                                                                                                   #with QUANT=61 is added to preceding sensor data but since there is a single sensor it implies just a positive quantity.              
# Plot_from_click_AERO_SENSORS={'WING_FRAME_FORCE_AXIS1':[],'WING_FRAME_FORCE_AXIS2':[],'WING_FRAME_FORCE_AXIS3':[],
#                               'FLAP_DEFLECTION_ANGLE':[7.00],'V_IND':[5.00],'CL':[61.00],'CM':[64.00],'CD':[62.00],'P_PROFILE':[93.00],
#                               'ALPHA':[25.00],'CL_V_IND_M^2':[61.00,5.20,26.20,26.20],'CL_M^2':[61.00,26.20,26.20],'CM_M^2':[64.00,26.20,26.20],'CD_M^2':[62.00,26.20,26.20],'P_INDUCED':[91.00],          #A quant value of 0 required for radius input; #Enter corresponding aerodynamic sensor QUANT values necessary to calculate the quantity. All entries must be with upto 2  
#                               'M':[26.00],'CLbyCD':[61.00,62.30],'R_CL_M^2':[0.00,61.20,26.20,26.20],'R_CM_M^2':[0.00,64.20,26.20,26.20],'R_CD_M^2':[0.00,62.20,26.20,26.20],'P_INDUCED+P_PROFILE':[91.00,93.00]}  #significant digits. First digit is for which operation is being performed on the sensor data corresponding to that quant value. For e.g., 61.00 implies that data associated                                                                                                                                                                                                                   #with QUANT=61 is added to preceding sensor data but since there is a single sensor it implies just a positive quantity.              
# Plot_from_click_AERO_SENSORS={'WING_FRAME_FORCE_AXIS1':[],'WING_FRAME_FORCE_AXIS2':[],'WING_FRAME_FORCE_AXIS3':[],
#                               'FLAP_DEFLECTION_ANGLE':[7.00],'V_IND':[],'CL':[],'CM':[],'CD':[],'P_PROFILE':[],
#                               'ALPHA':[],'CL_V_IND_M^2':[],'CL_M^2':[61.00,26.20,26.20],'CM_M^2':[64.00,26.20,26.20],'CD_M^2':[62.00,26.20,26.20],'P_INDUCED':[],          #A quant value of 0 required for radius input; #Enter corresponding aerodynamic sensor QUANT values necessary to calculate the quantity. All entries must be with upto 2  
#                               'M':[],'CLbyCD':[],'R_CL_M^2':[],'R_CM_M^2':[],'R_CD_M^2':[],'P_INDUCED+P_PROFILE':[]}  #significant digits. First digit is for which operation is being performed on the sensor data corresponding to that quant value. For e.g., 61.00 implies that data associated                                                                                                                                                                                                                   #with QUANT=61 is added to preceding sensor data but since there is a single sensor it implies just a positive quantity.              
Plot_from_click_additional_data={'TRIM_CONTROLS':[],'PJOINT_HISTORY':True,'FLAP_DEFLECTION_ANGLE':False}      #Include any additional data that needs to be plotted
#First two entries are the axis limits, the third entry correspond to the suitable power of 10 that is desired for display of tick labels (currently only being used for polar plot colobars display))
# third entry tick_details is causing errors (fix it later!!!)
PLOT_LIMITS={'NONROT_HUB_FORCE':{'UP':[],'AFT':[],'RIGHT':[]},'NONROT_HUB_FORCE_HARM':{'UP':[],'RIGHT':[],'AFT':[]},'NONROT_HUB_MOM':{'ROLL':[],'PITCH':[],'YAW':[]},'NONROT_HUB_MOM_HARM':{'ROLL':[],'PITCH':[],'YAW':[]},
          'TORSION':[],'FLAP':[],'LAG':[],'AXIAL':[],'CHORD':[],'NORM':[],'RIGID_BLADE_PITCH_POLAR':[-5,15],'ELASTIC_BLADE_PITCH_POLAR':[-2,15],'ELASTIC_TWIST':[],'WING_FRAME_FORCE_AXIS1':[],'WING_FRAME_FORCE_AXIS2':[],'WING_FRAME_FORCE_AXIS3':[],
          'FLAP_DEFLECTION_ANGLE':[],'V_IND':[],'CL':[-0.5,1.5],'CM':[-0.05,0.01],'CD':[0,0.04],'P_PROFILE':[],
          'ALPHA':[-8,20],'CL_V_IND_M^2':[],'CL_M^2':[-0.1,0.25],'CM_M^2':[-0.013,0.0],'CD_M^2':[0.0,0.01],'P_INDUCED':[],
          'M':[],'CLbyCD':[-50,120],'R_CL_M^2':[],'R_CM_M^2':[],'R_CD_M^2':[],'P_INDUCED+P_PROFILE':[],'PJOINT_HISTORY':[]}        
PLOT_LIMITS_DELTA={'NONROT_HUB_FORCE':{'UP':[],'AFT':[],'RIGHT':[]},'NONROT_HUB_FORCE_HARM':{'UP':[],'RIGHT':[],'AFT':[]},'NONROT_HUB_MOM':{'ROLL':[],'PITCH':[],'YAW':[]},'NONROT_HUB_MOM_HARM':{'ROLL':[],'PITCH':[],'YAW':[]},
          'TORSION':[],'FLAP':[],'LAG':[],'AXIAL':[],'CHORD':[],'NORM':[],'RIGID_BLADE_PITCH_POLAR':[-2,2],'ELASTIC_BLADE_PITCH_POLAR':[-2,2],'ELASTIC_TWIST':[-7,2],'WING_FRAME_FORCE_AXIS1':[],'WING_FRAME_FORCE_AXIS2':[],'WING_FRAME_FORCE_AXIS3':[],
          'FLAP_DEFLECTION_ANGLE':[],'V_IND':[-3,3],'CL':[-0.4,0.5],'CM':[-0.15,0.05],'CD':[-0.1,0.03],'P_PROFILE':[-10000,20000],
          'ALPHA':[-3,3],'CL_V_IND_M^2':[-1,0.5],'CL_M^2':[-0.05,0.05],'CM_M^2':[-0.003,0.003],'CD_M^2':[-0.003,0.005],'P_INDUCED':[-5000,15000],
          'M':[],'CLbyCD':[-20,20],'R_CL_M^2':[-0.08,0.08],'R_CM_M^2':[],'R_CD_M^2':[0,0.010],'P_INDUCED+P_PROFILE':[-40000,40000],'PJOINT_HISTORY':[]}        #Setting limits for each plot of each of the 'key' quantities in the 'DELTA' figure
LABELS={'NONROT_HUB_FORCE':'HUB_FORCE (N)','NONROT_HUB_FORCE_HARM':'HUB_FORCE (N)','NONROT_HUB_MOM':'HUB_MOMENT (N-m)','NONROT_HUB_MOM_HARM':'HUB_MOMENT (N-m)',
          'TORSION':'Torsion (N-m)','FLAP':'Flap Bending Moment (N-m)','LAG':'Lag Bending Moment (N-m)','AXIAL':'Axial Force (N)','CHORD':'Chordwise Force (N)','NORM':'Normal Force (N)','RIGID_BLADE_PITCH_POLAR':'RIGID BLADE PITCH POLAR','ELASTIC_BLADE_PITCH_POLAR':'ELASTIC BLADE PITCH POLAR','ELASTIC_TWIST':r'$\theta_{tw}$ [deg]',
          'WING_FRAME_FORCE_AXIS1':'WING FRAME FORCE AXIS1','WING_FRAME_FORCE_AXIS2':'WING FRAME FORCE AXIS2','WING_FRAME_FORCE_AXIS3':'WING FRAME FORCE AXIS3',
          'FLAP_DEFLECTION_ANGLE':r'$\delta$ [deg]','V_IND':r'$V_{ind}$'+'[m/s]','CL':r'$C_l$','CM':r'$C_m$','CD':r'$C_d$','P_PROFILE':'Profile Power [N-m/s/m]',
          'ALPHA':r'$\alpha$ [deg]','CL_V_IND_M^2':r'$C_lV_{ind}M^2$','CL_M^2':r'$C_lM^2$','CM_M^2':r'$C_mM^2$','CD_M^2':r'$C_dM^2$','P_INDUCED':'Induced Power [N-m/s/m]',
          'M':'Mach Number','CLbyCD':r'$C_l/C_d$','R_CL_M^2':r'$RC_lM^2$','R_CM_M^2':r'$RC_mM^2$','R_CD_M^2':r'$RC_dM^2$','P_INDUCED+P_PROFILE':r'$P_{ind}+P_{prof}$',
          'PJOINT_HISTORY':r'$\theta$ [deg]'}        #First two entries are the axis limits, the third entry correspond to the suitable power of 10 that is desired for display of tick labels (currently only being used for polar plot colobars display))

Display_data_fig=True            #if a figure with data corresponding to the file clicked on is desired
Display_delta_fig=True          #if simultaneously a figure with change in values compared to the Baseline (delta changes) is desired
Display_baseline_fig=False        #if simultaneously a figure with corresponding baseline data is desired
Display_wireplots_also=False      #plots 3D wireplots for each polar plot plotted
QUANTITIES_TO_BE_PLOTTED={'HUBLOAD_SENSORS':Plot_from_click_HUBLOAD_SENSORS,'LOAD_SENSORS':Plot_from_click_BLADELOAD_SENSORS,'POSITION_SENSORS':Plot_from_click_POSITION_SENSORS,'AERO_SENSORS':Plot_from_click_AERO_SENSORS,'ADDITIONAL_DATA':Plot_from_click_additional_data}   

Click_fig_size=(18.5,10)
Click_grid_rows=4
Click_grid_columns=7             #Need to make sure that the grid size is sufficient for the number of plots desired post-click  
CLICK_FIG_DETAILS=[Click_fig_size,Click_grid_rows,Click_grid_columns]

####################################    Input info corresponding to widgets plot    #######################################################################################################################################################################################################

Display_plot_with_widgets=False                                                #Displays the widget plot
Display_data_widgets=Display_data_fig                                          #Displays data correpsonding to file clicked on
Display_delta_widgets=Display_delta_fig                                        #Displays the delta results
Display_baseline_widgets=Display_baseline_fig                                  #Displays the baseline results in the widget plot
Widgets_fig_size=(18.5,10)    #WARNING: changing the figure size might make the buttons a bit skewed
Display_as_subplots=True      #Subplots in widget figure  
Display_all_clicks_combined=False#All keys corresponding to DATA_CLICK (after more than one files have been selected from single click or multiple clicks) are plotted together in their respective category of figure subplot 
WIDGETS_FIG_DETAILS=[Widgets_fig_size]
SET_DEFAULT_QUANTITIES={'LOAD_SENSORS':'TORSION','POSITION_SENSORS':'ELASTIC_TWIST','AERO_SENSORS':'ALPHA'}

####################################    Input info corresponding to saving plots    #######################################################################################################################################################################################################
SAVE_AS_FIG_POLAR={}
SAVE_AS_FIG_SURFACE={}
SAVE_AS_FIG_XY={}
SAVE_ENTIRE_FIGURE=False
SAVE_FIGURES_POLAR=True
SAVE_FIGURES_SURFACE=False
SAVE_FIGURES_XY=False

#dictionary of all plots to be saved based on input in QUANTITIES_TO_BE_PLOTTED (NOTE:: if CLICK_FIG_DETAILS are insufficient to plot all quantities then an error would reult here since saving all figures depends on data already plotted by CII_extract_from_click. 'save_figures_polar/surface' will try to access data that is not even returned by CII_extract_from_click) 
SAVE_AS_FIG_POLAR['AERO_SENSORS']=[]
SAVE_AS_FIG_SURFACE['AERO_SENSORS']=[]
for key,value in Plot_from_click_AERO_SENSORS.items():  
    if value: 
        SAVE_AS_FIG_POLAR['AERO_SENSORS'].append(key) 
        SAVE_AS_FIG_SURFACE['AERO_SENSORS'].append(key)
SAVE_AS_FIG_POLAR['POSITION_SENSORS']=[]
SAVE_AS_FIG_SURFACE['POSITION_SENSORS']=[]
for key,value in Plot_from_click_POSITION_SENSORS.items():
    if value: 
        SAVE_AS_FIG_POLAR['POSITION_SENSORS'].append(key) 
        SAVE_AS_FIG_SURFACE['POSITION_SENSORS'].append(key) 
             
#Alternately, the quantities can be explicitly given
#SAVE_AS_FIG_POLAR={'AERO_SENSORS':['CLbyCD','P_INDUCED+P_PROFILE','ALPHA','CL_M^2','CM','FLAP_DEFLECTION_ANGLE'],'POSITION_SENSORS':['ELASTIC_TWIST']}        
#SAVE_AS_FIG_POLAR={'AERO_SENSORS':['ALPHA','CL_M^2'],'POSITION_SENSORS':['ELASTIC_TWIST']}        
#SAVE_AS_FIG_POLAR={'AERO_SENSORS':['FLAP_DEFLECTION_ANGLE']}        
#SAVE_AS_FIG_SURFACE={'AERO_SENSORS':['CLbyCD','P_INDUCED+P_PROFILE','ALPHA','CL_M^2','CM','FLAP_DEFLECTION_ANGLE'],'POSITION_SENSORS':['ELASTIC_TWIST']}             
SAVE_AS_FIG_XY={'ADDITIONAL_DATA':['PJOINT_HISTORY','FLAP_DEFLECTION_ANGLE']}

# SAVE_AS_FIG_XY_TOGETHER={'PJOINT_HISTORY':['1P+2P','Baseline']}
SAVE_AS_FIG_XY_TOGETHER={}
##############################################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################
DISPLAY_SETTINGS = [Extract_osc_BL,Display_data_fig,Display_delta_fig,Display_baseline_fig,Plot_BL_harmonics,Plot_BL_individually,Display_wireplots_also]  #Organising all the display settings of figure after click
DISPLAY_SETTINGS_WIDGETS=[Display_plot_with_widgets,Display_data_widgets,Display_delta_widgets,Display_baseline_widgets,Display_as_subplots,Display_all_clicks_combined]

#Creating a tuple containing all the output extracted from output file of the baseline case
DATA_EXTRACTED_BASELINE = CII_extract_all.cii_extract_all(BASELINE_FILEPATH)   #Extracting data for the baseline case (single file) only

#Creating the 'Saved_figures' folder if it doesn't already exist
DIRECTORY_SAVE_PLOTS=DIRECTORY_PATH+'/Saved_figures'
try:
    os.makedirs(DIRECTORY_SAVE_PLOTS)
except FileExistsError:
    pass                # directory already exists                   

                    ###########################################################################################
                    #########   Extracting filenames and filepaths from DIRECTORY_PATH provided  ##############
                    ###########################################################################################    
ALL_FILE_PATHS=[]                                                              #List of complete file paths to each '.out' file
ALL_FILE_NAMES=[]
for root, dir, allfilenames in os.walk(DIRECTORY_PATH):
    for filename in allfilenames:
        if ".out" in filename:
            ALL_FILE_PATHS.append(DIRECTORY_PATH+'/'+filename)                 #List of file paths
            ALL_FILE_NAMES.append(filename.split('.out')[0])


        ##############################################################################################################
        #########   Creating a dictionary with filenames as 'keys' and extracted data tuple as 'value'  ##############
        ##############################################################################################################
        
if READ_STORED_DATA:
    with open(DIRECTORY_PATH+'/Stored_ALL_DATA_DICT.pckl', 'rb') as f:
        ALL_DATA_DICT = pickle.load(f)
    print('NOTE-- READING FROM STORED DATA!!!')
else:    
    ALL_DATA_DICT={}                                                               #Empty dictionary
    for count, FILE_PATH in enumerate(ALL_FILE_PATHS,1):
        FILENAME=ALL_FILE_NAMES[ALL_FILE_PATHS.index(FILE_PATH)]
        f=open(FILE_PATH)    
        Data_extracted_each_case = CII_extract_all.cii_extract_all(FILE_PATH)  
        print('\r READING ALL FILES: ',int(100*count/len(ALL_FILE_PATHS)),'% COMPLETE', end='')
        ALL_DATA_DICT[FILENAME]=Data_extracted_each_case                           #Dictionary: key-->filenames; values--> tuple of all extracted data from the corresponding output file
    with open(DIRECTORY_PATH+'/Stored_ALL_DATA_DICT.pckl', 'wb') as f:
        pickle.dump(ALL_DATA_DICT, f)
        
print('')       #This is needed to get newline after the print statement in the above loop    

        #######################################################################################################        
        ######      Saving desired subplots as separate figures with the subplot title as figure name   #######
        #######################################################################################################    

def save_figures_polar(FIG_CLICK,AX_CLICK,DATA_CLICK):
    # print(d)
    print('Saving Polar Figures for:')
    for fig in FIG_CLICK:
        print(fig)
        for key,value in SAVE_AS_FIG_POLAR.items():
            if value:
                for quantity_to_save in value: 
                    xdata=DATA_CLICK[fig][key][quantity_to_save]['Xdata']
                    ydata=DATA_CLICK[fig][key][quantity_to_save]['Ydata']
                    zdata=DATA_CLICK[fig][key][quantity_to_save]['Zdata']
                    title=quantity_to_save
                    limits,tick_details=PLOT_LIMITS[quantity_to_save][0:2],PLOT_LIMITS[quantity_to_save][2:3]
                    if quantity_to_save in PLOT_LIMITS_DELTA and '_MINUS_BASELINE' in fig: limits,tick_details=PLOT_LIMITS_DELTA[quantity_to_save][0:2],PLOT_LIMITS_DELTA[quantity_to_save][2:3]
                    if title=='P_INDUCED+P_PROFILE': tick_details=[4]
                    Directory_save_file_to_polar=DIRECTORY_SAVE_PLOTS+'/'+'Polar_plots'+'/'+fig
                    try:
                        os.makedirs(Directory_save_file_to_polar)
                        # Polar_plot.save_this_subplot_as_fig(title,xdata,ydata,zdata,limits,tick_details,Directory_save_file_to_polar,LABELS[title])                            
                    except FileExistsError:
                        pass                # directory already exists    
                    # if Path(f'{Directory_save_file_to_polar}/{title}.png').is_file() or Path(f'{Directory_save_file_to_polar}/{title}.pdf').is_file():
                    #     continue
                    Polar_plot.save_this_subplot_as_fig(title,xdata,ydata,zdata,limits,tick_details,Directory_save_file_to_polar,LABELS[title])
            else:
                continue
            
def save_figures_surface(FIG_CLICK,AX_CLICK,DATA_CLICK):
    print('\n\n\n ')
    # print(d)
    print('Saving Surface Figures')
    for fig in FIG_CLICK:
        print(fig)
        for key,value in SAVE_AS_FIG_SURFACE.items():
            if value:
                for quantity_to_save in value: 
                    xdata=DATA_CLICK[fig][key][quantity_to_save]['Xdata']
                    ydata=DATA_CLICK[fig][key][quantity_to_save]['Ydata']
                    zdata=DATA_CLICK[fig][key][quantity_to_save]['Zdata']
                    title=quantity_to_save
                    limits,tick_details=PLOT_LIMITS[quantity_to_save][0:2],PLOT_LIMITS[quantity_to_save][2:3]
                    if quantity_to_save in PLOT_LIMITS_DELTA and '_MINUS_BASELINE' in fig: limits,tick_details=PLOT_LIMITS_DELTA[quantity_to_save][0:2],PLOT_LIMITS_DELTA[quantity_to_save][2:3]
                    Directory_save_file_to_surface=DIRECTORY_SAVE_PLOTS+'/'+'Surface_plots'+'/'+fig
                    try:
                        os.makedirs(Directory_save_file_to_surface)
                    except FileExistsError:
                        pass                # directory already exists                   
                    Three_D_surface_plot.save_this_subplot_as_fig(title,xdata,ydata,zdata,limits,tick_details,Directory_save_file_to_surface,LABELS[title])
            else:
                continue

def save_figures_xy(FIG_CLICK,AX_CLICK,DATA_CLICK):
    print('\n\n\n ')
    print('Saving XY Figures')
    for fig in FIG_CLICK:
        print(fig)
        for key,value in SAVE_AS_FIG_XY.items():
            if value: 
                for quantity_to_save in value: 
                    xdata=DATA_CLICK[fig][key][quantity_to_save]['Xdata']
                    ydata=DATA_CLICK[fig][key][quantity_to_save]['Ydata']
                    title=quantity_to_save
                    limits=PLOT_LIMITS[quantity_to_save][0:2]
                    if quantity_to_save in PLOT_LIMITS_DELTA and '_MINUS_BASELINE' in fig: limits=PLOT_LIMITS_DELTA[quantity_to_save][0:2]
                    Directory_save_file_to_xy=DIRECTORY_SAVE_PLOTS+'/'+'XY_plots'+'/'+fig
                    try:
                        os.makedirs(Directory_save_file_to_xy)
                    except FileExistsError:
                        pass                # directory already exists                   
                    XY_plot.save_this_subplot_as_fig_2(title,xdata,ydata,limits,Directory_save_file_to_xy,LABELS[title])
            else:
                continue

                            
for best_case_file in ALL_FILE_NAMES:
    ####    Plotting QUANTITIES_TO_BE_PLOTTED corresponding to CLICK_FILENAME and other files based on DISPLAY_SETTINGS    ####
    All_info_returned_from_click = CII_extract_from_click.cii_extract_from_click(best_case_file,ALL_DATA_DICT,DATA_EXTRACTED_BASELINE,QUANTITIES_TO_BE_PLOTTED,PLOT_LIMITS,PLOT_LIMITS_DELTA,DISPLAY_SETTINGS,CLICK_FIG_DETAILS)
    #storing all the information returned post-click categorically for verification or saving specific plots later   
    FIG_CLICK=All_info_returned_from_click[0]
    AX_CLICK=All_info_returned_from_click[1]
    DATA_CLICK=All_info_returned_from_click[2]
    print('\n\n\n ')         
    for fig in FIG_CLICK:                               
        if SAVE_ENTIRE_FIGURE:
            print('Saving Figure:', fig)
            FIG_CLICK[fig].savefig(DIRECTORY_SAVE_PLOTS+'/'+fig, format='png')
        plt.close(FIG_CLICK[fig]) 
    print('\n\n\n ')
    if  SAVE_FIGURES_POLAR: save_figures_polar(FIG_CLICK,AX_CLICK,DATA_CLICK)     
    if SAVE_FIGURES_SURFACE: save_figures_surface(FIG_CLICK,AX_CLICK,DATA_CLICK)
    if SAVE_FIGURES_XY: save_figures_xy(FIG_CLICK,AX_CLICK,DATA_CLICK)



############################################    Plotting together    ##############################################
Axislabel_size=17
Ticklabel_size=13
Legend_size=15

def save_figures_xy_together(Xdata,Ydata,Label):
    global Ax
    XY_plot.save_as_fig_together(Ax,Xdata,Ydata,Label)
    
for plot_together_quant in SAVE_AS_FIG_XY_TOGETHER:
    Figure_name=plot_together_quant
    Fig = plt.figure()
    Ax = Fig.add_subplot(1,1,1)
    ylabel=LABELS[plot_together_quant]
    xdata,ydata={},{}
    for filename in ALL_DATA_DICT:  
        label=filename.split('_')[0]
        TIME_STEP=ALL_DATA_DICT[filename]['TIME_STEP']
        xdata[label]=(np.arange(0,360+360.0/TIME_STEP[3],360.0/TIME_STEP[3])).tolist()
        ydata[label]=ALL_DATA_DICT[filename][plot_together_quant]
    for value in SAVE_AS_FIG_XY_TOGETHER[plot_together_quant]: 
        save_figures_xy_together(xdata[value],ydata[value],value)        
    Ax.legend(frameon=False, prop={'size': Legend_size})
    Ax.set_xlabel(r'$\psi$',fontsize=Axislabel_size)
    if '[deg]' in  ylabel:    
        y_ticks = Ax.get_yticks()
        y_ticks_labels=[str(tick)+r"$\degree$" for tick in y_ticks]
        #Ax.set_yticks()
        #Ax.set_yticklabels(y_ticks_labels)
        plt.yticks(y_ticks,y_ticks_labels)
        ylabel=ylabel.replace(' [deg]','')    #removing '[deg]' from colorbar label    
    Ax.set_ylabel(ylabel, fontsize=Axislabel_size)    
    plt.grid(True)
    if PLOT_LIMITS[plot_together_quant]: Ax.set_ylim(PLOT_LIMITS[plot_together_quant][0],PLOT_LIMITS[plot_together_quant][1])
    Ax.tick_params(axis='both', labelsize=Ticklabel_size)
    Directory_save_file_to_xy_together=DIRECTORY_SAVE_PLOTS+'/'+'XY_plots_together'
    try:
        os.makedirs(Directory_save_file_to_xy_together)
    except FileExistsError:
        pass                # directory already exists                   
    Fig.savefig(Directory_save_file_to_xy_together+'/'+Figure_name+'.png', bbox_inches='tight')
    print('saved: ', Figure_name)
    plt.close(Fig)


####################################################################################################################################
