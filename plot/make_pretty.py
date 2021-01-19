#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 09:33:24 2020

@author: Sumeet Kumar

Plotting-relevant functions
"""
import numpy as np

def set_font_settings(target):
    if target=='AIAA_SciTech':
        tex_fonts = {
                    # Use LaTeX to write all text
                    "text.usetex": True,
                    "font.family": "Times New Roman",
                    # Use 10pt font in plots, to match 10pt font in document
                    "axes.labelsize": 10,
                    "font.size": 10,
                    # Make the legend/label fonts a little smaller
                    "legend.fontsize": 9,
                    "legend.frameon":False,
                    "xtick.labelsize": 9,
                    "ytick.labelsize": 9
                    }
    
    return tex_fonts

def set_size(target, custom_width=500, fraction=1):
    """Set figure dimensions to avoid scaling in LaTeX.

    obtained this function from - 
    https://jwalton.info/Embed-Publication-Matplotlib-Latex/
    
    Parameters
    ----------
    custom_width: float
            Explicit document textwidth or columnwidth in pts
    fraction: float, optional
            Fraction of the width in 'target' page which you wish the figure to
            occupy

    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    if target=='AIAA_SciTech':
        width=469.75502
    elif target=='VFS_Forum':
        width=469.75502
    else:
        width=custom_width
        
    # Width of figure (in pts)
    fig_width_pt = width * fraction

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    # https://disq.us/p/2940ij3
    golden_ratio = (5**.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio
 

    return (fig_width_in, fig_height_in)

