
### SHAPEFILES TO BE USED IN THE TESTS
many_polypath = r"D:\My Files\GIS Data\General\Global Subadmins\gadm2.shp"
polypath = r"D:\My Files\GIS Data\General\Country Borders\cshapes.shp"
linepath = r"C:\Users\BIGKIMO\Desktop\lines\ne_50m_rivers_lake_centerlines.shp"
pointpath = r"D:\Test Data\GPS\Ethiopia_2011\ETGE61FL.shp"
many_pointpath = r"D:\My Files\GIS Data\--(Project Specific Versions of Data)\To be continued,,,\GTD_georef\gtd_georef.shp"

### INSTALLING AND IMPORTING
# 1: either place geovis.py anywhere and do relative import
import sys
sys.path.append(r"C:\Users\BIGKIMO\Documents\GitHub\geovis")
import geovis
# 2: or place geovis.py in your Python "site-packages" folder and import normally
import geovis

### SETUP RENDERING QUALITY AND STYLE FOR ALL MAPS
geovis.SetRenderingOptions(renderer="aggdraw", numpyspeed=True, reducevectors=False)

### AD HOC USAGE 1:
"""JUST CURIOUS HOW THE SHAPEFILE LOOKS"""
geovis.ViewShapefile(polypath)

### AD HOC USAGE 2:
"""WANT TO SHARE WITH OTHERS HOW YOUR SHAPEFILE LOOKS,
SO GIVE MAP A MORE "TRENDY" STYLE USING THE EASILY STYLABLE COLOR FUNCTION"""
#first give the map an ocean background instead of the default transparent
geovis.SetMapBackground(geovis.Color("blue", style="pastelle") )
#then save your shapefile to an image
geovis.SaveShapefileImage(pointpath,
                   savepath="C:/Users/BIGKIMO/Desktop/TEST.png",
                   fillcolor=geovis.Color("green", style="pastelle"),
                   outlinecolor=geovis.Color("white"),
                   fillsize=8)

### BATCH USAGE 1:
"""HAVE A LARGE FOLDER DIRECTORY CONTAINING MANY SHAPEFILES,
AND WANTING TO EACH SHAPEFILE TO BE ACCOMPONIED BY AN IMAGE OF WHAT IT LOOKS LIKE"""
#dark color style for water
geovis.SetMapBackground(geovis.Color("blue", style="dark") )
#use a random dark-themed fillcolor to be used for all shapefiles
geovis.SetMapSymbols(fillcolor=geovis.Color(style="dark"),
            fillsize=8,
            outlinecolor=geovis.Color("black"),
            outlinewidth=1)
#use the handy ShapefileFolder function to retrieve all shapefiles from the folder
for eachfolder, eachshapefile, eachfiletype in geovis.ShapefileFolder(r"D:\Test Data\GPS"):
    shapefilepath = eachfolder+eachshapefile+eachfiletype
    #save map image next to each shapefile
    savepath = eachfolder+eachshapefile+".png"
    geovis.SaveShapefileImage(shapefilepath, savepath)

### BATCH USAGE 2
"""FROM MANY SCATTERED SHAPEFILES, CREATE MAPS OF EACH INTO A SINGLE GALLERY FOLDER"""
#same default batch style for all shapefiles
geovis.SetMapBackground(geovis.Color("blue", style="pastelle") )
geovis.SetMapSymbols(fillsize=8,
                outlinecolor=geovis.Color(basecolor="white", brightness=0.9),
                outlinewidth=1)
#save a gallery of map images from many shapefiles
for eachfolder, eachshapefile, eachfiletype in geovis.ShapefileFolder(r"D:\Test Data\GPS"):
    shapefilepath = eachfolder+eachshapefile+eachfiletype
    #vary up the fillcolor of each shapefile with a random pastelle
    geovis.SaveShapefileImage(shapefilepath, "C:/Users/BIGKIMO/Desktop/mapgallery/"+eachshapefile+".png", fillcolor=geovis.Color(style="pastelle"))

### MAP BUILD USAGE 1:
"""JUST A SIMPLE MAP OF TWO SHAPEFILES ON SAME MAP, NO SYMBOLS OR COLORS USED, TRANSPARENT BACKGROUND, AND USING ALL DEFAULT AND RANDOM COLORS"""
geovis.SetMapBackground(None)
newmap = geovis.NewMap()
newmap.AddToMap(polypath, fillcolor=geovis.Color())
newmap.AddToMap(pointpath, fillcolor=geovis.Color())
newmap.SaveMap("C:/Users/BIGKIMO/Desktop/heavycombined.png")

### MAP BUILD USAGE 2:
"""HOW ABOUT BUILDING A MAP, INCLUDING COMBINING ALL THE SHAPEFILES FROM ABOVE,
AND INSTEAD OF SPECIFYING SAME COLOR STYLE FOR EACH ONE, USING A SINGLE STYLED COLORFEEDER"""
#map background
geovis.SetMapBackground(geovis.Color("blue", style="pastelle"))
#some batch style for all shapefiles
geovis.SetMapSymbols(fillsize=4, outlinecolor=geovis.Color(basecolor="white", brightness=0.9), outlinewidth=1)
#set color theme to be varied for each shapefile
filltheme = geovis.ColorFeeder(style="pastelle")
#start by creating a new map builder
newmap = geovis.NewMap()
#first set background country layer
newmap.AddToMap(polypath, fillcolor=next(filltheme))
#then add contextual road layer
newmap.AddToMap(linepath, fillcolor=next(filltheme))
#then add each of many point shapefiles
for eachfolder, eachshapefile, eachfiletype in geovis.ShapefileFolder(r"D:\Test Data\GPS"):
    shapefilepath = eachfolder+eachshapefile+eachfiletype
    newmap.AddToMap(shapefilepath, fillcolor=next(filltheme))
#finally save map
newmap.SaveMap("C:/Users/BIGKIMO/Desktop/heavycombined2.png")
print "finished!"



