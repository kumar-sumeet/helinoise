#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 13:04:07 2019

@author: SumeetKumar
"""
import numpy as np

def wireframe_plot(Fig,Ax,Title,Xdata,Ydata,Zdata,Limits):
    r, theta = np.meshgrid(Ydata, Xdata)
    Ax.set_title(Title)    
    Ax.plot_wireframe(r,theta,Zdata)