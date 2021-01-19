#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 14:57:37 2020

@author: ge56beh
"""
import tecplot
from tecplot.constant import PlotType
from collections import Counter

tecplot.new_layout()
tecplot.session.connect()

dataset = tecplot.data.load_tecplot('grid_COAX_saneg_04.surface.pval.unsteady_i=1800_t=4.6666667e-01.plt')

frame = tecplot.active_frame()
plot = frame.plot(PlotType.Cartesian3D)
plot.activate()
plot.show_contour = True
frame.plot().view.fit_surfaces()

print(dataset.variable_names)
print(dataset.zone_names)
print(dataset.solution_times)

for coord in ['x','y','z']:
    dataset.add_variable('p*area_vec_'+coord)
    dataset.zone('blade_pressure_u1').values('p*area_vec_'+coord)[:] = dataset.zone('blade_pressure_u1').values('pressure')[:] \
                                                            *dataset.zone('blade_pressure_u1').values(coord+'-force')[:]

zone_names_of_interest = [ 'blade_pressure_u1', 'blade_suction_u1', 'blade_trEdge_u1', 
                          'cuff_pressure_u1', 'cuff_suction_u1', 'cuff_trEdge_u1', 'tip_face_u1',]
del_zones = list((Counter(dataset.zone_names) - Counter(zone_names_of_interest)).elements())
var_name_of_interest = ['density','pressure', 'x-force', 'y-force','p*area_vec']
del_vars = list((Counter(dataset.variable_names) - Counter(var_name_of_interest)).elements())


#for del_var in del_vars:
#    dataset.delete_variables(dataset.variable(del_var))
for del_zone in del_zones:
    dataset.delete_zones(dataset.zone(del_zone))

#frame.plot().show_mesh = True
frame.plot().view.fit_surfaces()
frame.plot().vector.u_variable = dataset.variable('x-force')
frame.plot().vector.v_variable = dataset.variable('y-force')
frame.plot().vector.w_variable = dataset.variable('z-force')

plot.show_vector = True

print(dataset.variable_names)
print(dataset.zone_names)
print(dataset.solution_times)

#plot.show_mesh = False
#
#variables_to_save = [dataset.variable(V)
#                     for V in ('x','y','z','Pressure_Coefficient')]
#
#zone_to_save = dataset.zone('WingSurface')
## write data out to an ascii file
#tecplot.data.save_tecplot_ascii('wing.dat', dataset=dataset,
#                                variables=variables_to_save,
#                                zones=[zone_to_save])

#x_value=zone_to_save.values('x')[:]
#x_value_arr=zone_to_save.values('x').as_numpy_array()
#y_value=zone_to_save.values('y')[:]
#z_value=zone_to_save.values('z')[:]
#arr=np.stack((x_value,y_value,z_value)).T
#pressure_val = zone_to_save.values('Pressure_Coefficient')[:]

###############################################################################
