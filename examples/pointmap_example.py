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
#SETUP
############
#set rendering options
geovis.SetRenderingOptions(renderer="aggdraw", numpyspeed=True, reducevectors=False)
#create map
geovis.SetMapBackground(geovis.Color("blue", brightness=0.9))
geovis.SetMapZoom(x2x=[-120,40],y2y=[-60,20])
newmap = geovis.NewMap()

############
#LOAD AND SYMBOLIZE LAYERS
############
countrylayer = geovis.Layer(filepath=r"D:\Test Data\necountries\necountries.shp", fillcolor=geovis.Color("yellow",brightness=0.8))
pointlayer = geovis.Layer(filepath=r"D:\Test Data\GTD_Georef\gtd_georef.shp", symbolizer="square")
pointlayer.AddClassification(symboltype="fillcolor", valuefield="nwound", symbolrange=[geovis.Color("white"),geovis.Color("red", intensity=0.9, brightness=0.9),geovis.Color("red", intensity=0.9, brightness=0.5)], classifytype="natural breaks", nrclasses=3)
pointlayer.AddClassification(symboltype="fillsize", valuefield="nwound", symbolrange=[0.3,2.8], classifytype="natural breaks", nrclasses=3)

############
#RENDER TO MAP
############
#add layers to map
newmap.AddToMap(countrylayer)
newmap.AddToMap(pointlayer)
#add legend
newmap.AddLegend(pointlayer, upperleft=(0.5,0.7), bottomright=(0.9,0.9))
#view map
newmap.ViewMap()


