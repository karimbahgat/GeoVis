"""
Example Script for the Python Geographic Visualizer (GeoVis)
https://github.com/karimbahgat/geovis
"""

############
#TEST INPUTS
############
TEMP_GEOVIS_FOLDER = r"C:\Users\BIGKIMO\Documents\GitHub\geovis"
##TEST_SHAPEFILE = r"D:\Test Data\Global Subadmins\gadm2.shp"
##ATTRIBUTE_TO_CLASSIFY = "NAME_2" #VALIDFR_1, NAME_1
TEST_SHAPEFILE = r"D:\Test Data\cshapes\cshapes.shp"
ATTRIBUTE_TO_CLASSIFY = "GWSYEAR" #VALIDFR_1, NAME_1
CLASSIFYTYPE = "natural breaks"
NRCLASSES = 5
############

#importing geovis from temporary location
import sys
sys.path.append(TEMP_GEOVIS_FOLDER)
import geovis

#setup for speed
geovis.SetRenderingOptions(numpyspeed=True, reducevectors=True)

#gradient colors
FILLGRADIENT = [geovis.Color("blue", intensity=0.9, brightness=0.5),
                geovis.Color("blue", intensity=0.99, brightness=0.8),
                geovis.Color("white"),
                geovis.Color("red", intensity=0.9, brightness=0.8),
                 geovis.Color("red", intensity=0.9, brightness=0.5)]
OUTLINEGRADIENT = [geovis.Color("black", brightness=0.8),
                 geovis.Color("black", brightness=0.0)]

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

#create map
geovis.SetMapBackground(geovis.Color("blue", brightness=0.9))
geovis.SetMapDimensions(8000,4000)
newmap = geovis.NewMap()
#addshapefile
newmap.AddToMap(shapefilepath=TEST_SHAPEFILE, classifier=classifier)
#view map
newmap.ViewMap()


