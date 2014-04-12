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
##TEST_SHAPEFILE = geovis.AskShapefilePath()
##ATTRIBUTE_TO_CLASSIFY = geovis.AskFieldName(TEST_SHAPEFILE)
##EXCLUDEQUERY = geovis.AskString("exclusion query")
##CLASSIFYTYPE = geovis.AskString("classification type")
##NRCLASSES = geovis.AskNumber("number of classes")

##TEST_SHAPEFILE = r"D:\Test Data\Global Subadmins\gadm2.shp"
##ATTRIBUTE_TO_CLASSIFY = "NAME_2" #VALIDFR_1, NAME_1
##EXCLUDEQUERY = ""
##CLASSIFYTYPE = "equal classes"
##NRCLASSES = 5

TEST_SHAPEFILE = r"D:\Test Data\necountries\necountries.shp"
ATTRIBUTE_TO_CLASSIFY = "pop_est" #VALIDFR_1, NAME_1
EXCLUDEQUERY = "pop_est <= 14000000"
CLASSIFYTYPE = "natural breaks"
NRCLASSES = 6

LINE_SHAPEFILE = r"D:\Test Data\lines\ne_50m_rivers_lake_centerlines.shp"
############

#setup for speed
geovis.SetRenderingOptions(renderer="aggdraw", numpyspeed=True, reducevectors=False)

#create map
geovis.SetMapBackground(geovis.Color("blue", brightness=0.9))
"geovis.SetMapDimensions(8000,4000)"
geovis.SetMapZoom((0,180),(0,90))
newmap = geovis.NewMap()

#load and symbolize countries
countrylayer = geovis.Layer(filepath=TEST_SHAPEFILE,
                            excludequery=EXCLUDEQUERY)
countrylayer.AddClassification(symboltype="fillcolor",
                             valuefield=ATTRIBUTE_TO_CLASSIFY,
                             symbolrange=[#geovis.Color("blue", intensity=0.9, brightness=0.5),
                                          #geovis.Color("blue", intensity=0.99, brightness=0.8),
                                          geovis.Color("white"),
                                          geovis.Color("red", intensity=0.9, brightness=0.8),
                                          geovis.Color("red", intensity=0.9, brightness=0.5)],
                             classifytype=CLASSIFYTYPE,
                             nrclasses=NRCLASSES)
countrylayer.AddClassification(symboltype="outlinewidth",
                             valuefield=ATTRIBUTE_TO_CLASSIFY,
                             symbolrange=[0.05,
                                          0.4],
                             classifytype=CLASSIFYTYPE,
                             nrclasses=NRCLASSES)
#load and symbolize rivers
riverlayer = geovis.Layer(filepath=LINE_SHAPEFILE,
                          fillcolor=geovis.Color("blue",brightness=0.9))

#add layers to map
newmap.AddToMap(countrylayer)
newmap.AddToMap(riverlayer)

#add legend
newmap.AddLegend(countrylayer, x2x=(0.03,0.6), y2y=(0.15,0.4))

#view map
newmap.ViewMap()
#newmap.SaveMap("C:/Users/BIGKIMO/Desktop/sdfdf.png")


