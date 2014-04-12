"""
Example Script for the Python Geographic Visualizer (GeoVis)
https://github.com/karimbahgat/geovis
"""

############
#TEST INPUTS
############
TEMP_GEOVIS_FOLDER = r"C:\Users\BIGKIMO\Documents\GitHub\geovis"
#TEST_SHAPEFILE = r"D:\Test Data\GTD_georef\gtd_georef.shp"
TEST_SHAPEFILE = r"D:\Test Data\DHS GPS\Cameroon_2011\CMGE61FL.shp"
ATTRIBUTE_TO_CLASSIFY = "LATNUM"
CLASSIFYTYPE = "equal interval"
############


#importing geovis from temporary location
import sys
sys.path.append(TEMP_GEOVIS_FOLDER)
import geovis

#setting up for speed
geovis.SetRenderingOptions(reducevectors=True)

#create map
newmap = geovis.NewMap()

#bubble color and sizerange
bubblecolor = geovis.Color(intensity=0.6, brightness=0.4)
fromsize = 6
tosize = 50

#create shapefile
shapefile = geovis.Shapefile(TEST_SHAPEFILE)
print shapefile.fieldnames

#classify values into symbols
classifier = geovis.Classifier()
shapefile.progresstext = "classifying"
for eachshape in shapefile:
    attributevalue = eachshape.GetAttributes(ATTRIBUTE_TO_CLASSIFY)
    classifier.AddValue(attributevalue)
classifier.CalculateClasses(fromsize, tosize, classifytype=CLASSIFYTYPE, nrclasses=4, excludevalues=[-1.0, 0.0])

#loop through shapefile
shapefile.progresstext = "rendering"
for eachshape in shapefile:
    #read attribute
    attributevalue = eachshape.GetAttributes(ATTRIBUTE_TO_CLASSIFY)
    #retrieve class color for that attribute value
    classsize = classifier.GetSymbol(attributevalue)
    #render with class color
    if classsize:
        newmap.AddShape(eachshape,
                        fillcolor=bubblecolor,
                        fillsize=classsize,
                        outlinewidth=0.3)
#view map
newmap.ViewMap()


