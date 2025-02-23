#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 11:23:57 2021

@author: ge56beh
"""

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

def thickness():
    tp.active_frame().plot().view.position=(3504.42,
        tp.active_frame().plot().view.position[1],
        tp.active_frame().plot().view.position[2])
    tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
        2138.75,
        tp.active_frame().plot().view.position[2])
    tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
        tp.active_frame().plot().view.position[1],
        2419.62)
    tp.active_frame().plot().view.width=812.486
    tp.active_frame().plot().view.position=(3472.61,
        tp.active_frame().plot().view.position[1],
        tp.active_frame().plot().view.position[2])
    tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
        2205.07,
        tp.active_frame().plot().view.position[2])
    tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
        tp.active_frame().plot().view.position[1],
        2409.89)
    tp.active_frame().plot().view.width=812.486
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 8.95699481865
      Y = 4.29559585492
      ConsiderStyle = Yes''')
    tp.active_frame().plot().contour(0).legend.show_header=False
    tp.macro.execute_command('$!RedrawAll')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 8.97357512953
      Y = 3.50803108808
      CollectingObjectsMode = HomogeneousAdd
      ConsiderStyle = Yes''')
    tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
    tp.macro.execute_command('''$!Pick Shift
      X = -0.124352331606
      Y = 1.46735751295''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 8.71658031088
      Y = 1.55984455959
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = 0.116062176166
      Y = 0.837305699482''')
    tp.macro.execute_command('''$!FrameControl ActivateAtPosition
      X = 8.57564766839
      Y = 3.1018134715''')
    tp.macro.execute_command('''$!Pick SetMouseMode
      MouseMode = Select''')
    tp.macro.execute_command("""$!AttachText 
      AnchorPos
        {
        X = 84.17386298215312
        Y = 64.35233160621762
        }
      TextShape
        {
        SizeUnits = Frame
        Height = 5
        }
      Anchor = HeadRight
      TextType = LaTeX
      Text = 'dB'""")
    tp.macro.execute_command('$!RedrawAll')
    tp.macro.execute_command('''$!Pick SetMouseMode
      MouseMode = Select''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 8.43471502591
      Y = 3.15984455959
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = 0.480829015544
      Y = -0.248704663212''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 8.87409326425
      Y = 5.29870466321
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = -0.0248704663212
      Y = -0.273575129534''')
    tp.macro.execute_command('''$!AttachGeom 
      AnchorPos
        {
        X = -273.9177793422199
        Y = -37.04698364153063
        }
      LineThickness = 0.6
      ArrowheadSize = 3
      ArrowheadAngle = 30
      RawData
    1
    2
    0 0 
    348.756225586 -101.03453064''')
    tp.macro.execute_command('''$!AttachGeom 
      AnchorPos
        {
        X = -148.9343255713506
        Y = -129.8490690761881
        }
      LineThickness = 0.6
      ArrowheadSize = 3
      ArrowheadAngle = 30
      RawData
    1
    2
    0 0 
    299.361572266 259.696166992''')
    tp.macro.execute_command('''$!Pick SetMouseMode
      MouseMode = Select''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 8.68341968912
      Y = 4.62720207254
      ConsiderStyle = Yes''')
    tp.active_frame().plot().contour(0).legend.vertical=False
    tp.macro.execute_command('$!RedrawAll')
    tp.macro.execute_command('''$!Pick Shift
      X = -1.01139896373
      Y = 3.35751295337''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 8.94870466321
      Y = 2.91113989637
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = -5.22279792746
      Y = 3.75544041451''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 8.96528497409
      Y = 2.33082901554
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = -0.331606217617
      Y = 2.78549222798''')


def loading():
    tp.active_frame().plot().view.position=(3504.42,
    tp.active_frame().plot().view.position[1],
    tp.active_frame().plot().view.position[2])
    tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
    2138.75,
    tp.active_frame().plot().view.position[2])
    tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
    tp.active_frame().plot().view.position[1],
    2419.62)
    tp.active_frame().plot().view.width=812.486
    tp.active_frame().plot().view.position=(3472.61,
    tp.active_frame().plot().view.position[1],
    tp.active_frame().plot().view.position[2])
    tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
    2205.07,
    tp.active_frame().plot().view.position[2])
    tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
    tp.active_frame().plot().view.position[1],
    2409.89)
    tp.active_frame().plot().view.width=812.486
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.61917098446
      Y = 3.8810880829
      ConsiderStyle = Yes''')
    tp.active_frame().plot().contour(0).legend.show_header=False
    tp.active_frame().plot().contour(0).legend.vertical=False
    tp.macro.execute_command('$!RedrawAll')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.13005181347
      Y = 1.9329015544
      CollectingObjectsMode = HomogeneousAdd
      ConsiderStyle = Yes''')
    tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
    tp.macro.execute_command('''$!Pick Shift
      X = -0.638341968912
      Y = 4.74196891192''')
    tp.macro.execute_command('''$!FrameControl ActivateAtPosition
      X = 3.00466321244
      Y = 6.88212435233''')
    tp.macro.execute_command('''$!Pick SetMouseMode
      MouseMode = Select''')
    tp.macro.execute_command("""$!AttachText 
      AnchorPos
        {
        X = 22.27403569372481
        Y = 17.09844559585493
        }
      TextShape
        {
        SizeUnits = Frame
        Height = 5
        }
      Anchor = HeadRight
      TextType = LaTeX
      Text = 'dB'""")
    tp.macro.execute_command('$!RedrawAll')
    tp.macro.execute_command('''$!Pick SetMouseMode
      MouseMode = Select''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 2.83056994819
      Y = 7.11424870466
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = 0.306735751295
      Y = -0.19896373057''')
    tp.macro.execute_command('''$!Pick Shift
      X = 0.19067357513
      Y = 0''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 8.6170984456
      Y = 1.38575129534
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = -0.223834196891
      Y = 3.56476683938''')
    tp.macro.execute_command('''$!AttachGeom 
      AnchorPos
        {
        X = -273.9177793422199
        Y = -37.04698364153063
        }
      LineThickness = 0.6
      ArrowheadSize = 3
      ArrowheadAngle = 30
      RawData
    1
    2
    0 0 
    348.756225586 -101.03453064''')
    tp.macro.execute_command('''$!AttachGeom 
      AnchorPos
        {
        X = -148.9343255713506
        Y = -129.8490690761881
        }
      LineThickness = 0.6
      ArrowheadSize = 3
      ArrowheadAngle = 30
      RawData
    1
    2
    0 0 
    299.361572266 259.696166992''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 4.12383419689
      Y = 6.91528497409
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = 1.01968911917
      Y = -0.0911917098446''')
    tp.macro.execute_command('$!RedrawAll')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 3.1621761658
      Y = 6.86554404145
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = -1.85699481865
      Y = 0.0911917098446''')
    tp.macro.execute_command('''$!Pick Shift
      X = 0.0911917098446
      Y = -0.0746113989637''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 4.49689119171
      Y = 6.79922279793
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = 0.068652849741
      Y = -0.0165803108808''')
    tp.macro.execute_command('$!RedrawAll')
    
def total():
    tp.active_frame().plot().view.position=(3504.42,
    tp.active_frame().plot().view.position[1],
    tp.active_frame().plot().view.position[2])
    tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
    2138.75,
    tp.active_frame().plot().view.position[2])
    tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
    tp.active_frame().plot().view.position[1],
    2419.62)
    tp.active_frame().plot().view.width=812.486
    tp.active_frame().plot().view.position=(3472.61,
    tp.active_frame().plot().view.position[1],
    tp.active_frame().plot().view.position[2])
    tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
    2205.07,
    tp.active_frame().plot().view.position[2])
    tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
    tp.active_frame().plot().view.position[1],
    2409.89)
    tp.active_frame().plot().view.width=812.486
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.61917098446
      Y = 3.8810880829
      ConsiderStyle = Yes''')
    tp.active_frame().plot().contour(0).legend.show_header=False
    tp.active_frame().plot().contour(0).legend.vertical=False
    tp.macro.execute_command('$!RedrawAll')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 6.13005181347
      Y = 1.9329015544
      CollectingObjectsMode = HomogeneousAdd
      ConsiderStyle = Yes''')
    tp.active_frame().plot().contour(0).legend.box.box_type=tp.constant.TextBox.None_
    tp.macro.execute_command('''$!Pick Shift
      X = -0.638341968912
      Y = 4.74196891192''')
    tp.macro.execute_command('''$!FrameControl ActivateAtPosition
      X = 3.00466321244
      Y = 6.88212435233''')
    tp.macro.execute_command('''$!Pick SetMouseMode
      MouseMode = Select''')
    tp.macro.execute_command("""$!AttachText 
      AnchorPos
        {
        X = 22.27403569372481
        Y = 17.09844559585493
        }
      TextShape
        {
        SizeUnits = Frame
        Height = 5
        }
      Anchor = HeadRight
      TextType = LaTeX
      Text = 'dB'""")
    tp.macro.execute_command('$!RedrawAll')
    tp.macro.execute_command('''$!Pick SetMouseMode
      MouseMode = Select''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 2.83056994819
      Y = 7.11424870466
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = 0.306735751295
      Y = -0.19896373057''')
    tp.macro.execute_command('''$!Pick Shift
      X = 0.19067357513
      Y = 0''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 8.6170984456
      Y = 1.38575129534
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = -0.223834196891
      Y = 3.56476683938''')
    tp.macro.execute_command('''$!AttachGeom 
      AnchorPos
        {
        X = -273.9177793422199
        Y = -37.04698364153063
        }
      LineThickness = 0.6
      ArrowheadSize = 3
      ArrowheadAngle = 30
      RawData
    1
    2
    0 0 
    348.756225586 -101.03453064''')
    tp.macro.execute_command('''$!AttachGeom 
      AnchorPos
        {
        X = -148.9343255713506
        Y = -129.8490690761881
        }
      LineThickness = 0.6
      ArrowheadSize = 3
      ArrowheadAngle = 30
      RawData
    1
    2
    0 0 
    299.361572266 259.696166992''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 4.12383419689
      Y = 6.91528497409
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = 1.01968911917
      Y = -0.0911917098446''')
    tp.macro.execute_command('$!RedrawAll')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 3.1621761658
      Y = 6.86554404145
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = -1.85699481865
      Y = 0.0911917098446''')
    tp.macro.execute_command('''$!Pick Shift
      X = 0.0911917098446
      Y = -0.0746113989637''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 4.49689119171
      Y = 6.79922279793
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = 0.068652849741
      Y = -0.0165803108808''')
    tp.macro.execute_command('$!RedrawAll')