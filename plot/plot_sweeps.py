#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 11:50:55 2019

@author: ge56beh
"""
import matplotlib.pyplot as plt
plt.ioff()
# plt.style.use('seaborn')
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mtick
from mpl_toolkits.mplot3d import Axes3D
from cycler import cycler
import os
import numpy as np
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from utl import crawler,cii
#plt.rcParams.update(make_pretty.set_font_settings('AIAA_scitech'))

##############################################################################################################################################################################################################################################################################
####################################    Necessary input information    #######################################################################################################################################################################################################
##############################################################################################################################################################################################################################################################################
freq='1P'

DesignVar_list=['R','DELTA-R','DELTA-MIN','PHI-1P','A-1P','PHI-2P','A-2P']#,'PHI-3P','A-3P','PHI-4P','A-4P','PHI-5P','A-5P'] #There need to be atleast 3 variables here

Data_dir = f'/home/HT/ge56beh/Work/AIAA_scitech_data/CII_{freq}'
All_filepath_dict,All_filenames_dict = crawler.get_files_info(Data_dir)
All_data_dict,DesignVar_ranges_dict = crawler.get_cii_output(Data_dir,All_filepath_dict,All_filenames_dict,Read_pckl=True,DesignVar=DesignVar_list)    
Vib_power_dict = cii.vib_power(All_data_dict)

WOPWOP_data_dir=f'/home/HT/ge56beh/Work/AIAA_scitech_data/PSU_WOPWOP/{freq}/out_of_plane'
All_folderpath_dict,All_foldernames_dict = crawler.get_wopwop_files_info(WOPWOP_data_dir)
All_data_dict_wopwop = crawler.get_wopwop_output(WOPWOP_data_dir,All_folderpath_dict,All_foldernames_dict,Read_pckl=True)
Vib_power_noise_dict=Vib_power_dict.copy()
for mu,filenames in Vib_power_dict.items():
    for filename in filenames:       
        Vib_power_noise_dict[mu][filename]['OASPL-A']=All_data_dict_wopwop[mu][filename][0][3]
        Vib_power_noise_dict[mu][filename]['delta_OASPL-A%']=(All_data_dict_wopwop[mu][filename][0][3]-All_data_dict_wopwop[mu]['Baseline'][0][3])*100/All_data_dict_wopwop[mu]['Baseline'][0][3]
        Vib_power_noise_dict[mu][filename]['delta_OASPL-A']=All_data_dict_wopwop[mu][filename][0][3]-All_data_dict_wopwop[mu]['Baseline'][0][3]

Var_1=f'A-{freq}'    #this variable is kept constant for one sweep of VAR_2; name based on that used in Design_variables
Var_2=f'PHI-{freq}'    #sweep variable


# Plot_amps={'A-1P':[1.0,2.0,3.0],'A-2P':[0.25,0.75,1.0]}
# Plot_amps={'A-1P':[0.5,1.0,1.5],'A-2P':[0.25,0.75,1.0]}
Plot_amps={'A-1P':[0.0,1.0,1.5],'A-2P':[0.25,0.75,1.0]}
DIRECTORY_SAVE_PLOTS=Data_dir+'/figures'

    ###############################################################################################################
    ####     Plotting all the parametric sweep figures (take note of figure and subplot titles for details)    ####
    ###############################################################################################################
Axislabel_size=21
Ticklabel_size=15
Legend_size=21
LABELS={'mu':r'$\mu$','CP':r'$C_P$','P':r'$P_{HP}$','CPS':r'$C_P/\sigma$','Fx':r'$F_X$ [N]',
        'Fy':r'$F_Y$ [N]','Fz':r'$F_Z$ [N]','Mx':r'$M_X$ [Nm]','My':r'$M_Y$ [Nm]','Mz':r'$M_Z$ [Nm]',
          'In-plane Hub Moment': 'Hub Moment','Hub Shear':'Hub Shear','J':r'$J$','J_Mz':r'$J+Mz$',
          'Torsion':'Torsion Bending Moment [Nm]','Flap':'Flap Bending Moment [Nm]','Lag':'Lag Bending Moment [Nm]',
          'Axial':'Axial Tension Force [N]','Chord':'Chordwise Shear Force [N]','Norm':'Flapwise Shear Force [N]',
          'A-1P':r'$A_{1P}$','PHI-1P':r'$\phi_{1P}$','A-2P':r'$A_{2P}$','PHI-2P':r'$\phi_{2P}$',
          'delta_CP%':r'$\Delta C_P [\%]$','delta_J%':r'$\Delta J [\%]$','delta_OASPL-A%':r'$\Delta dB [\%]$','delta_OASPL-A':r'$\Delta$'+'dB',
          'delta_Fz%':r'$\Delta F_{4Z} [\%]$','delta_Fy%':r'$\Delta F_{4Y} [\%]$','delta_Fx%':r'$\Delta F_{4X} [\%]$',
          'delta_Mz%':r'$\Delta M_{4Z} [\%]$','delta_My%':r'$\Delta M_{4Y} [\%]$','delta_Mx%':r'$\Delta M_{4X} [\%]$',
          'delta_In_plane_Hub_Shear%':r'$\Delta Shear [\%]$','delta_In_plane_Hub_Moment%':r'$\Delta Moment [\%]$'}
force_perc=300
mom_perc=300
Limits={'Fx':[],'Fy':[],'Fz':[],'Mx':[],'My':[],'Mz':[],'In-plane Hub Moment': [],'In-plane Hub Shear':[],
        'J':[0,10],'J_Mz':[0,10],
        'CP':[0.0003,0.00055],'mu':[0,0.4],
        'delta_CP%':[-10,20],'delta_J%':[-100,400],'delta_OASPL-A%':[-25,25],'delta_OASPL-A':[-10,10],
        'delta_Fz%':[-100,force_perc],'delta_Fy%':[-100,force_perc],'delta_Fx%':[-100,force_perc],
        'delta_Mz%':[-100,mom_perc],'delta_My%':[-100,mom_perc],'delta_Mx%':[-100,mom_perc],
        'delta_In_plane_Hub_Shear%':[-100,force_perc],'delta_In_plane_Hub_Moment%':[-100,mom_perc],
        'PHI-1P':[0,360],'PHI-2P':[0,360],
        'Torsion':[-300,400],'Flap':[],'Lag':[],'Axial':[],'Chord':[],'Norm':[-400,450],'Delta_Torsion':[-250,150],
        'Delta_Flap':[],'Delta_Lag':[],'Delta_Axial':[],'Delta_Chord':[],'Delta_Norm':[]}

Ticks_number={'delta_CP%':7,'delta_J%':6,'PHI-2P':7,'PHI-1P':7,'delta_OASPL-A%':5,'delta_OASPL-A':5,
              'delta_Fz%':7,'delta_Fy%':7,'delta_Fx%':7,'delta_Mz%':7,'delta_My%':7,'delta_Mx%':7,
              'delta_In_plane_Hub_Shear%':7,'delta_In_plane_Hub_Moment%':7}
COLORS=['blue','red','green','darkorange','limegreen','gold','gray','dimgray','dodgerblue','limegreen','teal','burlywood', 'plum', 'lightblue', 'peru','greenyellow'] # CHOOSE FROM THIS LIST obtained from--> https://matplotlib.org/gallery/color/named_colors.html
LIMITS_percent={'CP':[-4,10],'Fx':[],'Fy':[],'Fz':[],'Mx':[],'My':[],'Mz':[],'In-plane Hub Moment': [],'In-plane Hub Shear':[],'J':[-100,300],'J_abs':[],'J_Mz':[]}

# Var_3='delta_OASPL-A'            #Z-axis; 
# Var_3='delta_J%'
# Var_3='delta_CP%'
Default_set_of_values=['0.700','0.400','2.000','000.0','0.000','0.000','0.000','0.000','0.000','0.000','0.000','0.000','0.000']
# for Var_3 in ['delta_OASPL-A','delta_J%','delta_CP%','delta_Fz%','delta_Fy%','delta_Fx%','delta_Mz%','delta_My%','delta_Mx%']:
for Var_3 in ['delta_OASPL-A','delta_J%','delta_CP%']:
    Fig=plt.figure(figsize=(11, 6))
    Ax = Axes3D(Fig)
    label_show=True
    scatter_label=True
    mu_lst=[]
    marker_size=55
    # Ax.set_prop_cycle(cycler('color', COLORS[0:3]))
    for idx_mu,mu in enumerate(Vib_power_noise_dict):
        # if idx_mu%2==0: continue
        print('mu-->',mu)
        mu_lst.append(float(mu))
        filename_set_of_values = Default_set_of_values.copy()
        color_idx=0
        for amp in DesignVar_ranges_dict[mu][Var_1]:
            if amp not in Plot_amps[Var_1]: continue
            print('amp-->',amp)
            filename_set_of_values[DesignVar_list.index(Var_1)]=format(amp,'.3f') 
            phidata=[]
            quantdata=[]
            for phi in DesignVar_ranges_dict[mu][Var_2]:
                filename_set_of_values[DesignVar_list.index(Var_2)]=format('%05.1f' % phi) 
                filename='_'.join(filename_set_of_values)
                
                if filename_set_of_values==Default_set_of_values: filename='Baseline'
                print('filename-->', filename)
                if filename in Vib_power_noise_dict[mu]: 
                    print('filename-->', filename)
                    phidata.append(phi)
                    quantdata.append(Vib_power_noise_dict[mu][filename][Var_3])
            if phidata:
                phidata.append(360)
                quantdata.append(quantdata[0])
            if label_show: label=LABELS[Var_1]+'='+str(amp)+r'$\degree$'
            print('quantdata-->',quantdata)
            xdata=float(mu)*np.ones_like(phidata)
            # # make_fancy(xdata,phidata,quantdata)
            # # for x,y,z in zip(xdata,phidata,quantdata):
            # #     linestyle='-'
            # #     if z>Vib_power_noise_dict[mu]['Baseline'][Var_3]: linestyle='--'
            # #     Ax.plot(x,y,z,marker='*', linestyle=linestyle)
            
            # linestyl_lst=[]
            # for z_id,z in enumerate(quantdata): 
            #     if z>Vib_power_noise_dict[mu]['Baseline'][Var_3]: linestyl_lst.append('--')  
            #     else: linestyl_lst.append('-')
            #     # Ax.plot(list(xdata)[z_id],list(phidata)[z_id],list(quantdata)[z_id])#,marker='*', linestyle=linestyl_lst[z_id],label=label)
            # Ax.plot(xdata,phidata,quantdata,marker='*', linestyle='-',label=label)        
            x_low,x_high=[],[]
            y_low,y_high=[],[]
            z_low,z_high=[],[]
            for z_id,z in enumerate(quantdata): 
                if z<Vib_power_noise_dict[mu]['Baseline'][Var_3]: 
                    x_low.append(xdata[z_id])
                    y_low.append(phidata[z_id])
                    z_low.append(quantdata[z_id])
                    
                else: 
                    x_high.append(xdata[z_id])
                    y_high.append(phidata[z_id])
                    z_high.append(quantdata[z_id])
            if scatter_label:
                label1=LABELS[Var_3]+'>0'
                label2=LABELS[Var_3]+'<0'
            else:
                label1=None
                label2=None
            Ax.scatter(x_low, y_low,z_low, c=COLORS[color_idx],s=marker_size,alpha=1, edgecolor=COLORS[color_idx], facecolors='none')    
            Ax.scatter(x_high, y_high,z_high,c=COLORS[color_idx], marker='+',s=marker_size+35,alpha=1)
            if scatter_label:
                Ax.scatter(np.nan,np.nan, marker='+',color='black',label=LABELS[Var_3]+' > 0')
                Ax.scatter(np.nan,np.nan, color='black',  alpha=1,label=LABELS[Var_3]+' < 0')
                l1=Ax.legend(loc='upper left', bbox_to_anchor=(0.1,0.7), prop={'size': Legend_size})
            scatter_label=False
            
            Ax.plot(xdata,phidata,quantdata, linestyle='-',label=label,color=COLORS[color_idx],linewidth=0.5,alpha=1)
            color_idx=color_idx+1
        label_show=False
        label=None
    
     
    Ax.set_xlabel(LABELS['mu'],labelpad=15, fontsize=Axislabel_size)
    Ax.set_ylabel(LABELS[Var_2]+' ['+r'$\degree$'+']',labelpad=25, fontsize=Axislabel_size)
    Ax.set_zlabel(LABELS[Var_3],labelpad=15, fontsize=Axislabel_size)
    Ax.set_xlim(lim for lim in Limits['mu'])
    Ax.set_ylim(lim for lim in Limits[Var_2])
    Ax.set_zlim(lim for lim in Limits[Var_3])
    Ax.set_xticks([0.0,0.1,0.2,0.3,0.4])
    Ax.set_yticks(np.linspace(Limits[Var_2][0],Limits[Var_2][1],Ticks_number[Var_2]))
    Ax.set_zticks(np.linspace(Limits[Var_3][0],Limits[Var_3][1],Ticks_number[Var_3]))
    Ax.zaxis.set_rotate_label(False) 
    Ax.yaxis.set_rotate_label(False) 
    Ax.xaxis.set_rotate_label(False) 
    for t in Ax.xaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
    for t in Ax.yaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
    for t in Ax.zaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
    # Ax.tick_params(axis='z', which='major', pad=5)
    Ax.view_init(elev=35,azim=-70)
    if Var_3=='delta_OASPL-A': Ax.view_init(elev=45,azim=-72)
    # above_zero=Ax.scatter(np.nan,np.nan,np.nan, marker='*',s=24,  alpha=1, color='black',label='adfhjasdf')
    # below_zero=Ax.scatter(np.nan,np.nan,np.nan, edgecolor='black',  alpha=1, facecolors='none',s=24)
    l2=Ax.legend(loc='upper left', bbox_to_anchor=(0.0,0.9), prop={'size': Legend_size})
    for handle in l2.legendHandles[:3]: handle.set_linewidth(2)
    for handle in l2.legendHandles[3:]: handle.set_sizes(np.array([marker_size+75]))
    
    # l2=Ax.legend([above_zero,below_zero],[LABELS[Var_3]+'>0',LABELS[Var_3]+'<0'])
    # Ax.add_artist(l1)
    # xx,yy=np.meshgrid(mu_lst,phidata)
    # Ax.plot_surface(xx, yy, 0*np.ones_like(xx), alpha=0.2)
    
    figname=f'mu_{Var_3}_{Var_1}_all_A0_2'
    Fig.savefig(DIRECTORY_SAVE_PLOTS+'/'+figname.replace("%", "perc")+'.pdf', bbox_inches='tight', facecolor=Fig.get_facecolor(), transparent=True)
    print('saved: ', figname)
    plt.close(Fig)
        
