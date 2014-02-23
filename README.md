#H1 The Python Geographic Visualizer (Geovis)
*Version: 0.1.0*
*Author: Karim Bahgat, karim.bahgat.norway@gmail.com*
*Date: February 21, 2014*
*License: Creative Commons Attribution-ShareAlike CC BY-SA, http://creativecommons.org/licenses/by-sa/4.0/*

##H2 Introduction

###H3 About
The Python Geographic Visualizer (GeoVis) is a complete geographic visualization module intended for easy everyday-use by the general user. It has one-liners for quickly visualizing a shapefile, building and styling basic maps with multiple shapefile layers, and/or saving to imagefiles. Uses the built-in Tkinter or other third-party rendering modules to do its main work. The current version is functional, but should be considered a work in progress with potential bugs, so use with care.

###H3 Modules Included
GeoVis relies on and uses the excellent work of others before it. In order to be dependency-free GeoVis has these already included in its main folder: 
-For shapefile reading it uses a modified version of 
[Joel Lawhead’s PyShp module](http://code.google.com/p/pyshp/). 
-For color-wizardry it uses [Valentin Lab’s Colour module](https://pypi.python.org/pypi/colour). 

###H3 Installation
No installation required, just use sys.path.append to the geovis folder location or place the geovis folder in you Python site-packages folder, and import it using “import geovis”.

###H3 Dependencies
Technically speaking, GeoVis has no external dependencies, but it is highly recommended to be used with either Aggdraw, PIL or PyCairo. Default is set to Aggdraw so if using a different renderer this has to be specified for each session. If none of these are available it is still possible to use the Tkinterer Canvas as a renderer, but due to major limitations this is not recommended for viewing larger shapefiles. 

###H3 Python Compatibility
Should work on Python version 2.x. Has not yet been tested on Python 3.x.

###H3 Known Problems
Current problems and limitations that I hope to change in future releases include:
-The shapefiles have to be in lat/long coordinates (i.e. unprojected) in order to be displayed correctly. That is, GeoVis does not yet handle projections or coordinate transformation. 
-There is currently no way to zoom in to a certain extent, meaning that the visualizations always show the entire world (-180 to 180, and -90 to 90), which is unfortunate if your shapefiles are local/within-country-based. This shouldn't be too hard to fix in a future release however. 


##H2 Basic Usage
*This next section describes the basic functions and syntax of GeoVis. If you're unsure about or experiencing problems with a particular function you can look up the full documentation by typing `help(geovis)`, or by going online to [the GeoVis Wiki at Github](https://github.com/karimbahgat/geovis/wiki).

###H3 Importing
Assuming you have already installed it as described in the Installation section, GeoVis is imported as:

```python
import geovis

###H3 Choosing Your Renderer
If you do not have Aggdraw installed (which is the default renderer) then begin your script by changing to a renderer that you know you have, for instance PIL (if you have Numpy installed you might as well enable that for faster speed while you're at it):

```python
geovis.SetRenderingOptions(renderer="PIL", numpyspeed=True)

###H3 Instant Mapping
If you are simply wanting to inspect some shapefile interactively, or for seeing how your processed shapefile turned out, then you do this with a simple one-liner:

```python
geovis.ViewShapefile("C:/shapefile.shp")

If you quickly want to show someone else your shapefile over email or on a forum you can just as easily save you map to an image either by clicking the "save image" button in the interactive window viewer or with the following line:

```python
geovis.SaveShapefileImage("C:/shapefile.shp",
                   savepath="C:/output_picture.png")

###H3 Batch Map Creation
Sometimes it is necessary to quickly create a gallery of images of all your shapefiles in a given directory. GeoVis provides a general utility tool that can help you do this; it loops through, parses, and returns the foldername, filename, and extension of all shapefiles in a folder tree, which in turn can be used as input for the SaveShapefileImage function. So for instance we may write it as:

```python
for eachfolder, eachshapefile, eachfiletype in geovis.ShapefileFolder(r"D:\Test Data\GPS"):
    shapefilepath = eachfolder+eachshapefile+eachfiletype
    savetopath = "C:/Users/BIGKIMO/Desktop/mapgallery/"+eachshapefile+".png"
    geovis.SaveShapefileImage(shapefilepath, savetopath)

The filename, parent-folder, and file extension can be played around with to do many other batch operations as well, such as placing each map image next to (in the same folder as) each shapefile. 

###H3 Adding Flavor to Your Map
The above quick methods used a set of default symbol options for the shapefiles that they rendered. There are however several ways to add more flavor to your map. The most basic stylizing tool you will want to know about is the Color creator (a wrapper around [Valentin Lab’s Colour module](https://pypi.python.org/pypi/colour) with added convenience functionality). You can either create a random color by not specifying any arguments:

```python
randomcolor = geovis.Color()

Or you can create a specific color the way you imagine it in your head by writing the color name and optionally tweaking the color intensity and brightness (float value between 0 and 1). Let's create a strong (high intensity) but dark (low brightness) red:

```python
strongdarkred = geovis.Color("red", intensity=0.8, brightness=0.2)

Alternatively, instead of creating a very specific color you can create a random color that still keeps within certain limits. This can be done because the color options that you do not specify are left to vary at random. This means that you can create any random color across, say, the spectrum of dark and weak colors by specifying a low brightness value and low intensity value but not specifying a color name, which will produce a random matte-looking color. Better yet, you can set the style argument to "matte" (among many other style names, see the documentation for the full list) which automatically chooses the brightness and intensity for you:

```python
randompallettecolor = geovis.Color(style="matte")

Assuming you now know how to set your own colors or color styles, these colors are useful since they can be used to specify the color of any number of symbol options passed as keyword arguments to GeoVis' various rendering functions (see the autogenerated documentation for a full list of changable symbol options). For instance, you may set the fillcolor of your shapefile polygons/lines/circles to our strong-dark-red from previously. In addition we will increase the outline width to match the strong fillcolor (we leave the outline *color to its defaul black since this fits with the map):

```python
geovis.SetMapSymbols(fillcolor=strongdarkred,
            outlinewidth=5)

###H3 Building Your Map From Scratch
However, if creating a visually appealing map is your goal then you are probably going to want to add additional shapefiles to the same map, in which case you will need to build your map from scratch. Let's decide to make it a pastelle themed map. Furthermore, to add to the pastelle theme of the map we specify that the ocean background should be a pastelle blue, rather than the default transparent color. Let's also make it a higher resolution map (the default is the pixel dimensions of your screen) so that one can zoom in and see all the details of your beautiful creation:

```python
geovis.SetMapDimensions(width=8000, height=4000)
geovis.SetMapBackground(geovis.Color("blue", style="pallette")
newmap = geovis.NewMap()
newmap.AddToMap(polypath, fillcolor=geovis.Color(style="pallette"))
newmap.AddToMap(pointpath, fillcolor=geovis.Color(style="pallette"))
newmap.SaveMap("C:/Users/BIGKIMO/Desktop/heavycombined.png")

And that about covers the basic functionality of GeoVis. Yet, there are many possibilities left to explore by combining the various functions in new ways. For a full list of all the functions and details on exactly how to use them see the documentation. 

