import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()

tp.macro.execute_command("""$!ReadDataSet  '\"/home/HT/ge56beh/Work/Python/Acoustics/Tecplot/OneraM6_SU2_RANS.plt\" '
  ReadDataOption = New
  ResetStyle = No
  VarLoadMode = ByName
  AssignStrandIDs = Yes
  VarNameList = '\"x\" \"y\" \"z\" \"Density\" \"Momentum U (Density*U)\" \"Momentum V (Density*V)\" \"Momentum W (Density*W)\" \"Energy (Density*E)\" \"SA Turbulent Eddy Viscosity\" \"Pressure\" \"Temperature\" \"Pressure_Coefficient\" \"Mach\" \"Laminar_Viscosity\" \"Skin_Friction_Coefficient\" \"Heat_Flux\" \"Y_Plus\" \"Eddy_Viscosity\"'""")
tp.macro.execute_command('''$!Pick AddAtPosition
  X = 1.03575129534
  Y = 1.15362694301
  ConsiderStyle = Yes''')
tp.macro.execute_command('''$!Pick AddAtPosition
  X = 1.01088082902
  Y = 1.17849740933
  ConsiderStyle = Yes''')
tp.macro.execute_command('''$!Pick AddAtPosition
  X = 0.977720207254
  Y = 1.9329015544
  ConsiderStyle = Yes''')
tp.macro.execute_command('''$!FrameControl ActivateByNumber
  Frame = 1''')
tp.macro.execute_command('$!Pick Copy')
tp.macro.execute_command('$!Pick Paste')
tp.active_frame().plot().linking_between_frames.link_slice_positions=True
tp.macro.execute_command('$!RedrawAll')
tp.macro.execute_command('''$!Pick AddAtPosition
  X = 1.01917098446
  Y = 2.02409326425
  ConsiderStyle = Yes''')
tp.macro.execute_command('''$!Pick AddAtPosition
  X = 1.01917098446
  Y = 2.02409326425
  ConsiderStyle = Yes''')
tp.macro.execute_command('''$!Pick AddAtPosition
  X = 1.03575129534
  Y = 2.34740932642
  ConsiderStyle = Yes''')
tp.macro.execute_command("""$!ReadDataSet  '\"/HTOpt/TecPlot/2019R1/360ex_2019r1/examples/OneraM6wing/OneraM6_SU2_RANS.plt\" '
  ReadDataOption = Append
  ResetStyle = Yes
  VarLoadMode = ByName
  AssignStrandIDs = Yes
  VarNameList = '\"x\" \"y\" \"z\" \"Density\" \"Momentum U (Density*U)\" \"Momentum V (Density*V)\" \"Momentum W (Density*W)\" \"Energy (Density*E)\" \"SA Turbulent Eddy Viscosity\" \"Pressure\" \"Temperature\" \"Pressure_Coefficient\" \"Mach\" \"Laminar_Viscosity\" \"Skin_Friction_Coefficient\" \"Heat_Flux\" \"Y_Plus\" \"Eddy_Viscosity\"'""")
tp.active_frame().plot().contour(0).variable_index=3
tp.active_frame().plot().show_contour=True
tp.active_frame().plot().contour(0).levels.reset_to_nice(num_levels=15)
tp.export.save_png('/home/HT/ge56beh/Work/Python/Acoustics/Tecplot/wing.png',
    width=600,
    region=ExportRegion.AllFrames,
    supersample=3,
    convert_to_256_colors=False)
tp.macro.execute_command('''$!ExtractSliceToZones 
  SliceSource = SurfaceZones
  SurfaceGenerationMethod = AllowQuads
  CopyCellCenteredValues = No
  Resulting1DZoneType = FELineSegment
  TransientOperationMode = SingleSolutionTime
  Origin
    {
    X = 0
    Y = 0.25
    Z = 0
    }
  Normal
    {
    X = 0
    Y = 1
    Z = 0
    }''')
tp.macro.execute_command("""$!RenameDataSetZone 
  Zone = 5
  Name = 'Quarter-chord C_p'""")
tp.active_frame().plot_type=PlotType.XYLine
tp.active_frame().plot().delete_linemaps()
tp.active_frame().plot().add_linemap()
tp.active_frame().plot().linemap(0).name='Quarter-chord C_p'
tp.active_frame().plot().linemap(0).zone_index=4
#  $!ActiveLineMaps  +=  [1]
tp.active_frame().plot().linemap(0).show=True
tp.active_frame().plot().linemap(0).y_variable_index=11
tp.macro.execute_extended_command(command_processor_id='CFDAnalyzer4',
    command="Integrate VariableOption='Average' XOrigin=0 YOrigin=0 ZOrigin=0 ScalarVar=12 Absolute='F' ExcludeBlanked='F' XVariable=1 YVariable=0 ZVariable=0 IntegrateOver='Cells' IntegrateBy='Zones' IRange={MIN =1 MAX = 0 SKIP = 1} JRange={MIN =1 MAX = 0 SKIP = 1} KRange={MIN =1 MAX = 0 SKIP = 1} PlotResults='F' PlotAs='Result' TimeMin=0 TimeMax=0")
tp.macro.execute_command("""$!AttachText 
  AnchorPos
    {
    X = 60
    Y = 90
    }
  Box
    {
    Margin = 0.2
    LineThickness = 0.001
    }
  Text = 'integration result: 0.54054'""")
tp.active_frame().plot().linemap(0).line.color=Color.Blue
tp.active_frame().plot().linemap(0).line.line_thickness=0.8
tp.active_frame().plot().axes.y_axis(0).reverse=True
tp.active_frame().plot().view.fit()
tp.export.save_png('/home/HT/ge56beh/Work/Python/Acoustics/Tecplot/wing_pressure_coefficient.png',
    width=600,
    region=ExportRegion.AllFrames,
    supersample=3,
    convert_to_256_colors=False)
# End Macro.

