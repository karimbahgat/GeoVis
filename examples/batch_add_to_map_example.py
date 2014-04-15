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

#create map
MAPCOLORSTYLE = "pastelle"
geovis.SetMapBackground(geovis.Color("blue",style=MAPCOLORSTYLE))
newmap = geovis.NewMap()

#add base shapefile layer
base_layer = geovis.Layer("D:\Test Data\Global Subadmins\gadm2.shp")
newmap.AddToMap(base_layer)

#overlay with a folder of many shapefiles
for eachfolder, eachfile, eachext in geovis.ShapefileFolder(r"D:\Test Data\DHS GPS"):
    eachlayer = geovis.Layer(filepath=eachfolder+eachfile+eachext, fillcolor=geovis.Color("random", style=MAPCOLORSTYLE))
    newmap.AddToMap(eachlayer)

#add title
newmap.AddText(relx=0.5, rely=0.1, text="Batch Map Example", textsize=0.06)

#finally view the map
newmap.ViewMap()
