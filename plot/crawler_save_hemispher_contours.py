#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 16:50:21 2020

@author: ge56beh
"""

import numpy as np
import sys
import os
import matplotlib.pyplot as plt

plt.style.use('seaborn')
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from plot import Scatter_plot
from utl import crawler




Dir_wopwop_data = '/home/HT/ge56beh/Work/Python/Acoustics/Data/PSU_WOPWOP/PSU_WOPWOP_new/Hemisphere_50'
All_filepath_dict,All_filenames_dict = crawler.get_files_info(Dir_wopwop_data)

