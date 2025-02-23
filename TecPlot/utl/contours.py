#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions that accept path to PSU-WOPWOP acoustic footprint hemisphere results 
and generate hemisphere contours
"""

import tecplot as tp
import numpy as np
import os
import sys
from tecplot.constant import ZoneType
from tecplot.exception import *
from tecplot.constant import *
from tecplot.macro import *

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from macros import (create_rotor_on_plane,
                    plane_50_extended,plane_50_extended_delta,
                    hemisphere_50,validationplane,
                    plane50extended)

def save_Hemisphere_50_delta(dir_path,case,baseline_case,dB_or_dBA='dBA',drag_or_lift=''):  
    dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{case}/{case}/{drag_or_lift}OASPL.x', 
                                       solution_filenames=None,
                                       function_filenames=f'{dir_path}/{case}/{case}/{drag_or_lift}OASPL{dB_or_dBA}.fn', 
                                       name_filename=f'{dir_path}/{case}/{case}/{drag_or_lift}OASPL{dB_or_dBA}.nam')
    dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{baseline_case}/{baseline_case}/{drag_or_lift}OASPL.x', 
                                       solution_filenames=None,
                                       function_filenames=f'{dir_path}/{baseline_case}/{baseline_case}/{drag_or_lift}OASPL{dB_or_dBA}.fn', 
                                       name_filename=f'{dir_path}/{baseline_case}/{baseline_case}/{drag_or_lift}OASPL{dB_or_dBA}.nam')
    delta_zone = dataset.add_zone(ZoneType.Ordered, 'Delta_Zone', dataset.zone(0).dimensions)   

    for var in dataset.variable_names[:-3]:
        delta_zone.values(var)[:]=dataset.zone(0).values(var)[:]
    for var in dataset.variable_names[-3:]:
        delta_zone.values(var)[:]=dataset.zone(0).values(var)[:]-dataset.zone(1).values(var)[:]
        
    dataset.delete_zones(dataset.zone(0))
    dataset.delete_zones(dataset.zone(0))

    loading_cb_levels=[-14,-12,-10,-8,-6,-4,-2,0,2,4]
    thickness_cb_levels=[-5,-4,-3,-2,-1,1,2,3,4]
    total_cb_levels=[-15,-13,-11,-9,-5,-3,-1,1,3,5,7,9,11]
    cb_levels_dict={'thickness':thickness_cb_levels,'loading':loading_cb_levels,'total':total_cb_levels}
    
    frame = tp.active_frame()
    frame.plot().fieldmap(0).show=True
    frame.plot().show_contour = True
    execute_macro=True
    for idx,key in enumerate(cb_levels_dict,4):
        print(key)
        tp.active_frame().plot().contour(0).variable_index=idx
    #    tp.active_frame().plot().contour(0).colormap_name='Sequential - Viridis'
        tp.active_frame().plot().contour(0).colormap_name='Modified Rainbow - Dark ends'
        tp.active_frame().plot().contour(0).levels.reset_levels(cb_levels_dict[key])
        tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
        tp.active_frame().plot().contour(0).legend.show_header=False
        tp.active_frame().plot().contour(0).legend.number_font.size=4.0
        tp.active_frame().plot().axes.orientation_axis.size=14
        tp.active_frame().plot().axes.orientation_axis.line_thickness=0.8
        tp.active_frame().plot().view.position=(630.581,
            tp.active_frame().plot().view.position[1],
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            379.91,
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            tp.active_frame().plot().view.position[1],
            416.552)
        tp.active_frame().plot().view.width=136.329
        if execute_macro:
            hemisphere_50.hemisphere_50_delta()            
        execute_macro=False    
        tp.export.save_eps(f'{dir_path}/delta_{drag_or_lift}{case}_{key}.eps')
        tp.export.save_png(f'{dir_path}/delta_{drag_or_lift}{case}_{key}.png')



def save_Hemisphere_50(dir_path,case,dB_or_dBA='dBA',drag_or_lift=''):
    dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{case}/{case}/{drag_or_lift}OASPL.x', 
                                       solution_filenames=None,
                                       function_filenames=f'{dir_path}/{case}/{case}/{drag_or_lift}OASPL{dB_or_dBA}.fn', 
                                       name_filename=f'{dir_path}/{case}/{case}/{drag_or_lift}OASPL{dB_or_dBA}.nam')
    # print(dataset.variable_names)
    # print(dataset.zone_names)

    # loading_cb_levels=[35,40,45,50,55,60,56,70,75,80,85,90]
    # thickness_cb_levels=[20,25,30,35,40,45,50,55,60,56,70,75]
    loading_cb_levels=[20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
    thickness_cb_levels=[20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
    total_cb_levels=[40,44,48,52,56,60,64,68,72,76,80,84,88,92]
    cb_levels_dict={'thickness':thickness_cb_levels,'loading':loading_cb_levels,'total':total_cb_levels}
    
    frame = tp.active_frame()
    frame.plot().show_contour = True
    execute_macro=True
    for idx,key in enumerate(cb_levels_dict,4):
        tp.active_frame().plot().contour(0).variable_index=idx
    #    tp.active_frame().plot().contour(0).colormap_name='Sequential - Viridis'
        tp.active_frame().plot().contour(0).colormap_name='Modified Rainbow - Dark ends'
        tp.active_frame().plot().contour(0).levels.reset_levels(cb_levels_dict[key])
        tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
        tp.active_frame().plot().contour(0).legend.show_header=False
        tp.active_frame().plot().contour(0).legend.number_font.size=4.0
        tp.active_frame().plot().axes.orientation_axis.size=14
        tp.active_frame().plot().axes.orientation_axis.line_thickness=0.8
        tp.active_frame().plot().view.position=(630.581,
            tp.active_frame().plot().view.position[1],
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            379.91,
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            tp.active_frame().plot().view.position[1],
            416.552)
        tp.active_frame().plot().view.width=136.329
        if execute_macro:
            hemisphere_50.hemisphere_50()
        execute_macro=False    
        tp.export.save_eps(f'{dir_path}/{drag_or_lift}{case}_{key}.eps')
        tp.export.save_png(f'{dir_path}/{drag_or_lift}{case}_{key}.png')


def save_Hemisphere_150(dir_path,case,dB_or_dBA='dBA'):
    dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{case}/{case}/OASPL.x', 
                                       solution_filenames=None,
                                       function_filenames=f'{dir_path}/{case}/{case}/OASPL{dB_or_dBA}.fn', 
                                       name_filename=f'{dir_path}/{case}/{case}/OASPL{dB_or_dBA}.nam')
    loading_cb_levels=[40,45,50,55,60,65,70,75,80,85,90]
    thickness_cb_levels=[20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
    total_cb_levels=[50,55,60,65,70,75,80,85,90,95,100]
    cb_levels_dict={'thickness':thickness_cb_levels,'loading':loading_cb_levels,'total':total_cb_levels}
    
    frame = tp.active_frame()
    frame.plot().show_contour = True
    execute_macro=True
    for idx,key in enumerate(cb_levels_dict,4):
        tp.active_frame().plot().contour(0).variable_index=idx
    #    tp.active_frame().plot().contour(0).colormap_name='Sequential - Viridis'
        tp.active_frame().plot().contour(0).colormap_name='Modified Rainbow - Dark ends'
        tp.active_frame().plot().contour(0).levels.reset_levels(cb_levels_dict[key])
        tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
        tp.active_frame().plot().contour(0).legend.show_header=False
        tp.active_frame().plot().contour(0).legend.number_font.size=4.0
        tp.active_frame().plot().axes.orientation_axis.size=14
        tp.active_frame().plot().axes.orientation_axis.line_thickness=0.8
        if execute_macro:
            tp.macro.execute_command('''$!Pick AddAtPosition
              X = 9.01088082902
              Y = 3.66554404145
              ConsiderStyle = Yes''')
            tp.macro.execute_command('''$!Pick Shift
              X = 0.364766839378
              Y = 0.364766839378''')
        tp.active_frame().plot().view.position=(1907.83,
            tp.active_frame().plot().view.position[1],
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            1143.86,
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            tp.active_frame().plot().view.position[1],
            1221.95)
        tp.active_frame().plot().view.width=408.987
        if execute_macro:
            tp.macro.execute_command('''$!Pick SetMouseMode
              MouseMode = Select''')
            tp.macro.execute_command('''$!Pick AddAtPosition
              X = 8.7207253886
              Y = 1.48523316062
              ConsiderStyle = Yes''')
            tp.macro.execute_command('''$!Pick Shift
              X = -0.0497409326425
              Y = 0.248704663212''')
        execute_macro=False    
        tp.export.save_eps(f'{dir_path}/{case}/{case}/{case}_{key}.eps',render_type=1)
        tp.export.save_png(f'{dir_path}/{case}/{case}/{case}_{key}.png')
        
def save_Plane_50(dir_path,case,dB_or_dBA='dBA',drag_or_lift=''):
    dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{case}/{case}/{drag_or_lift}OASPL.x', 
                                       solution_filenames=None,
                                       function_filenames=f'{dir_path}/{case}/{case}/{drag_or_lift}OASPL{dB_or_dBA}.fn', 
                                       name_filename=f'{dir_path}/{case}/{case}/{drag_or_lift}OASPL{dB_or_dBA}.nam')
    # loading_cb_levels=[40,45,50,55,60,65,70,75,80]
    loading_cb_levels=[40,44,48,52,56,60,64,68,72,76,80]
    thickness_cb_levels=[20,25,30,35,40,45,50,55,60]
    # total_cb_levels=[40,44,48,52,56,60,64,68,72,76,80]
    total_cb_levels=[36,39,42,45,48,51,54,57,60,63,66,69,72,75,78,81]
    cb_levels_dict={'thickness':thickness_cb_levels,'loading':loading_cb_levels,'total':total_cb_levels}
    
    frame = tp.active_frame()
    frame.plot().show_contour = True
    frame.plot().show_mesh = True
    execute_macro=True
    for idx,key in enumerate(cb_levels_dict,4):
        tp.active_frame().plot().contour(0).variable_index=idx
        # tp.active_frame().plot().contour(0).colormap_name='Sequential - Viridis'
        tp.active_frame().plot().contour(0).colormap_name='Modified Rainbow - Dark ends'
        tp.active_frame().plot().contour(0).levels.reset_levels(cb_levels_dict[key])
        tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
        tp.active_frame().plot().contour(0).legend.show_header=False
        tp.active_frame().plot().contour(0).legend.number_font.size=4.0
        tp.active_frame().plot().axes.orientation_axis.size=14
        tp.active_frame().plot().axes.orientation_axis.line_thickness=0.8
        if execute_macro:
            tp.active_frame().plot().view.position=(1514.71,
                tp.active_frame().plot().view.position[1],
                tp.active_frame().plot().view.position[2])
            tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
                874.519,
                tp.active_frame().plot().view.position[2])
            tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
                tp.active_frame().plot().view.position[1],
                959.808)
            tp.active_frame().plot().view.width=336.172
            tp.active_frame().plot().view.position=(1496.82,
                tp.active_frame().plot().view.position[1],
                tp.active_frame().plot().view.position[2])
            tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
                899.943,
                tp.active_frame().plot().view.position[2])
            tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
                tp.active_frame().plot().view.position[1],
                964.635)
            tp.active_frame().plot().view.width=336.172
            tp.macro.execute_command('''$!Pick SetMouseMode
              MouseMode = Select''')
            tp.macro.execute_command('''$!Pick AddAtPosition
              X = 8.85336787565
              Y = 3.56606217617
              ConsiderStyle = Yes''')
            tp.macro.execute_command('''$!Pick Shift
              X = 0.107772020725
              Y = 0.878756476684''')
            tp.macro.execute_command('''$!Pick AddAtPosition
              X = 8.66269430052
              Y = 1.55155440415
              ConsiderStyle = Yes''')
            tp.macro.execute_command('''$!Pick Shift
              X = -0.472538860104
              Y = 0.339896373057''')
            tp.macro.execute_command('''$!Pick AddAtPosition
              X = 4.45958549223
              Y = 7.33808290155
              ConsiderStyle = Yes''')
            tp.macro.execute_command('''$!Pick SetMouseMode
              MouseMode = Select''')
            tp.macro.execute_command("""$!AttachText 
              AnchorPos
                {
                X = 92.2061
                Y = 70.7668
                }
              TextShape
                {
                SizeUnits = Frame
                Height = 5
                }
              Box
                {
                Margin = 10
                LineThickness = 0.4
                }
              Anchor = HeadRight
              TextType = LaTeX
              Text = 'dB'""")
            create_rotor_on_plane.plane_50()

        execute_macro=False    
        tp.export.save_eps(f'{dir_path}/{drag_or_lift}{case}_{key}.eps',render_type=0)
        tp.export.save_png(f'{dir_path}/{drag_or_lift}{case}_{key}.png')
        # tp.export.save_png(f'{dir_path}/{drag_or_lift}{case}_{key}.png')


def save_Plane_50_extended(dir_path,case,dB_or_dBA='dBA',drag_or_lift=''):

    # loading_cb_levels=[42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76]
    # thickness_cb_levels=[20,25,30,35,40,45,50,55,60]
    # total_cb_levels=[42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76]
    loading_cb_levels=[20,24,28,32,36,40,44,48,52,56,58,62]
    thickness_cb_levels=[20,25,30,35,40,45,50,55,60]
    total_cb_levels=[20,24,28,32,36,40,44,48,52,56,58,62]
    cb_levels_dict={'thickness':thickness_cb_levels,'loading':loading_cb_levels,'total':total_cb_levels}

    for idx,key in enumerate(cb_levels_dict,4):
        tp.new_layout()
        dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{case}/{case}/{drag_or_lift}OASPL.x', 
                                           solution_filenames=None,
                                           function_filenames=f'{dir_path}/{case}/{case}/{drag_or_lift}OASPL{dB_or_dBA}.fn', 
                                           name_filename=f'{dir_path}/{case}/{case}/{drag_or_lift}OASPL{dB_or_dBA}.nam')
        frame = tp.active_frame()
        frame.plot().show_contour = True
        frame.plot().show_mesh = False
        tp.active_frame().plot().contour(0).variable_index=idx
        # tp.active_frame().plot().contour(0).colormap_name='Sequential - Viridis'
        tp.active_frame().plot().contour(0).colormap_name='Modified Rainbow - Dark ends'
        tp.active_frame().plot().contour(0).levels.reset_levels(cb_levels_dict[key])
        tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
        tp.active_frame().plot().contour(0).legend.show_header=False
        tp.active_frame().plot().contour(0).legend.number_font.size=4.0
        tp.active_frame().plot().axes.orientation_axis.size=14
        tp.active_frame().plot().axes.orientation_axis.line_thickness=0.8       
        getattr(plane_50_extended, key)()
        tp.export.save_eps(f'{dir_path}/{drag_or_lift}{case}_{key}.eps')
        tp.export.save_png(f'{dir_path}/{drag_or_lift}{case}_{key}.png')

def save_Plane_50_extended_animatepressure(dir_path,case,animation_dict,dB_or_dBA='dBA',drag_or_lift=''):
    dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{case}/{case}/pressure.x', 
                                        solution_filenames=None,
                                        function_filenames=f'{dir_path}/{case}/{case}/pressure.fn', 
                                        name_filename=f'{dir_path}/{case}/{case}/pressure.nam')
    tp.active_frame().plot().rgb_coloring.red_variable_index=3
    tp.active_frame().plot().rgb_coloring.green_variable_index=3
    tp.active_frame().plot().rgb_coloring.blue_variable_index=3
    tp.active_frame().plot().contour(0).variable_index=3
    tp.active_frame().plot().contour(1).variable_index=4
    tp.active_frame().plot().contour(2).variable_index=5
    tp.active_frame().plot().contour(3).variable_index=6
    tp.active_frame().plot().contour(4).variable_index=7
    tp.active_frame().plot().contour(5).variable_index=8
    tp.active_frame().plot().contour(6).variable_index=9
    tp.active_frame().plot().contour(7).variable_index=10
    tp.active_frame().plot(PlotType.Cartesian3D).show_isosurfaces=True
    tp.active_frame().plot().isosurface(0).contour.flood_contour_group_index=1
    tp.active_frame().plot().isosurface(0).isosurface_values[0]=0.2

    #from here on it should call the animatemp4_multiprocess


def save_Plane_50_extended_delta(dir_path,case,baseline_case,dB_or_dBA='dBA',drag_or_lift=''): 
    if case==baseline_case: return
    
    loading_cb_levels=[-14,-12,-10,-8,-6,-4,-2,0,2,4]
    thickness_cb_levels=[-5,-4,-3,-2,-1,1,2]
    total_cb_levels=[-15,-13,-11,-9,-7,-5,-3,-1,1,3,5]
    cb_levels_dict={'thickness':thickness_cb_levels,'loading':loading_cb_levels,'total':total_cb_levels}
    
    for idx,key in enumerate(cb_levels_dict,4):
        tp.new_layout()
        dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{case}/{case}/{drag_or_lift}OASPL.x', 
                                           solution_filenames=None,
                                           function_filenames=f'{dir_path}/{case}/{case}/{drag_or_lift}OASPL{dB_or_dBA}.fn', 
                                           name_filename=f'{dir_path}/{case}/{case}/{drag_or_lift}OASPL{dB_or_dBA}.nam')
        dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{baseline_case}/{baseline_case}/{drag_or_lift}OASPL.x', 
                                           solution_filenames=None,
                                           function_filenames=f'{dir_path}/{baseline_case}/{baseline_case}/{drag_or_lift}OASPL{dB_or_dBA}.fn', 
                                           name_filename=f'{dir_path}/{baseline_case}/{baseline_case}/{drag_or_lift}OASPL{dB_or_dBA}.nam')
        delta_zone = dataset.add_zone(ZoneType.Ordered, 'Delta_Zone', dataset.zone(0).dimensions)   
    
        for var in dataset.variable_names[:-3]:
            delta_zone.values(var)[:]=dataset.zone(0).values(var)[:]
        for var in dataset.variable_names[-3:]:
            delta_zone.values(var)[:]=dataset.zone(0).values(var)[:]-dataset.zone(1).values(var)[:]
            
        dataset.delete_zones(dataset.zone(0))
        dataset.delete_zones(dataset.zone(0))
        frame = tp.active_frame()
        frame.plot().fieldmap(0).show=True
        frame.plot().show_contour = True
        tp.active_frame().plot().contour(0).variable_index=idx
        # tp.active_frame().plot().contour(0).colormap_name='Sequential - Viridis'
        tp.active_frame().plot().contour(0).colormap_name='Modified Rainbow - Dark ends'
        tp.active_frame().plot().contour(0).levels.reset_levels(cb_levels_dict[key])
        tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
        tp.active_frame().plot().contour(0).legend.show_header=False
        tp.active_frame().plot().contour(0).legend.number_font.size=4.0
        tp.active_frame().plot().axes.orientation_axis.size=14
        tp.active_frame().plot().axes.orientation_axis.line_thickness=0.8
        getattr(plane_50_extended_delta, key)()
        tp.export.save_eps(f'{dir_path}/delta_{drag_or_lift}{case}_{key}.eps')
        tp.export.save_png(f'{dir_path}/delta_{drag_or_lift}{case}_{key}.png')

def save_Hemisphere_50_pressure(dir_path,case,connectTec = False):
    if connectTec:
        tp.session.connect(port=7600)
        tp.new_layout()
        
    loading_cb_levels = np.linspace(-0.1,0.5, 13)
    thickness_cb_levels = np.linspace(-0.55,0.15, 15)
    total_cb_levels=np.linspace(-0.3,0.5, 17)
    cb_levels_dict={'thickness':thickness_cb_levels,'loading':loading_cb_levels,'total':total_cb_levels}
    dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{case}/{case}/pressure.x', 
                                        solution_filenames=None,
                                        function_filenames=f'{dir_path}/{case}/{case}/pressure.fn', 
                                        name_filename=f'{dir_path}/{case}/{case}/pressure.nam')
    frame = tp.active_frame()
    frame.plot().show_contour = True
    # for idx,key in enumerate(cb_levels_dict,4):
    #     tp.active_frame().plot().contour(0).variable_index=idx
    # #    tp.active_frame().plot().contour(0).colormap_name='Sequential - Viridis'
    #     tp.active_frame().plot().contour(0).colormap_name='Modified Rainbow - Dark ends'
    #     tp.active_frame().plot().contour(0).levels.reset_levels(cb_levels_dict[key])
    #     tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
    #     tp.active_frame().plot().contour(0).legend.show_header=False
    #     tp.active_frame().plot().contour(0).legend.number_font.size=4.0
    #     tp.active_frame().plot().axes.orientation_axis.size=14
    #     tp.active_frame().plot().axes.orientation_axis.line_thickness=0.8


    #     tp.active_frame().plot(PlotType.Cartesian3D).show_isosurfaces=True
    #     tp.active_frame().plot().isosurface(0).contour.flood_contour_group_index=1
    #     tp.export.save_eps(f'{dir_path}/{case}/{case}/pressure_{key}.eps')
    #     tp.export.save_png(f'{dir_path}/{case}/{case}/pressure_{key}.png')

def save_sphere50(dir_path,case,dB_or_dBA='dBA',drag_or_lift=''):
    dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{case}_OASPL.x', 
                                       solution_filenames=None,
                                       function_filenames=f'{dir_path}/{case}_OASPL{dB_or_dBA}.fn', 
                                       name_filename=f'{dir_path}/{case}_OASPL{dB_or_dBA}.nam')
    # print(dataset.variable_names)
    # print(dataset.zone_names)

    # loading_cb_levels=[35,40,45,50,55,60,56,70,75,80,85,90]
    # thickness_cb_levels=[20,25,30,35,40,45,50,55,60,56,70,75]
    loading_cb_levels=[20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
    thickness_cb_levels=[20,25,30,35,40,45,50,55,60,65,70,75,80,85,90]
    total_cb_levels=[40,44,48,52,56,60,64,68,72,76,80,84,88,92]
    cb_levels_dict={'thickness':thickness_cb_levels,'loading':loading_cb_levels,'total':total_cb_levels}
    
    frame = tp.active_frame()
    frame.plot().show_contour = True
    execute_macro=True
    for idx,key in enumerate(cb_levels_dict,4):
        tp.active_frame().plot().contour(0).variable_index=idx
    #    tp.active_frame().plot().contour(0).colormap_name='Sequential - Viridis'
        tp.active_frame().plot().contour(0).colormap_name='Modified Rainbow - Dark ends'
        # tp.active_frame().plot().contour(0).levels.reset_levels(cb_levels_dict[key])
        # tp.active_frame().plot().contour(0).levels.reset_levels.reset_to_nice()
        tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
        tp.active_frame().plot().contour(0).legend.show_header=False
        tp.active_frame().plot().contour(0).legend.number_font.size=4.0
        tp.active_frame().plot().axes.orientation_axis.size=14
        tp.active_frame().plot().axes.orientation_axis.line_thickness=0.8
        tp.active_frame().plot().view.position=(630.581,
            tp.active_frame().plot().view.position[1],
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            379.91,
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            tp.active_frame().plot().view.position[1],
            416.552)
        tp.active_frame().plot().view.width=136.329
        if execute_macro:
            hemisphere_50.hemisphere_50()
        execute_macro=False    
        # tp.export.save_eps(f'{dir_path}/{drag_or_lift}{case}_{key}.eps')
        tp.export.save_png(f'{dir_path}/{drag_or_lift}{case}_{key}.png')

def save_plane50extended(dir_path,case,dB_or_dBA='dBA',drag_or_lift=''):

    # loading_cb_levels=[42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76]
    # thickness_cb_levels=[20,25,30,35,40,45,50,55,60]
    # total_cb_levels=[42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76]
    loading_cb_levels=[20,24,28,32,36,40,44,48,52,56,58,62]
    thickness_cb_levels=[20,25,30,35,40,45,50,55,60]
    total_cb_levels=[20,24,28,32,36,40,44,48,52,56,58,62]
    cb_levels_dict={'thickness':thickness_cb_levels,'loading':loading_cb_levels,'total':total_cb_levels}

    for idx,key in enumerate(cb_levels_dict,4):
        tp.new_layout()
        dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{case}_OASPL.x', 
                                           solution_filenames=None,
                                           function_filenames=f'{dir_path}/{case}_OASPL{dB_or_dBA}.fn', 
                                           name_filename=f'{dir_path}/{case}_OASPL{dB_or_dBA}.nam')
        frame = tp.active_frame()
        frame.plot().show_contour = True
        frame.plot().show_mesh = False
        tp.active_frame().plot().contour(0).variable_index=idx
        # tp.active_frame().plot().contour(0).colormap_name='Sequential - Viridis'
        tp.active_frame().plot().contour(0).colormap_name='Modified Rainbow - Dark ends'
        # tp.active_frame().plot().contour(0).levels.reset_levels(cb_levels_dict[key])
        tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
        tp.active_frame().plot().contour(0).legend.show_header=False
        tp.active_frame().plot().contour(0).legend.number_font.size=4.0
        tp.active_frame().plot().axes.orientation_axis.size=14
        tp.active_frame().plot().axes.orientation_axis.line_thickness=0.8       
        getattr(plane_50_extended, key)()
        # tp.export.save_eps(f'{dir_path}/{drag_or_lift}{case}_{key}.eps')
        tp.export.save_png(f'{dir_path}/{drag_or_lift}{case}_{key}.png')

def save_sphere50pressure(dir_path,case,connectTec = False):
    if connectTec:
        tp.session.connect(port=7600)
        tp.new_layout()
        
    loading_cb_levels = np.linspace(-0.1,0.5, 13)
    thickness_cb_levels = np.linspace(-0.55,0.15, 15)
    total_cb_levels=np.linspace(-0.3,0.5, 17)
    cb_levels_dict={'thickness':thickness_cb_levels,'loading':loading_cb_levels,'total':total_cb_levels}
    dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{case}_pressure.x', 
                                       solution_filenames=None,
                                       function_filenames=f'{dir_path}/{case}_pressure.fn', 
                                       name_filename=f'{dir_path}/{case}_pressure.nam')
    frame = tp.active_frame()
    frame.plot().show_contour = True
    for idx,key in enumerate(cb_levels_dict,4):
        tp.active_frame().plot().contour(0).variable_index=idx
    #    tp.active_frame().plot().contour(0).colormap_name='Sequential - Viridis'
        tp.active_frame().plot().contour(0).colormap_name='Modified Rainbow - Dark ends'
        tp.active_frame().plot().contour(0).levels.reset_levels(cb_levels_dict[key])
        tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
        tp.active_frame().plot().contour(0).legend.show_header=False
        tp.active_frame().plot().contour(0).legend.number_font.size=4.0
        tp.active_frame().plot().axes.orientation_axis.size=14
        tp.active_frame().plot().axes.orientation_axis.line_thickness=0.8


        tp.active_frame().plot(PlotType.Cartesian3D).show_isosurfaces=True
        tp.active_frame().plot().isosurface(0).contour.flood_contour_group_index=1
        tp.export.save_eps(f'{dir_path}/{case}/{case}/pressure_{key}.eps')
        tp.export.save_png(f'{dir_path}/{case}/{case}/pressure_{key}.png')

def save_validationplane(dir_path,case,dB_or_dBA='dB',drag_or_lift=''):

    # loading_cb_levels=[20,24,28,32,36,40,44,48,52,56,58,62]
    # thickness_cb_levels=[20,24,28,32,36,40,44,48,52,56,58,62]
    # total_cb_levels=[20,24,28,32,36,40,44,48,52,56,58,62]
    loading_cb_levels=np.linspace(86,116,16)
    thickness_cb_levels=np.linspace(86,116,16)
    total_cb_levels=np.linspace(86,116,16)
    cb_levels_dict={'thickness':thickness_cb_levels,'loading':loading_cb_levels,'total':total_cb_levels}
    # cb_levels_dict={'total':total_cb_levels}

    for idx,key in enumerate(cb_levels_dict,4):
        tp.new_layout()
        dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{case}_OASPL.x', 
                                           solution_filenames=None,
                                           function_filenames=f'{dir_path}/{case}_OASPL{dB_or_dBA}.fn', 
                                           name_filename=f'{dir_path}/{case}_OASPL{dB_or_dBA}.nam')
        frame = tp.active_frame()
        frame.plot().show_contour = True
        frame.plot().show_mesh = False
        tp.active_frame().plot().contour(0).variable_index=idx
        # tp.active_frame().plot().contour(0).colormap_name='Sequential - Viridis'
        tp.active_frame().plot().contour(0).colormap_name='Modified Rainbow - Dark ends'
        tp.active_frame().plot().contour(0).levels.reset_levels(cb_levels_dict[key])
        tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
        tp.active_frame().plot().contour(0).legend.show_header=False
        tp.active_frame().plot().contour(0).legend.number_font.size=4.0
        tp.active_frame().plot().axes.orientation_axis.size=14
        tp.active_frame().plot().axes.orientation_axis.line_thickness=0.8       
        validationplane.xyplot()
        validationplane.labelandminorfix()
        tp.export.save_png(f'{dir_path}/{drag_or_lift}{case}_{key}.png')

def save_hemisphere50(dir_path,case,dB_or_dBA='dBA',drag_or_lift='',show_vinf=True):
    # print(dataset.variable_names)
    # print(dataset.zone_names)

    loading_cb_levels=[40,45,50,55,60,65,70,75,80,85,90,95,100]
    thickness_cb_levels=[40,45,50,55,60,65,70,75,80,85,90,95,100]
    total_cb_levels=np.arange(64,116,2)
    total_cb_levels=[64,66,68,70,72,74,76,78,80,82,84,86,88,92]
    if show_vinf:
        cb_levels_dict={'thickness':np.arange(50,100,4),'loading':np.arange(50,110,4),'total':np.arange(50,110,4)}
    else:
        cb_levels_dict={'thickness':np.arange(10,50,4),'loading':np.arange(68,82,1),'total':np.arange(68,82,1)}
    
    for idx,key in enumerate(cb_levels_dict,4):
        tp.new_layout()
        dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{case}_OASPL.x', 
                                           solution_filenames=None,
                                           function_filenames=f'{dir_path}/{case}_OASPL{dB_or_dBA}.fn', 
                                           name_filename=f'{dir_path}/{case}_OASPL{dB_or_dBA}.nam')
        frame = tp.active_frame()
        frame.plot().show_contour = True
        frame.plot().show_mesh = False
        tp.active_frame().plot().contour(0).variable_index=idx
    #    tp.active_frame().plot().contour(0).colormap_name='Sequential - Viridis'
        tp.active_frame().plot().contour(0).colormap_name='Modified Rainbow - Dark ends'
        tp.active_frame().plot().contour(0).levels.reset_levels(cb_levels_dict[key])
        tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
        tp.active_frame().plot().contour(0).legend.show_header=False
        tp.active_frame().plot().contour(0).legend.number_font.size=4.0
        tp.active_frame().plot().axes.orientation_axis.size=14
        tp.active_frame().plot().axes.orientation_axis.line_thickness=0.8
        tp.active_frame().plot().view.position=(630.581,
            tp.active_frame().plot().view.position[1],
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            379.91,
            tp.active_frame().plot().view.position[2])
        tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
            tp.active_frame().plot().view.position[1],
            416.552)
        tp.active_frame().plot().view.width=136.329
        tp.macro.execute_file('/home/HT/ge56beh/Work/HeliNoise/TecPlot/macros/hemisphere50.mcr')
        if show_vinf:
        	tp.macro.execute_file('/home/HT/ge56beh/Work/HeliNoise/TecPlot/macros/forwardflight.mcr')
        else:
        	tp.macro.execute_file('/home/HT/ge56beh/Work/HeliNoise/TecPlot/macros/hover.mcr')
        
        # if not show_vinf:
        #     tp.macro.execute_command('''$!Pick AddAtPosition
        #                               X = 7.52849002849
        #                               Y = 4.34116809117
        #                           ConsiderStyle = Yes''')
        #     tp.macro.execute_command('$!Pick Clear')
        #     tp.macro.execute_command('''$!Pick AddAtPosition
        #                               X = 6.0584045584
        #                               Y = 4.5462962963
        #                           ConsiderStyle = Yes''')
        #     tp.macro.execute_command('$!Pick Clear')

        #     tp.macro.execute_command('''$!ThreeDView 
        #       ViewerPosition
        #         {
        #         X = 625.4412742262031
        #         Y = 361.4471645785457
        #         Z = 440.2508731615613
        #         }
        #       ViewWidth = 186.475''')
        #     tp.macro.execute_command('''$!Pick AddAtPosition
        #       X = 5.81908831909
        #       Y = 3.05341880342
        #       ConsiderStyle = Yes''')
        #     tp.macro.execute_command('''$!Pick Shift
        #       X = 1.24216524217
        #       Y = -0.148148148148''')
        tp.export.save_png(f'{dir_path}/{dB_or_dBA}_{drag_or_lift}{case}_{key}.png')
        # if key=='total':
        folder_path = '/'.join(dir_path.split('/')[:-2])
        filename=dir_path.split('/')[-1]
        tp.export.save_png(f'{folder_path}/Allfigures/{dB_or_dBA}_{key}_{drag_or_lift}{case}_{filename}.png')

def save_plane50extendedfinal(dir_path,case,dB_or_dBA='dBA',drag_or_lift='',show_vinf=True):
    
    loading_cb_levels=[40,45,50,55,60,65,70,75,80,85,90]
    thickness_cb_levels=[40,45,50,55,60,65,70,75,80,85,90]
    total_cb_levels=np.arange(64,116,2)
    total_cb_levels=[64,66,68,70,72,74,76,78,80,82,84,86,88,92]
    if show_vinf:
        cb_levels_dict={'thickness':np.arange(50,90,4),'loading':np.arange(50,100,4),'total':np.arange(50,100,4)}
    else:    
        cb_levels_dict={'thickness':np.arange(10,50,3),'loading':np.arange(40,94,2),'total':np.arange(49,94,3)}

    for idx,key in enumerate(cb_levels_dict,4):
        tp.new_layout()
        dataset = tp.data.load_plot3d(grid_filenames=f'{dir_path}/{case}_OASPL.x', 
                                           solution_filenames=None,
                                           function_filenames=f'{dir_path}/{case}_OASPL{dB_or_dBA}.fn', 
                                           name_filename=f'{dir_path}/{case}_OASPL{dB_or_dBA}.nam')
        frame = tp.active_frame()
        frame.plot().show_contour = True
        frame.plot().show_mesh = False
        tp.active_frame().plot().contour(0).variable_index=idx
        # tp.active_frame().plot().contour(0).colormap_name='Sequential - Viridis'
        tp.active_frame().plot().contour(0).colormap_name='Modified Rainbow - Dark ends'
        tp.active_frame().plot().contour(0).levels.reset_levels(cb_levels_dict[key])
        tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
        tp.active_frame().plot().contour(0).legend.show_header=False
        tp.active_frame().plot().contour(0).legend.number_font.size=4.0
        tp.active_frame().plot().axes.orientation_axis.size=14
        tp.active_frame().plot().axes.orientation_axis.line_thickness=0.8       
        plane50extended.cleanup(show_vinf=show_vinf)
        tp.export.save_png(f'{dir_path}/{dB_or_dBA}_{drag_or_lift}{case}_{key}.png')
        # if key=='total':
        folder_path = '/'.join(dir_path.split('/')[:-2])
        filename=dir_path.split('/')[-1]
        tp.export.save_png(f'{folder_path}/Allfigures/{dB_or_dBA}_{key}_{drag_or_lift}{case}_{filename}.png')


if __name__ == "__main__":
    main_directry = '/home/HT/ge56beh/Work/Python/HeliNoise/Data/Diss_runs/2_simple_hemisphere_aperiodic'
    filename = '1994_Run15_5_hover_FishBAC_PetersUnsteady'
    
    save_Hemisphere_50_pressure(main_directry,filename,connectTec = True)    
    
