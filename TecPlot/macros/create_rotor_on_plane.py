import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()
def plane_50():
	tp.macro.execute_command('''$!AttachGeom 
	  AnchorPos
	    {
	    X = -53.41818800978243
	    Y = 104.5074569048953
	    }
	  LineThickness = 0.6
	  ArrowheadSize = 3
	  ArrowheadAngle = 30
	  RawData
	1
	2
	0 0 
	4.9545211792 2.4772605896''')
	tp.macro.execute_command('''$!AttachGeom 
	  AnchorPos
	    {
	    X = -55.27613343292577
	    Y = 104.1977993343715
	    }
	  LineThickness = 0.6
	  ArrowheadSize = 3
	  ArrowheadAngle = 30
	  RawData
	1
	2
	0 0 
	-1.5482878685 4.3352060318''')
	tp.macro.execute_command('''$!Pick SetMouseMode
	  MouseMode = Select''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.32383419689
	  Y = 1.56813471503
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('$!Pick Copy')
	tp.macro.execute_command('$!Pick Paste')
	tp.macro.execute_command('''$!Pick Shift
	  X = -0.20725388601
	  Y = 0.116062176166''')
	tp.macro.execute_command('$!Pick Copy')
	tp.macro.execute_command('$!Pick Paste')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.34041450777
	  Y = 1.58471502591
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('$!Pick Copy')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.16632124352
	  Y = 1.53497409326
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('$!Pick Copy')
	tp.macro.execute_command('$!Pick Paste')
	tp.macro.execute_command('''$!Pick Shift
	  X = 0.0580310880829
	  Y = 0.116062176166''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.15803108808
	  Y = 1.47694300518
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('$!Pick Paste')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 4.49274611399
	  Y = 1.31113989637
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.11658031088
	  Y = 1.67590673575
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('''$!Pick Shift
	  X = 0.00829015544041
	  Y = 0''')
	tp.macro.execute_command('''$!Pick Shift
	  X = 0
	  Y = -0.00829015544041''')
	tp.macro.execute_command('''$!Pick Shift
	  X = 0.00829015544041
	  Y = 0''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 5.32176165803
	  Y = 1.4603626943
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.15803108808
	  Y = 1.53497409326
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('''$!Pick Shift
	  X = 0
	  Y = -0.00829015544041''')
	tp.macro.execute_command('''$!Pick Shift
	  X = -0.00829015544041
	  Y = 0''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.51450777202
	  Y = 1.5018134715
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.24093264249
	  Y = 1.66761658031
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('''$!Pick Shift
	  X = 0.00829015544041
	  Y = 0''')
	tp.macro.execute_command('''$!Pick Shift
	  X = 0
	  Y = 0.00829015544041''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.78808290155
	  Y = 1.74222797927
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('$!Pick DeselectAll')
	tp.macro.execute_command('''$!Pick AddAllInRect
	  SelectText = Yes
	  SelectGeoms = Yes
	  SelectZones = Yes
	  ConsiderStyle = Yes
	  X1 = 3.04196891192
	  X2 = 3.54766839378
	  Y1 = 1.49352331606
	  Y2 = 1.82512953368''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.19119170984
	  Y = 1.66761658031
	  CollectingObjectsMode = HomogeneousAdd
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.15803108808
	  Y = 1.59300518135
	  CollectingObjectsMode = HomogeneousAdd
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.00051813472
	  Y = 1.53497409326
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('$!Pick DeselectAll')
	tp.macro.execute_command('''$!Pick AddAllInRect
	  SelectText = Yes
	  SelectGeoms = Yes
	  SelectZones = Yes
	  ConsiderStyle = Yes
	  X1 = 2.71865284974
	  X2 = 3.63056994819
	  Y1 = 1.33601036269
	  Y2 = 2.11528497409''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.11658031088
	  Y = 1.63445595855
	  CollectingObjectsMode = HomogeneousAdd
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('''$!Pick SetMouseMode
	  MouseMode = Select''')
	tp.macro.execute_command('$!Pick DeselectAll')
	tp.macro.execute_command('''$!Pick AddAllInRect
	  SelectText = Yes
	  SelectGeoms = Yes
	  SelectZones = Yes
	  ConsiderStyle = Yes
	  X1 = 2.94248704663
	  X2 = 3.60569948187
	  Y1 = 1.35259067358
	  Y2 = 2.26450777202''')
	tp.macro.execute_command('''$!Pick Magnify
	  Mag = 0.952380952381''')
	tp.macro.execute_command('''$!Pick Magnify
	  Mag = 0.952380952381''')
	tp.macro.execute_command('''$!Pick Magnify
	  Mag = 0.952380952381''')
	tp.macro.execute_command('''$!Pick Magnify
	  Mag = 0.952380952381''')
	tp.macro.execute_command('''$!Pick Magnify
	  Mag = 0.952380952381''')
	tp.macro.execute_command('''$!Pick Magnify
	  Mag = 0.952380952381''')
	tp.macro.execute_command('''$!Pick Magnify
	  Mag = 0.952380952381''')
	tp.macro.execute_command('''$!Pick Magnify
	  Mag = 0.952380952381''')
	tp.macro.execute_command('''$!Pick Magnify
	  Mag = 0.952380952381''')
	tp.macro.execute_command('''$!Pick Magnify
	  Mag = 0.952380952381''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.68031088083
	  Y = 1.32772020725
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('$!Pick DeselectAll')
	tp.macro.execute_command('''$!Pick AddAllInRect
	  SelectText = Yes
	  SelectGeoms = Yes
	  SelectZones = Yes
	  ConsiderStyle = Yes
	  X1 = 2.90103626943
	  X2 = 3.78808290155
	  Y1 = 1.47694300518
	  Y2 = 1.99093264249''')
	tp.macro.execute_command('''$!Pick SetMouseMode
	  MouseMode = Select''')
	tp.macro.execute_command('$!Pick DeselectAll')
	tp.macro.execute_command('''$!Pick AddAllInRect
	  SelectText = Yes
	  SelectGeoms = Yes
	  SelectZones = Yes
	  ConsiderStyle = Yes
	  X1 = 2.95906735751
	  X2 = 3.56424870466
	  Y1 = 1.47694300518
	  Y2 = 2.01580310881''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.11658031088
	  Y = 1.65103626943
	  CollectingObjectsMode = HomogeneousAdd
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('''$!Pick Edit
	  LineThickness = 0.1''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 2.66062176166
	  Y = 1.78367875648
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('$!Pick DeselectAll')
	tp.macro.execute_command('''$!Pick AddAllInRect
	  SelectText = Yes
	  SelectGeoms = Yes
	  SelectZones = Yes
	  ConsiderStyle = Yes
	  X1 = 2.89274611399
	  X2 = 3.64715025907
	  Y1 = 1.48523316062
	  Y2 = 1.92461139896''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 3.1414507772
	  Y = 1.62616580311
	  CollectingObjectsMode = HomogeneousAdd
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('''$!Pick Edit
	  LineThickness = 0.4''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 2.44507772021
	  Y = 1.51839378238
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('$!Pick DeselectAll')
	tp.macro.execute_command('''$!Pick AddAllInRect
	  SelectText = Yes
	  SelectGeoms = Yes
	  SelectZones = Yes
	  ConsiderStyle = Yes
	  X1 = 2.86787564767
	  X2 = 3.56424870466
	  Y1 = 1.49352331606
	  Y2 = 1.89974093264''')
	tp.macro.execute_command('''$!Pick Shift
	  X = 1.84870466321
	  Y = 2.27150259067''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 4.12797927461
	  Y = 0.904922279793
	  ConsiderStyle = Yes''')
	# End Macro.

