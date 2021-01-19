#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 13:21:51 2021

@author: ge56beh
"""

def get_labels_dict():
    return {
            'mu':r'$\mu$',
            'CP':r'$C_P$','P':r'$P_{HP}$','CPS':r'$C_P/\sigma$',
            'Fx':r'$F_X$ [N]','Fy':r'$F_Y$ [N]','Fz':r'$F_Z$ [N]',
            'Mx':r'$M_X$ [Nm]','My':r'$M_Y$ [Nm]','Mz':r'$M_Z$ [Nm]',
            'In-plane Hub Moment': 'Hub Moment','Hub Shear':'Hub Shear',
            'J':r'$J$','J_Mz':r'$J+Mz$',
            'Torsion':'Torsion Bending Moment [Nm]','Flap':'Flap Bending Moment [Nm]','Lag':'Lag Bending Moment [Nm]',
            'Axial':'Axial Tension Force [N]','Chord':'Chordwise Shear Force [N]','Norm':'Flapwise Shear Force [N]',
            'delta_CP%':r'$\Delta C_P [\%]$','delta_J%':r'$\Delta J [\%]$',
            'delta_Mz%':'Torque','delta_Fz%':'Lift','delta_In_plane_Hub_Shear%':'Shear','delta_In_plane_Hub_Moment%':'Moment',
            'A-1P':r'$A_{1P}$','PHI-1P':r'$\phi_{1P}$','A-2P':r'$A_{2P}$','PHI-2P':r'$\phi_{2P}$'
            }

def get_limits_dict():
    return {
            'mu':[0,0.4],
            'CP':[0.0003,0.00055],
            'Fx':[],'Fy':[],'Fz':[],
            'Mx':[],'My':[],'Mz':[],
            'In-plane Hub Moment': [],'In-plane Hub Shear':[],
            'J':[0,10],'J_Mz':[0,10],
            'Torsion':[-300,400],'Flap':[],'Lag':[],'Axial':[],'Chord':[],'Norm':[-400,450],
            'Delta_Torsion':[-250,150],'Delta_Flap':[],'Delta_Lag':[],'Delta_Axial':[],'Delta_Chord':[],'Delta_Norm':[],            
            'delta_CP%':[-10,20],'delta_J%':[-100,400],
            'delta_Mz%':[-70,70],'delta_Fz%':[-70,70],'delta_In_plane_Hub_Shear%':[-70,70],'delta_In_plane_Hub_Moment%':[-70,70],
            'PHI-1P':[0,360],'PHI-2P':[0,360]
            }
        
def get_colors_lst():
    return ['blue','red','green','black','darkorange','gray','limegreen','plum', 'blue','dimgray','dodgerblue','limegreen','teal','burlywood', 'gold', 'peru','greenyellow'] # CHOOSE FROM THIS LIST obtained from--> https://matplotlib.org/gallery/color/named_colors.html

def get_dimcolors_lst():
    return ['lightcoral','lightgreen','silver','bisque','lightgrey'] # CHOOSE FROM THIS LIST obtained from--> https://matplotlib.org/gallery/color/named_colors.html
