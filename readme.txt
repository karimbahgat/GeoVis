The Python Geographic Visualizer (Geovis)
Version 0.1.0

Author
Karim Bahgat, karim.bahgat.norway@gmail.com
Date
February 21, 2014
License
Creative Commons Attribution-ShareAlike CC BY-SA, http://creativecommons.org/licenses/by-sa/4.0/

Introduction
The Python Geographic Visualizer (GeoVis) is a complete geographic visualization module intended for easy everyday-use by the general user. It has one-liners for quickly visualizing a shapefile, building and styling basic maps with multiple shapefile layers, and/or saving to imagefiles. Works as a wrapper around multiple possible rendering modules. For shapefile reading it uses a modified version of Joel Lawhead’s PyShp module. For color magic it uses Valentin Lab’s Colour module, 
The current version is functional, but should be considered a work in progress with potential bugs.

Dependencies
Technically has no external dependencies, but is highly recommended to be used with either Aggdraw, PIL or PyCairo. Default is set to Aggdraw so if using a different renderer this has to be specified for each session. If none of these are available it is still possible to use the Tkinterer Canvas as a renderer, but due to major limitations this is discouraged for larger files. 

Python Versions
Should work on Python version 2.x. Has not yet been tested on Python 3.x.

Installation
No installation required, just use sys.path.append to the geovis folder location or place the geovis folder in you Python site-packages folder, and import it using “import geovis”.

How to Use
Check out the user manual Word document in the "docs" folder for details about how to use the module, its functions, and methods. Also see and try to run the examples.py script in the examples folder. 

