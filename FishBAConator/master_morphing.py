"""
@Python:
    2.7
    
@Author:
    Amine Abdelmoula (amine.abdelmoula@tum.de)
    Technical University of Munich
    Institute of Helicopter Technology 

@Project:
    SABRE
    
@Aim:
    Generation of morphed 2D airfoil based on the FishBAC concept.
    This script was developed based on the scripts delivered by the University of Bristol.
    The delivered codes assumed that the coordinates of the trailing edge of the baseline and the morphed airfoil
    were identical. This caused a chord extension of morphed airfoil.
    
    This developed script by the Technical University of Munich offers an alternative
    that computes the coordinates of a FishBAC morphed airfoil without chord extension.    


@Import tools:
    
    baseline_generator: smoothing of the baseline based on the imported coordinates.
    
    FishBAC_generator: camber morphed airfoils based on the FishBAC concept.
    
    close_te: generation of the coordinates of an arc, which closes an open trailing edge

@Remarks: 
    
    data_filename: Name of the point cloud data file in airfoil_data folder.
    
    Very important: The file should consist of the surface coordinates starting with the upper 
    surface from the leading edge (left) to the trailing edge (right) followed 
    by the lower surface from the leading to the trailing edge. The x and y 
    coordinates should be separated by a space. At the trailing edge, the 
    x-values of the lower and upper surface need to be identical.    

Please contact the author, in case you want to extend this code or improve it. 

"""
# pylint ignores style-choices as this code is taken from another module
# pylint: disable=too-many-arguments, too-many-locals, too-many-statements, relative-import
# pylint: disable=invalid-name, import-error, wildcard-import, too-many-branches,
# pylint: disable=unused-wildcard-import, bare-except, unidiomatic-typecheck
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
from os import chdir, getcwd
from os.path import join
import os
import matplotlib.pyplot as plt
import numpy as np
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import FishBAC_generator
import baseline_generator
import close_te

# Examples:
#     NACA23012
#     SC1094R8
#     VR-12
#     NACA23012tab
#     SC1095

def create_fishbac_deformation(
        data_filename='NACA23012.dat',
        morphing_method='FishBAC',
        smoothing_method='bezier',
        airfoil_name="airfoil",
        deflection_level=2,
        beginning_of_camber_morphing=75,
        end_of_morphed_section=95,
        trailing_edge_shape='open',
        norm_by_morphed_chord=False,
        origin_shift=False,
        scaling_factor=1.0,
):
    """ Method created to interface with Fishbac Generator module.
    """
    # cwd = getcwd()
    # cwd = os.path.dirname(os.path.abspath(__file__))
    # print('ajsdhfjds -->',os.path.dirname(os.path.abspath(__file__)))
    # chdir(join(cwd, "./"))
    # cwd='/home/HT/ge56beh/Work/Python/Acoustics/FishBAConator'

    # ------------------------------ ERROR HANDLING -------------------------------

    if beginning_of_camber_morphing > end_of_morphed_section:
        raise ValueError('Beginning cannot be behind the end of camber morphing.')

    if (end_of_morphed_section - beginning_of_camber_morphing) * 0.4 < abs(deflection_level):
        raise ValueError('Deflection level too high.')

    if beginning_of_camber_morphing >= 90:
        raise ValueError('Beginning of camber morphing too high.')

    if deflection_level < 0 and morphing_method == 'plain_flap':
        raise ValueError('No upward deflections possible with the plain flap.')

    # ---------------------------------- SPACING ----------------------------------

    # point distribution of the rigid section
    leading_edge_distribution = (
        (np.arange(0, .001, .0001)).tolist()
        + (np.arange(.001, .002, .001)).tolist()
        + (np.arange(.002, .05, .002)).tolist()
        + (np.arange(.05, beginning_of_camber_morphing / 100, 0.0080)).tolist())

    # point distribution of the morphed section
    morphed_section_distribution = (
        (np.linspace(beginning_of_camber_morphing / 100,
                     beginning_of_camber_morphing / 100 + 0.05, 50,
                     endpoint=False)).tolist()
        + (np.linspace(beginning_of_camber_morphing / 100 + 0.05,
                       end_of_morphed_section / 100, 20, endpoint=True)).tolist())

    # point distribution of the rigid section
    # for tabbed airfoils
    if 'tab' in airfoil_name:
        trailing_edge_distribution = (
            (np.linspace(end_of_morphed_section / 100, end_of_morphed_section / 100
                         + 0.01, 300, endpoint=False)).tolist()
            + (np.linspace(end_of_morphed_section / 100 + 0.01, 1, 50,
                           endpoint=True)).tolist())
    # for untabbed airfoils
    else:
        trailing_edge_distribution = (
            np.linspace(end_of_morphed_section / 100, 1, 10,
                        endpoint=True)).tolist()

    # complete point distribution
    x_distribution = (
        leading_edge_distribution
        + morphed_section_distribution
        + trailing_edge_distribution[1:])

    # -------------------------------- DATA IMPORT --------------------------------

    # import the baseline surface data points
    x_raw, y_raw = np.loadtxt(os.path.dirname(__file__)+'/airfoil_data/' + data_filename, delimiter=' ',
                              unpack=True).tolist()

    # ---------------------------- AIRFOIL GENERATION -----------------------------

    # generate the baseline airfoil (dict)
    baseline = baseline_generator.baseline_generator(x_distribution, x_raw, y_raw,
                                                     smoothing_method)

    # assign the camber line and thickness distribution variables (list of float)
    x_camber_line = baseline['x_camber_line']
    y_camber_line = baseline['y_camber_line']
    thickness_distribution = baseline['thickness_distribution']

    # generate the morphed airfoil using the chosen parameters
    if morphing_method == 'FishBAC':
        airfoil = FishBAC_generator.fishbac_generator(
            x_camber_line, y_camber_line, thickness_distribution,
            beginning_of_camber_morphing, end_of_morphed_section,
            deflection_level)


    else:
        raise Exception('invalid morphing method')

    # assign the airfoil surface variables (list of float)
    airfoil_x = airfoil['x']
    airfoil_y = airfoil['y']
    baseline_x = baseline['x']
    baseline_y = baseline['y']

    # ---------------------------- ROUND TRAILING EDGE ----------------------------

    # close the trailing edge with a circle arc
    if trailing_edge_shape != 'open':

        # generate the trailing edge arc coordinates (list of float)
        if trailing_edge_shape == 'round':
            te_arc = close_te.close_te_round(airfoil['x'], airfoil['y'], 41)
            te_arc_baseline = close_te.close_te_round(baseline['x'],
                                                      baseline['y'], 41)
        else:
            raise ValueError('Invalid trailing edge shape.')

        # attach the arcs to the corresponding airfoils
        airfoil_x = airfoil['x'] + te_arc['x']
        airfoil_y = airfoil['y'] + te_arc['y']
        baseline_x = baseline['x'] + te_arc_baseline['x']
        baseline_y = baseline['y'] + te_arc_baseline['y']

    # indices of leading and trailing edges
    i_le = airfoil_x.index(min(airfoil_x))
    i_te = airfoil_x.index(max(airfoil_x))
    i_le_baseline = baseline_x.index(min(baseline_x))
    i_te_baseline = baseline_x.index(max(baseline_x))

    # leading edge coordinates
    le_x = airfoil_x[i_le]
    le_y = airfoil_y[i_le]

    # ---------------------------------- SCALING ----------------------------------


    # normalization
    if norm_by_morphed_chord:
        norm_factor = np.abs(airfoil_x[i_le] - airfoil_x[i_te])
        airfoil_x = [x_el / norm_factor for x_el in airfoil_x]
        airfoil_y = [y_el / norm_factor for y_el in airfoil_y]
    else:
        norm_factor = np.abs(baseline_x[i_le_baseline] - baseline_x[i_te_baseline])
        airfoil_x = [x_el / norm_factor for x_el in airfoil_x]
        airfoil_y = [y_el / norm_factor for y_el in airfoil_y]

    # scaling
    airfoil_x = scaling_factor * np.array(airfoil_x)
    airfoil_y = scaling_factor * np.array(airfoil_y)
    baseline_x = scaling_factor * np.array(baseline_x)
    baseline_y = scaling_factor * np.array(baseline_y)

    # -------------------------- ORIGIN TO QUARTER CHORD --------------------------

    if origin_shift:
        # position of the quarter chord
        delta_x = le_x + (airfoil_x[i_te] - le_x) / 4
        delta_y = le_y + (airfoil_y[i_le] - le_y) / 4
        delta_y = 0

        # shift the airfoil coordinates so that the quarter chord is located at
        # the origin
        airfoil_x_shifted = [x_el - delta_x for x_el in airfoil_x]
        airfoil_y_shifted = [y_el - delta_y for y_el in airfoil_y]

        # new chord (for plotting)
        # x_chord = np.linspace(airfoil_x_shifted[i_le], airfoil_x_shifted[i_te], 3)
        # y_chord = np.linspace(airfoil_y_shifted[i_le], airfoil_y_shifted[i_te], 3)

        # overwrite with the shifted coordinates
        airfoil_x = airfoil_x_shifted
        airfoil_y = airfoil_y_shifted

    if trailing_edge_shape != 'open':
        xu = list(airfoil_x[1:i_le + 1][::-1]) + list(airfoil_x[i_te:][::-1])
        zu = list(airfoil_y[1:i_le + 1][::-1]) + list(airfoil_y[i_te:][::-1])
        xl = airfoil_x[i_le:i_te + 1]
        zl = airfoil_y[i_le:i_te + 1]
    else:
        xu = airfoil_x[:i_le + 1][::-1]
        zu = airfoil_y[:i_le + 1][::-1]
        xl = airfoil_x[i_le:]
        zl = airfoil_y[i_le:]

    x = np.hstack((np.flip(xu)[:-1], xl[1:]))
    z = np.hstack((np.flip(zu)[:-1], zl[1:]))

    base_grid = np.vstack((x, z))
    # chdir(cwd)
    
    
    
    # return base_grid.T,\
    #          scaling_factor*np.array(x_raw[:])-0.25*scaling_factor,\
    #          scaling_factor*np.array(y_raw)
    return base_grid.T,\
             scaling_factor*np.array(x_raw[:]),\
             scaling_factor*np.array(y_raw)


if __name__ == "__main__":
    a,x_raw,y_raw = create_fishbac_deformation()
    print(a.shape)
    plt.plot(a[:,0],a[:,1],x_raw,y_raw,'b')
    plt.grid()
    
