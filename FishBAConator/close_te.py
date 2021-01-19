#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 15.06.2019

@authors: Amine Abdelmoula, Fabian Grimm

Tool for the generation of the coordinates, which close an open trailing edge.
"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
import numpy as np


def close_te_round(x, y, n):
    
    """Generates a trailing edge arc.
    
    Creates the coordinates of an arc, which closes the open trailing edge 
    of an airfoil. This arc is tangential to the ending upper and lower 
    surface lines.
    
    Args:
        x: List of x-coordinates of the airfoil surface (counterclockwise 
            starting above the trailing edge).
        y: List of y-coordinates of the airfoil surface (counterclockwise 
            starting above the trailing edge).
        n (int): number of points on the arc
    
    Returns:
        Dictionary containing the following data:
            'x': List of x-coordinates of the arc (counterclockwise)
            'y': List of y-coordinates of the arc (counterclockwise)
        
    """
    
    # ------------------------------ CALCULATION ------------------------------
    
    # taper of the trailing edge, needed for the arc to be tangential
    taper_te_rad = np.arctan((y[-1] - y[-2]) / (x[-1] - x[-2]) 
                              - (y[0] - y[1]) / (x[0] - x[1]))
    
    # angle that the arc spans [rad]
    arc_total_rad = np.pi - taper_te_rad
    
    # angular space between the points on the arc
    arc_space_rad = arc_total_rad / (n + 1)
    
    # slope of the ending lower surface line
    ls_slope = (y[-1] - y[-2]) / (x[-1] - x[-2])
    
    # angle of the ending lower surface line
    ls_theta = np.arctan(ls_slope)
    
    # distance between the final lower surface point and the end point of the 
    # camber line
    d = np.sqrt((y[0] - y[-1]) ** 2 + (x[0] - x[-1]) ** 2) / 2
    
    # radius of the arc
    r = d / np.cos(taper_te_rad / 2)
    
    # center point of the arc
    center = {'x': x[-1] - r * np.sin(ls_theta), 
              'y': y[-1] + r * np.cos(ls_theta)}
    
    # list of angles of the arc coordinates relative to the center point
    angle_list = [ls_theta]
    
    # initialization of the arc coordinates
    x_round = []
    y_round = []
    
    # iterate through the number of points on the arc
    for i in range(n + 1):
        
        # append incremented angle to the list
        angle_list.append(angle_list[-1] + arc_space_rad)
        
        # calculate the arc coordinate with the most recent angle in the list
        x_round.append(center['x'] + r * np.sin(angle_list[-1]))
        y_round.append(center['y'] - r * np.cos(angle_list[-1]))

    # overwrite the final point of the arc with the initial surface 
    # coordinates in order to avoid any inaccuracies
    x_round[-1] = x[0]
    y_round[-1] = y[0]

    
    
    
    
    
    
    
    
    
    # -------------------------------- OUTPUT ---------------------------------
    
    # create dictionary of the arc coordinates
    te_round_out = {'x': x_round, 
                    'y': y_round}
    
    # return dictionary
    return te_round_out




























