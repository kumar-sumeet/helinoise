#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 14:47:01 2020

@author: ge56beh
"""

import os

import tecplot 
from tecplot.constant import *

# Run this script with "-c" to connect to Tecplot 360 on port 7600
# To enable connections in Tecplot 360, click on:
#   "Scripting" -> "PyTecplot Connections..." -> "Accept connections"
tecplot.new_layout()
tecplot.session.connect()

examples_dir = tecplot.session.tecplot_examples_directory()
datafile = os.path.join(examples_dir, 'SimpleData', 'Rainfall.dat')
dataset = tecplot.data.load_tecplot(datafile)

frame = tecplot.active_frame()
plot = frame.plot()
frame.plot_type = tecplot.constant.PlotType.XYLine

for i in range(3):
    plot.linemap(i).show = True
    plot.linemap(i).line.line_thickness = .4

y_axis = plot.axes.y_axis(0)
y_axis.title.title_mode = AxisTitleMode.UseText
y_axis.title.text = 'Rainfall (in)'
y_axis.fit_range_to_nice()

legend = plot.legend
legend.show = True
legend.box.box_type = TextBox.Filled
legend.box.color = Color.Purple
legend.box.fill_color = Color.LightGrey
legend.box.line_thickness = .4
legend.box.margin = 5

legend.anchor_alignment = AnchorAlignment.MiddleRight
legend.row_spacing = 1.5
legend.show_text = True
legend.font.typeface = 'Arial'
legend.font.italic = True

legend.text_color = Color.Black
legend.position = (90, 88)

tecplot.export.save_png('legend_line.png', 600, supersample=3)