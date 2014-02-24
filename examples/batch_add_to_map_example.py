"""
Example Script for the Python Geographic Visualizer (GeoVis)
https://github.com/karimbahgat/geovis

Creates map from scratch, using a baselayer and adding
an entire folder of shapefiles.

Alter the testinputs to folders/shapefiles of your choice.
"""

############
#TEST INPUTS
############
TEMP_GEOVIS_FOLDER = r"C:\Users\BIGKIMO\Documents\GitHub\geovis"
MAPCOLORSTYLE = "pastelle"
BASE_SHAPEFILE = "D:\Test Data\Global Subadmins\gadm2.shp"
MANY_SHAPEFILES_FOLDER = r"D:\Test Data\DHS GPS"
############


#importing geovis from temporary location
import sys
sys.path.append(TEMP_GEOVIS_FOLDER)
import geovis

#setting up for speed
geovis.SetRenderingOptions(reducevectors=True)

#create map
geovis.SetMapBackground(geovis.Color(style=MAPCOLORSTYLE))
newmap = geovis.NewMap()

#add base shapefile layer
newmap.AddToMap(BASE_SHAPEFILE)

#overlay with a folder of many shapefiles
for eachfolder, eachfile, eachext in geovis.ShapefileFolder(MANY_SHAPEFILES_FOLDER):
    newmap.AddToMap(eachfolder+eachfile+eachext, style=MAPCOLORSTYLE)

#finally view the map
newmap.ViewMap()
