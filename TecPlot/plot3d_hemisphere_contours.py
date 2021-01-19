#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
(Multi-observer)
Accepts path to finished hemisphere acoustics PSU-WOPWOP files and generates
(and saves) hemisphere contours plots
"""

import tecplot as tp
import os
import sys
from tecplot.constant import ZoneType

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
from HeliNoise.TecPlot import pytecplot
tp.new_layout()
tp.session.connect()


dir_path='/home/HT/ge56beh/Work/Python/Data_SciTech_2021/PSU_WOPWOP/Misc_results/Hemisphere_50'
baseline_case='baseline_highresAero_hartstyl_hemisphere'
case = '0.750_0.300_1.960_000.0_0.000_355.0_0.980_0.0_0.0_0.0_0.0_0.0_0.0_highresAero_hartstyl_hemisphere'

drag_or_lift='' # enter 'drag' or 'lift' if just need to accoust for acoustic footpprint due to drag forces or lift forces only
dB_or_dBA='dBA' # enter 'db' or 'dBA'  

  
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
        tp.macro.execute_command('''$!Pick SetMouseMode
          MouseMode = Select''')
        tp.macro.execute_command('$!Pick DeselectAll')
        tp.macro.execute_command('''$!Pick AddAllInRect
          SelectText = Yes
          SelectGeoms = Yes
          SelectZones = Yes
          ConsiderStyle = Yes
          X1 = 8.90455341506
          X2 = 9.04465849387
          Y1 = 3.0380910683
          Y2 = 3.57049036778''')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 8.96059544658
          Y = 3.50043782837
          ConsiderStyle = Yes''')
        tp.macro.execute_command('''$!Pick Shift
          X = -0.210157618214
          Y = 1.23292469352''')
        tp.macro.execute_command('''$!Pick Shift
          X = -0.0700525394046
          Y = 0.266199649737''')
        tp.macro.execute_command('''$!Pick Shift
          X = -0.224168126095
          Y = 0.364273204904''')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 8.5823117338
          Y = 4.69133099825
          ConsiderStyle = Yes''')
        tp.macro.execute_command('''$!Pick Shift
          X = 0.182136602452
          Y = -0.882661996497''')
        tp.macro.execute_command('''$!Pick Shift
          X = 0
          Y = -0.168126094571''')
        tp.macro.execute_command('''$!Pick Shift
          X = -0.0140105078809
          Y = -0.168126094571''')
        tp.macro.execute_command('''$!Pick SetMouseMode
          MouseMode = Select''')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 8.56830122592
          Y = 1.44089316988
          ConsiderStyle = Yes''')
        tp.macro.execute_command('''$!Pick Shift
          X = -0.266199649737
          Y = 0.490367775832''')
        tp.macro.execute_command('''$!FrameControl ActivateAtPosition
          X = 8.23204903678
          Y = 2.53371278459''')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 8.2180385289
          Y = 4.36908931699
          ConsiderStyle = Yes''')
        tp.macro.execute_command('''$!Pick Shift
          X = 0.196147110333
          Y = 0.0280210157618''')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 8.5823117338
          Y = 2.33756567426
          ConsiderStyle = Yes''')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 8.56830122592
          Y = 2.35157618214
          ConsiderStyle = Yes''')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 8.5122591944
          Y = 2.40761821366
          ConsiderStyle = Yes''')
        tp.macro.execute_command('''$!Pick Shift
          X = 0.0280210157618
          Y = 0.0700525394046''')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 8.54028021016
          Y = 2.47767075306
          ConsiderStyle = Yes''')

        tp.macro.execute_command('''$!Pick SetMouseMode
          MouseMode = Select''')
        tp.macro.execute_command("""$!AttachText 
          AnchorPos
            {
            X = 86.3561004086398
            Y = 72.45359019264448
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
          Text = '$\\Delta$dB'""")
        
    execute_macro=False    
    tp.export.save_eps(f'{dir_path}/{case}/{case}/delta_{drag_or_lift}{case}_{key}.eps')
    tp.export.save_png(f'{dir_path}/{case}/{case}/delta_{drag_or_lift}{case}_{key}.png')
