#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 12:55:24 2019

@authors: Amine Abdelmoula, Fabian Grimm

Tools for the generation of baseline airfoils by means of smoothing out the 
imported coordinates.

"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import numpy as np
from scipy.interpolate import interp1d


def quad_bezier(t, points):
    
    """Definition of a quadratic bezier curve.
    
    Args:
        t: Point distribution on each curve from 0 to 1. 
            Example: [0, 0.1, ... , 0.9, 1.0]
        points: List of three points (first anchor point, control point, 
            second anchor point) with [x, y] for each point.
            Example: [[0, 1], [1, 3], [2, 2]]
    
    Returns:
        x, y values of the Bezier curve coordinates
        
    """
    
    #Formula for quadratic Bezier curves
    b_x = ((1 - t) * ((1 - t) * points[0][0] + t * points[1][0]) 
           + t * ((1 - t) * points[1][0] + t * points[2][0]))
    b_y = ((1 - t) * ((1 - t) * points[0][1] + t * points[1][1]) 
           + t * ((1 - t) * points[1][1] + t * points[2][1]))

    return b_x, b_y










def baseline_generator(x_distribution, x_raw, y_raw, smoothing_method):
    
    """Generator for the baseline airfoil.
    
    This function creates a smoothed out airfoil surface using either Bezier 
    curves or cubic splines. Additionally, it approximates the camber line and 
    the thickness distribution. 
    
    Args:
        x_distribution: Point distribution from 0 to 1.
            Example: [0, 0.001, 0.003, ... , 0.99, 1.0]
        x_raw: List of imported x-values (from leading to trailing edge, first 
            upper, then lower surface).
        y_raw: List of imported y-values (from leading to trailing edge, first 
            upper, then lower surface).
        smoothing_method: Smoothing method. 
            Options: 'none', 'bezier', 'spline'
        
    Returns:
        Dictionary containing the following data:
            'xu': List of smooth upper surface x-values.
            'xl': List of smooth lower surface x-values.
            'yu': List of smooth upper surface y-values.
            'yl': List of smooth lower surface y-values.
            'x_camber_line': List of x-values of the approximated camber line.
            'y_camber_line': List of y-values of the approximated camber line.
            'thickness_distribution': List of the thickness distribution.
            'x': List of the smooth surface x-values as a loop 
                (counterclockwise starting above the trailing edge).
            'y': List of the smooth surface y-values as a loop. 
                (counterclockwise starting above the trailing edge).
            'xu_new': List of smooth upper surface x-values with new spacing.
            'xl_new': List of smooth lower surface x-values with new spacing. 
            'yu_new': List of smooth upper surface y-values with new spacing. 
            'yl_new': List of smooth lower surface y-values with new spacing.
            'u_spline': upper surface interpolator, f(x). 
            'l_spline': lower surface interpolator, f(x).
            'x_raw': List of imported x-values (from leading to trailing edge, 
                first upper, then lower surface).
            'y_raw': List of imported y-values (from leading to trailing edge, 
                first upper, then lower surface).
    """
    
    
    
    
    
    
    
    
    
    
    # ---------------------------- DATA UNPACKING -----------------------------
    
    # normalization
    x_raw = (np.array(x_raw)/(max(x_raw)-min(x_raw)) - min(x_raw)).tolist()
    y_raw = (np.array(y_raw)/(max(x_raw)-min(x_raw))).tolist()

    # index of surface switch
    for i in range(len(x_raw)):
        if x_raw[i+1] < x_raw[i]:
            i_split = i
            break
    
    # split into upper and lower surface
    xu = x_raw[:i_split + 1]  
    xl = x_raw[i_split + 1:]
    yu = y_raw[:i_split + 1]
    yl = y_raw[i_split + 1:]
    
    # check, whether upper and lower surface points at the trailing edge have 
    # the same x-value. This is necessary because the thickness distribution 
    # is approximated vertically
    if xu[-1] != xl[-1]:
        err_msg = ('Upper and lower surface points at the trailing edge ' + 
                   'need to have the same x-value. Correct the coordinates ' + 
                   'in airfoil_data/ if necessary.')
        raise ValueError(err_msg)
    
    # create a loop
    x_loop = list(xu[1:][::-1]) + list(xl)
    y_loop = list(yu[1:][::-1]) + list(yl)

    
    
    
    
    
    
    
    
    
    # ----------------------------- NO SMOOTHING ------------------------------

    if smoothing_method == 'none':

        # assign x and y to the raw data
        x = x_loop
        y = y_loop










    # --------------------------- BEZIER SMOOTHING ----------------------------

    elif smoothing_method == 'bezier':

        """
        In the Bezier method, the surface is represented by a series of 
        adjacent quadratic Bezier curves. The imported surface coordinates 
        serve as the control points of the individual curves. The midpoints 
        between them are used as the anchor points of each Bezier curve. The 
        result is a continuous, smooth airfoil surface. The first and last 
        Bezier curves are an exception. Here, the first and last of the 
        imported coordinates instead of the center points are used as the 
        anchor points.
        
        """
        
        # assign the raw data as control points
        # Format: [[x0, y0],
        #          [x1, y1],
        #            ...   ]
        ctl_pts = [[x, y] for x, y in zip(x_loop, y_loop)]
        
        # number of points on each Bezier curve
        num_pts = 18
        
        # initialize the smooth cumulative curve of the surface
        curve = [[], []]
        
        # point distribution on each curve 
        # Format: [t0, t1, ...]
        t = [i * 1 / num_pts for i in range(0, num_pts)]
        
        
        # first curve ---------------------------------------------------------
        
        # calculate the center points
        mid_x = (ctl_pts[1][0] + ctl_pts[2][0]) / 2
        mid_y = (ctl_pts[1][1] + ctl_pts[2][1]) / 2
        
        # iterate through the desired point distribution on the Bezier curve
        for i in range(len(t)):
            
            # determine the Bezier curve coordinates (initial control point is 
            # used as the first anchor point)
            b_x, b_y = quad_bezier(t[i], [ctl_pts[0], ctl_pts[1], 
                                   [mid_x, mid_y]])
            
            # append to the cumulative curve of the surface
            curve[0].append(b_x)
            curve[1].append(b_y)


        # middle curves -------------------------------------------------------
        
        # iterate through the individual Bezier curves
        for i in range(1, len(ctl_pts) - 3):
            
            # calculate the center points
            mid_x_1 = (ctl_pts[i][0] + ctl_pts[i + 1][0]) / 2
            mid_y_1 = (ctl_pts[i][1] + ctl_pts[i + 1][1]) / 2
            mid_x_2 = (ctl_pts[i + 1][0] + ctl_pts[i + 2][0]) / 2
            mid_y_2 = (ctl_pts[i + 1][1] + ctl_pts[i + 2][1]) / 2
            
            # iterate through the desired point distribution on each Bezier 
            # curve
            for i2 in range(len(t)):
                
                # determine the Bezier curve coordinates
                b_x, b_y = quad_bezier(t[i2], [[mid_x_1, mid_y_1], 
                                       ctl_pts[i + 1], [mid_x_2, mid_y_2]])
    
                # append to the cumulative curve of the surface
                curve[0].append(b_x)
                curve[1].append(b_y)


        # last curve ----------------------------------------------------------
        
        # calculate the center points
        mid_x = (ctl_pts[-3][0] + ctl_pts[-2][0]) / 2
        mid_y = (ctl_pts[-3][1] + ctl_pts[-2][1]) / 2
        
        # iterate through the desired point distribution on the Bezier curve
        for i in range(len(t)):
            
            # determine the Bezier curve coordinates (final control point is 
            # used as the final anchor point)
            b_x, b_y = quad_bezier(t[i], [[mid_x, mid_y], ctl_pts[-2], 
                                   ctl_pts[-1]])
            
            # append to the cumulative curve of the surface
            curve[0].append(b_x)
            curve[1].append(b_y)
        
        
        # include the final control points in the surface
        curve[0].append(ctl_pts[-1][0])
        curve[1].append(ctl_pts[-1][1])
        
        # assign x and y to the calculated smooth surface coordinates
        x = curve[0]
        y = curve[1]










    # --------------------------- SPLINE SMOOTHING ----------------------------

    elif smoothing_method == 'spline':
        
        """
        In the spline method, the discrete curve of surface coordinates is 
        interpolated with a series of cubic splines.
        
        """
        
        # transposed imported coordinates
        # Format: [[x0, y0], 
        #          [x1, y1], 
        #            ...   ]
        points = np.array([x_loop, y_loop]).T

        # linear length along the imported coordinates:
        # Format: [d0, d01, d012, ...]
        distance = np.cumsum(np.sqrt(np.sum(np.diff(points, axis=0) ** 2, 
                                            axis=1)))
        
        # insert 0 at the beginning of the list and normalize by the final
        # value to obtain a list from 0 to 1.
        distance = np.insert(distance, 0, 0) / distance[-1]
        
        # total distribution of smooth surface coordinates
        alpha = np.linspace(0, 1, 5000)
        
        # interpolation
        interpolator = interp1d(distance, points, kind='cubic', axis=0)
        interpolated_points = interpolator(alpha)
        
        # assign x and y to the smooth surface coordinates
        x, y = interpolated_points[:, 0], interpolated_points[:, 1]

    else:
        raise ValueError('Invalid smoothing method.')










    # -------------------------------- SURFACE --------------------------------

    # normalization and shift to x = 0
    norm_factor = max(x) - min(x)
    x_loop = [(x_el - min(x)) / norm_factor for x_el in x_loop]
    y_loop = [(y_el) / norm_factor for y_el in y_loop]
    x = [(x_el - min(x)) / norm_factor for x_el in x]
    y = [(y_el) / norm_factor for y_el in y]

    # split into upper and lower surface
    xu = x[:x.index(0.0) + 1]
    xl = x[x.index(0.0):]
    yu = y[:x.index(0.0) + 1]
    yl = y[x.index(0.0):]

    # linear interpolation of the upper and lower surface
    u_spline = interp1d(xu, yu, kind='linear')
    l_spline = interp1d(xl, yl, kind='linear')

    # redistribute surface points to the spacing of x_distribution 
    xu_new = x_distribution
    yu_new = [u_spline(x) for x in xu_new]
    xl_new = x_distribution
    yl_new = [l_spline(x) for x in xl_new]










    # ----------------------- CAMBER LINE AND THICKNESS -----------------------

    # define the camberline at vertical half
    x_camber_line = x_distribution
    y_camber_line = [(yu_new_el + yl_new_el) / 2 
            for yu_new_el, yl_new_el in zip(yu_new, yl_new)]

    # define the thickness as vertical half
    thickness_distribution = [(yu_new_el - yl_new_el) / 2 
           for yu_new_el, yl_new_el in zip(yu_new, yl_new)]
    
    # create a loop of surface points
    x = list(xu_new[::-1]) + list(xl_new)
    y = list(yu_new[::-1]) + list(yl_new)










    # -------------------------------- OUTPUT ---------------------------------
    
    # output
    dict_out = {'xu': np.array(xu), 
                'xl': np.array(xl), 
                'yu': np.array(yu),
                'yl': np.array(yl), 
                'y_camber_line': np.array(y_camber_line), 
                'x_camber_line': np.array(x_camber_line),
                'thickness_distribution': thickness_distribution,
                'x': x, 
                'y': y, 
                'xu_new': xu_new, 
                'yu_new': yu_new, 
                'xl_new': xl_new, 
                'yl_new': yl_new,
                'u_spline': u_spline, 
                'l_spline': l_spline,
                'x_raw': x_loop, 
                'y_raw': y_loop}

    # return the dictionary
    return dict_out

























