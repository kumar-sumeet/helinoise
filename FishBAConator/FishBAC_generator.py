#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 12:55:24 2019

@authors: Amine Abdelmoula, Fabian Grimm

Tools for the generation of camber morphed airfoils based on the FishBAC 
concept.

"""
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
import numpy as np
from scipy.interpolate import UnivariateSpline


def fishbac_generator(x_camber_line, y_camber_line, thickness_distribution, 
                      beginning_of_camber_morphing, end_of_morphed_section, 
                      deflection_level):
    
    """Generates a camber morphed airfoil based on the FishBAC concept.
    
    The geometry of the FishBAC concept consists of a smooth increase in 
    camber applied to the aft section of an airfoil. This module executes a 
    transformation of the camber line coordinates in both coordinate 
    directions in order to fulfill the deflection requirement. The reference 
    for this transformation is a 3rd order polynomial function. The morphing 
    is only considered up to a certain point, followed by a straight trailing 
    edge section. The coefficient of the 3rd order polynomial function is 
    determined via a bisection algorithm. The length of the camber line as 
    well as the original thickness distribution along it is maintained. 
    Finally, the morphed airfoil surface is obtained by means of the thickness 
    distribution.
    
    Args:
        x_camber_line: List of the camber line's x-values.
        y_camber_line: List of the camber line's y-values.
        thickness_distribution: List of the thickness distribution.
        beginning_of_camber_morphing (float): Beginning of camber morphing
            [percent of the chord].
        end_of_morphed_section (float): End of the morphed section [percent of 
            the chord].
        deflection_level (float): Deflection level [percent of the chord].
        
    Returns:
        Dictionary containing the following data:
            'x': List of morphed surface x-values as a loop (counterclockwise 
                starting above the trailing edge).
            'y': List of morphed surface y-values as a loop (counterclockwise 
                starting above the trailing edge).
            'x_camber_line_new': List of the x-coordinates of the mophed 
                camber line. 
            'y_camber_line_new': List of the y-coordinates of the mophed 
                camber line. 
            'cl_spline_new': Spline interpolation of the moprhed camber line, 
                f(x).
            'chord_new' (float): Chord length of the morphed airfoil.
            'delta_alpha_deg' (float): Difference in angle of attack between 
                the baseline and the morphed airfoil.
            'xte_new' (float): New x-coordinate of the transition between the 
                morphed section and the straight trailing edge section.
    
    """
    
    # --------------------- VARIABLES AND INITIALIZATION ----------------------
    
    # x-location of the beginning of camber morphing
    xr = beginning_of_camber_morphing/100
    
    # x-location of the end of the morphed section
    xte = end_of_morphed_section/100
    
    # y-location of the deflected trailing edge
    wte = - deflection_level/100

    # initialization of the morphed surface coordinates
    xu_fb = []
    yu_fb = []
    xl_fb = []
    yl_fb = []
    
    # initialization of the morphed camber line slope angle
    theta = []

    # first estimation for the coefficient of the polynomial
    k_list = [-10]

    # first correction range, which is then divided in half every iteration
    margin = 10

    # first error, to ensure at least one iteration
    error = 1










    # ------------------------------ CAMBER LINE ------------------------------

    # iterative generation of the morphed camber line using a bisection 
    # algorithm in respect of the polynomial's coefficient k until the desired 
    # precision of the trailing edge deflection is achieved
    while abs(error) > 1e-5:

        # reset the camber line variables
        x_camber_line_fb = []
        y_camber_line_fb = []
        x_camber_line_shifted = []
        
        # coefficient of the polynomial
        k = k_list[-1]
        
        # length of the camber line
        len_fb = [0]
        
        # indicator of the transition between morphed section and straight
        # trailing edge section
        trailing_edge_section_reached = False

        # determine the index of the trailing edge section transition point on 
        # the baseline airfoil
        for i in range(len(x_camber_line)):
            if x_camber_line[i] >= xte:
                i_te = i
                break
        
        # iterate through the camber line points
        for i in range(0, len(x_camber_line)):

            
            # rigid section ---------------------------------------------------
            
            # copy the rigid section of the baseline
            if x_camber_line[i] < xr:
                x_camber_line_fb.append(x_camber_line[i])
                y_camber_line_fb.append(y_camber_line[i])

                # track the camber line length
                if i > 0:
                    len_fb.append(
                            len_fb[-1] 
                            + np.sqrt((x_camber_line_fb[-1] 
                                        - x_camber_line_fb[-2]) ** 2 
                                      + (y_camber_line_fb[-1] 
                                        - y_camber_line_fb[-2]) ** 2))

    
            # morphed section -------------------------------------------------
    
            # determine the morphed section points with current coefficient k
            elif x_camber_line[i] >= xr and i < i_te:

                # create a shifted coordinate system with its origin at xr
                x_camber_line_shifted.append(x_camber_line[i] - xr)  
                
                # slope of the polynomial
                poly_slope = 3 * k * (x_camber_line_fb[-1] - xr) ** 2
                
                # slope angle of the polynomial [rad]
                poly_angle_rad = np.arctan(poly_slope)
                
                # step between x-values of the baseline
                x_step = x_camber_line[i] - x_camber_line[i - 1]

                # morphed camber line coordinates
                x_camber_line_fb.append(x_camber_line_fb[-1] 
                                        + x_step * np.cos(poly_angle_rad))
                y_camber_line_fb.append(y_camber_line[i] 
                                        + k * (x_camber_line_fb[-1] - xr) ** 3)
                
                # track the camber line length
                len_fb.append(
                        len_fb[-1] 
                        + np.sqrt((x_camber_line_fb[-1] 
                                    - x_camber_line_fb[-2]) ** 2 
                                  + (y_camber_line_fb[-1] 
                                    - y_camber_line_fb[-2]) ** 2))


            # trailing edge section -------------------------------------------

            # straight continuation of the ending morphed section
            else:

                # new x-coordinate of the transition point
                if not trailing_edge_section_reached:
                    xte_new = x_camber_line_fb[-1]
                
                # continue the shifted coordinate system
                x_camber_line_shifted.append(x_camber_line[i] - xr)
                
                # slope of the ending morphed section
                te_slope_fb = ((y_camber_line_fb[-1] - y_camber_line_fb[-2]) 
                               / (x_camber_line_fb[-1] - x_camber_line_fb[-2]))

                # morphed camber line coordinates
                x_camber_line_fb.append(
                    x_camber_line_fb[-1] 
                    + np.cos(poly_angle_rad) * (x_camber_line_shifted[-1] 
                                                - x_camber_line_shifted[-2]))
                y_camber_line_fb.append(
                    y_camber_line_fb[-1] 
                    + te_slope_fb * (x_camber_line_fb[-1] 
                                     - x_camber_line_fb[-2]))

                # trailing edge section reached
                trailing_edge_section_reached = True
                
                # track the camber line length
                len_fb.append(
                    len_fb[-1] 
                    + np.sqrt((x_camber_line_fb[-1] 
                                - x_camber_line_fb[-2]) ** 2 
                              + (y_camber_line_fb[-1] 
                                - y_camber_line_fb[-2]) ** 2))


        # calculate the difference in TE deflection to desired deflection
        error = y_camber_line_fb[-1] - wte

        # determine the direction of the bisection method
        if error > 0:
            k_list.append(k_list[-1] - margin)
        else:
            k_list.append(k_list[-1] + margin)

        # new margin for next iteration
        margin *= 0.5

    # interpolate the new camber line, calculate the slope at every step
    cl_spline_fb = UnivariateSpline(x_camber_line_fb, y_camber_line_fb)
    cl_spline_fb.set_smoothing_factor(0)
    cl_spline_diff_fb = cl_spline_fb.derivative()

    # determine crest of camber line
    x_max = x_camber_line_fb[y_camber_line_fb.index(max(y_camber_line_fb))]










    # -------------------------------- SURFACE --------------------------------

    # iterate through the morphed camber line coordinates
    for i in range(0, len(x_camber_line_fb)):

        # slope angle of the morphed camber line
        theta.append(np.arctan(cl_spline_diff_fb(x_camber_line_fb[i])))


        # before the crest ----------------------------------------------------
        
        # extrude the surface points vertically in order to retain the 
        # original leading edge shape (the reason for this is the vertical 
        # approximation of the camber line and the thickness distribution in 
        # the module baseline_generator.py)
        if x_camber_line_fb[i] < x_max:
            xu_fb.append(x_camber_line_fb[i])
            yu_fb.append(y_camber_line_fb[i] + thickness_distribution[i])
            xl_fb.append(x_camber_line_fb[i])
            yl_fb.append(y_camber_line_fb[i] - thickness_distribution[i])

        
        # after the crest -----------------------------------------------------
        
        # switch at the crest of the camber line, in order to obtain a smooth,
        # continuous surface
        # extrude the surface points perpendicular to the camber line, as not 
        # to introduce shear to considerably morphed cases
        else:
            xu_fb.append(x_camber_line_fb[i] 
                         - thickness_distribution[i] * np.sin(theta[-1]))
            yu_fb.append(y_camber_line_fb[i] 
                         + thickness_distribution[i] * np.cos(theta[-1]))
            xl_fb.append(x_camber_line_fb[i] 
                         + thickness_distribution[i] * np.sin(theta[-1]))
            yl_fb.append(y_camber_line_fb[i] 
                         - thickness_distribution[i] * np.cos(theta[-1]))










    # ---------------------------- FINAL VARIABLES ----------------------------

    # new chord length
    chord_fb = np.sqrt((y_camber_line_fb[-1] - y_camber_line_fb[1]) ** 2 
                       + (x_camber_line_fb[-1] - x_camber_line_fb[1]) ** 2)

    # change in the angle of attack
    delta_alpha_deg = (np.arctan(-y_camber_line_fb[-1] / x_camber_line_fb[-1]) 
                       * 360 / (2 * np.pi))

    # create a loop of surface points for plotting
    x = xu_fb[::-1] + xl_fb
    y = yu_fb[::-1] + yl_fb

    # output
    fb_airfoil = {'x': x, 
                  'y': y, 
                  'x_camber_line_new': x_camber_line_fb, 
                  'y_camber_line_new': y_camber_line_fb, 
                  'cl_spline_new': cl_spline_fb,
                  'chord_new': chord_fb, 
                  'delta_alpha_deg': delta_alpha_deg, 
                  'xte_new': xte_new}
    
    # return the dictionary
    return fb_airfoil
