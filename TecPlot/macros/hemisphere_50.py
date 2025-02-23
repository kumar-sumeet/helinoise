#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 10 11:23:57 2021

@author: ge56beh
"""

import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *


def hemisphere_50():
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
          Text = 'dB'""")


def hemisphere_50_delta():
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
          Text = '$\\Delta$dB'""")
