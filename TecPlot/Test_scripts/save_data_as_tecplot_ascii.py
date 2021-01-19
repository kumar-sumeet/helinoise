#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 14:57:37 2020

@author: ge56beh
"""
import numpy as np
from os import path
import tecplot
import pickle
import time

tecplot.new_layout()
tecplot.session.connect()

examples_directory = tecplot.session.tecplot_examples_directory()
infile = path.join(examples_directory,
                   'OneraM6wing', 'OneraM6_SU2_RANS.plt')
dataset = tecplot.data.load_tecplot(infile)

frame = tecplot.active_frame()
plot = frame.plot()
plot.show_mesh = False
#plot.show_scatter = True
#plot.scatter.variable = dataset.variable('Pressure_Coefficient')
#from tecplot.constant import *
#for z in dataset.zones():
#    scatter = plot.fieldmap(z).scatter
#    scatter.symbol_type = SymbolType.Geometry
#    scatter.symbol().shape = GeomShape.Circle
#    scatter.fill_mode = FillMode.UseSpecificColor
#    scatter.fill_color = plot.contour(0)
#    scatter.color = plot.contour(0)
#    scatter.size_by_variable = True
#frame.add_text('Size of dots indicate relative pressure', (20, 80))
#
## ensure consistent output between interactive (connected) and batch
#plot.contour(0).levels.reset_to_nice()
#




variables_to_save = [dataset.variable(V)
                     for V in ('x','y','z','Pressure_Coefficient')]

zone_to_save = dataset.zone('WingSurface')
# write data out to an ascii file
tecplot.data.save_tecplot_ascii('wing.dat', dataset=dataset,
                                variables=variables_to_save,
                                zones=[zone_to_save])
print(dataset.variable_names)
print(dataset.zone_names)
print(dataset.solution_times)

x_value=zone_to_save.values('x')[:]
x_value_arr=zone_to_save.values('x').as_numpy_array()
y_value=zone_to_save.values('y')[:]
z_value=zone_to_save.values('z')[:]
arr=np.stack((x_value,y_value,z_value)).T
pressure_val = zone_to_save.values('Pressure_Coefficient')[:]

###############################################################################


#time.sleep(3)
#
#node_pos_arr_dict = pickle.load( open( "../node_pos_arr_dict.p", "rb" ) )
#norm_pos_arr_dict = pickle.load( open( "../norm_pos_arr_dict.p", "rb" ) )
#
#arr2 = node_pos_arr_dict['upper surface'][:,:,:,0]
##dataset.zone('WingSurface').value('x')[:] = x_value
#
#dataset.zone('WingSurface').values('x')[:] = node_pos_arr_dict['upper surface'][:,:,0,0].ravel()
#dataset.zone('WingSurface').values('y')[:] = node_pos_arr_dict['upper surface'][:,:,1,0].ravel()
#dataset.zone('WingSurface').values('z')[:] = node_pos_arr_dict['upper surface'][:,:,2,0].ravel()

from tecplot.constant import *


#tecplot.new_layout()

dataset.zone('WingSurface').values('x')[:] = arr[:,0]
dataset.zone('WingSurface').values('y')[:] = arr[:,1]
dataset.zone('WingSurface').values('z')[:] = arr[:,2]


# Enable 3D field plot and turn on contouring
# with boundary faces
frame.plot_type = PlotType.Cartesian3D
plot = frame.plot()
frame.plot().show_mesh = True

#srf = plot.fieldmap(0).surfaces
#srf.surfaces_to_plot = SurfacesToPlot.BoundaryFaces
#plot.show_contour = True
#
# get the contour group associated with the
# newly created zone
#contour = plot.fieldmap(dataset.zone('WingSurface')).contour
#
## assign flooding to the first contour group
#contour.flood_contour_group = plot.contour(0)
#contour.flood_contour_group.variable = dataset.variable('Pressure_Coefficient')
#contour.flood_contour_group.colormap_name = 'Sequential - Yellow/Green/Blue'
#contour.flood_contour_group.legend.show = False

