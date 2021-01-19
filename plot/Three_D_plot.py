#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  19 11:35:17 2020

@author: SumeetKumar
"""
import matplotlib.pyplot as plt
plt.ioff()
# plt.style.use('seaborn')
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mtick
from mpl_toolkits.mplot3d import Axes3D

def three_d_plot(Fig, Ax, xdata,ydata,zdata,label,c):
    Axislabel_size=21
    Ticklabel_size=18
    Legend_size=18
    
    Ax.plot(xdata,ydata,zdata, linestyle='-',label=label,color=c)
    # Ax.set_xlabel(LABELS['mu'],labelpad=15, fontsize=Axislabel_size)
    # Ax.set_ylabel(LABELS[Var_2]+' ['+r'$\degree$'+']',labelpad=25, fontsize=Axislabel_size)
    # Ax.set_zlabel(LABELS[f'delta_{Var_3}%'],labelpad=15, fontsize=Axislabel_size)
    # Ax.set_xlim(lim for lim in Limits['mu'])
    # Ax.set_ylim(lim for lim in Limits[Var_2])
    # Ax.set_zlim(lim for lim in Limits[f'delta_{Var_3}%'])
    # Ax.set_xticks([0.0,0.1,0.2,0.3,0.4])
    # Ax.set_yticks(np.linspace(Limits[Var_2][0],Limits[Var_2][1],Ticks_number[Var_2]))
    # Ax.set_zticks(np.linspace(Limits[f'delta_{Var_3}%'][0],Limits[f'delta_{Var_3}%'][1],Ticks_number[f'delta_{Var_3}%']))
    # Ax.zaxis.set_rotate_label(False) 
    # Ax.yaxis.set_rotate_label(False) 
    # Ax.xaxis.set_rotate_label(False) 
    # for t in Ax.xaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
    # for t in Ax.yaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
    # for t in Ax.zaxis.get_major_ticks(): t.label.set_fontsize(Ticklabel_size)
    # # Ax.tick_params(axis='z', which='major', pad=5)
    # Ax.legend(loc='upper left', bbox_to_anchor=(0.1,0.9), prop={'size': Legend_size})
   