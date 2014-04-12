"""
Example Script for the Python Geographic Visualizer (GeoVis)
https://github.com/karimbahgat/geovis
"""

############
#TEST INPUTS
############
TEMP_GEOVIS_FOLDER = r"C:\Users\BIGKIMO\Documents\GitHub\geovis"
TEST_SHAPEFILE = r"D:\Test Data\cshapes\cshapes.shp"
ATTRIBUTE_TO_COLOR = "CNTRY_NAME"
GRADIENT_BASECOLOR = "green"
############


#importing geovis from temporary location
import sys
sys.path.append(TEMP_GEOVIS_FOLDER)
import geovis

#setting up for speed
geovis.SetRenderingOptions(reducevectors=True)

#create map
newmap = geovis.NewMap()

#gradient colors, next color for each unique attribute
fromcolor = geovis.Color(GRADIENT_BASECOLOR, intensity=0.6, brightness=0.9)
tocolor = geovis.Color(GRADIENT_BASECOLOR, intensity=0.6, brightness=0.4)
gradient = geovis.Gradient(fromcolor, tocolor, 250)
assignedcolors = dict()

#missing link, read all attributes in memory, sort them, then assign classes to each range
#...

#loop through shapefile
shapefile = geovis.Shapefile(TEST_SHAPEFILE)
for eachshape in shapefile:
    #read attribute
    attributevalue = eachshape.GetAttributes(ATTRIBUTE_TO_COLOR)
    #assign next gradual color if new country
    if attributevalue not in assignedcolors:
        assignedcolors[attributevalue] = next(gradient)
    #render with assigned color
    newmap.AddShape(eachshape,
                    fillcolor=assignedcolors[attributevalue],
                    outlinewidth=0.3)
#view map
newmap.ViewMap()


