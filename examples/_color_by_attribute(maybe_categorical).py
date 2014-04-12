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
############


#importing geovis from temporary location
import sys
sys.path.append(TEMP_GEOVIS_FOLDER)
import geovis

#setting up for speed
geovis.SetRenderingOptions(reducevectors=True)

#create map
newmap = geovis.NewMap()

#categorical colors, one color per unique attribute
assignedcolors = dict()

#loop through shapefile
shapefile = geovis.Shapefile(TEST_SHAPEFILE)
print shapefile.fieldnames
for eachshape in shapefile:
    #read attribute
    attributevalue = eachshape.GetAttributes(ATTRIBUTE_TO_COLOR)
    #assign random color if new country
    if attributevalue not in assignedcolors:
        assignedcolors[attributevalue] = geovis.Color()
    #render with assigned color
    newmap.AddShape(eachshape,
                    fillcolor=assignedcolors[attributevalue],
                    outlinewidth=0.3)

#view map
newmap.ViewMap()


