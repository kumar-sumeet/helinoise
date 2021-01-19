#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 16:43:01 2019

@author: SumeetKumar
"""
 
import matplotlib.pyplot as plt

def scatter_plot(Fig,Ax,Xdata,Ydata,color,Labl,Baseline_rotor_power):
    Sc=Ax.scatter(Xdata, Ydata, c=color, label=Labl, alpha=0.65)       #alpha=1.0 for opaque points
    Ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    Ax.set_xlabel(r'ALL FILES $\longrightarrow$',fontweight='bold')
    Ax.set_ylabel('ROTOR POWER (HP)',fontweight='bold')   
    
    #Adding horizontal line corresponding to Baseline 
    Ax.axhline(y=Baseline_rotor_power, color='k', linestyle='--', linewidth=2.0)
    plt.show()
    return Sc

def save_this_subplot_as_fig(Fig_name,Xdata,Ydata,Labl,color,Dir):    
    Fig=plt.figure()
    Ax=Fig.add_subplot(1,1,1)
    Ax.scatter(Xdata, Ydata, c=color, label=Labl, alpha=0.65)       #alpha=1.0 for opaque points
    
    Fig.savefig(Dir+'/'+Fig_name+'.png')
    print('saved: ', Fig_name)
    plt.close(Fig)

