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
#setup rendering options
geovis.SetRenderingOptions(renderer="aggdraw", numpyspeed=True, reducevectors=False)
#create map
geovis.SetMapBackground(geovis.Color("blue", brightness=0.9))
geovis.SetMapZoom(x2x=[0,180],y2y=[0,90])
newmap = geovis.NewMap()

############
#LOAD AND SYMBOLIZE LAYERS
############
countrylayer = geovis.Layer(filepath=r"D:\Test Data\necountries\necountries.shp")
countrylayer.AddClassification(symboltype="fillcolor", valuefield="pop_est", symbolrange=[geovis.Color("white"),geovis.Color("red", intensity=0.9, brightness=0.8),geovis.Color("red", intensity=0.9, brightness=0.5)], classifytype="natural breaks", nrclasses=3)
countrylayer.AddClassification(symboltype="outlinewidth", valuefield="pop_est", symbolrange=[0.05,0.4], classifytype="natural breaks", nrclasses=3)
riverlayer = geovis.Layer(filepath=r"D:\Test Data\lines\ne_50m_rivers_lake_centerlines.shp", fillcolor=geovis.Color("blue",brightness=0.9))

############
#RENDER TO MAP
############
#add layers to map
newmap.AddToMap(countrylayer)
newmap.AddToMap(riverlayer)
#add legend
newmap.AddLegend(countrylayer, upperleft=(0.03,0.15), bottomright=(0.6,0.4))
#view map
newmap.ViewMap()


