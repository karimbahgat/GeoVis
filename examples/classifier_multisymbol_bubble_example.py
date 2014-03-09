"""
Example Script for the Python Geographic Visualizer (GeoVis)
https://github.com/karimbahgat/geovis
"""

############
#TEST INPUTS
############
TEMP_GEOVIS_FOLDER = r"C:\Users\BIGKIMO\Documents\GitHub\geovis"
TEST_SHAPEFILE = r"D:\Test Data\GTD_georef\gtd_georef.shp"
ATTRIBUTE_TO_CLASSIFY = "nkill"
CLASSIFYTYPE = "natural breaks"
NRCLASSES = 3
############

#importing geovis from temporary location
import sys
sys.path.append(TEMP_GEOVIS_FOLDER)
import geovis

#gradient colors, next color for each unique attribute
FILLGRADIENT = [geovis.Color("green", intensity=0.9, brightness=0.5),
                geovis.Color("yellow", intensity=0.9, brightness=0.5),
                geovis.Color("red", intensity=0.9, brightness=0.5)]
OUTLINEGRADIENT = [geovis.Color("black", brightness=0.6),
                 geovis.Color("black", brightness=0.0)]
FILLSIZERANGE = [5, 50, 70]

#create classifications
classifier = geovis.Classifier()
classifier.AddClassification(symboltype="fillcolor",
                             valuefield=ATTRIBUTE_TO_CLASSIFY,
                             symbolrange=FILLGRADIENT,
                             classifytype=CLASSIFYTYPE,
                             nrclasses=NRCLASSES,
                             excludevalues=[0,-1])
classifier.AddClassification(symboltype="outlinecolor",
                             valuefield=ATTRIBUTE_TO_CLASSIFY,
                             symbolrange=OUTLINEGRADIENT,
                             classifytype=CLASSIFYTYPE,
                             nrclasses=NRCLASSES,
                             excludevalues=[0,-1])
classifier.AddClassification(symboltype="fillsize",
                             valuefield=ATTRIBUTE_TO_CLASSIFY,
                             symbolrange=FILLSIZERANGE,
                             classifytype=CLASSIFYTYPE,
                             nrclasses=NRCLASSES,
                             excludevalues=[0,-1])

#create map
newmap = geovis.NewMap()
#addshapefile
newmap.AddToMap(shapefilepath=TEST_SHAPEFILE, classifier=classifier)
#view map
newmap.ViewMap()


