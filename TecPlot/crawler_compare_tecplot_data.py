#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Used to generate and compare acoustic results for a number of cases in 
Cases_dict


****Needs extensive cleaning****

"""

import numpy as np
import matplotlib.pyplot as plt
# plt.style.use('seaborn')
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
import matplotlib.animation as animation

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from plot import Three_D_plot, make_pretty
from TecPlot import read_wopwop_tecfile
    
plt.rcParams.update(make_pretty.set_font_settings('AIAA_scitech'))


rot_freq_hz = 4*7.083349897247894   #Bo 105 BPF                               
#rot_freq_hz = 4*109.028/(2*np.pi)   #HART II BPF                              

Main_dir=f'../Data/PSU_WOPWOP/PSU_WOPWOP_new/SingleObserver_50m'
Cases_dict = {
            'Baseline':'baseline_highresAero_hartstyl',
            '1P':'0.700_0.400_3.160_278.0_2.440_0.0_0.0_0.0_0.0_0.0_0.0_0.0_0.0_highresAero_hartstyl',
            '2P':'0.750_0.300_1.960_000.0_0.000_355.0_0.980_0.0_0.0_0.0_0.0_0.0_0.0_highresAero_hartstyl',
            '1P+2P':'0.700_0.400_3.100_322.0_3.530_267.0_1.116_0.0_0.0_0.0_0.0_0.0_0.0_highresAero_hartstyl',
             }
Limits={'in_plane':{'pressure':{'X':[0.0,0.1412/4],'Y':[-6.0,4.0]},
                    'spl_spectrum':{'X':[0.0,2500],'Y':[-30,100]},
                    'OASPL':{'X':[],'Y':[10,90]}
                    },
        'out_of_plane':{'pressure':{'X':[0.0,0.1412/4],'Y':[-6.0,4.0]},
                    'spl_spectrum':{'X':[0.0,2500],'Y':[-30,100]},
                    'OASPL':{'X':[],'Y':[10,90]}
                    },
        'below':{'pressure':{'X':[0.0,0.1412/4],'Y':[-6.0,4.0]},
                    'spl_spectrum':{'X':[0.0,2500],'Y':[-30,100]},
                    'OASPL':{'X':[],'Y':[10,90]}
                    },
        }
Xlabels={'pressure':r'$t$'+' [s]',
         'spl_spectrum':'Frequency [Hz]',
         'OASPL':'OASPL-A[dB]',
        }
Ylabels = {'pressure':'Acoustic \n Pressure [Pa]',
           'spl_spectrum':'Sound Pressure Level [dB]',
           'OASPL':'OASPL-A[dB]'
           }

Fig_3d_bar=plt.figure(figsize=(11.5, 6))
Ax_3d_bar = Axes3D(Fig_3d_bar)
Locations=['in_plane','out_of_plane','below']
drag_or_lift='' # enter 'drag' or 'lift' if just need to accoust for acoustic footpprint due to drag forces or lift forces only
for idx_loc,loc in enumerate(Locations):
    
            
    Quantities_1=['Thickness','Loading','Total']
    Quantities_2=['pressure', 'spl_spectrum']
    # Plot_together = True
    # Plot_separately = True                                                             #plot all quantities in one plot
    # Frequency_in_bpf = True
    # if Frequency_in_bpf: 
    #     Xlabels.update({'spl_spectrum':'Blade Passage Frequency'})
    #     Limits.update({'in_plane':{'spl_spectrum':{'X':[0,50],'Y':[-30,100]}},
    #                    'out_of_plane':{'spl_spectrum':{'X':[0,50],'Y':[-30,100]}},
    #                    'below':{'spl_spectrum':{'X':[0,50],'Y':[-30,100]}}                  
    #                    })
    # Time_in_azimuth = False
    # if Time_in_azimuth: Xlabels.update({'pressure':r'$\psi$'})
    
    # fontsize_dict={'Axislabel_size':10,'Ticklabel_size':10,'Legend_size':9}
    ###############################################################################
    
    Fig_3d_p=plt.figure(figsize=(11.5, 6))
    Fig_2d_p=plt.figure(figsize=make_pretty.set_size('AIAA_scitech',fraction=0.5))
    Ax_2d_p=Fig_2d_p.add_subplot(1,1,1)
    # Ax_3d_p = Fig_3d_p.gca(projection='3d')
    Ax_3d_p = Axes3D(Fig_3d_p)
    COLORS=['blue','red','green','black'] # CHOOSE FROM THIS LIST obtained from--> https://matplotlib.org/gallery/color/named_colors.html
    # COLORS=['#4C72B0', '#55A868', '#C44E52', '#8172B2', '#CCB974', '#64B5CD']
    for idx,quantity_1 in enumerate(Quantities_1,1):

        Fig_p = plt.figure(figsize=make_pretty.set_size('AIAA_scitech',fraction=0.5))
        Ax_p = Fig_p.add_subplot(1,1,1)
        Data_OASPLdBA = []
        for case_idx,label in enumerate(Cases_dict):
            filename_pressure=f'{Main_dir}/{loc}/{Cases_dict[label]}/{Cases_dict[label]}/{drag_or_lift}pressure.tec'
            filename_OASPLdBA=f'{Main_dir}/{loc}/{Cases_dict[label]}/{Cases_dict[label]}/{drag_or_lift}OASPLdBA.tec'
            
            Data_pressure = read_wopwop_tecfile.p_spl(filename_pressure)
            Data_OASPLdBA.append(read_wopwop_tecfile.dB(filename_OASPLdBA)[0])
            xdata_p=Data_pressure[:,0]     #this needs to be modified
            ydata_p=Data_pressure[:,idx]
            ylabel_p = 'Acoustic pressure (Pa)'
    
            Ax_p.plot(xdata_p,ydata_p,label=label)
            xdata_p_3d=xdata_p[xdata_p<Limits[loc]['pressure']['X'][1]]
            ydata_p_3d=ydata_p[:np.size(xdata_p_3d)]
            Three_D_plot.three_d_plot(Fig_3d_p,Ax_3d_p,xdata_p_3d,idx*np.ones_like(xdata_p_3d),ydata_p_3d,label,COLORS[case_idx])
            if quantity_1 in ['Thickness','Loading']:
                if quantity_1=='Thickness':
                    linestyle='--'
                else:
                    linestyle='-'
                Ax_2d_p.plot(xdata_p,ydata_p,linestyle=linestyle,color=COLORS[case_idx])
        # Ax_p.legend(frameon=False, prop={'size': fontsize_dict['Legend_size']})
        
    #    Ax_p.set_xlim(min(xdata_p), max(xdata_p)) 
        Ax_p.set_xlim(lim for lim in Limits[loc]['pressure']['X']) 
        Ax_p.set_ylim(lim for lim in Limits[loc]['pressure']['Y']) 
        Ax_p.set_xlabel(Xlabels['pressure'])
        Ax_p.set_ylabel(Ylabels['pressure'])        
        Fig_p.savefig(f'{Main_dir}/{loc}/{quantity_1}_{drag_or_lift}Pressure.pdf', bbox_inches='tight')
    
    Ax_2d_p.plot([],[],label='Thickness',linestyle='--',color='black')
    Ax_2d_p.plot([],[],label='Loading',linestyle='-',color='black')
    Ax_2d_p.set_xlim(lim for lim in Limits[loc]['pressure']['X']) 
    Ax_2d_p.set_ylim(lim for lim in Limits[loc]['pressure']['Y']) 
    Ax_2d_p.set_xlabel(Xlabels['pressure'])
    Ax_2d_p.set_ylabel(Ylabels['pressure'])      
    Ax_2d_p.legend()
    Ax_2d_p.grid()
        
        
    Axislabel_size=21
    Ticklabel_size=15
    Legend_size=15    
    Ax_3d_p.set_xlabel(Xlabels['pressure'],labelpad=15, fontsize=Axislabel_size)
    # Ax_3d_p.set_zlabel(Ylabels['pressure'],labelpad=15, fontsize=Axislabel_size)
    Ax_3d_p.text(0.035,2.5,12, Ylabels['pressure'], fontsize=Axislabel_size)
    
    Ax_3d_p.set_xlim(lim for lim in Limits[loc]['pressure']['X'])
    Ax_3d_p.set_zlim(2*lim for lim in Limits[loc]['pressure']['Y'])
    # Ax.set_zticks(np.linspace(Limits[f'delta_{Var_3}%'][0],Limits[f'delta_{Var_3}%'][1],Ticks_number[f'delta_{Var_3}%']))
    Ax_3d_p.set_yticks(1+np.arange(len(Quantities_1)))
    Ax_3d_p.set_yticklabels(Quantities_1)
    Ax_3d_p.zaxis.set_rotate_label(False) 
    Ax_3d_p.zaxis.set_label_coords(1.0, 1.0,2.1)
    Ax_3d_p.yaxis.set_rotate_label(False) 
    Ax_3d_p.xaxis.set_rotate_label(False) 
    Ax_3d_p.tick_params(axis='y', which='major', labelsize=Ticklabel_size+4)
    for t in Ax_3d_p.xaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
    # for t in Ax_3d_p.yaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
    for t in Ax_3d_p.zaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
    # Ax.tick_params(axis='z', which='major', pad=5)
    # Ax_3d.legend(loc='upper left', bbox_to_anchor=(0.1,0.9), prop={'size': Legend_size})
    Fig_3d_p.savefig(f'{Main_dir}/{loc}_{drag_or_lift}Pressure_3d.pdf', bbox_inches='tight', facecolor=Fig_3d_p.get_facecolor(), transparent=True)
    Fig_2d_p.savefig(f'{Main_dir}/{loc}_{drag_or_lift}Pressure_2d.pdf', bbox_inches='tight')
        
    
    Fig_p_bar = plt.figure(figsize=(4,4))
    Ax_p_bar = Fig_p_bar.add_subplot(1,1,1)
    
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            Ax_p_bar.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    
    
    x = np.arange(len(Quantities_1))
    width = 0.05
    Data_OASPLdBA_arr = np.asarray(Data_OASPLdBA)
    for idx_bar,labl in enumerate(Cases_dict):
        xdata_bar=x+(idx_bar-0.5*(len(Cases_dict.keys())-1))*width
        Ax_p_bar.bar(xdata_bar,  Data_OASPLdBA_arr[idx_bar,1:4], width, label=labl,color=COLORS[idx_bar])
        if idx_loc: labl=None #to avoid a mess of repeating labels
        Ax_3d_bar.bar(xdata_bar,Data_OASPLdBA_arr[idx_bar,1:4],width=width,zs=idx_loc,zdir='y', label=labl,color=COLORS[idx_bar])
        # print(Data_OASPLdBA_arr[idx_bar,1:4] )
    Ax_p_bar.set_ylabel(Xlabels['OASPL'])
    Ax_p_bar.set_xticks(x)
    Ax_p_bar.set_xticklabels(Quantities_1)
    Ax_p_bar.legend()
    #Ax_p_bar.set_xlim(lim_p_dict['X'][0], lim_p_dict['X'][1]) 
    Ax_p_bar.set_ylim(lim for lim in Limits[loc]['OASPL']['Y']) 
    # plt.setp(Ax_p_bar.get_xticklabels(), fontweight="bold")
    Fig_p_bar.savefig(f'{Main_dir}/{loc}/{drag_or_lift}OASPLdBA.pdf', bbox_inches='tight')

Axislabel_size=24
Ticklabel_size=21
Legend_size=20
# Ax_3d_bar.set_zlabel(Xlabels['OASPL'],labelpad=15, fontsize=Axislabel_size)
Ax_3d_bar.text(1.4,2.5,72, Xlabels['OASPL'], fontsize=Axislabel_size)
# Ax_3d_bar.text2D(0.85, 0.85, Xlabels['OASPL'], transform=Ax_3d_bar.transAxes)
Ax_3d_bar.set_xticks(x-0.8*width)
Ax_3d_bar.set_xticklabels(Quantities_1)
Ax_3d_bar.tick_params(axis='both', which='major', labelsize=Ticklabel_size)
Ax_3d_bar.set_yticks(1.3*width+np.arange(len(Locations)))
Ax_3d_bar.set_yticklabels(['A (in-plane)','B (out-of-plane)','C (below)'])

# Ax_3d_bar.set_xlim(lim for lim in Limits[loc]['pressure']['X'])
# Ax_3d_bar.set_zlim(10,100)
# Ax_3d_bar.set_ylim(-0.5,3.5)
# Ax_3d_bar.set_zticks(np.linspace(10,100))
Ax_3d_bar.zaxis.set_rotate_label(False) 
Ax_3d_bar.zaxis.set_label_coords(0.9, 1.0,1.1)
Ax_3d_bar.yaxis.set_rotate_label(False) 
Ax_3d_bar.xaxis.set_rotate_label(False) 
for t in Ax_3d_bar.xaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
for t in Ax_3d_bar.yaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
for t in Ax_3d_bar.zaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
# Ax.tick_params(axis='z', which='major', pad=5)

Ax_3d_bar.legend(frameon=False,loc='upper left', bbox_to_anchor=(0.2,0.98), prop={'size': Legend_size})
Ax_3d_bar.view_init(elev=35,azim=-58)

def rotate(angle):
    Ax_3d_bar.view_init(azim=angle)
print("Making animation")
rot_animation = animation.FuncAnimation(Fig_3d_bar, rotate, frames=np.concatenate([np.arange(-60,-55,0.25),-1*np.arange(55,60,0.25)]), interval=100)
rot_animation.save(f'{Main_dir}/{drag_or_lift}rotation.gif', dpi=80, writer='imagemagick')

#Fig_3d_bar.show()

Fig_3d_bar.savefig(f'{Main_dir}/{drag_or_lift}OASPLdBA_3d.pdf', bbox_inches='tight', facecolor=Fig_3d_p.get_facecolor(), transparent=True)

# Ax_3d_bar.view_init(elev=45., azim=-35)  
# Fig_3d_bar.show()  
