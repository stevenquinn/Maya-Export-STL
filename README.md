Maya-Export-STL
===============

An STL exported created for Maya using python.

This Maya script allows you to export a model as an STL file, which is popular for use in 3d printing. First, select a polygonal model (currently only works with polygons), and then run the script. Use the python code below in the script editor to load the script:

_________________________________

import exportSTL as stl
reload(stl)

stl.exportSTL()
