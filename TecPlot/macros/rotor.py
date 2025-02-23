#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 12:53:46 2022

@author: ge56beh
"""
import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *
import glob
import time
import removeborder as rb

def common_mcr(directry,basename,framename):

    pltfilepaths = glob.glob("{}/{}_Blade_*_LL*.plt".format(directry,basename))
    pltfiles_quotes = [f"\"{pltfile}\"" for pltfile in pltfilepaths]
    pltfiles_quotes_joined = (' ').join(pltfiles_quotes)
    pltfiles_quotes_joinedsinglequotes = f"  \'{pltfiles_quotes_joined}\' "
    
    tp.macro.execute_command("""$!Page Name = 'Untitled'
     $!PageControl Create
     $!NewLayout""")     
    tp.macro.execute_command("""$!ReadDataSet """+ pltfiles_quotes_joinedsinglequotes
      + """ReadDataOption = New
      ResetStyle = Yes
      VarLoadMode = ByName
      AssignStrandIDs = Yes
      VarNameList = '"x" "y" "z" "x_normal" "y_normal" "z_normal" "Fx" "Fy" "Fz"'""")
    tp.macro.execute_command("""$!GlobalRGB RedChannelVar = 3
        $!GlobalRGB GreenChannelVar = 3
        $!GlobalRGB BlueChannelVar = 3
        $!SetContourVar 
          Var = 4
          ContourGroup = 1
          LevelInitMode = ResetToNice
        $!SetContourVar 
          Var = 5
          ContourGroup = 2
          LevelInitMode = ResetToNice
        $!SetContourVar 
          Var = 6
          ContourGroup = 3
          LevelInitMode = ResetToNice
        $!SetContourVar 
          Var = 4
          ContourGroup = 4
          LevelInitMode = ResetToNice
        $!SetContourVar 
          Var = 4
          ContourGroup = 5
          LevelInitMode = ResetToNice
        $!SetContourVar 
          Var = 4
          ContourGroup = 6
          LevelInitMode = ResetToNice
        $!SetContourVar 
          Var = 4
          ContourGroup = 7
          LevelInitMode = ResetToNice
        $!SetContourVar 
          Var = 4
          ContourGroup = 8
          LevelInitMode = ResetToNice
        $!FieldLayers ShowContour = Yes
        $!PlotType = Cartesian3D
        $!ThreeDAxis FrameAxis{XYPos{X = 50}}
        $!ThreeDAxis FrameAxis{XYPos{Y = 50}}
        $!ThreeDAxis FrameAxis{Size = 9}
        $!ThreeDAxis FrameAxis{Size = 8}
        $!ThreeDAxis FrameAxis{Size = 7}""")    
    tp.macro.execute_command('''$!FrameControl ActivateAtPosition
      X = 2.62836185819
      Y = 1.1913202934''')
    tp.macro.execute_command('''$!Pick SetMouseMode
      MouseMode = Select''')
    tp.macro.execute_command("""$!AttachText 
      AnchorPos
        {
        X = 18.09290953545232
        Y = 88.23349633251834
        }
      TextShape
        {
        IsBold = No
        }
      Text = 'Time = &(SOLUTIONTIME%.2f)'""")

def inertialview():
    tp.macro.execute_command("""$!ThreeDView ViewerPosition{X = 52.3990420029029877}
        $!ThreeDView ViewerPosition{Y = 30.2523425599148403}
        $!ThreeDView ViewerPosition{Z = -35.0605371396055219}
        $!ThreeDView PSIAngle = 119.999999999999986
        $!ThreeDView ViewerPosition{X = -56.8562918491878762}
        $!ThreeDView ViewerPosition{Y = 20.6937394181167349}
        $!ThreeDView ThetaAngle = 110
        $!ThreeDView ViewerPosition{Z = -35.0605371396055148}
        $!ThreeDView AlphaAngle = 180
        $!SetContourVar 
          Var = 3
          ContourGroup = 1
          LevelInitMode = ResetToNice""")
    
def nonrotatingview():
    tp.macro.execute_command("""$!ThreeDView ViewerPosition{X = -57.0412115574466796}
        $!ThreeDView ViewerPosition{Y = 20.7197087231812311}
        $!ThreeDView ViewerPosition{Z = 34.9999072878418787}
        $!ThreeDView PSIAngle = 59.9999999999999929
        $!ThreeDView ViewerPosition{X = 57.0144751859310688}
        $!ThreeDView ViewerPosition{Y = 20.7931663001985569}
        $!ThreeDView ViewerPosition{Z = 34.9999072878418858}
        $!ThreeDView ThetaAngle = -110
        $!ThreeDView ViewerPosition{X = 56.9060775472634575}
        $!ThreeDView ViewerPosition{Y = 20.6705239658375106}
        $!ThreeDView ViewerPosition{Z = 35.2489876427266182}
        $!ThreeDView AlphaAngle = 0
        $!SetContourVar 
          Var = 3
          ContourGroup = 1
          LevelInitMode = ResetToNice""")
    
def inoneframe(directry,basename,framename,connectTec = False,savelay = False):

    if connectTec:
        tp.session.connect(port=7600)
        
    common_mcr(directry,basename,framename)
    if framename == 'DymInertial' :
        inertialview()
    if framename == 'Rotor(non-rotating)' :
        nonrotatingview()
    # if framename == 'Rotor(rotating)' :
    #     rotatingview()
    # if framename == 'BladeRoot' :
    #     bladerootview()
    # if framename == 'BladePrecone' :
    #     bladepreconeview()
    
    if savelay:
        layoutpath = f"\"{directry}/{basename}.lay\""
        tp.macro.execute_command("""$!SaveLayout  """+layoutpath
                                +"""UseRelativePaths = Yes""")




def in4tiledframes(directry,basename,framename,connectTec = False,savelay = False, removeborder=True):
    
    pltfilepaths = glob.glob("{}/{}_Blade_*_LL*.plt".format(directry,basename))
    pltfiles_quotes = [f"\"{pltfile}\"" for pltfile in pltfilepaths]
    pltfiles_quotes_joined = (' ').join(pltfiles_quotes)
    pltfiles_quotes_joinedsinglequotes = f"  \'{pltfiles_quotes_joined}\' "
    if connectTec:
        tp.session.connect(port=7600)
    tp.macro.execute_command("""$!Page Name = 'Untitled'
     $!PageControl Create
     $!NewLayout""")     
    tp.macro.execute_command("""$!CreateNewFrame 
      XYPos
        {
        X = 1.3015
        Y = 0.87921
        }
      Width = 1.3109
      Height = 1.5581
    $!CreateNewFrame 
      XYPos
        {
        X = 3.5337
        Y = 0.9691
        }
      Width = 1.6854
      Height = 0.75655
    $!CreateNewFrame 
      XYPos
        {
        X = 7.3015
        Y = 1.8006
        }
      Width = 1.5506
      Height = 1.3258
    $!ExtendedCommand 
      CommandProcessorID = 'Multi Frame Manager'
      Command = 'TILEFRAMESSQUARE'""")
    tp.macro.execute_command("""$!ReadDataSet """+ pltfiles_quotes_joinedsinglequotes
      + """ReadDataOption = New
      ResetStyle = Yes
      VarLoadMode = ByName
      AssignStrandIDs = Yes
      VarNameList = '"x" "y" "z" "x_normal" "y_normal" "z_normal" "Fx" "Fy" "Fz"'""")
    tp.macro.execute_command("""$!GlobalRGB RedChannelVar = 3
    $!GlobalRGB GreenChannelVar = 3
    $!GlobalRGB BlueChannelVar = 3
    $!SetContourVar 
      Var = 4
      ContourGroup = 1
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 5
      ContourGroup = 2
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 6
      ContourGroup = 3
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 4
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 5
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 6
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 7
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 8
      LevelInitMode = ResetToNice
    $!FieldLayers ShowContour = Yes
    $!PlotType = Cartesian3D
    $!ThreeDAxis FrameAxis{XYPos{X = 50}}
    $!ThreeDAxis FrameAxis{XYPos{Y = 50}}
    $!ThreeDAxis FrameAxis{Size = 9}
    $!ThreeDAxis FrameAxis{Size = 8}
    $!ThreeDAxis FrameAxis{Size = 7}
    $!ThreeDView ViewerPosition{X = 52.3990420029029877}
    $!ThreeDView ViewerPosition{Y = 30.2523425599148403}
    $!ThreeDView ViewerPosition{Z = -35.0605371396055219}
    $!ThreeDView PSIAngle = 119.999999999999986
    $!ThreeDView ViewerPosition{X = -56.8562918491878762}
    $!ThreeDView ViewerPosition{Y = 20.6937394181167349}
    $!ThreeDView ThetaAngle = 110
    $!ThreeDView ViewerPosition{Z = -35.0605371396055148}
    $!ThreeDView AlphaAngle = 180
    $!SetContourVar 
      Var = 3
      ContourGroup = 1
      LevelInitMode = ResetToNice
    $!Pick SetMouseMode
      MouseMode = Select
    $!FrameControl ActivateAtPosition
      X = 1.5936329588
      Y = 2.05524344569
    $!Pick AddAtPosition
      X = 1.5936329588
      Y = 2.05524344569
      ConsiderStyle = Yes""")
    tp.macro.execute_command("""$!ReadDataSet """+ pltfiles_quotes_joinedsinglequotes
      + """ReadDataOption = New
      ResetStyle = Yes
      VarLoadMode = ByName
      AssignStrandIDs = Yes
      VarNameList = '"x" "y" "z" "x_normal" "y_normal" "z_normal" "Fx" "Fy" "Fz"'""")
    tp.macro.execute_command("""$!GlobalRGB RedChannelVar = 3
    $!GlobalRGB GreenChannelVar = 3
    $!GlobalRGB BlueChannelVar = 3
    $!SetContourVar 
      Var = 4
      ContourGroup = 1
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 5
      ContourGroup = 2
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 6
      ContourGroup = 3
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 4
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 5
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 6
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 7
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 8
      LevelInitMode = ResetToNice
    $!FieldLayers ShowContour = Yes
    $!PlotType = Cartesian3D
    $!ThreeDAxis FrameAxis{XYPos{X = 50}}
    $!ThreeDAxis FrameAxis{XYPos{Y = 50}}
    $!ThreeDAxis FrameAxis{Size = 9}
    $!ThreeDAxis FrameAxis{Size = 8}
    $!ThreeDAxis FrameAxis{Size = 7}
    $!ThreeDView ViewerPosition{X = 52.3990420029029877}
    $!ThreeDView ViewerPosition{Y = 30.2523425599148403}
    $!ThreeDView ViewerPosition{Z = -35.0605371396055219}
    $!ThreeDView PSIAngle = 119.999999999999986
    $!ThreeDView ViewerPosition{X = -56.8562918491878762}
    $!ThreeDView ViewerPosition{Y = 20.6937394181167349}
    $!ThreeDView ThetaAngle = 110
    $!ThreeDView ViewerPosition{Z = -35.0605371396055148}
    $!ThreeDView AlphaAngle = 180
    $!SetContourVar 
      Var = 3
      ContourGroup = 1
      LevelInitMode = ResetToNice
    $!FrameControl ActivateAtPosition
      X = 6.59737827715
      Y = 2.45973782772
    $!Pick AddAtPosition
      X = 6.59737827715
      Y = 2.45973782772
      ConsiderStyle = Yes""")
    tp.macro.execute_command("""$!ReadDataSet """+ pltfiles_quotes_joinedsinglequotes
      + """ReadDataOption = New
      ResetStyle = Yes
      VarLoadMode = ByName
      AssignStrandIDs = Yes
      VarNameList = '"x" "y" "z" "x_normal" "y_normal" "z_normal" "Fx" "Fy" "Fz"'""")
    tp.macro.execute_command("""$!GlobalRGB RedChannelVar = 3
    $!GlobalRGB GreenChannelVar = 3
    $!GlobalRGB BlueChannelVar = 3
    $!SetContourVar 
      Var = 4
      ContourGroup = 1
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 5
      ContourGroup = 2
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 6
      ContourGroup = 3
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 4
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 5
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 6
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 7
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 8
      LevelInitMode = ResetToNice
    $!FieldLayers ShowContour = Yes
    $!PlotType = Cartesian3D
    $!ThreeDAxis FrameAxis{XYPos{X = 50}}
    $!ThreeDAxis FrameAxis{XYPos{Y = 50}}
    $!ThreeDAxis FrameAxis{Size = 9}
    $!ThreeDAxis FrameAxis{Size = 8}
    $!ThreeDAxis FrameAxis{Size = 7}
    $!ThreeDView ViewerPosition{X = 52.3990420029029877}
    $!ThreeDView ViewerPosition{Y = 30.2523425599148403}
    $!ThreeDView ViewerPosition{Z = -35.0605371396055219}
    $!ThreeDView PSIAngle = 119.999999999999986
    $!ThreeDView ViewerPosition{X = -56.8562918491878762}
    $!ThreeDView ViewerPosition{Y = 20.6937394181167349}
    $!ThreeDView ThetaAngle = 110
    $!ThreeDView ViewerPosition{Z = -35.0605371396055148}
    $!ThreeDView AlphaAngle = 180
    $!SetContourVar 
      Var = 3
      ContourGroup = 1
      LevelInitMode = ResetToNice
    $!FrameControl ActivateAtPosition
      X = 4.58239700375
      Y = 5.12640449438
    $!Pick AddAtPosition
      X = 4.58239700375
      Y = 5.12640449438
      ConsiderStyle = Yes""")
    tp.macro.execute_command("""$!ReadDataSet """+ pltfiles_quotes_joinedsinglequotes
      + """ReadDataOption = New
      ResetStyle = Yes
      VarLoadMode = ByName
      AssignStrandIDs = Yes
      VarNameList = '"x" "y" "z" "x_normal" "y_normal" "z_normal" "Fx" "Fy" "Fz"'""")
    tp.macro.execute_command("""$!GlobalRGB RedChannelVar = 3
    $!GlobalRGB GreenChannelVar = 3
    $!GlobalRGB BlueChannelVar = 3
    $!SetContourVar 
      Var = 4
      ContourGroup = 1
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 5
      ContourGroup = 2
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 6
      ContourGroup = 3
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 4
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 5
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 6
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 7
      LevelInitMode = ResetToNice
    $!SetContourVar 
      Var = 4
      ContourGroup = 8
      LevelInitMode = ResetToNice
    $!FieldLayers ShowContour = Yes
    $!PlotType = Cartesian3D
    $!ThreeDAxis FrameAxis{XYPos{X = 50}}
    $!ThreeDAxis FrameAxis{XYPos{Y = 50}}
    $!ThreeDAxis FrameAxis{Size = 9}
    $!ThreeDAxis FrameAxis{Size = 8}
    $!ThreeDAxis FrameAxis{Size = 7}
    $!ThreeDView ViewerPosition{X = 52.3990420029029877}
    $!ThreeDView ViewerPosition{Y = 30.2523425599148403}
    $!ThreeDView ViewerPosition{Z = -35.0605371396055219}
    $!ThreeDView PSIAngle = 119.999999999999986
    $!ThreeDView ViewerPosition{X = -56.8562918491878762}
    $!ThreeDView ViewerPosition{Y = 20.6937394181167349}
    $!ThreeDView ThetaAngle = 110
    $!ThreeDView ViewerPosition{Z = -35.0605371396055148}
    $!ThreeDView AlphaAngle = 180
    $!SetContourVar 
      Var = 3
      ContourGroup = 1
      LevelInitMode = ResetToNice
    $!FrameControl ActivateAtPosition
      X = 6.01310861423
      Y = 2.13764044944
    $!Pick AddAtPosition
      X = 6.01310861423
      Y = 2.13764044944
      ConsiderStyle = Yes
    $!FrameControl ActivateAtPosition
      X = 0.799625468165
      Y = 2.57958801498
    $!Pick AddAtPosition
      X = 0.799625468165
      Y = 2.57958801498
      ConsiderStyle = Yes
    $!ThreeDView ViewerPosition{X = -4.35081943503005138E-31}
    $!ThreeDView ViewerPosition{Y = -0.000258445739749646464}
    $!ThreeDView ViewerPosition{Z = 69.7375468662004607}
    $!ThreeDView PSIAngle = 0
    $!ThreeDView ThetaAngle = 0
    $!ThreeDView AlphaAngle = 0
    $!FrameControl ActivateAtPosition
      X = 5.9531835206
      Y = 1.36610486891
    $!Pick AddAtPosition
      X = 5.9531835206
      Y = 1.36610486891
      ConsiderStyle = Yes
    $!ThreeDView ViewerPosition{X = -4.35081943503005138E-31}
    $!ThreeDView ViewerPosition{Y = -69.8656477829437392}
    $!ThreeDView ViewerPosition{Z = -0.127842471003531688}
    $!ThreeDView PSIAngle = 90
    $!ThreeDView ThetaAngle = 0
    $!ThreeDView AlphaAngle = 0
    $!FrameControl ActivateAtPosition
      X = 6.3127340824
      Y = 5.05149812734
    $!Pick AddAtPosition
      X = 6.3127340824
      Y = 5.05149812734
      ConsiderStyle = Yes
    $!ThreeDView ViewerPosition{X = 69.8653893372039931}
    $!ThreeDView ViewerPosition{Y = -0.000258445739750371795}
    $!ThreeDView ViewerPosition{Z = -0.127842471003531688}
    $!ThreeDView PSIAngle = 90
    $!ThreeDView ThetaAngle = -90
    $!ThreeDView AlphaAngle = 0
    $!FrameControl ActivateAtPosition
      X = 1.51123595506
      Y = 1.67322097378
    $!Pick AddAtPosition
      X = 1.51123595506
      Y = 1.67322097378
      ConsiderStyle = Yes
    $!ThreeDView ViewerPosition{Y = -0.000258445739751097072}
    $!ThreeDView ViewerPosition{Z = -69.9932318082075255}
    $!ThreeDView PSIAngle = 180
    $!ThreeDView ViewerPosition{X = 5.00332197547748159E-15}
    $!ThreeDView ViewerPosition{Y = -0.00025844573974609375}
    $!ThreeDView ThetaAngle = -90
    $!Pick SetMouseMode
      MouseMode = Select
    $!FrameControl ActivateAtPosition
      X = 8.21535580524
      Y = 1.13389513109
    $!Pick AddAtPosition
      X = 8.21535580524
      Y = 1.13389513109
      ConsiderStyle = Yes
    $!ThreeDView ViewerPosition{X = 8.55604254229904954E-15}
    $!ThreeDView ViewerPosition{Y = 69.865130891464247}
    $!ThreeDView ThetaAngle = -180
    $!ThreeDView ViewerPosition{Z = -0.127842471003524583}
    $!ThreeDView AlphaAngle = -180
    $!FrameControl ActivateAtPosition
      X = 6.54494382022
      Y = 4.72191011236
    $!ThreeDView ViewerPosition{X = -69.8653893372039931}
    $!ThreeDView ViewerPosition{Y = -0.000258445739750371741}
    $!ThreeDView ThetaAngle = 90
    $!ThreeDView ViewerPosition{Y = -0.000258445739750371795}
    $!ThreeDView ViewerPosition{Z = -0.127842471003524583}
    $!ThreeDView AlphaAngle = 180
    $!FrameControl ActivateAtPosition
      X = 4.30524344569
      Y = 4.95411985019
    $!Linking BetweenFrames{LinkSolutionTime = Yes}
    $!RedrawAll 
    $!PropagateLinking 
      LinkType = BetweenFrames
      FrameCollection = All""")   
    if removeborder:
        # tp.macro.execute_file(f'removeborder_in4tiledframes.mcr')  #loading the macro files appears to jumble up things
        rb.in4tiledframes()
    if savelay:
        layoutpath = f"\"{directry}/{basename}.lay\""
        tp.macro.execute_command("""$!SaveLayout  """+layoutpath
                                +"""UseRelativePaths = Yes""")
          
if __name__ == "__main__":
    # pckl_datadir = '/media/ge56beh/c84065d4-8a10-4d18-9817-2d94ebda4319/HeliNoise/Data/Diss_runs/3_simple_hemisphere_aperiodicARCTIS/1994_Run15_5_hover_FishBAC_PetersUnsteadyARCTIS/1994_Run15_5_hover_FishBAC_PetersUnsteadyARCTIS'
    # basename = '1994_Run15_5_hover_FishBAC_PetersUnsteadyARCTIS'
    # # framename = 'Rotor(non-rotating)'  
    # framename = 'WopwopInertial'
    # # inoneframe(pckl_datadir,basename,framename,connectTec = True,savelay = False)
    # in4tiledframes(pckl_datadir,basename,framename,connectTec = True,savelay = False)   


    # pckl_datadir = '/media/ge56beh/c84065d4-8a10-4d18-9817-2d94ebda4319/HeliNoise/Data/Diss_runs/2_simple_hemisphere_aperiodic/1994_Run14_4/1994_Run14_4'
    # filename = '1994_Run14_4'
    
    pckl_datadir = '/home/HT/ge56beh/Work/Python/HeliNoise/Data/Diss_runs/2_simple_sphere_aperiodic/H1_rigid/H1_rigid'
    filename = 'H1_rigid'
    framename = 'DymInertial'  
    # framename = 'Rotor(non-rotating)'  
    # framename = 'WopwopInertial'
    basename = f'{filename}_{framename}' 
    # inoneframe(pckl_datadir,basename,framename,connectTec = True,savelay = False)
    in4tiledframes(pckl_datadir,basename,framename,connectTec = True,savelay = False)   
         