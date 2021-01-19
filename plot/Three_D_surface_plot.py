#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 10:50:07 2019

@author: SumeetKumar
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
#plt.ioff()
import matplotlib.colors as colors
import matplotlib as mpl
import matplotlib.ticker
import numpy as np
import scipy.interpolate 

class OOMFormatter(matplotlib.ticker.ScalarFormatter):
    """
    adopted from 
    https://stackoverflow.com/questions/43324152/python-matplotlib-colorbar-scientific-notation-base
    """
    def __init__(self, order=0, fformat="%1.1f", offset=True, mathText=True):
        self.oom = order
        self.fformat = fformat
        matplotlib.ticker.ScalarFormatter.__init__(self,useOffset=offset,useMathText=mathText)
    def _set_orderOfMagnitude(self, nothing):
        self.orderOfMagnitude = self.oom
    def _set_format(self, vmin, vmax):
        self.format = self.fformat
        if self._useMathText:
            self.format = '$%s$' % matplotlib.ticker._mathdefault(self.format)


def three_d_surface_plot(Xdata,Ydata,Zdata):
    Ydata=[float(i) for i in Ydata]        #since 'POSITION_SENSORS' radial stations are stored as strings
    Xdata=np.asarray(Xdata)
    Ydata=np.asarray(Ydata) 
    f = scipy.interpolate.interp2d(Ydata, Xdata, Zdata, kind='cubic')    
    Xdata_smooth = np.linspace(min(Xdata), max(Xdata), 1*len(Xdata))               #smoothing the xdata distribution by increasing the resolution to 5 times
    Ydata_smooth = np.linspace(min(Ydata), max(Ydata), 1*len(Ydata))
    r_new,theta_new=np.meshgrid(Ydata_smooth, Xdata_smooth) 
    Zdata_smooth=f(Ydata_smooth,Xdata_smooth)         
    # Make the plot
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf2=ax.plot_surface(r_new,theta_new, Zdata_smooth, cmap=plt.cm.jet, rcount=len(Zdata_smooth), ccount=len(Zdata_smooth[0]))
    ax.set_ylabel('r')
    ax.set_xlabel(r'$\Psi$')
    fig.colorbar( surf2, shrink=0.5, aspect=5)
    # Rotate it
    ax.view_init(30, 220)
        
def save_this_subplot_as_fig(Figure_name,Xdata,Ydata,Zdata,Limits,Tick_details,Directory,Zlabel):  
    padding=-0.05
    axis_labels_fontsize=14
    Fig=plt.figure()
    Ax=Fig.add_subplot(1,1,1,projection='3d')    
    Ydata=[float(i) for i in Ydata]                                #since 'POSITION_SENSORS' radial stations are stored as strings
    Xdata=np.asarray(Xdata)
    Ydata=np.asarray(Ydata) 
    f = scipy.interpolate.interp2d(Ydata, Xdata, Zdata, kind='cubic')    
    Xdata_smooth = np.linspace(min(Xdata), max(Xdata), 10*len(Xdata))               #smoothing the xdata distribution by increasing the resolution to 5 times
    Ydata_smooth = np.linspace(min(Ydata), max(Ydata), 10*len(Ydata))
    r,theta=np.meshgrid(Ydata_smooth, Xdata_smooth) 
    Zdata_smooth=f(Ydata_smooth,Xdata_smooth)      

####    Colorbar extension based on the fact that the prescribed limits don not sufficiently cover the entire range of Zdata    
    extension='neither'
    if Limits:
        if np.amax(Zdata)>Limits[1]:    extension='max'
        if np.amin(Zdata)<Limits[0]:    extension='min'
        if np.amax(Zdata)>Limits[1] and np.amin(Zdata)<Limits[0]:    extension='both'
    use_format=None    
#    if not Tick_details:    use_format=None                                     #if Tick_details were not explicitly provided in PLOT_LIMITS then a default value is assumed 
#    else:  use_format=OOMFormatter(Tick_details[0], mathText=True)
    if Limits:
        norm = mpl.colors.Normalize(vmin=Limits[0],vmax=Limits[1])
        surf=Ax.plot_surface(theta,r,Zdata_smooth,cmap=plt.cm.jet,vmin=Limits[0],vmax=Limits[1], rcount=len(Zdata_smooth), ccount=len(Zdata_smooth[0]))
        cb=Fig.colorbar(surf, shrink=0.5,norm=norm, aspect=20, ax=Ax, format=use_format,extend=extension, pad=padding)
    else:
        surf=Ax.plot_surface(theta,r,Zdata_smooth,cmap=plt.cm.jet, rcount=len(Zdata_smooth), ccount=len(Zdata_smooth[0]))
        cb=Fig.colorbar(surf, shrink=0.5, aspect=20,extend=extension, pad=padding)#, ax=Ax, format=OOMFormatter(Tick_details[0], mathText=True), pad=0.1)
    
####    changing some properties if the quantity being plotted is in degrees
    if '[deg]' in  Zlabel:    
        cb_ticks = cb.ax.get_yticklabels()                  #returns a list of objects (not float or str)
        cb_ticks = [tick.get_text() for tick in cb_ticks]
        cb_ticks_new=[tick+r"$\degree$" for tick in cb_ticks] #Adding degrees symbol to the colorbar ticks
        cb.ax.set_yticklabels(cb_ticks_new)
    Ax.set_ylabel(r'$R$', fontsize=axis_labels_fontsize)
    Ax.yaxis.set_rotate_label(False) 
    Ax.set_xlabel(r'$\psi$', fontsize=axis_labels_fontsize)
    Ax.xaxis.set_rotate_label(False) 
    Ax.zaxis.set_rotate_label(False)
    Ax.set_zlabel(Zlabel, fontsize=axis_labels_fontsize)
#    if Tick_details[0]!=0: 
#        if Tick_details[0]>0:
#            Ax.ticklabel_format(axis='z', style='sci', scilimits=(0,1), useOffset=None, useLocale=None, useMathText=None)
#        else:
#            Ax.ticklabel_format(axis='z', style='sci', scilimits=(-1,0), useOffset=None, useLocale=None, useMathText=None)
    deg_labels=np.linspace(0,360,5,endpoint=True)
    Ax.set_xticks(deg_labels)
    Ax.set_xticklabels([r"${:.0f}\degree$".format(_) for _ in deg_labels])
    zticks=Ax.get_zticks(minor=False)
    zticklabels=[str("{:.1f}".format(tick)) for tick in zticks]
    if '[deg]' in  Zlabel:            
        zticklabels=[ticklabel+r"$\degree$" for ticklabel in zticklabels] #Adding degrees symbol to the Z-axis ticks        
        Zlabel=Zlabel.replace(' [deg]','')    #removing '[deg]' from Z-axis label
        Ax.set_zticklabels(zticklabels)  
        Ax.set_zlabel(Zlabel)
    if 'MINUS_BASELINE' in Directory: Ax.set_zlabel(r'$\Delta$'+Zlabel, labelpad=18)                    #Adding a delta symbol to the label if the plot corrresponds to a delta quantity
    Ax.view_init(30, 220)     # Rotate it
    Fig.savefig(Directory+'/'+Figure_name+'.png')
    print('saved: ', Figure_name)
    plt.close(Fig)
  
