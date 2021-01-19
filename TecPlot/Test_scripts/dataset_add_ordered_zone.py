#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 10:25:12 2020

@author: ge56beh
"""
#%%
import numpy as np
import tecplot as tp
from tecplot.constant import PlotType, Color

# Generate data
x = np.linspace(-4, 4, 100)

# Setup Tecplot dataset
dataset = tp.active_frame().create_dataset('Data', ['x', 'y'])

# Create a zone
zone = dataset.add_ordered_zone('sin(x)', len(x))
zone.values('x')[:] = x
zone.values('y')[:] = np.sin(x)

# Create another zone
zone = dataset.add_ordered_zone('cos(x)', len(x))
zone.values('x')[:] = x
zone.values('y')[:] = np.cos(x)

# And one more zone
zone = dataset.add_ordered_zone('tan(x)', len(x))
zone.values('x')[:] = x
zone.values('y')[:] = np.tan(x)

# Set plot type to XYLine
plot = tp.active_frame().plot(PlotType.XYLine)
plot.activate()

# Show all linemaps and make the lines a bit thicker
for lmap in plot.linemaps():
    lmap.show = True
    lmap.line.line_thickness = 0.6

plot.legend.show = True

tp.export.save_png('add_ordered_zones.png', 600, supersample=3)

#%%
#######################################################################################################################

import math

# Setup Tecplot dataset
dataset = tp.active_frame().create_dataset('Data')
dataset.add_variable('x')
dataset.add_variable('s')
zone = dataset.add_ordered_zone('Zone', 100)

# Fill the dataset
x = [0.1 * i for i in range(100)]
zone.values('x')[:] = x
zone.values('s')[:] = [math.sin(i) for i in x]

# Set plot type to XYLine
tp.active_frame().plot(PlotType.XYLine).activate()

tp.export.save_png('add_variables.png', 600, supersample=3)
#%%