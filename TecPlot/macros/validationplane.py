import tecplot as tp
from tecplot.exception import *
from tecplot.constant import *

# Uncomment the following line to connect to a running instance of Tecplot 360:
# tp.session.connect()
def xyplot():
	tp.active_frame().plot().view.theta=-90.1425
	tp.active_frame().plot().view.position=(-263.976,
	    tp.active_frame().plot().view.position[1],
	    tp.active_frame().plot().view.position[2])
	tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
	    0.142601,
	    tp.active_frame().plot().view.position[2])
	tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
	    tp.active_frame().plot().view.position[1],
	    30.8998)
	tp.active_frame().plot().view.width=8.67654
	tp.active_frame().plot().view.psi=0.310695
	tp.active_frame().plot().view.theta=-113.395
	tp.active_frame().plot().view.alpha=23.3233
	tp.active_frame().plot().view.position=(-321.002,
	    tp.active_frame().plot().view.position[1],
	    tp.active_frame().plot().view.position[2])
	tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
	    0.142601,
	    tp.active_frame().plot().view.position[2])
	tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
	    tp.active_frame().plot().view.position[1],
	    64.0136)
	tp.active_frame().plot().view.width=8.67654
	tp.active_frame().plot().view.psi=108.532
	tp.active_frame().plot().view.theta=-90.1301
	tp.active_frame().plot().view.alpha=-0.11258
	tp.active_frame().plot().view.position=(-258.537,
	    tp.active_frame().plot().view.position[1],
	    tp.active_frame().plot().view.position[2])
	tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
	    0.142601,
	    tp.active_frame().plot().view.position[2])
	tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
	    tp.active_frame().plot().view.position[1],
	    -23.2652)
	tp.active_frame().plot().view.width=8.67654
	tp.active_frame().plot().view.psi=176.703
	tp.active_frame().plot().view.theta=92.1453
	tp.active_frame().plot().view.alpha=-177.929
	tp.active_frame().plot().view.position=(-325.139,
	    tp.active_frame().plot().view.position[1],
	    tp.active_frame().plot().view.position[2])
	tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
	    0.142601,
	    tp.active_frame().plot().view.position[2])
	tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
	    tp.active_frame().plot().view.position[1],
	    -68.335)
	tp.active_frame().plot().view.width=8.67654
	tp.active_frame().plot().view.position=(-325.139,
	    tp.active_frame().plot().view.position[1],
	    tp.active_frame().plot().view.position[2])
	tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
	    0.142601,
	    tp.active_frame().plot().view.position[2])
	tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
	    tp.active_frame().plot().view.position[1],
	    -68.335)
	tp.active_frame().plot().view.width=9.23918
	tp.active_frame().plot().view.position=(-325.184,
	    tp.active_frame().plot().view.position[1],
	    tp.active_frame().plot().view.position[2])
	tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
	    0.903083,
	    tp.active_frame().plot().view.position[2])
	tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
	    tp.active_frame().plot().view.position[1],
	    -68.3307)
	tp.active_frame().plot().view.width=9.23918
	tp.active_frame().plot().show_mesh=True
	tp.macro.execute_command('$!RedrawAll')
	tp.macro.execute_command('''$!Pick SetMouseMode
	  MouseMode = Select''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 8.33760683761
	  Y = 5.51495726496
	  ConsiderStyle = Yes''')
	tp.active_frame().plot().view.position=(-325.184,
	    tp.active_frame().plot().view.position[1],
	    tp.active_frame().plot().view.position[2])
	tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
	    0.903083,
	    tp.active_frame().plot().view.position[2])
	tp.active_frame().plot().view.position=(tp.active_frame().plot().view.position[0],
	    tp.active_frame().plot().view.position[1],
	    -68.3307)
	tp.active_frame().plot().view.width=9.44091
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 8.55413105413
	  Y = 5.25284900285
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 8.57692307692
	  Y = 6.22150997151
	  ConsiderStyle = Yes''')
	tp.macro.execute_command('''$!Pick AddAtPosition
	  X = 8.57692307692
	  Y = 6.21011396011
	  CollectingObjectsMode = HomogeneousAdd
	  ConsiderStyle = Yes''')

def labelandminorfix():
    tp.macro.execute_command('''$!Pick AddAtPosition
  X = 8.32621082621
  Y = 4.62606837607
  CollectingObjectsMode = HomogeneousAdd
  ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{Header{Show = Yes}}''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{Header{TextShape{Height = 3.5}}}''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{Header{TextShape{Height = 4.5}}}''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{Header{UseCustomText = Yes}}''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{Header{CustomText = 'd'}}''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{Header{CustomText = 'dB'}}''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{NumberTextShape{SizeUnits = Point}}''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{NumberTextShape{Height = 22.0399999999999991}}''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{NumberTextShape{Height = 21.0399999999999991}}''')
    tp.macro.execute_command('''$!GlobalContour 1  Legend{NumberTextShape{Height = 20.0399999999999991}}''')
    tp.macro.execute_command('''$!RedrawAll ''')
    tp.macro.execute_command('''$!Pick Shift
      X = -0.011396011396
      Y = 0.22792022792''')
    tp.macro.execute_command('''$!Pick AddAtPosition
      X = 8.69088319088
      Y = 0.888176638177
      ConsiderStyle = Yes''')
    tp.macro.execute_command('''$!Pick Shift
      X = -0.296296296296
      Y = 0.17094017094''')
    tp.macro.execute_command('''$!Pick Shift
      X = -0.148148148148
      Y = 0.250712250712''')

# End Macro.

	# End Macro.

