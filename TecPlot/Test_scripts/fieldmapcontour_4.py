#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 15:53:19 2020

@author: sumeetkumar
"""

import numpy as np

import tecplot as tp
from tecplot.constant import *
from tecplot.data.operate import execute_equation


tp.session.connect()

tp.new_layout()

# Get the active frame, setup a grid (30x30x30)
# where each dimension ranges from 0 to 30.
# Add variables P,Q,R to the dataset and give
# values to the data.
frame = tp.active_frame()
dataset = frame.dataset
for v in ['X','Y','Z','P','Q','R']:
    dataset.add_variable(v)

#zone = dataset.add_ordered_zone('Zone', (x,y,z))
# zone = dataset.add_zone(ZoneType.Ordered, 'Zone', (3,3,3))
# xx = np.arange(0,3,1)
# yy = np.arange(0,3,1)
# zz = np.arange(0,3,1)
# for v,arr in zip(['X','Y','Z'],np.meshgrid(xx,yy,xx)):
#     zone.values(v)[:] = arr.ravel()
    
zone = dataset.add_zone(ZoneType.Ordered, 'Zone', (3,2,2))    
#zone.values('X')[:]=([0,3,6,0,3,6,0,3,6,0,3,6])
#zone.values('Y')[:]=([0,0,0,6,6,6,0,0,0,6,6,6])
#zone.values('Z')[:]=([0,1,3,3,4,6,8,9,11,11,12,14])

zone.values('X')[:]=([0,3,6,0,3,6,0,3,6,0,3,6])
zone.values('Y')[:]=([0,0,0,6,6,6,0,0,0,6,6,6])
zone.values('Z')[:]=([0,0,0,0,0,0,10,10,10,10,10,10])

execute_equation('{P} = {X}')
execute_equation('{Q} = {Y}')
execute_equation('{R} = {Z}')


x_value=zone.values('X')[:]
y_value=zone.values('Y')[:]
z_value=zone.values('Z')[:]
arr=np.column_stack((x_value,y_value,z_value))


# Enable 3D field plot and turn on contouring
# with boundary faces
frame.plot_type = PlotType.Cartesian3D
plot = frame.plot()
srf = plot.fieldmap(0).surfaces
srf.surfaces_to_plot = SurfacesToPlot.BoundaryFaces
#plot.show_contour = True
plot.show_mesh = True
plot.data_labels.show_node_labels = True

# get the contour group associated with the
# newly created zone
# contour = plot.fieldmap(dataset.zone('Zone')).contour

# # assign flooding to the first contour group
# contour.flood_contour_group = plot.contour(0)
# contour.flood_contour_group.variable = dataset.variable('P')
# contour.flood_contour_group.colormap_name = 'Sequential - Yellow/Green/Blue'
# contour.flood_contour_group.legend.show = True

# save image to PNG file
tp.export.save_png('fieldmap_contour.png', 600, supersample=3)