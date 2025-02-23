#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 11:23:57 2021

@author: ge56beh
"""

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

def cleanup(show_vinf=True):
    tp.macro.execute_command('''$!ThreeDView 
      ViewerPosition
        {
        X = 3063.838347834397
        Y = 1846.46520542053
        Z = 2082.114366797639
        }
      ViewWidth = 784.222''')
    tp.macro.execute_command('''$!ThreeDView 
      ViewerPosition
        {
        X = 2948.042366332285
        Y = 1878.219572276276
        Z = 2228.30825067264
        }
      ViewWidth = 784.222''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 8.73646723647
      Y = 1.35541310541
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = -1.98290598291
      Y = 2.25641025641''')
    tp.macro.execute_command('''$!Pick Shift
      X = -0.0569800569801
      Y = -0.763532763533''')
    tp.macro.execute_command('''$!Pick Shift
      X = -1.19658119658
      Y = 0''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 8.6339031339
      Y = 2.8141025641
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 8.6339031339
      Y = 2.8141025641
      CollectingObjectsMode = HomogeneousAdd
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{NumberTextShape{FontFamily = 'Times New Roman'}}''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{NumberTextShape{SizeUnits = Point}}''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{Header{Show = Yes}}''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{Header{UseCustomText = Yes}}''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{Header{CustomText = 'dB'}}''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{Header{TextShape{FontFamily = 'Times New Roman'}}}''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{Header{TextShape{SizeUnits = Point}}}''')
    tp.macro.execute_command('$!RedrawAll') 
    tp.macro.execute_command('$!GlobalContour 1  Legend{Header{TextShape{Height = 25.3999999999999986}}}')
    tp.macro.execute_command('''$!AttachGeom 
      AnchorPos
        {
        X = 195.6211812611272
        Y = 214.4881987431506
        }
      RawData
    1
    2
    0 0 
    -56.6010513306 -57.5940551758''')
    tp.macro.execute_command('''$!Pick SetMouseMode
      MouseMode = Select''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.38888888889
      Y = 4.10185185185
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.38888888889
      Y = 4.10185185185
      CollectingObjectsMode = HomogeneousAdd
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.17236467236
      Y = 4.40954415954
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.11538461538
      Y = 4.40954415954
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.11538461538
      Y = 4.40954415954
      CollectingObjectsMode = HomogeneousAdd
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!FrameControl ActivateAtPosition
      X = 6.81054131054
      Y = 4.35256410256''')
    tp.macro.execute_command('''$!Pick SetMouseMode
      MouseMode = Select''')
    tp.macro.execute_command("""$!AttachText 
      AnchorPos
        {
        X = 64.56157011712567
        Y = 48.71794871794871
        }
      TextShape
        {
        Height = 20
        }
      TextType = LaTeX
      Text = '$\mathbf{V_{\infty}}$'""") 
    tp.macro.execute_command('$!RedrawAll') 
    tp.macro.execute_command('''$!Pick SetMouseMode
      MouseMode = Select''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.91310541311
      Y = 4.25
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.91310541311
      Y = 4.25
      CollectingObjectsMode = HomogeneousAdd
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Magnify
      Mag = 1.05''')
    tp.macro.execute_command('''$!Pick Magnify
      Mag = 1.05''')
    tp.macro.execute_command('''$!Pick Magnify
      Mag = 1.05''')
    tp.macro.execute_command('''$!Pick Magnify
      Mag = 1.05''')
    tp.macro.execute_command('''$!Pick Magnify
      Mag = 1.05''')
    tp.macro.execute_command('''$!Pick Magnify
      Mag = 1.05''')
    tp.macro.execute_command('$!RedrawAll') 
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.04700854701
      Y = 0.683048433048
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 5.56837606838
      Y = 2.83689458689
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = -0.547008547009
      Y = 0.364672364672''')
    tp.macro.execute_command('''$!Pick Shift
      X = -0.034188034188
      Y = 0.148148148148''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 3.01566951567
      Y = 3.74857549858
      ConsiderStyle = Yes''')
    tp.macro.execute_command('$!FrameLayout ShowBorder = No')
    tp.macro.execute_command('$!RedrawAll')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.45726495726
      Y = 4.11324786325
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.32051282051
      Y = 4.2613960114
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.25213675214
      Y = 4.30698005698
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.57122507123
      Y = 3.9537037037
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.57122507123
      Y = 3.9537037037
      CollectingObjectsMode = HomogeneousAdd
      ConsiderStyle = Yes''')
    tp.macro.execute_command('$!Pick Clear')
    tp.macro.execute_command('''$!AttachGeom 
      AnchorPos
        {
        X = 195.6211812611272
        Y = 214.4881987431506
        }
      LineThickness = 0.3
      ArrowheadStyle = Filled
      ArrowheadAttachment = AtEnd
      ArrowheadSize = 3
      ArrowheadAngle = 22
      RawData
    1
    2
    0 0 
    -56.6010513306 -57.5940551758''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 7.01566951567
      Y = 4.11324786325
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 7.01566951567
      Y = 4.11324786325
      CollectingObjectsMode = HomogeneousAdd
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Magnify
      Mag = 1.05''')
    tp.macro.execute_command('''$!Pick Magnify
      Mag = 1.05''')
    tp.macro.execute_command('$!RedrawAll')     
    if not show_vinf:
        tp.macro.execute_command('''$!Pick AddAtPosition
                              X = 7.00427350427
                              Y = 4.12464387464
                              ConsiderStyle = Yes''')
        tp.macro.execute_command('$!Pick Clear')
        tp.macro.execute_command('''$!Pick AddAtPosition
                              X = 6.21794871795
                              Y = 4.31837606838
                              ConsiderStyle = Yes''')
        tp.macro.execute_command('$!Pick Clear')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 4.91963015647
          Y = 3.34530583215
          ConsiderStyle = Yes''')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 4.91963015647
          Y = 3.34530583215
          CollectingObjectsMode = HomogeneousAdd
          ConsiderStyle = Yes''')
        tp.macro.execute_command('$!ThreeDAxis FrameAxis{Size = 15.0000000000000018}')
        tp.macro.execute_command('$!ThreeDAxis FrameAxis{Size = 16}')
        tp.macro.execute_command('$!ThreeDAxis FrameAxis{Size = 17}')
        tp.macro.execute_command('$!ThreeDAxis FrameAxis{Size = 18}')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 9.18705547653
          Y = 3.20874822191
          ConsiderStyle = Yes''')
        tp.macro.execute_command('''$!Pick AddAtPosition
          X = 9.18705547653
          Y = 3.20874822191
          CollectingObjectsMode = HomogeneousAdd
          ConsiderStyle = Yes''')
        tp.macro.execute_command('$!GlobalContour 1  Legend{NumberTextShape{Height = 29}}')
        tp.macro.execute_command('$!GlobalContour 1  Legend{Header{TextShape{Height = 33}}}')
        tp.macro.execute_command('$!RedrawAll') 
        tp.macro.execute_command('''$!Pick Shift
          X = 0.0455192034139
          Y = -1.08108108108''')
        tp.macro.execute_command('''$!Pick Shift
          X = -0.0682788051209
          Y = -0.512091038407''')
    
def hemisphere():
    pass    