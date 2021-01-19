#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 12:24:19 2020

@author: ge56beh
"""
import math
import numpy as np
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec
from shutil import copy

from matplotlib.legend_handler import HandlerTuple
from mpl_toolkits.mplot3d import Axes3D
plt.ioff()

# plt.style.use('seaborn')
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from plot import Scatter_plot,make_pretty
from utl import crawler,cii
plt.rcParams.update(make_pretty.set_font_settings('AIAA_scitech'))
# from tecplot import read_wopwop_tecfile

freq='2P'
Data_dir = f'/home/HT/ge56beh/Work/AIAA_scitech_data/CII_{freq}'
All_filepath_dict,All_filenames_dict = crawler.get_files_info(Data_dir)
All_data_dict = crawler.get_cii_output(Data_dir,All_filepath_dict,All_filenames_dict,Read_pckl=True)
Vib_power_dict = cii.vib_power(All_data_dict)
J_baseline=math.sqrt(6)
J_Mz_baseline=math.sqrt(5)


WOPWOP_data_dir=f'/home/HT/ge56beh/Work/AIAA_scitech_data/PSU_WOPWOP/{freq}/out_of_plane'
All_folderpath_dict,All_foldernames_dict = crawler.get_wopwop_files_info(WOPWOP_data_dir)
All_data_dict_wopwop = crawler.get_wopwop_output(WOPWOP_data_dir,All_folderpath_dict,All_foldernames_dict,Read_pckl=True)
Vib_power_noise_dict=Vib_power_dict.copy()
for mu,filenames in Vib_power_dict.items():
    for filename in filenames:       
        Vib_power_noise_dict[mu][filename]['OASPL-A']=All_data_dict_wopwop[mu][filename][0][3]
        Vib_power_noise_dict[mu][filename]['delta_OASPL-A%']=(All_data_dict_wopwop[mu][filename][0][3]-All_data_dict_wopwop[mu]['Baseline'][0][3])*100/All_data_dict_wopwop[mu]['Baseline'][0][3]
        Vib_power_noise_dict[mu][filename]['delta_OASPL-A']=All_data_dict_wopwop[mu][filename][0][3]-All_data_dict_wopwop[mu]['Baseline'][0][3]

delta_cp=[]
for filename in Vib_power_dict['0.05']:
    delta_cp.append(Vib_power_dict['0.05'][filename]['delta_CP%'])



Best_cases_dict={}
Best_cases_dict_onlyone={}
Best_cases_dict_overall={}
Best_phases_dict_onlyone={}
split_idx={'1P':3,'2P':5}
for idx,subdir in enumerate(Vib_power_noise_dict):
    try: os.makedirs(f'{Data_dir}/figures/best_cases_onlyone')
    except FileExistsError: pass                # directory already exists                   
    try: os.makedirs(f'{Data_dir}/figures/best_cases_overall')
    except FileExistsError: pass                # directory already exists                   
    try: os.makedirs(f'{Data_dir}/figures/baseline_results')
    except FileExistsError: pass                # directory already exists                   
    # copy(f'{Data_dir}/{subdir}/Saved_figures/Polar_plots/Baseline/CD_M^2.png', f'{Data_dir}/figures/baseline_results/')
    # os.rename(f'{Data_dir}/figures/baseline_results/CD_M^2.png', f'{Data_dir}/figures/baseline_results/CD_{subdir}')
    # copy(f'{Data_dir}/{subdir}/Saved_figures/Polar_plots/Baseline/CL_M^2.png', f'{Data_dir}/figures/baseline_results/')
    # os.rename(f'{Data_dir}/figures/baseline_results/CL_M^2.png', f'{Data_dir}/figures/baseline_results/CL_{subdir}')

    Best_cases_dict_onlyone[subdir]={'OASPL-A':[],'CP':[],'J':[]}
    Best_cases_dict_overall[subdir]=[]
    phases_dict={'OASPL-A':[],'CP':[],'J':[]}
    for filename,data_dict in Vib_power_noise_dict[subdir].items():
        if data_dict['delta_OASPL-A']<0:
            try: os.makedirs(f'{Data_dir}/figures/best_cases_onlyone/OASPL-A')
            except FileExistsError: pass                # directory already exists                   
            # copy(f'{Data_dir}/{subdir}/Saved_figures/Polar_plots/{filename}_MINUS_BASELINE/CD_M^2.png', f'{Data_dir}/figures/best_cases_onlyone/OASPL-A/')
            # os.rename(f'{Data_dir}/figures/best_cases_onlyone/OASPL-A/CD_M^2.png', f'{Data_dir}/figures/best_cases_onlyone/OASPL-A/CD_{subdir}_{filename}')
            # copy(f'{Data_dir}/{subdir}/Saved_figures/Polar_plots/{filename}_MINUS_BASELINE/CL_M^2.png', f'{Data_dir}/figures/best_cases_onlyone/OASPL-A/')
            # os.rename(f'{Data_dir}/figures/best_cases_onlyone/OASPL-A/CL_M^2.png', f'{Data_dir}/figures/best_cases_onlyone/OASPL-A/CL_{subdir}_{filename}')
            if Vib_power_noise_dict[subdir][filename]['CP']<Vib_power_noise_dict[subdir]['Baseline']['CP']:
                if Vib_power_noise_dict[subdir][filename]['J']<Vib_power_noise_dict[subdir]['Baseline']['J']:
                    Best_cases_dict_overall[subdir].append(filename)
                    # copy(f'{Data_dir}/{subdir}/Saved_figures/Polar_plots/{filename}_MINUS_BASELINE/CD_M^2.png', f'{Data_dir}/figures/best_cases_overall/')
                    # os.rename(f'{Data_dir}/figures/best_cases_overall/CD_M^2.png', f'{Data_dir}/figures/best_cases_overall/CD_{subdir}_{filename}')
                    # copy(f'{Data_dir}/{subdir}/Saved_figures/Polar_plots/{filename}_MINUS_BASELINE/CL_M^2.png', f'{Data_dir}/figures/best_cases_overall')
                    # os.rename(f'{Data_dir}/figures/best_cases_overall/CL_M^2.png', f'{Data_dir}/figures/best_cases_overall/CL_{subdir}_{filename}')
            Best_cases_dict_onlyone[subdir]['OASPL-A'].append(filename)
            phases_dict['OASPL-A'].append(float(filename.split('_')[split_idx[freq]]))
        if Vib_power_noise_dict[subdir][filename]['CP']<Vib_power_noise_dict[subdir]['Baseline']['CP']:
            try: os.makedirs(f'{Data_dir}/figures/best_cases_onlyone/CP')
            except FileExistsError: pass                # directory already exists                   
            # copy(f'{Data_dir}/{subdir}/Saved_figures/Polar_plots/{filename}_MINUS_BASELINE/CD_M^2.png', f'{Data_dir}/figures/best_cases_onlyone/CP/')
            # os.rename(f'{Data_dir}/figures/best_cases_onlyone/CP/CD_M^2.png', f'{Data_dir}/figures/best_cases_onlyone/CP/CD_{subdir}_{filename}')
            # copy(f'{Data_dir}/{subdir}/Saved_figures/Polar_plots/{filename}_MINUS_BASELINE/CL_M^2.png', f'{Data_dir}/figures/best_cases_onlyone/CP/')
            # os.rename(f'{Data_dir}/figures/best_cases_onlyone/CP/CL_M^2.png', f'{Data_dir}/figures/best_cases_onlyone/CP/CL_{subdir}_{filename}')
            Best_cases_dict_onlyone[subdir]['CP'].append(filename)
            phases_dict['CP'].append(float(filename.split('_')[split_idx[freq]]))
        if Vib_power_noise_dict[subdir][filename]['J']<Vib_power_noise_dict[subdir]['Baseline']['J']:
            try: os.makedirs(f'{Data_dir}/figures/best_cases_onlyone/J')
            except FileExistsError: pass                # directory already exists                   
            # copy(f'{Data_dir}/{subdir}/Saved_figures/Polar_plots/{filename}_MINUS_BASELINE/CD_M^2.png', f'{Data_dir}/figures/best_cases_onlyone/J/')
            # os.rename(f'{Data_dir}/figures/best_cases_onlyone/J/CD_M^2.png', f'{Data_dir}/figures/best_cases_onlyone/J/CD_{subdir}_{filename}')
            # copy(f'{Data_dir}/{subdir}/Saved_figures/Polar_plots/{filename}_MINUS_BASELINE/CL_M^2.png', f'{Data_dir}/figures/best_cases_onlyone/J/')
            # os.rename(f'{Data_dir}/figures/best_cases_onlyone/J/CL_M^2.png', f'{Data_dir}/figures/best_cases_onlyone/J/CL_{subdir}_{filename}')
            Best_cases_dict_onlyone[subdir]['J'].append(filename)
            phases_dict['J'].append(float(filename.split('_')[split_idx[freq]]))
    Best_phases_dict_onlyone[subdir]={'OASPL-A':set(phases_dict['OASPL-A']),'CP':set(phases_dict['CP']),'J':set(phases_dict['J'])}
           
DIRECTORY_SAVE_PLOTS=Data_dir+'/figures'
YLABELS={'mu':r'$\mu$','CP':r'$C_P$','P':r'$P_{HP}$','CPS':r'$C_P/\sigma$',
         'Fx':r'$F_X$ [N]','Fy':r'$F_Y$ [N]','Fz':r'$F_Z$ [N]',
         'Mx':r'$M_X$ [Nm]','My':r'$M_Y$ [Nm]','Mz':r'$M_Z$ [Nm]',
          'In-plane Hub Moment': 'Hub Moment','Hub Shear':'Hub Shear',
          'J':r'$J$','J_Mz':r'$J+Mz$',
          'Torsion':'Torsion Bending Moment [Nm]','Flap':'Flap Bending Moment [Nm]','Lag':'Lag Bending Moment [Nm]',
          'Axial':'Axial Tension Force [N]','Chord':'Chordwise Shear Force [N]','Norm':'Flapwise Shear Force [N]',
          'OASPL-A':'OASPL-A [dB]','delta_CP%':r'$\Delta C_P [\%]$','delta_J%':r'$\Delta J [\%]$','delta_OASPL-A':r'$\Delta dB$'}
Limits={'mu':[0,0.4],'Fx':[],'Fy':[],'Fz':[],'Mx':[],'My':[],'Mz':[],'In-plane Hub Moment': [],'In-plane Hub Shear':[],
        'Torsion':[-300,400],'Flap':[],'Lag':[],'Axial':[],'Chord':[],'Norm':[-400,450],'Delta_Torsion':[-250,150],
        'Delta_Flap':[],'Delta_Lag':[],'Delta_Axial':[],'Delta_Chord':[],'Delta_Norm':[],'J_Mz':[0,10],
        
        'CP':[0.00025,0.00065],'J':[0,4],
        'OASPL-A':[45,80],'delta_CP%':[-6,2],'delta_J%':[-60,200],'delta_OASPL-A':[-15,10]}
COLORS=['cyan','darkorange','lightseagreen','purple','blue','red','green','gold','burlywood', 'plum','dimgray','dodgerblue','teal', 'lightblue', 'peru','greenyellow'] # CHOOSE FROM THIS LIST obtained from--> https://matplotlib.org/gallery/color/named_colors.html

try:
    os.makedirs(DIRECTORY_SAVE_PLOTS)
except FileExistsError:
    pass                # directory already exists                   

# if SAVE_AS_SCATTER:
#     Scatter_plot.save_this_subplot_as_fig(DIRECTORY_SAVE_PLOTS)

Mu_list=[float(subdir) for subdir in Vib_power_noise_dict]
Baseline_CP_list=[Vib_power_noise_dict[subdir]['Baseline']['CP'] for subdir in Vib_power_noise_dict]
Baseline_J_list=[Vib_power_noise_dict[subdir]['Baseline']['J'] for subdir in Vib_power_noise_dict]

def plot_scatter(Fig,Ax,Vib_power_noise_dict,x,y,z,Labels,plot_tef=True):
    Best_cases_dict={}
    figname=f'{y}_{x}_{z}'
    figname=figname.replace("%", "perc")
    for idx,subdir in enumerate(Vib_power_noise_dict):
        Best_cases_dict[subdir]=[]
        Ax_tef = Fig_tef.add_subplot(Gs_tef[idx])
        # print(subdir)
        #Ax.axhline(y=Vib_power_dict[subdir]['Baseline']['CP'], color=COLORS[idx], linestyle='--', linewidth=2.0)
        for filename,data_dict in Vib_power_noise_dict[subdir].items():
            # if noise_lst[0][3]>All_data_dict_wopwop[subdir]['Baseline'][0][3]: 
            if data_dict[y]>Vib_power_noise_dict[subdir]['Baseline'][y]: 
                if noise_lst[0][3]<=All_data_dict_wopwop[subdir]['Baseline'][0][3] and Vib_power_dict[subdir][filename]['delta_CP%']<Vib_power_dict[subdir]['Baseline']['delta_CP%']:
                    p_1 = Ax.scatter(Vib_power_dict[subdir][filename]['J'], noise_lst[0][3], c=COLORS[idx], marker='+')
            else:
                if noise_lst[0][3]<All_data_dict_wopwop[subdir]['Baseline'][0][3] and Vib_power_dict[subdir][filename]['J']<Vib_power_dict[subdir]['Baseline']['J']:
                    Best_cases_dict[subdir].append(filename)
                    azimuth, tef_deflection = cii.get_tef_deflection(All_data_dict[subdir][filename])
                    Ax.plot(Ax_tef,azimuth,tef_deflection,color=COLORS[idx])
                    # Ax_tef.plot(All_data_dict[subdir][filename])
                    p_2 = Ax.scatter( Vib_power_dict[subdir][filename]['J'],noise_lst[0][3], edgecolor=COLORS[idx],  alpha=1, facecolors='none')       #alpha=1.0 for opaque points                
        Ax.axhline(y=All_data_dict_wopwop[subdir]['Baseline'][0][3],linestyle='--',color=COLORS[idx])
        # if subdir in ['0.00','0.35','0.05','0.25','0.20']: 
        #     va='bottom'
        #     loc_multiplier=1.0
        # if subdir in ['0.15','0.10','0.30']: 
        #     va='top'
        #     loc_multiplier=1
        va='top'
        loc_multiplier=0.997
        Ax.text(Limits['J'][0],loc_multiplier*All_data_dict_wopwop[subdir]['Baseline'][0][3],r'$\mu=$'+subdir,va=va)#,fontsize=12,ha="right",rotation_mode="anchor")
        P.append((p_1,p_2))
        # p_3=Ax.scatter(Vib_power_dict[subdir]['Baseline']['J'],All_data_dict_wopwop[subdir]['Baseline'][0][3], c='black', marker='*')
    P.append((p_3))
    Ax.set_xlim(lim for lim in Limits[x])
    Ax.set_ylim(lim for lim in Limits[y])
    Ax.set_xlabel(YLABELS[x])#, fontsize=Axislabel_size)
    Ax.set_ylabel(YLABELS[y])#, fontsize=Axislabel_size)
    Ax.grid()
    Ax.text(J_baseline,Limits[y][0], 'Baseline J',rotation=45, fontsize=12,ha="right",va='top',
             rotation_mode="anchor")
    Ax.axvline(x=J_baseline,linestyle='--',color='black')
    
    # l=Ax.legend(P, [r'$\mu=$'+subdir for subdir in All_data_dict_wopwop]+['Baseline'],
    #                handler_map={tuple: HandlerTuple(ndivide=None)})
    # Ax.axvline(x=J_baseline,linestyle='--',color='black')
    # Ax.plot(Mu_list,Baseline_J_list,Baseline_CP_list,marker='o',color='black',linewidth=3,label='Baseline')
    Ax.scatter(np.nan,np.nan, marker='+',color='black',label='> Baseline '+r'$C_P$')
    Ax.scatter(np.nan,np.nan, edgecolor='black',  alpha=1, facecolors='none',color='black',label='< Baseline '+r'$C_P$')
    Ax.legend()
    
    Fig_tef.savefig(DIRECTORY_SAVE_PLOTS+'/'+f'{figname}_tef.png', bbox_inches='tight')
    Fig.savefig(DIRECTORY_SAVE_PLOTS+'/'+f'{figname}.png', bbox_inches='tight')
    print('saved: ', figname)
    plt.close(Fig)
    
Vib_power_noise_dict.pop('0.00', None)
###############################################################################
# Fig=plt.figure(figsize=make_pretty.set_size('AIAA_scitech',fraction=0.5))
Fig=plt.figure(figsize=(8, 7))
Ax=Fig.add_subplot(1,1,1)
P=[]
for idx,subdir in enumerate(Vib_power_noise_dict):
    for filename,data_dict in Vib_power_noise_dict[subdir].items():
        if data_dict['OASPL-A']>Vib_power_noise_dict[subdir]['Baseline']['OASPL-A']: 
            p_1 = Ax.scatter(data_dict['OASPL-A'], Vib_power_noise_dict[subdir][filename]['CP'], c=COLORS[idx], marker='+')
        else:
            p_2 = Ax.scatter(data_dict['OASPL-A'], Vib_power_noise_dict[subdir][filename]['CP'], edgecolor=COLORS[idx],  alpha=1, facecolors='none')       #alpha=1.0 for opaque points                
    Ax.axhline(y=Vib_power_noise_dict[subdir]['Baseline']['CP'],linestyle='--',color=COLORS[idx])
    if subdir in ['0.00','0.35','0.05','0.25','0.20']: 
        va='bottom'
        loc_multiplier=1.005
    if subdir in ['0.15','0.10','0.30']: 
        va='top'
        loc_multiplier=0.995
    Ax.text(Limits['OASPL-A'][0],loc_multiplier*Vib_power_noise_dict[subdir]['Baseline']['CP'],r'$\mu=$'+subdir,va=va)#,fontsize=12,ha="right",rotation_mode="anchor")
    P.append((p_1,p_2))
    # p_3 = Ax.scatter(All_data_dict_wopwop[subdir]['Baseline'][0][3], Vib_power_noise_dict[subdir]['Baseline']['CP'], c='black', marker='*')
# P.append((p_3))
Ax.set_xlim(lim for lim in Limits['OASPL-A'])
Ax.set_ylim(lim for lim in Limits['CP'])
Ax.set_xlabel(YLABELS['OASPL-A'])#, fontsize=Axislabel_size)
Ax.set_ylabel(YLABELS['CP'])#, fontsize=Axislabel_size)
Ax.grid()
# l=Ax.legend(P, [r'$\mu=$'+subdir for subdir in All_data_dict_wopwop]+['Baseline'],
#                handler_map={tuple: HandlerTuple(ndivide=None)})
# Ax.axvline(x=J_baseline,linestyle='--',color='black')
# Ax.plot(Mu_list,Baseline_J_list,Baseline_CP_list,marker='o',color='black',linewidth=3,label='Baseline')
Ax.scatter(np.nan,np.nan, marker='+',color='black',label=r'$>$ Baseline OASPL')
Ax.scatter(np.nan,np.nan, edgecolor='black',  alpha=1, facecolors='none',color='black',label=r'$<$ Baseline OASPL')
Ax.legend()

Fig.savefig(DIRECTORY_SAVE_PLOTS+'/'+'CP_OASPL-A'+'.pdf', bbox_inches='tight')
print('saved: ', 'CP_OASPL-A')
plt.close(Fig)
###############################################################################
# Fig=plt.figure(figsize=make_pretty.set_size('AIAA_scitech',fraction=0.5))
Fig=plt.figure(figsize=(8, 7))
Ax=Fig.add_subplot(1,1,1)
P=[]
for idx,subdir in enumerate(Vib_power_noise_dict):
    for filename,data_dict in Vib_power_noise_dict[subdir].items():
        alpha=1
        # if dict_['J']<J_baseline: alpha=0.8

        if data_dict['OASPL-A']>Vib_power_noise_dict[subdir]['Baseline']['OASPL-A']:  
            p_1 = Ax.scatter(Vib_power_dict[subdir][filename]['delta_CP%'],data_dict['OASPL-A'],  c=COLORS[idx], marker='+',alpha=alpha)
        else:
            p_2 = Ax.scatter(Vib_power_dict[subdir][filename]['delta_CP%'],data_dict['OASPL-A'],  edgecolor=COLORS[idx],  alpha=alpha, facecolors='none')       #alpha=1.0 for opaque points                
    Ax.axhline(y=Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'],linestyle='--',color=COLORS[idx])
    # if subdir in ['0.00','0.35','0.05','0.25','0.20']: 
    #     va='bottom'
    #     loc_multiplier=1.005
    # if subdir in ['0.15','0.10','0.30']: 
    #     va='top'
    #     loc_multiplier=0.995
    va='top'
    Ax.text(Limits['delta_CP%'][0],loc_multiplier*Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'],r'$\mu=$'+subdir,va=va)#,fontsize=12,ha="right",rotation_mode="anchor")
# P.append((p_3))
Ax.set_xlim(lim for lim in Limits['delta_CP%'])
Ax.set_ylim(lim for lim in Limits['OASPL-A'])
Ax.set_ylabel(YLABELS['OASPL-A'])#, fontsize=Axislabel_size)
Ax.set_xlabel(YLABELS['delta_CP%'])#, fontsize=Axislabel_size)
Ax.grid()
# l=Ax.legend(P, [r'$\mu=$'+subdir for subdir in All_data_dict_wopwop]+['Baseline'],
#                handler_map={tuple: HandlerTuple(ndivide=None)})
# Ax.axvline(x=J_baseline,linestyle='--',color='black')
# Ax.plot(Mu_list,Baseline_J_list,Baseline_CP_list,marker='o',color='black',linewidth=3,label='Baseline')
Ax.scatter(np.nan,np.nan, marker='+',color='black',label=r'$>$ Baseline OASPL')
Ax.scatter(np.nan,np.nan, edgecolor='black',  alpha=1, facecolors='none',color='black',label=r'$<$ Baseline OASPL')
Ax.legend()

Fig.savefig(DIRECTORY_SAVE_PLOTS+'/'+'OASPL-A_delta_CP'+'.pdf', bbox_inches='tight')
print('saved: ', 'OASPL-A_delta_CP')
plt.close(Fig)

###############################################################################
# Fig=plt.figure(figsize=make_pretty.set_size('AIAA_scitech',fraction=0.5))
y='OASPL-A'
x='J'
Fig=plt.figure(figsize=(8, 7))
Ax=Fig.add_subplot(1,1,1)
P=[]
for idx,subdir in enumerate(Vib_power_noise_dict):
    # print(subdir)
    #Ax.axhline(y=Vib_power_dict[subdir]['Baseline']['CP'], color=COLORS[idx], linestyle='--', linewidth=2.0)
    for filename,data_dict in Vib_power_noise_dict[subdir].items():
        if data_dict['OASPL-A']>Vib_power_noise_dict[subdir]['Baseline']['OASPL-A']: 
            p_1 = Ax.scatter( Vib_power_dict[subdir][filename]['J'],data_dict['OASPL-A'], c=COLORS[idx], marker='+')
        else:
            p_2 = Ax.scatter( Vib_power_dict[subdir][filename]['J'],data_dict['OASPL-A'], edgecolor=COLORS[idx],  alpha=1, facecolors='none')       #alpha=1.0 for opaque points                
    Ax.axhline(y=Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'],linestyle='--',color=COLORS[idx])
    loc_multiplier=1.0
    # if subdir in ['0.00','0.35','0.05','0.25','0.20']: 
    #     va='bottom'
    #     loc_multiplier=1.0
    # if subdir in ['0.15','0.10','0.30']: 
    #     va='top'
    #     loc_multiplier=1
    va='top'
    Ax.text(Limits[x][0],loc_multiplier*Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'],r'$\mu=$'+subdir,va=va)#,fontsize=12,ha="right",rotation_mode="anchor")
    P.append((p_1,p_2))
    p_3=Ax.scatter(Vib_power_noise_dict[subdir]['Baseline']['J'],Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'], c='black', marker='*')
P.append((p_3))
Ax.set_xlim(lim for lim in Limits[x])
Ax.set_ylim(lim for lim in Limits[y])
Ax.set_xlabel(YLABELS[x])#, fontsize=Axislabel_size)
Ax.set_ylabel(YLABELS[y])#, fontsize=Axislabel_size)
Ax.grid()
Ax.text(J_baseline,Limits[y][0], 'Baseline J',rotation=45, fontsize=12,ha="right",
         rotation_mode="anchor")
Ax.axvline(x=J_baseline,linestyle='--',color='black')

# l=Ax.legend(P, [r'$\mu=$'+subdir for subdir in All_data_dict_wopwop]+['Baseline'],
#                handler_map={tuple: HandlerTuple(ndivide=None)})
# Ax.axvline(x=J_baseline,linestyle='--',color='black')
# Ax.plot(Mu_list,Baseline_J_list,Baseline_CP_list,marker='o',color='black',linewidth=3,label='Baseline')
Ax.scatter(np.nan,np.nan, marker='+',color='black',label=r'$>$ Baseline OASPL')
Ax.scatter(np.nan,np.nan, edgecolor='black',  alpha=1, facecolors='none',color='black',label=r'$>$ Baseline OASPL')
Ax.legend()

Fig.savefig(DIRECTORY_SAVE_PLOTS+'/'+f'{y}_{x}'+'.pdf', bbox_inches='tight')
print('saved: ', f'{y}_{x}')
plt.close(Fig)



###############################################################################
# Fig=plt.figure(figsize=make_pretty.set_size('AIAA_scitech',fraction=0.5))
Fig=plt.figure(figsize=(8, 7))
Ax=Fig.add_subplot(1,1,1)
P=[]


for idx,subdir in enumerate(Vib_power_noise_dict):
    #Ax.axhline(y=Vib_power_dict[subdir]['Baseline']['CP'], color=COLORS[idx], linestyle='--', linewidth=2.0)
    for filename,dict_ in Vib_power_noise_dict[subdir].items():
        alpha=1       
        if dict_['CP']>Vib_power_noise_dict[subdir]['Baseline']['CP']: 
            p_1 = Ax.scatter(dict_['J'], dict_['CP'], c=COLORS[idx], marker='+',s=18,alpha=alpha)
        else:
            p_2 = Ax.scatter(dict_['J'], dict_['CP'], edgecolor=COLORS[idx],  alpha=alpha, facecolors='none',s=18)       #alpha=1.0 for opaque points                
    Ax.axhline(y=Vib_power_noise_dict[subdir]['Baseline']['CP'],linestyle='--',color=COLORS[idx])
    if subdir in ['0.00','0.05','0.25','0.20']: 
        va='bottom'
        loc_multiplier=1.005
    if subdir in ['0.15','0.10','0.30','0.35']: 
        va='top'
        loc_multiplier=0.995
    Ax.text(Limits['J'][0],loc_multiplier*Vib_power_noise_dict[subdir]['Baseline']['CP'],r'$\mu=$'+subdir,va=va)#,fontsize=12,ha="right",rotation_mode="anchor")
    P.append((p_1,p_2))
Ax.set_xlim(lim for lim in Limits['J'])
Ax.set_ylim(lim for lim in Limits['CP'])
Ax.set_xlabel(YLABELS['J'])#, fontsize=Axislabel_size)
Ax.set_ylabel(YLABELS['CP'])#, fontsize=Axislabel_size)
Ax.set_xticks([0.0,1.0,2.0,3.0,4.0])
# Ax.set_xticks(list(Ax.get_xticks()) + [J_baseline])
# Ax.set_xticklabels(list(Ax.get_xticklabels())[:-1] + [text.Text(J_baseline,0,'Baseline J')])
Ax.text(J_baseline,Limits['CP'][0], 'Baseline J',rotation=45, fontsize=12,ha="right",va='top',
         rotation_mode="anchor")
Ax.scatter(np.nan,np.nan, marker='+',color='black',label=r'$>$ Baseline $C_P$')
Ax.scatter(np.nan,np.nan, edgecolor='black',  alpha=1, facecolors='none',color='black',label=r'$<$ Baseline $C_P$')
leg=Ax.legend(frameon=True)
leg.get_frame().set_edgecolor('black')
leg.get_frame().set_linewidth(1.5)
Ax.grid()
# l=Ax.legend(P, [r'$\mu=$'+subdir for subdir in All_data_dict],
#                handler_map={tuple: HandlerTuple(ndivide=None)})
Ax.axvline(x=J_baseline,linestyle='--',color='black')
# Ax.plot(Mu_list,Baseline_J_list,Baseline_CP_list,marker='o',color='black',linewidth=3,label='Baseline')

Fig.savefig(DIRECTORY_SAVE_PLOTS+'/'+'CP_J'+'.pdf', bbox_inches='tight')
print('saved: ', 'CP_J')
plt.close(Fig)
###############################################################################
Fig=plt.figure(figsize=(8, 7))
Ax=Fig.add_subplot(1,1,1)
P=[]
best_cp_j_values={}

for idx,subdir in enumerate(best_cp_j_values):
    print(subdir)
    max_cp=min(best_cp_j_values[subdir]['cp'])
    max_j=min(best_cp_j_values[subdir]['j'])
    print(max_cp,max_j)
    
figname='delta_CP_delta_J_additional_info'
for idx,subdir in enumerate(Vib_power_noise_dict):
    # if subdir!='0.35': continue
    best_cp_j_values[subdir]={'cp':[],'j':[]}
    #Ax.axhline(y=Vib_power_dict[subdir]['Baseline']['CP'], color=COLORS[idx], linestyle='--', linewidth=2.0)
    for filename,dict_ in Vib_power_noise_dict[subdir].items():
        alpha=1.0
        # if dict_['delta_J%']<Vib_power_dict[subdir]['Baseline']['delta_J%']: alpha=0.8
        cp=dict_['delta_CP%']
        j=dict_['delta_J%']
        if cp<0 and j<0: 
            best_cp_j_values[subdir]['cp'].append(cp)
            best_cp_j_values[subdir]['j'].append(j)
        if Vib_power_noise_dict[subdir][filename]['delta_OASPL-A']>0: 
        # if dict_['delta_CP%']>Vib_power_dict[subdir]['Baseline']['delta_CP%']: 
            p_1 = Ax.scatter(dict_['delta_J%'], dict_['delta_CP%'], c=COLORS[idx], marker='+',s=18,alpha=alpha)
            
        else:
            p_2 = Ax.scatter(dict_['delta_J%'], dict_['delta_CP%'], edgecolor=COLORS[idx],  alpha=alpha, facecolors='none',s=18)       #alpha=1.0 for opaque points                
    # Ax.axhline(y=Vib_power_dict[subdir]['Baseline']['delta_CP%'],linestyle='--',color=COLORS[idx])
    Ax.axhline(y=Vib_power_noise_dict[subdir]['Baseline']['delta_J%'],linestyle='--',color='black')
    # if subdir in ['0.00','0.35','0.05','0.25','0.20']: 
    #     va='bottom'
    #     loc_multiplier=1.005
    # if subdir in ['0.15','0.10','0.30']: 
    #     va='top'
    #     loc_multiplier=0.995
    # Ax.text(Limits['J'][0],loc_multiplier*Vib_power_dict[subdir]['Baseline']['delta_CP%'],r'$\mu=$'+subdir,va=va)#,fontsize=12,ha="right",rotation_mode="anchor")
    # P.append((p_1,p_2))
Ax.set_xlim(lim for lim in Limits['delta_J%'])
Ax.set_ylim(lim for lim in Limits['delta_CP%'])
Ax.set_xlabel(YLABELS['delta_J%'])#, fontsize=Axislabel_size)
Ax.set_ylabel(YLABELS['delta_CP%'])#, fontsize=Axislabel_size)
Ax.scatter(np.nan,np.nan, marker='+',color='black',label=r'$>$ Baseline OASPL')
Ax.scatter(np.nan,np.nan, edgecolor='black',  alpha=1, facecolors='none',color='black',label=r'$<$ Baseline OASPL')
Ax.legend()
Ax.grid()
# l=Ax.legend(P, [r'$\mu=$'+subdir for subdir in All_data_dict],
#                handler_map={tuple: HandlerTuple(ndivide=None)})
Ax.axvline(x=J_baseline,linestyle='--',color='black')
# Ax.plot(Mu_list,Baseline_J_list,Baseline_CP_list,marker='o',color='black',linewidth=3,label='Baseline')

Fig.savefig(DIRECTORY_SAVE_PLOTS+'/'+figname+'.pdf', bbox_inches='tight')
print('saved: ', figname)
plt.close(Fig)
###############################################################################
# Fig=plt.figure(figsize=make_pretty.set_size('AIAA_scitech',fraction=0.5))
Fig=plt.figure(figsize=(8, 7))
Ax=Fig.add_subplot(1,1,1)
P=[]
for idx,subdir in enumerate(Vib_power_noise_dict):
    for filename,data_dict in Vib_power_noise_dict[subdir].items():
        if data_dict['J']>Vib_power_noise_dict[subdir]['Baseline']['J']: 
            p_1 = Ax.scatter(data_dict['OASPL-A'], data_dict['CP'], c=COLORS[idx], marker='+')
        else:
            p_2 = Ax.scatter(data_dict['OASPL-A'], data_dict['CP'], edgecolor=COLORS[idx],  alpha=1, facecolors='none')       #alpha=1.0 for opaque points                
    Ax.axhline(y=Vib_power_noise_dict[subdir]['Baseline']['CP'],linestyle='--',color=COLORS[idx])
    if subdir in ['0.00','0.35','0.05','0.25','0.20']: 
        va='bottom'
        loc_multiplier=1.005
    if subdir in ['0.15','0.10','0.30']: 
        va='top'
        loc_multiplier=0.995
    Ax.text(Limits['OASPL-A'][0],loc_multiplier*Vib_power_noise_dict[subdir]['Baseline']['CP'],r'$\mu=$'+subdir,va=va)#,fontsize=12,ha="right",rotation_mode="anchor")
    P.append((p_1,p_2))
    # p_3 = Ax.scatter(All_data_dict_wopwop[subdir]['Baseline'][0][3], Vib_power_dict[subdir]['Baseline']['CP'], c='black', marker='*')
    Ax.axvline(x=Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'],linestyle='--',color=COLORS[idx])
# P.append((p_3))
Ax.set_xlim(lim for lim in Limits['OASPL-A'])
Ax.set_ylim(lim for lim in Limits['CP'])
Ax.set_xlabel(YLABELS['OASPL-A'])#, fontsize=Axislabel_size)
Ax.set_ylabel(YLABELS['CP'])#, fontsize=Axislabel_size)
Ax.grid()
# l=Ax.legend(P, [r'$\mu=$'+subdir for subdir in All_data_dict_wopwop]+['Baseline'],
#                handler_map={tuple: HandlerTuple(ndivide=None)})
# Ax.axvline(x=J_baseline,linestyle='--',color='black')
# Ax.plot(Mu_list,Baseline_J_list,Baseline_CP_list,marker='o',color='black',linewidth=3,label='Baseline')
Ax.scatter(np.nan,np.nan, marker='+',color='black',label=r'$>$ Baseline $J$')
Ax.scatter(np.nan,np.nan, edgecolor='black',  alpha=1, facecolors='none',color='black',label=r'$<$ Baseline $J$')
Ax.legend()

Fig.savefig(DIRECTORY_SAVE_PLOTS+'/'+'CP_OASPL-A_additional_info'+'.pdf', bbox_inches='tight')
print('saved: ', 'CP_OASPL-A_additional_info')
plt.close(Fig)
###############################################################################
Fig=plt.figure(figsize=(8, 7))
Ax=Fig.add_subplot(1,1,1)
P=[]
for idx,subdir in enumerate(Vib_power_noise_dict):
    for filename,data_dict in Vib_power_noise_dict[subdir].items():
        if data_dict['J']>Vib_power_noise_dict[subdir]['Baseline']['J']: 
            p_1 = Ax.scatter( data_dict['delta_CP%'],data_dict['OASPL-A'], c=COLORS[idx], marker='+')
        else:
            p_2 = Ax.scatter(data_dict['delta_CP%'],data_dict['OASPL-A'], edgecolor=COLORS[idx],  alpha=1, facecolors='none')       #alpha=1.0 for opaque points                
    P.append((p_1,p_2))
    Ax.axhline(y=Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'],linestyle='--',color=COLORS[idx])
    # if subdir in ['0.00','0.35','0.05','0.25','0.20']: 
    #     va='bottom'
    #     loc_multiplier=1.005
    # if subdir in ['0.15','0.10','0.30']: 
    #     va='top'
    #     loc_multiplier=0.995
    va='top'
    Ax.text(Limits['delta_CP%'][0],loc_multiplier*Vib_power_noise_dict[subdir][filename]['OASPL-A'],r'$\mu=$'+subdir,va=va)#,fontsize=12,ha="right",rotation_mode="anchor")
# P.append((p_3))
Ax.set_ylim(lim for lim in Limits['OASPL-A'])
Ax.set_xlim(lim for lim in Limits['delta_CP%'])
Ax.set_ylabel(YLABELS['OASPL-A'])#, fontsize=Axislabel_size)
Ax.set_xlabel(YLABELS['delta_CP%'])#, fontsize=Axislabel_size)
Ax.grid()
# l=Ax.legend(P, [r'$\mu=$'+subdir for subdir in All_data_dict_wopwop]+['Baseline'],
#                handler_map={tuple: HandlerTuple(ndivide=None)})
# Ax.axvline(x=J_baseline,linestyle='--',color='black')
# Ax.plot(Mu_list,Baseline_J_list,Baseline_CP_list,marker='o',color='black',linewidth=3,label='Baseline')
Ax.scatter(np.nan,np.nan, marker='+',color='black',label=r'$>$ Baseline $J$')
Ax.scatter(np.nan,np.nan, edgecolor='black',  alpha=1, facecolors='none',color='black',label=r'$<$ Baseline $J$')
Ax.legend()

Fig.savefig(DIRECTORY_SAVE_PLOTS+'/'+'OASPL-A_delta_CP_additional_info'+'.pdf', bbox_inches='tight')
print('saved: ', 'OASPL-A_delta_CP_additional_info')
plt.close(Fig)
###############################################################################
Fig=plt.figure(figsize=(8, 7))
Ax=Fig.add_subplot(1,1,1)
Fig_tef=plt.figure(figsize=(8, 6))
Gs_tef = gridspec.GridSpec(2, 4, figure=Fig_tef)

figname='OASPL-A_delta_CP_additional_info_2'
P=[]
Best_cases_dict[figname]={}
for idx,subdir in enumerate(Vib_power_noise_dict):
    Best_cases_dict[figname][subdir]=[]
    Ax_tef = Fig_tef.add_subplot(Gs_tef[idx])
    
    for filename,data_dict in Vib_power_noise_dict[subdir].items():
        if data_dict['OASPL-A']<Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'] and Vib_power_noise_dict[subdir][filename]['delta_CP%']<Vib_power_noise_dict[subdir]['Baseline']['delta_CP%']:
            if Vib_power_noise_dict[subdir][filename]['J']>Vib_power_noise_dict[subdir]['Baseline']['J']:
                p_1 = Ax.scatter(data_dict['delta_CP%'],data_dict['OASPL-A'], c=COLORS[idx], marker='+')
            else:
                Best_cases_dict[figname][subdir].append(filename)
                azimuth, tef_deflection = cii.get_tef_deflection(All_data_dict[subdir][filename])
                Ax.plot(Ax_tef,azimuth,tef_deflection,color=COLORS[idx])
                p_2 = Ax.scatter(data_dict['delta_CP%'],data_dict['OASPL-A'], edgecolor=COLORS[idx],  alpha=1, facecolors='none')       #alpha=1.0 for opaque points                        
         
        #     if data_dict['OASPL-A']<Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'] and Vib_power_noise_dict[subdir][filename]['delta_CP%']<Vib_power_noise_dict[subdir]['Baseline']['delta_CP%']:
        #         p_1 = Ax.scatter(data_dict['delta_CP%'],data_dict['OASPL-A'], c=COLORS[idx], marker='+')
           
        # else:
        #     if data_dict['OASPL-A']<Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'] and Vib_power_noise_dict[subdir][filename]['delta_CP%']<Vib_power_noise_dict[subdir]['Baseline']['delta_CP%']:
        #         Best_cases_dict[figname][subdir].append(filename)
        #         azimuth, tef_deflection = cii.get_tef_deflection(All_data_dict[subdir][filename])
        #         Ax.plot(Ax_tef,azimuth,tef_deflection,color=COLORS[idx])
        #         p_2 = Ax.scatter(data_dict['delta_CP%'],data_dict['OASPL-A'], edgecolor=COLORS[idx],  alpha=1, facecolors='none')       #alpha=1.0 for opaque points                
    P.append((p_1,p_2))
    Ax.axhline(y=Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'],linestyle='--',color=COLORS[idx])
    if subdir in ['0.00','0.05','0.10','0.15','0.25','0.30','0.35']: 
        va='bottom'
        loc_multiplier=1.005
    if subdir in ['0.20']: 
        va='top'
        loc_multiplier=0.995
    # va='top'
    Ax.text(Limits['delta_CP%'][0],loc_multiplier*Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'],r'$\mu=$'+subdir,va=va)#,fontsize=12,ha="right",rotation_mode="anchor")
# P.append((p_3))
Ax.set_ylim(lim for lim in Limits['OASPL-A'])
Ax.set_xlim(lim for lim in Limits['delta_CP%'])
Ax.set_ylabel(YLABELS['OASPL-A'])#, fontsize=Axislabel_size)
Ax.set_xlabel(YLABELS['delta_CP%'])#, fontsize=Axislabel_size)
Ax.grid()
Ax.axvline(x=0,linestyle='--',color='black')
# l=Ax.legend(P, [r'$\mu=$'+subdir for subdir in All_data_dict_wopwop]+['Baseline'],
#                handler_map={tuple: HandlerTuple(ndivide=None)})
# Ax.axvline(x=J_baseline,linestyle='--',color='black')
# Ax.plot(Mu_list,Baseline_J_list,Baseline_CP_list,marker='o',color='black',linewidth=3,label='Baseline')
Ax.scatter(np.nan,np.nan, marker='+',color='black',label=r'$>$ Baseline $J$')
Ax.scatter(np.nan,np.nan, edgecolor='black',  alpha=1, facecolors='none',color='black',label=r'$<$ Baseline $J$')
leg=Ax.legend(frameon=True)
leg.get_frame().set_edgecolor('black')
leg.get_frame().set_linewidth(1.5)

Fig_tef.savefig(DIRECTORY_SAVE_PLOTS+'/'+f'{figname}_tef.pdf', bbox_inches='tight')
Fig.savefig(DIRECTORY_SAVE_PLOTS+'/'+figname+'.pdf', bbox_inches='tight')
print('saved: ', figname)
plt.close(Fig)
###############################################################################
# Fig=plt.figure(figsize=make_pretty.set_size('AIAA_scitech',fraction=0.5))
y='OASPL-A'
x='J'
figname=f'{y}_{x}_additional_info'
Fig=plt.figure(figsize=(8, 7))
Ax=Fig.add_subplot(1,1,1)
Fig_tef=plt.figure(figsize=(8, 6))
Gs_tef = gridspec.GridSpec(2, 4, figure=Fig_tef)

P=[]
Best_cases_dict[figname]={}
for idx,subdir in enumerate(Vib_power_noise_dict):
    Best_cases_dict[figname][subdir]=[]
    Ax_tef = Fig_tef.add_subplot(Gs_tef[idx])
    # print(subdir)
    #Ax.axhline(y=Vib_power_dict[subdir]['Baseline']['CP'], color=COLORS[idx], linestyle='--', linewidth=2.0)
    for filename,data_dict in Vib_power_noise_dict[subdir].items():
        # if noise_lst[0][3]>All_data_dict_wopwop[subdir]['Baseline'][0][3]: 
        if Vib_power_dict[subdir][filename]['CP']>Vib_power_dict[subdir]['Baseline']['CP']: 
            p_1 = Ax.scatter(Vib_power_dict[subdir][filename]['J'], data_dict['OASPL-A'], c=COLORS[idx], marker='+')
        else:
            p_2 = Ax.scatter( Vib_power_dict[subdir][filename]['J'],data_dict['OASPL-A'], edgecolor=COLORS[idx],  alpha=1, facecolors='none')       #alpha=1.0 for opaque points                
            if data_dict['OASPL-A']<Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'] and Vib_power_dict[subdir][filename]['J']<Vib_power_dict[subdir]['Baseline']['J']:
                Best_cases_dict[figname][subdir].append(filename)
                azimuth, tef_deflection = cii.get_tef_deflection(All_data_dict[subdir][filename])
                Ax.plot(Ax_tef,azimuth,tef_deflection,color=COLORS[idx])
                # Ax_tef.plot(All_data_dict[subdir][filename])
    Ax.axhline(y=Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'],linestyle='--',color=COLORS[idx])
    # if subdir in ['0.00','0.35','0.05','0.25','0.20']: 
    #     va='bottom'
    #     loc_multiplier=1.0
    # if subdir in ['0.15','0.10','0.30']: 
    #     va='top'
    #     loc_multiplier=1
    va='top'
    loc_multiplier=0.997
    Ax.text(Limits['J'][0],loc_multiplier*Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'],r'$\mu=$'+subdir,va=va)#,fontsize=12,ha="right",rotation_mode="anchor")
    P.append((p_1,p_2))
    # p_3=Ax.scatter(Vib_power_dict[subdir]['Baseline']['J'],All_data_dict_wopwop[subdir]['Baseline'][0][3], c='black', marker='*')
P.append((p_3))
Ax.set_xlim(lim for lim in Limits[x])
Ax.set_ylim(lim for lim in Limits[y])
Ax.set_xlabel(YLABELS[x])#, fontsize=Axislabel_size)
Ax.set_ylabel(YLABELS[y])#, fontsize=Axislabel_size)
Ax.grid()
Ax.text(J_baseline,Limits[y][0], 'Baseline J',rotation=45, fontsize=12,ha="right",va='top',
         rotation_mode="anchor")
Ax.axvline(x=J_baseline,linestyle='--',color='black')

# l=Ax.legend(P, [r'$\mu=$'+subdir for subdir in All_data_dict_wopwop]+['Baseline'],
#                handler_map={tuple: HandlerTuple(ndivide=None)})
# Ax.axvline(x=J_baseline,linestyle='--',color='black')
# Ax.plot(Mu_list,Baseline_J_list,Baseline_CP_list,marker='o',color='black',linewidth=3,label='Baseline')
Ax.scatter(np.nan,np.nan, marker='+',color='black',label=r'$>$ Baseline $C_P$')
Ax.scatter(np.nan,np.nan, edgecolor='black',  alpha=1, facecolors='none',color='black',label=r'$<$ Baseline $C_P$')
Ax.legend()

Fig_tef.savefig(DIRECTORY_SAVE_PLOTS+'/'+f'{figname}_tef.pdf', bbox_inches='tight')
Fig.savefig(DIRECTORY_SAVE_PLOTS+'/'+f'{figname}.pdf', bbox_inches='tight')
print('saved: ', figname)
plt.close(Fig)



###############################################################################
# Fig=plt.figure(figsize=make_pretty.set_size('AIAA_scitech',fraction=0.5))
y='OASPL-A'
x='J'
figname=f'{y}_{x}_additional_info_2'
Fig=plt.figure(figsize=(8, 7))
Ax=Fig.add_subplot(1,1,1)
Fig_tef=plt.figure(figsize=(8, 6))
Gs_tef = gridspec.GridSpec(2, 4, figure=Fig_tef)

P=[]
Best_cases_dict[figname]={}
for idx,subdir in enumerate(Vib_power_noise_dict):
    Best_cases_dict[figname][subdir]=[]
    Ax_tef = Fig_tef.add_subplot(Gs_tef[idx])
    # print(subdir)
    #Ax.axhline(y=Vib_power_dict[subdir]['Baseline']['CP'], color=COLORS[idx], linestyle='--', linewidth=2.0)
    for filename,data_dict in Vib_power_noise_dict[subdir].items():
        # if noise_lst[0][3]>All_data_dict_wopwop[subdir]['Baseline'][0][3]: 
        if Vib_power_dict[subdir][filename]['CP']>Vib_power_dict[subdir]['Baseline']['CP']: 
            if data_dict['OASPL-A']<Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'] and Vib_power_dict[subdir][filename]['delta_CP%']<Vib_power_dict[subdir]['Baseline']['delta_CP%']:
                p_1 = Ax.scatter(Vib_power_dict[subdir][filename]['J'], data_dict['OASPL-A'], c=COLORS[idx], marker='+')
        else:
            if data_dict['OASPL-A']<Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'] and Vib_power_dict[subdir][filename]['J']<Vib_power_dict[subdir]['Baseline']['J']:
                Best_cases_dict[figname][subdir].append(filename)
                azimuth, tef_deflection = cii.get_tef_deflection(All_data_dict[subdir][filename])
                Ax.plot(Ax_tef,azimuth,tef_deflection,color=COLORS[idx])
                # Ax_tef.plot(All_data_dict[subdir][filename])
                p_2 = Ax.scatter( Vib_power_dict[subdir][filename]['J'],data_dict['OASPL-A'], edgecolor=COLORS[idx],  alpha=1, facecolors='none')       #alpha=1.0 for opaque points                
    Ax.axhline(y=Vib_power_noise_dict[subdir]['Baseline']['OASPL-A'],linestyle='--',color=COLORS[idx])
    # if subdir in ['0.00','0.35','0.05','0.25','0.20']: 
    #     va='bottom'
    #     loc_multiplier=1.0
    # if subdir in ['0.15','0.10','0.30']: 
    #     va='top'
    #     loc_multiplier=1
    va='top'
    loc_multiplier=0.997
    Ax.text(Limits['J'][0],loc_multiplier*All_data_dict_wopwop[subdir]['Baseline'][0][3],r'$\mu=$'+subdir,va=va)#,fontsize=12,ha="right",rotation_mode="anchor")
    P.append((p_1,p_2))
    # p_3=Ax.scatter(Vib_power_dict[subdir]['Baseline']['J'],All_data_dict_wopwop[subdir]['Baseline'][0][3], c='black', marker='*')
P.append((p_3))
Ax.set_xlim(lim for lim in Limits[x])
Ax.set_ylim(lim for lim in Limits[y])
Ax.set_xlabel(YLABELS[x])#, fontsize=Axislabel_size)
Ax.set_ylabel(YLABELS[y])#, fontsize=Axislabel_size)
Ax.grid()
Ax.text(J_baseline,Limits[y][0], 'Baseline J',rotation=45, fontsize=12,ha="right",va='top',
         rotation_mode="anchor")
Ax.axvline(x=J_baseline,linestyle='--',color='black')

# l=Ax.legend(P, [r'$\mu=$'+subdir for subdir in All_data_dict_wopwop]+['Baseline'],
#                handler_map={tuple: HandlerTuple(ndivide=None)})
# Ax.axvline(x=J_baseline,linestyle='--',color='black')
# Ax.plot(Mu_list,Baseline_J_list,Baseline_CP_list,marker='o',color='black',linewidth=3,label='Baseline')
Ax.scatter(np.nan,np.nan, marker='+',color='black',label=r'$>$ Baseline $C_P$')
Ax.scatter(np.nan,np.nan, edgecolor='black',  alpha=1, facecolors='none',color='black',label=r'$<$ Baseline $C_P$')
Ax.legend()

Fig_tef.savefig(DIRECTORY_SAVE_PLOTS+'/'+f'{figname}_tef.pdf', bbox_inches='tight')
Fig.savefig(DIRECTORY_SAVE_PLOTS+'/'+f'{figname}.pdf', bbox_inches='tight')
print('saved: ', figname)
plt.close(Fig)
###############################################################################
# # Fig=plt.figure(figsize=make_pretty.set_size('AIAA_scitech',fraction=0.5))
# Fig=plt.figure(figsize=(8, 5))
# Ax=Fig.add_subplot(1,1,1)
# P=[]
# for idx,subdir in enumerate(Vib_power_dict):
#     #Ax.axhline(y=Vib_power_dict[subdir]['Baseline']['CP'], color=COLORS[idx], linestyle='--', linewidth=2.0)
#     for filename,dict_ in Vib_power_dict[subdir].items():
#         if All_data_dict_wopwop[subdir][filename][0][3]>All_data_dict_wopwop[subdir]['Baseline'][0][3]: 
#             p_1 = Ax.scatter(dict_['J'], dict_['CP'], c=COLORS[idx], marker='+')
#         else:
#             p_2 = Ax.scatter(dict_['J'], dict_['CP'], edgecolor=COLORS[idx],  alpha=1, facecolors='none')       #alpha=1.0 for opaque points                
#     Ax.axhline(y=Vib_power_dict[subdir]['Baseline']['CP'],linestyle='--',color=COLORS[idx])
#     if subdir in ['0.00','0.35','0.05','0.25','0.20']: 
#         va='bottom'
#         loc_multiplier=1.005
#     if subdir in ['0.15','0.10','0.30']: 
#         va='top'
#         loc_multiplier=0.995
#     Ax.text(0,loc_multiplier*Vib_power_dict[subdir]['Baseline']['CP'],r'$\mu=$'+subdir,va=va)#,fontsize=12,ha="right",rotation_mode="anchor")
#     P.append((p_1,p_2))
# Ax.set_xlim(lim for lim in Limits['J'])
# Ax.set_ylim(lim for lim in Limits['CP'])
# Ax.set_xlabel(YLABELS['J'])#, fontsize=Axislabel_size)
# Ax.set_ylabel(YLABELS['CP'])#, fontsize=Axislabel_size)
# # Ax.set_xticks(list(Ax.get_xticks()) + [J_baseline])
# # Ax.set_xticklabels(list(Ax.get_xticklabels())[:-1] + [text.Text(J_baseline,0,'Baseline J')])
# Ax.text(J_baseline,Limits['CP'][0], 'Baseline J',rotation=45, fontsize=12,ha="right",
#          rotation_mode="anchor")
# Ax.grid()
# # l=Ax.legend(P, [r'$\mu=$'+subdir for subdir in All_data_dict],
# #                handler_map={tuple: HandlerTuple(ndivide=None)})
# Ax.axvline(x=J_baseline,linestyle='--',color='black')
# # Ax.plot(Mu_list,Baseline_J_list,Baseline_CP_list,marker='o',color='black',linewidth=3,label='Baseline')

# Fig.savefig(DIRECTORY_SAVE_PLOTS+'/'+'CP_J_additional_info'+'.png', facecolor=Fig.get_facecolor(), transparent=True)
# print('saved: ', 'CP_J_additional_info')
# plt.close(Fig)

###############################################################################
Axislabel_size=21
Ticklabel_size=15
Legend_size=15
Fig=plt.figure(figsize=(11.5, 6))
# Ax=Fig.add_subplot(1,1,1,projection='3d')
Ax = Axes3D(Fig)
for idx, subdir in enumerate(Vib_power_noise_dict):
    for _, dict_ in Vib_power_noise_dict[subdir].items():
        if Limits['J'][0]<=dict_['J']<=Limits['J'][1]: 
            pass
        else:
            dict_['J']=np.nan
        if Limits['CP'][0]<=dict_['CP']<=Limits['CP'][1]: 
            pass
        else:
            dict_['CP']=np.nan
        if dict_['J']>J_baseline: 
            Ax.scatter(float(subdir),dict_['J'], dict_['CP'], c=COLORS[idx], alpha=0.2, marker='+')
        else:
            Ax.scatter(float(subdir),dict_['J'],dict_['CP'], c=COLORS[idx], alpha=0.65)       #alpha=1.0 for opaque points                
Ax.set_xlabel(YLABELS['mu'],labelpad=15, fontsize=Axislabel_size)
Ax.set_ylabel(YLABELS['J'],labelpad=15, fontsize=Axislabel_size)
Ax.set_zlabel(YLABELS['CP'],labelpad=20, fontsize=Axislabel_size)
Ax.set_xlim(lim for lim in Limits['mu'])
Ax.set_ylim(lim for lim in Limits['J'])
Ax.set_zlim(lim for lim in Limits['CP'])
Ax.set_xticks([0.0,0.1,0.2,0.3,0.4])
Ax.set_zticks([0.00025,0.00035,0.00045,0.00055,0.00065])
Ax.zaxis.set_rotate_label(False) 
Ax.xaxis.set_rotate_label(False) 
for t in Ax.xaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
for t in Ax.yaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
for t in Ax.zaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
Ax.tick_params(axis='z', which='major', pad=15)
Ax.zaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))

Ax.plot(Mu_list,Baseline_J_list,Baseline_CP_list,marker='*',color='black', linestyle='--', linewidth=3,label='Baseline')

# xx,zz=np.meshgrid(np.linspace(Limits['mu'][0],Limits['mu'][1],10), np.linspace(Limits['CP'][0],Limits['CP'][1],10))
# Ax.plot_surface(xx, J_baseline*np.ones_like(xx), zz, alpha=0.2)
# Ax.text(0.4, J_baseline, 0, "J-baseline")

Fig.savefig(DIRECTORY_SAVE_PLOTS+'/'+'mu_CP_J'+'.pdf', bbox_inches='tight', facecolor=Fig.get_facecolor(), transparent=True)
print('saved: ', 'mu_CP_J')
plt.close(Fig)
###############################################################################

Fig=plt.figure(figsize=(11.5, 6))
# Ax=Fig.add_subplot(1,1,1,projection='3d')
Ax = Axes3D(Fig)
for idx, subdir in enumerate(Vib_power_noise_dict):
    for _, dict_ in Vib_power_noise_dict[subdir].items():
        if Limits['J'][0]<=dict_['J']<=Limits['J'][1]: 
            pass
        else:
            dict_['J']=np.nan
        if Limits['CP'][0]<=dict_['CP']<=Limits['CP'][1]: 
            pass
        else:
            dict_['CP']=np.nan
        if dict_['J']>J_baseline: 
            Ax.scatter(float(subdir),dict_['J'], dict_['CP'], c=COLORS[idx], alpha=0.2, marker='+')
        else:
            Ax.scatter(float(subdir),dict_['J'],dict_['CP'], c=COLORS[idx], alpha=0.65)       #alpha=1.0 for opaque points                
Ax.set_xlabel(YLABELS['mu'],labelpad=15, fontsize=Axislabel_size)
Ax.set_ylabel(YLABELS['J'],labelpad=15, fontsize=Axislabel_size)
Ax.set_zlabel(YLABELS['CP'],labelpad=20, fontsize=Axislabel_size)
Ax.set_xlim(lim for lim in Limits['mu'])
Ax.set_ylim(lim for lim in Limits['J'])
Ax.set_zlim(lim for lim in Limits['CP'])
Ax.set_xticks([0.0,0.1,0.2,0.3,0.4])
Ax.set_zticks([0.00025,0.00035,0.00045,0.00055,0.00065])
Ax.zaxis.set_rotate_label(False) 
Ax.xaxis.set_rotate_label(False) 
for t in Ax.xaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
for t in Ax.yaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
for t in Ax.zaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
Ax.tick_params(axis='z', which='major', pad=15)
Ax.zaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))

Ax.plot(Mu_list,Baseline_J_list,Baseline_CP_list,marker='*',color='black', linestyle='--', linewidth=3,label='Baseline')

# xx,zz=np.meshgrid(np.linspace(Limits['mu'][0],Limits['mu'][1],10), np.linspace(Limits['CP'][0],Limits['CP'][1],10))
# Ax.plot_surface(xx, J_baseline*np.ones_like(xx), zz, alpha=0.2)
# Ax.text(0.4, J_baseline, 0, "J-baseline")

Fig.savefig(DIRECTORY_SAVE_PLOTS+'/'+'mu_CP_J'+'.pdf', bbox_inches='tight', facecolor=Fig.get_facecolor(), transparent=True)
print('saved: ', 'mu_CP_J')
plt.close(Fig)
