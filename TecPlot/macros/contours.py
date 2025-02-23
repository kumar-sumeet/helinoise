#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 10:47:33 2022

@author: ge56beh
"""
import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

def savelay(directry,filename):
        layoutpath = f"\"{directry}/{filename}.lay\""
        tp.macro.execute_command("""$!SaveLayout  """+layoutpath
                                +"""UseRelativePaths = Yes""")

def in3tiledframes(directry,filename,quantity='pressure',dBordBA= 'dB',connectTec = False,savelay = False):
    if connectTec:
        tp.session.connect(port=7600)

    createtiledframes()
    
    if quantity=='OASPL':
        OASPL(directry,filename,dBordBA)
    elif quantity=='pressure':
        pressure(directry,filename)
  
    if savelay:
        savelay(directry,filename)
        
def createtiledframes():
    tp.macro.execute_command("""$!Page Name = 'Untitled'
     $!PageControl Create
     $!NewLayout""")
    tp.macro.execute_command("""$!CreateNewFrame 
  XYPos
    {
    X = 1.1364
    Y = 2.6423
    }
  Width = 3.7512
  Height = 1.8565
$!CreateNewFrame 
  XYPos
    {
    X = 5.6914
    Y = 2.6041
    }
  Width = 2.9282
  Height = 1.378
$!ExtendedCommand 
  CommandProcessorID = 'Multi Frame Manager'
  Command = 'TILEFRAMESSQUARE'
$!ExtendedCommand 
  CommandProcessorID = 'Multi Frame Manager'
  Command = 'TILEFRAMESVERT'
$!ExtendedCommand 
  CommandProcessorID = 'Multi Frame Manager'
  Command = 'TILEFRAMESSQUARE'
$!Pick SetMouseMode
  MouseMode = Select
$!FrameControl ActivateAtPosition
  X = 0.925837320574
  Y = 3.7523923445
$!Pick AddAtPosition
  X = 0.925837320574
  Y = 3.7523923445
  ConsiderStyle = Yes""")
        
def pressure(directry,filename):
    
    plot3Dfiles = ['pressure.x', f'pressure.fn', f'pressure.nam']    
    plot3Dfilepaths = [f'\"{directry}/{filename}\"' for filename in plot3Dfiles]
    
    txt1 = '\'"STANDARDSYNTAX" "1.0" "APPEND" "No" "FILELIST_GRIDFILES" "1" ' 
    txt2 = ' "FILELIST_FUNCTIONFILES" "1" '
    txt3 = ' "FILENAME_NAMEFILE" '
    txt4 = ' "IINDEXRANGE" "1,,1" "JINDEXRANGE" "1,,1" "KINDEXRANGE" "1,,1" "AUTODETECT" "Yes" "LOADBOUNDARY" "No" "ASCIIISDOUBLE" "No" "ASCIIHASIBLANK" "No" "SOLUTIONSSHARESTRUCTURE" "No" "ASSIGNSTRANDIDS" "Yes" "ADDTOEXISTINGSTRANDS" "No" "UNIFORMGRIDSTRUCTURE" "Yes" "ASSIGNNEWSTRANDIDFOREACHTIMESTEP" "Yes" "EXTRACTTIMEFROMSOLFILENAMES" "No"\'\n'
    readdataset = txt1 + plot3Dfilepaths[0] + txt2 + plot3Dfilepaths[1] + txt3 + plot3Dfilepaths[2] + txt4

    tp.macro.execute_command("""$!ReadDataSet  """+readdataset+
  """  DataSetReader = 'PLOT3D Loader'""")
    tp.macro.execute_command("""$!GlobalRGB RedChannelVar = 4
$!GlobalRGB GreenChannelVar = 4
$!GlobalRGB BlueChannelVar = 4
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
  Var = 7
  ContourGroup = 4
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 8
  ContourGroup = 5
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 9
  ContourGroup = 6
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 10
  ContourGroup = 7
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 11
  ContourGroup = 8
  LevelInitMode = ResetToNice
$!IsoSurfaceLayers Show = Yes
$!IsoSurfaceAttributes 1  Contour{FloodColoring = Group3}
$!FrameControl ActivateAtPosition
  X = 5.33823529412
  Y = 5.83823529412
$!Pick AddAtPosition
  X = 5.33823529412
  Y = 5.83823529412
  ConsiderStyle = Yes""")
    tp.macro.execute_command("""$!ReadDataSet  """+readdataset+
  """  DataSetReader = 'PLOT3D Loader'""")
    tp.macro.execute_command("""$!GlobalRGB RedChannelVar = 4
$!GlobalRGB GreenChannelVar = 4
$!GlobalRGB BlueChannelVar = 4
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
  Var = 7
  ContourGroup = 4
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 8
  ContourGroup = 5
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 9
  ContourGroup = 6
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 10
  ContourGroup = 7
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 11
  ContourGroup = 8
  LevelInitMode = ResetToNice
$!IsoSurfaceLayers Show = Yes
$!IsoSurfaceAttributes 1  Contour{FloodColoring = Group2}
$!Pick AddAtPosition
  X = 6.32843137255
  Y = 5.82843137255
  ConsiderStyle = Yes
$!FrameControl ActivateAtPosition
  X = 8.46568627451
  Y = 5.75980392157
$!Pick AddAtPosition
  X = 8.46568627451
  Y = 5.75980392157
  ConsiderStyle = Yes""")
    tp.macro.execute_command("""$!ReadDataSet  """+readdataset+
  """  DataSetReader = 'PLOT3D Loader'""")
    tp.macro.execute_command("""$!GlobalRGB RedChannelVar = 4
$!GlobalRGB GreenChannelVar = 4
$!GlobalRGB BlueChannelVar = 4
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
  Var = 7
  ContourGroup = 4
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 8
  ContourGroup = 5
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 9
  ContourGroup = 6
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 10
  ContourGroup = 7
  LevelInitMode = ResetToNice
$!SetContourVar 
  Var = 11
  ContourGroup = 8
  LevelInitMode = ResetToNice
$!IsoSurfaceLayers Show = Yes
$!IsoSurfaceAttributes 1  Contour{FloodColoring = Group4}
$!Linking BetweenFrames{LinkSolutionTime = Yes}
$!Linking BetweenFrames{LinkIsoSurfaceValues = Yes}
$!RedrawAll 
$!PropagateLinking 
  LinkType = BetweenFrames
  FrameCollection = All
$!AnimateIsoSurfaces 
  StartValue = 0.0705263157895
  EndValue = 0.26
  NumSteps = 16
  Group = 1
  CreateMovieFile = No""")    
  
def OASPL(directry,filename,dBordBA):
    
    plot3Dfiles = ['OASPL.x', f'OASPL{dBordBA}.fn', f'OASPL{dBordBA}.nam']    
    plot3Dfilepaths = [f'\"{directry}/{filename}\"' for filename in plot3Dfiles]
    
    txt1 = '\'"STANDARDSYNTAX" "1.0" "APPEND" "No" "FILELIST_GRIDFILES" "1" ' 
    txt2 = ' "FILELIST_FUNCTIONFILES" "1" '
    txt3 = ' "FILENAME_NAMEFILE" '
    txt4 = ' "IINDEXRANGE" "1,,1" "JINDEXRANGE" "1,,1" "KINDEXRANGE" "1,,1" "AUTODETECT" "Yes" "LOADBOUNDARY" "No" "ASCIIISDOUBLE" "No" "ASCIIHASIBLANK" "No" "SOLUTIONSSHARESTRUCTURE" "No" "ASSIGNSTRANDIDS" "Yes" "ADDTOEXISTINGSTRANDS" "No" "UNIFORMGRIDSTRUCTURE" "Yes" "ASSIGNNEWSTRANDIDFOREACHTIMESTEP" "Yes" "EXTRACTTIMEFROMSOLFILENAMES" "No"\'\n'
    readdataset = txt1 + plot3Dfilepaths[0] + txt2 + plot3Dfilepaths[1] + txt3 + plot3Dfilepaths[2] + txt4

    tp.macro.execute_command("""$!ReadDataSet  """+readdataset+
  """  DataSetReader = 'PLOT3D Loader'""")
    tp.macro.execute_command("""$!FrameControl ActivateAtPosition
  X = 5.27033492823
  Y = 6.69976076555
$!Pick AddAtPosition
  X = 5.27033492823
  Y = 6.69976076555
  ConsiderStyle = Yes""")
    tp.macro.execute_command("""$!ReadDataSet  """+readdataset+
  """  DataSetReader = 'PLOT3D Loader'""")
    tp.macro.execute_command("""$!FrameControl ActivateAtPosition
  X = 7.89234449761
  Y = 5.99162679426
$!Pick AddAtPosition
  X = 7.89234449761
  Y = 5.99162679426
  ConsiderStyle = Yes""")
    tp.macro.execute_command("""$!ReadDataSet  """+readdataset+
  """  DataSetReader = 'PLOT3D Loader'""")
    tp.macro.execute_command("""$!FrameControl ActivateAtPosition
  X = 0.638755980861
  Y = 5.97248803828
$!Pick AddAtPosition
  X = 0.638755980861
  Y = 5.97248803828
  ConsiderStyle = Yes
$!GlobalRGB RedChannelVar = 4
$!GlobalRGB GreenChannelVar = 4
$!GlobalRGB BlueChannelVar = 4
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
  Var = 7
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
$!SetContourVar 
  Var = 5
  ContourGroup = 1
  LevelInitMode = ResetToNice
$!FrameControl ActivateAtPosition
  X = 5.4043062201
  Y = 3.33133971292
$!Pick AddAtPosition
  X = 5.4043062201
  Y = 3.33133971292
  ConsiderStyle = Yes
$!GlobalRGB RedChannelVar = 4
$!GlobalRGB GreenChannelVar = 4
$!GlobalRGB BlueChannelVar = 4
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
  Var = 7
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
$!SetContourVar 
  Var = 6
  ContourGroup = 1
  LevelInitMode = ResetToNice
$!FrameControl ActivateAtPosition
  X = 8.84928229665
  Y = 3.33133971292
$!Pick AddAtPosition
  X = 8.84928229665
  Y = 3.33133971292
  ConsiderStyle = Yes
$!GlobalRGB RedChannelVar = 4
$!GlobalRGB GreenChannelVar = 4
$!GlobalRGB BlueChannelVar = 4
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
  Var = 7
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
$!SetContourVar 
  Var = 7
  ContourGroup = 1
  LevelInitMode = ResetToNice
$!FrameControl ActivateAtPosition
  X = 0.562200956938
  Y = 6.77631578947
$!Pick AddAtPosition
  X = 0.562200956938
  Y = 6.77631578947
  ConsiderStyle = Yes""")    
  

if __name__ == "__main__":
    main_directry = '/home/HT/ge56beh/Work/Python/HeliNoise/Data/Diss_runs/2_simple_hemisphere_periodic'
    filename = '1994_Run15_5_hover_FishBAC_PetersUnsteady'
    directry = f'{main_directry}/{filename}/{filename}'
    
    in3tiledframes(directry,filename,quantity='pressure',dBordBA= 'dB',connectTec = True)