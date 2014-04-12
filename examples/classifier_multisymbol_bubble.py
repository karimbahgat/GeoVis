"""
Example Script for the Python Geographic Visualizer (GeoVis)
https://github.com/karimbahgat/geovis
"""

#importing geovis from temporary location
TEMP_GEOVIS_FOLDER = r"C:\Users\BIGKIMO\Documents\GitHub\geovis"
import sys
sys.path.append(TEMP_GEOVIS_FOLDER)
import geovis

############
#TEST INPUTS
############
BACKGROUND_SHAPEFILE = r"D:\Test Data\necountries\necountries.shp"

##TEST_SHAPEFILE = geovis.AskShapefilePath()
##ATTRIBUTE_TO_CLASSIFY = geovis.AskFieldName(TEST_SHAPEFILE)
##EXCLUDEQUERY = geovis.AskString("exclusion query")
##CLASSIFYTYPE = geovis.AskString("classification type")
##NRCLASSES = geovis.AskNumber("number of classes")

##TEST_SHAPEFILE = r"D:\Test Data\GTD_georef\gtd_georef.shp"
##ATTRIBUTE_TO_CLASSIFY = "nkill"
##CLASSIFYTYPE = "equal interval"
##NRCLASSES = 7
TEST_SHAPEFILE = r"D:\Test Data\GTD_georef\intnat_source.shp"
ATTRIBUTE_TO_CLASSIFY = "Average_nk"
CLASSIFYTYPE = "equal interval"
NRCLASSES = 5
############

#set rendering speed/quality
geovis.SetRenderingOptions(renderer="aggdraw", reducevectors=False)

#create map with background
"geovis.SetMapDimensions(6000,3000)"
geovis.SetMapZoom((0,180),(0,90))
#geovis.SetMapZoom((0,60),(0,30))
geovis.SetMapBackground(geovis.Color("blue",style="pastelle"))
newmap = geovis.NewMap()
#newmap.AddGridLines()
newmap.AddToMap(BACKGROUND_SHAPEFILE,
                fillcolor=geovis.Color("green",style="pastelle"))

#classify shapefile
classifier = geovis.Classifier()
classifier.AddClassification(symboltype="fillsize",
                             valuefield=ATTRIBUTE_TO_CLASSIFY,
                             symbolrange=[0.4,
                                          8],
                             classifytype=CLASSIFYTYPE,
                             nrclasses=NRCLASSES)
classifier.AddClassification(symboltype="outlinewidth",
                             valuefield=ATTRIBUTE_TO_CLASSIFY,
                             symbolrange=[0.01,
                                          0.5],
                             classifytype=CLASSIFYTYPE,
                             nrclasses=NRCLASSES)
classifier.AddClassification(symboltype="fillcolor",
                             valuefield=ATTRIBUTE_TO_CLASSIFY,
                             symbolrange=[geovis.Color("yellow"),
                                          geovis.Color("red")],
                             classifytype=CLASSIFYTYPE,
                             nrclasses=NRCLASSES)
##classifier.AddClassification(symboltype="fillcolor",
##                             valuefield="Average_nk", #"cntry_code",#geovis.AskFieldName(TEST_SHAPEFILE,"classifying categorical fillcolors"),
##                             classifytype="categorical")

#add shapefile to map along with the created classifier
newmap.AddToMap(shapefilepath=TEST_SHAPEFILE,
                classifier=classifier,
                symbolizer="circle",
                #fillcolor=geovis.Color("red"),
                excludequery="")#"transdyad.split(';')[0] <> 'Afghanistan'")

#add legend
newmap.AddLegend((0.03,0.5),(0.43,0.7), classifier)

#view map
newmap.ViewMap()
#newmap.SaveMap("C:/Users/BIGKIMO/Desktop/sdfdf.png")


