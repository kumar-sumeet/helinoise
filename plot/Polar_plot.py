#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 14:45:19 2019

@author: SumeetKumar
"""
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')
#plt.ioff()
import matplotlib as mpl
import matplotlib.colors as colors
import scipy.interpolate
from math import pi as pi
import matplotlib.ticker

# import make_pretty

class OOMFormatter(matplotlib.ticker.ScalarFormatter):
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

def pcolormesh_plot_smooth(Fig,Ax,Key,Xdata,Ydata,Zdata,Limits,Tick_details):
    if not Tick_details:    Tick_details=[0]                                     #if Tick_details were not explicitly provided in PLOT_LIMITS then a default value is assumed 
    Xdata=[(pi/180)*float(i) for i in Xdata]
    Ydata=[float(i) for i in Ydata]    
    r, theta = np.meshgrid(Ydata, Xdata)        
    f = scipy.interpolate.interp2d(Ydata, Xdata, Zdata, kind='cubic')    
    Xdata_new=np.arange(min(Xdata), max(Xdata)+1.5*pi/180, 1.5*pi/180)                            
    Ydata_new=np.arange(min(Ydata), max(Ydata)+0.01, 0.01)    
    r_new,theta_new=np.meshgrid(Ydata_new, Xdata_new) 
    Zdata_new=f(Ydata_new,Xdata_new)      
    extension='neither'
    if Limits:
        v=(np.linspace(Limits[0],Limits[1],7,endpoint=True)).tolist()
        pcm=Ax.pcolormesh(theta_new,r_new,Zdata_new,cmap='jet',shading='gouraud',vmin=Limits[0],vmax=Limits[1])
#        cb=Fig.colorbar(pcm, ax=Ax, ticks=v, format=OOMFormatter(Tick_details[0], mathText=True),extend=extension)
    else:
        pcm=Ax.pcolormesh(theta_new,r_new,Zdata_new,cmap='jet',shading='gouraud')
#        cb=Fig.colorbar(pcm, ax=Ax, format=OOMFormatter(Tick_details[0], mathText=True),extend=extension)
    Ax.set_title(Key, fontsize=9,fontweight='bold',y=1.15)       #Shifting the subplot title to not overlap with the azimuth  value displayed    
    Ax.set_yticklabels([])                                #Removing the radial ticks

def pcolormesh_plot(Fig,Ax,Key,Xdata,Ydata,Zdata,Limits,Tick_details):
    if not Tick_details:    Tick_details=[0]                                     #if Tick_details were not explicitly provided in PLOT_LIMITS then a default value is assumed 
    Xdata=[(3.14/180)*float(i) for i in Xdata]
    Ydata=[float(i) for i in Ydata]    
    r, theta = np.meshgrid(Ydata, Xdata)    
    extension='neither'
    if Limits:
        v=(np.linspace(Limits[0],Limits[1],7,endpoint=True)).tolist()
        pcm=Ax.pcolormesh(theta,r,Zdata,cmap='jet',shading='gouraud',vmin=Limits[0],vmax=Limits[1])
        # cb=Fig.colorbar(pcm, ax=Ax, ticks=v, format=OOMFormatter(Tick_details[0], mathText=True),extend=extension)
    else:
        pcm=Ax.pcolormesh(theta,r,Zdata,cmap='jet',shading='gouraud')
        # cb=Fig.colorbar(pcm, ax=Ax, format=OOMFormatter(Tick_details[0], mathText=True),extend=extension)
    Ax.set_title(Key, fontsize=9,fontweight='bold',y=1.15)       #Shifting the subplot title to not overlap with the azimuth  value displayed    
    Ax.set_yticklabels([])                                #Removing the radial ticks

def save_this_subplot_as_fig(Figure_name,Xdata,Ydata,Zdata,Limits,Tick_details,Directory,Colorbar_label,conf='AIAA_scitech'):
    Colorbar_label_fontsize=28
    Colorbar_ticklabel_size=21
    Ticklabel_size=21
    padding=0.1
    # Fig=plt.figure(figsize=make_pretty.set_size(conf))
    Fig=plt.figure()
    Ax=Fig.add_subplot(1,1,1,projection='polar')
    use_format=None
#    if not Tick_details:    use_format=None                                     #if Tick_details were not explicitly provided in PLOT_LIMITS then a default value is assumed 
#    else:  use_format=OOMFormatter(Tick_details[0], mathText=True)
    Xdata=[(3.14/180)*i for i in Xdata]
    Ydata=[float(i) for i in Ydata]                         #since 'POSITION_SENSORS' radial stations are stored as strings
    f = scipy.interpolate.interp2d(Ydata, Xdata, Zdata, kind='linear')    
    Xdata=np.linspace(min(Xdata), max(Xdata), 1*len(Xdata),endpoint=True)                            
    Ydata=np.linspace(min(Ydata), max(Ydata), 1*len(Ydata),endpoint=True)   
    r,theta=np.meshgrid(Ydata, Xdata) 
    Zdata=f(Ydata,Xdata)      
    
####    Colorbar extension based on the fact that the prescribed limits don not sufficiently cover the entire range of Zdata    
    extension='neither'
    if Limits:
        if np.amax(Zdata)>Limits[1]:    extension='max'
        if np.amin(Zdata)<Limits[0]:    extension='min'
        if np.amax(Zdata)>Limits[1] and np.amin(Zdata)<Limits[0]:    extension='both'

    if Figure_name=='ALPHA': extension='both'
    if Limits:
        norm = mpl.colors.Normalize(vmin=Limits[0],vmax=Limits[1])
        pcm=Ax.pcolormesh(theta,r,Zdata,cmap='jet',shading='gouraud',vmin=Limits[0],vmax=Limits[1])
        cb=Fig.colorbar(pcm, ax=Ax,norm=norm, format=use_format, pad=padding,extend=extension)
    else:
        pcm=Ax.pcolormesh(theta,r,Zdata,cmap='jet',shading='gouraud')
        cb=Fig.colorbar(pcm, ax=Ax, format=use_format, pad=padding,extend=extension)
    
    if '[deg]' in  Colorbar_label:    
        cb_ticks = cb.ax.get_yticklabels()                  #returns a list of objects (not float or str)
        cb_ticks = [tick.get_text() for tick in cb_ticks]
        cb_ticks_new=[tick+r"$^\circ$" for tick in cb_ticks] #Adding degrees symbol to the colorbar ticks
        cb.ax.set_yticklabels(cb_ticks_new)
        Colorbar_label=Colorbar_label.replace(' [deg]','')    #removing '[deg]' from colorbar label
    cb.ax.tick_params(labelsize=Colorbar_ticklabel_size) 
    if Tick_details: cb.ax.yaxis.offsetText.set(size=Colorbar_ticklabel_size)
    if 'MINUS_BASELINE' in Directory: 
        if '+' in Figure_name:
            Colorbar_label=r'$\Delta$'+'('+Colorbar_label+')'
        elif Figure_name=='FLAP_DEFLECTION_ANGLE':                  #when generating plot for flap deflection angle just keep the colorlabel without adding delta
            pass
        else:
            Colorbar_label=r'$\Delta$'+Colorbar_label                    #Adding a delta symbol to the label if the plot corrresponds to a delta quantity    
    cb.set_label(Colorbar_label,fontsize=Colorbar_label_fontsize,labelpad=10)#,fontweight='bold')
    
    # Ax.set_theta_zero_location("SW")
    #Ax.set_xticks([0,90,180,270])
    #Ax.set_xticklabels([r'$0^\circe$',r'$90^\circ$',r'$180^\circ$',r'$270^\circ$'])
    Ax.tick_params(axis='x', labelsize=Ticklabel_size,pad=15)
    Ax.set_yticklabels([])                                #Removing the radial ticks
    Fig.savefig(Directory+'/'+Figure_name+'.pdf')
    Fig.savefig(Directory+'/'+Figure_name+'.png')
    print('saved: ', Figure_name)
    plt.close(Fig)

def save_stress_as_fig(Fig,Ax,Figure_name,Xdata,Ydata,Zdata,Limits,Tick_details,Directory,Colorbar_label):
    print('1')
    Colorbar_label_fontsize=17
    Colorbar_ticklabel_size=13
    Ticklabel_size=13
    padding=0.1
    #Fig=plt.figure()
    #Ax=Fig.add_subplot(1,1,1,projection='polar')
    if not Tick_details:    use_format=None                                     #if Tick_details were not explicitly provided in PLOT_LIMITS then a default value is assumed 
    else:  use_format=OOMFormatter(Tick_details[0], mathText=True)
    Xdata=[(3.14/180)*i for i in Xdata]
    Ydata=[float(i) for i in Ydata]                         #since 'POSITION_SENSORS' radial stations are stored as strings
    f = scipy.interpolate.interp2d(Ydata, Xdata, Zdata, kind='linear')    
    Xdata=np.linspace(min(Xdata), max(Xdata), 10*len(Xdata),endpoint=True)                            
    Ydata=np.linspace(min(Ydata), max(Ydata), 10*len(Ydata),endpoint=True)   
    r,theta=np.meshgrid(Ydata, Xdata) 
    Zdata=f(Ydata,Xdata)      
    print('1')
    
####    Colorbar extension based on the fact that the prescribed limits don not sufficiently cover the entire range of Zdata    
    extension='neither'
    if Limits:
        if np.amax(Zdata)>Limits[1]:    extension='max'
        if np.amin(Zdata)<Limits[0]:    extension='min'
        if np.amax(Zdata)>Limits[1] and np.amin(Zdata)<Limits[0]:    extension='both'
    print('1')

    if Figure_name=='ALPHA': extension='both'
    if Limits:
        norm = mpl.colors.Normalize(vmin=Limits[0],vmax=Limits[1])
        pcm=Ax.pcolormesh(theta,r,Zdata,cmap='jet',shading='gouraud',vmin=Limits[0],vmax=Limits[1])
        cb=Fig.colorbar(pcm, ax=Ax,norm=norm, format=use_format, pad=padding,extend=extension)
    else:
        pcm=Ax.pcolormesh(theta,r,Zdata,cmap='jet',shading='gouraud')
        cb=Fig.colorbar(pcm, ax=Ax, format=use_format, pad=padding,extend=extension)
    print('1')
    
    if '[deg]' in  Colorbar_label:    
        cb_ticks = cb.ax.get_yticklabels()                  #returns a list of objects (not float or str)
        cb_ticks = [tick.get_text() for tick in cb_ticks]
        cb_ticks_new=[tick+r"$^\circ$" for tick in cb_ticks] #Adding degrees symbol to the colorbar ticks
        cb.ax.set_yticklabels(cb_ticks_new)
        Colorbar_label=Colorbar_label.replace(' [deg]','')    #removing '[deg]' from colorbar label
    cb.ax.tick_params(labelsize=Colorbar_ticklabel_size) 
#    if Tick_details: cb.ax.yaxis.offsetText.set(size=Colorbar_ticklabel_size)
    if 'MINUS_BASELINE' in Directory: 
        if '+' in Figure_name:
            Colorbar_label=r'$\Delta$'+'('+Colorbar_label+')'
        elif Figure_name=='FLAP_DEFLECTION_ANGLE':                  #when generating plot for flap deflection angle just keep the colorlabel without adding delta
            pass
        else:
            Colorbar_label=r'$\Delta$'+Colorbar_label                    #Adding a delta symbol to the label if the plot corrresponds to a delta quantity    
    cb.set_label(Colorbar_label,fontsize=Colorbar_label_fontsize)#,fontweight='bold')
    
    #Ax.set_xticks([0,90,180,270])
    #Ax.set_xticklabels([r'$0^\circ$',r'$90^\circ$',r'$180^\circ$',r'$270^\circ$'])
    Ax.tick_params(axis='x', labelsize=Ticklabel_size)
    Ax.set_yticklabels([])                                #Removing the radial ticks
    Fig.savefig(Directory+'/'+Figure_name+'.png')
    #print(Figure_name)
    plt.close(Fig)

