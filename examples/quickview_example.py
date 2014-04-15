"""
Example Script for the Python Geographic Visualizer (GeoVis)
https://github.com/karimbahgat/geovis
"""

#importing geovis from temporary location
TEMP_GEOVIS_FOLDER = r"C:\Users\BIGKIMO\Documents\GitHub\geovis"
import sys
sys.path.append(TEMP_GEOVIS_FOLDER)
import geovis

#setting up for speed
geovis.SetRenderingOptions(reducevectors=True)

#view shapefile
geovis.ViewShapefile(r"D:\Test Data\cshapes\cshapes.shp", maptitle="ViewShapefile Example")
