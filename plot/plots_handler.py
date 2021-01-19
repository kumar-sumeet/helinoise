#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 10:40:05 2020

@author: ge56beh
"""

import os

import threeDSurface_plot 

def save_figures_surface(FIG_CLICK,AX_CLICK,DATA_CLICK):
    print('\n\n\n ')
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
                    threeDSurface_plot.save_this_subplot_as_fig(title,xdata,ydata,zdata,limits,tick_details,Directory_save_file_to_surface,LABELS[title])
            else:
                continue

def save_figures_polar(FIG_CLICK,AX_CLICK,DATA_CLICK):
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
                    Directory_save_file_to_polar=DIRECTORY_SAVE_PLOTS+'/'+'Polar_plots'+'/'+fig
                    try:
                        os.makedirs(Directory_save_file_to_polar)
                    except FileExistsError:
                        pass                # directory already exists                   
                    Polar_plot.save_this_subplot_as_fig(title,xdata,ydata,zdata,limits,tick_details,Directory_save_file_to_polar,LABELS[title])
            else:
