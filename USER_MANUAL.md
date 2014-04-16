# User Manual for Python Geographic Visualizer (GeoVis)

**Version: 0.2.0**

**Date: April 15, 2014**

**Author: [Karim Bahgat](https://uit.academia.edu/KarimBahgat)**

**Contact: karim.bahgat.norway@gmail.com**

**Homepage: https://github.com/karimbahgat/geovis**

## Table of Contents

- [About](#about)
  - [System Compatibility](#system-compatibility)
  - [Dependencies](#dependencies)
  - [License](#license)
- [How GeoVis Works](#how-geovis-works)
  - [Usage Philosophy](#usage-philosophy)
  - [Screen Coordinate System](#screen-coordinate-system)
  - [Stylizing Options](#stylizing-options)
  - [Text Options](#text-options)
  - [Available Text Fonts](#available-text-fonts)
- [Functions and Classes](#functions-and-classes)
  - [geovis.AskColor](#geovisaskcolor)
  - [geovis.AskFieldName](#geovisaskfieldname)
  - [geovis.AskNumber](#geovisasknumber)
  - [geovis.AskShapefilePath](#geovisaskshapefilepath)
  - [geovis.AskString](#geovisaskstring)
  - [geovis.Color](#geoviscolor)
  - [geovis.Layer](#geovislayer----class-object)
    - [.AddClassification](#addclassification)
  - [geovis.NewMap](#geovisnewmap----class-object)
    - [.AddLegend](#addlegend)
    - [.AddShape](#addshape)
    - [.AddText](#addtext)
    - [.AddToMap](#addtomap)
    - [.DrawCircle](#drawcircle)
    - [.DrawLine](#drawline)
    - [.DrawRectangle](#drawrectangle)
    - [.SaveMap](#savemap)
    - [.ViewMap](#viewmap)
  - [geovis.SaveShapefileImage](#geovissaveshapefileimage)
  - [geovis.SetMapBackground](#geovissetmapbackground)
  - [geovis.SetMapDimensions](#geovissetmapdimensions)
  - [geovis.SetMapZoom](#geovissetmapzoom)
  - [geovis.SetRenderingOptions](#geovissetrenderingoptions)
  - [geovis.Shapefile](#geovisshapefile----class-object)
    - [.ClearSelection](#clearselection)
    - [.InvertSelection](#invertselection)
    - [.SelectByQuery](#selectbyquery)
  - [geovis.ShapefileFolder](#geovisshapefilefolder)
  - [geovis.ViewShapefile](#geovisviewshapefile)

## About

Python Geographic Visualizer (GeoVis) is a standalone geographic visualization
module for the Python programming language intended for easy everyday-use by
novices and power-programmers alike. It has one-liners for quickly visualizing
a shapefile, building and styling basic maps with multiple shapefile layers,
and/or saving to imagefiles. Uses the built-in Tkinter or other third-party
rendering modules to do its main work. The current version is functional, but
should be considered a work in progress with potential bugs, so use with care.
For now, only visualizes shapefiles that are in lat/long unprojected coordinate
system.

### System Compatibility

Should work on Python version 2.x and Windows. Has not yet been tested on
Python 3.x or other OS systems.

### Dependencies

Technically speaking, GeoVis has no external dependencies, but it is highly
recommended that you install the [Aggdraw](http://effbot.org/zone/aggdraw-index.htm),
[PIL](http://www.pythonware.com/products/pil/) or [PyCairo](http://cairographics.org/pycairo/)
renderer libraries to do the rendering. GeoVis automatically detects which
renderer module you have and uses the first it finds in the following order
(aggdraw, PIL, pycairo). If you wish to manually choose a different renderer
this has to be specified for each session. If none of these are available then
GeoVis will default to using the built-in Tkinter Canvas as its renderer, but
due to major limitations this is not recommended for viewing larger shapefiles. 

### License

Contributors are wanted and needed, so this code is free to share, use, reuse,
and modify according to the MIT license, see license.txt

## How GeoVis works

The following section describes some general info and options about how
GeoVis works. 

### Usage Philosophy

The general philosophy of GeoVis is that it should be easy to both learn
and use for end-users, particularly for people who are new to programming.
More specifically: 

- It should be logical and intuitive what commands to use.
- Making a simple map should require relatively few lines of code.
- The user should only have to learn and deal with a few basic commands.
- All command names use full wording and first-letter uppercasing  
  of each word for easy identification, ala the Arcpy syntax. 

The precise commands and arguments to use can be looked up in the
documentation. Using these the general steps to follow are:

1. Create a new map
2. Create and symbolize layers of geographical data
3. Add the layers to the map
4. View or save the map

### Screen Coordinate system

Many of the rendering methods let the user to specify one or more
locations in relative screen coordinates. These screen coordinates
are given as x and y values with a float between 0 and 1. The relative
coordinates (0,0) places something in the upper left corner of the
screen, while (1,1) places it in the bottom right corner.

### Stylizing Options

Styling a map layer is done by setting one or more keyword arguments
during the creation of the Layer class. The same styling keywords can
also be used when manually drawing shapes and figures on a map (the ones 
offering the "customoptions" argument option). 

| __option__ | __description__ 
| --- | --- 
| fillsize | the size of a circle, square, pyramid, or the thickness of a line. Has no effect on polygon shapes. Given as proportion of the map size, so that a circle of size 0.10 will cover about 10 percent of the map. A float between 0 and 1
| fillwidth | currently only used for the width of a pyramid when using the pyramid symbolizer. Given as proportion of the map size. A float between 0 and 1
| fillheight | currently has no effect
| fillcolor | the hex color of the fill
| outlinewidth | the width of the outline if any, given as proportion of the fillsize. A float between 0 and 1
| outlinecolor | the hex color of the outline

### Text Options

When adding text to a map one can use one or more of the following
keyword arguments:

| __option__ | __description__ 
| --- | --- 
| textfont | the name of the textfont to use; available textfonts vary depending on the renderer being used, see list below.
| textsize | the size of the text, given as percent pixelheight of the map dimensions (eg 0.20 being a really large text with a size of about 20 percent of the map)
| textcolor | the hex color string of the text
| textopacity | currently not being used
| texteffect | currently not being used
| textanchor | what area of the text to use as the anchor point when placing it, given as one of the following compass direction strings: center, n, ne, e, se, s, sw, w, nw
| textboxfillcolor | the fillcolor of the text's bounding box, if any (default is None, meaning no bounding box)
| textboxoutlinecolor | the outlinecolor of the bounding box, if any (default is None, meaning no bounding box outline)
| textboxfillsize | proportional size of the text's bounding box relative to the textsize (eg 1.10 gives the bounding box about a 10 percent padding around the text, default is 1.10)
| textboxoutlinewidth | width of the textbox outline as percent of the textboxfilling (eg 1 gives a 1 percent outline width)
| textboxopacity | currently not being used

### Available Text Fonts

Only a few basic text fonts are currently supported by each renderer.
They are: 

- Tkinter
  - times new roman
  - courier
  - helvetica
- PIL
  - times new roman
  - arial
- Aggdraw
  - times new roman
  - arial
- PyCairo
  - serif
  - sans-serif
  - cursive
  - fantasy
  - monospace


## Functions and Classes

### geovis.AskColor(...):
Pops up a temporary tk window asking user to visually choose a color.
Returns the chosen color as a hex string. Also prints it as text in case
the user wants to remember which color was picked and hardcode it in the script.

| __option__ | __description__ 
| --- | --- 
| *text | an optional string to identify what purpose the color was chosen for when printing the result as text.

### geovis.AskFieldName(...):
Loads and prints the available fieldnames of a shapefile, and asks the user which one to choose.
Returns the chosen fieldname as a string.

| __option__ | __description__ 
| --- | --- 
| *text | an optional string to identify for what purpose the chosen fieldname will be used.

### geovis.AskNumber(...):
Asks the user to interactively input a number (float or int) at any point in the script, and returns the input number.

| __option__ | __description__ 
| --- | --- 
| *text | an optional string to identify for what purpose the chosen number will be used.

### geovis.AskShapefilePath(...):
Pops up a temporary tk window asking user to visually choose a shapefile.
Returns the chosen shapefile path as a text string. Also prints it as text in case
the user wants to remember which shapefile was picked and hardcode it in the script.

| __option__ | __description__ 
| --- | --- 
| *text | an optional string to identify what purpose the shapefile was chosen for when printing the result as text.

### geovis.AskString(...):
Asks the user to interactively input a string at any point in the script, and returns the input string.

| __option__ | __description__ 
| --- | --- 
| *text | an optional string to identify for what purpose the chosen string will be used.

### geovis.Color(...):
Returns a hex color string of the color options specified.
NOTE: New in v0.2.0, basecolor, intensity, and brightness no longer defaults to random, and it is no longer possible to call an empty Color() function (a basecolor must now always be specified).

| __option__    | __description__ | __input__ 
| --- | --- | --- 
| basecolor | the human-like name of a color. Always required, but can also be set to 'random'. | string
| *intensity | how strong the color should be. Must be a float between 0 and 1, or set to 'random' (by default uses the 'strong' style values, see 'style' below). | float between 0 and 1
| *brightness | how light or dark the color should be. Must be a float between 0 and 1 , or set to 'random' (by default uses the 'strong' style values, see 'style' below). | float between 0 and 1
| *style | a named style that overrides the brightness and intensity options (optional). | For valid style names, see below.

Valid style names are:

- 'strong'
- 'dark'
- 'matte'
- 'bright'
- 'pastelle'

### geovis.Layer(...) --> class object
Creates and returns a thematic layer instance (a visual representation of a geographic file) that can be symbolized and used to add to a map.

| __option__ | __description__ 
| --- | --- 
| filepath | the path string of the geographic file to add, including the file extension.
| **customoptions | any series of named arguments of how to style the shapefile visualization (optional). Valid arguments are: fillcolor, fillsize (determines the circle size for point shapefiles, line width for line shapefiles, and has no effect for polygon shapefiles), outlinecolor, outlinewidth. For more info see the special section on how to stylize a layer. 

  - #### .AddClassification(...):
  Adds a classification/instruction to the layer on how to symbolize a particular symbol part (e.g. fillcolor) based on a shapefile's attribute values.
  
  | __option__ | __description__ | __input__ 
  | --- | --- | --- 
  | symboltype | a string indicating which type of symbol the classification should apply to. | any of: "fillsize", "fillwidth", "fillheight", "fillcolor", "outlinewidth", "outlinecolor"
  | valuefield | a string with the name of a shapefile attribute field whose values will be used to inform the classification. | string
  | symbolrange | a list or tuple of the range of symbol values that should be used for the symbol type being classified. You only need to assign the edge/breakpoints in an imaginary gradient of symbol values representing the transition from low to high value classes; the values in between will be interpolated if needed. The symbol values must be floats or integers when classifying a size-based symbol type, or hex color strings when classifying a color-based symbol type. | list or tuple
  | classifytype | a string with the name of the mathematical algorithm used to calculate the break points that separate the classes in the attribute values. | For valid classification type names see list below 
  | nrclasses | an integer or float for how many classes to subdivide the data and symbol values into. | Integer or float  
  
  Valid names for the classifytype option are:  
  
  - __"categorical"__  
    Assigns a unique class/symbol color to each unique attribute value, so can only be used when classifying color-based symbol types
  - __"equal classes"__  
    Makes sure that there are equally many features in each class, which means that features with the same attribute values can be found in multiple classes
  - __"equal interval"__  
    Classes are calculated so that each class only contains features that fall within a value range that is equally large for all classes
  - __"natural breaks"__  
    The Fisher-Jenks natural breaks algorithm, adapted from the Python implementation by Daniel J. Lewis (http://danieljlewis.org/files/2010/06/Jenks.pdf), is used to find 'natural' breaks in the shapefile dataset, i.e. where the value range within each class is as similar as possible and where the classes are as different as possible from each other. This algorithm is notorious for being slow for large datasets, so for datasets larger than 1000 records the calculation will be limited to a random sample of 1000 records (thanks to Carston Farmer for that idea, see: http://www.carsonfarmer.com/2010/09/adding-a-bit-of-classification-to-qgis/), and in addition that calculation will be performed 6 times, with the final break points being the sample mean of all the calculations. For large datasets this means that the natural breaks algorithm and the resultant map classification may turn out differently each time; however, the results should be somewhat consistent especially due to the random nature of the approach and the multiple sample means

### geovis.NewMap(...) --> class object
Creates and returns a new map based on previously defined mapsettings.

*Takes no arguments*

  - #### .AddLegend(...):
  Draws a basic legend for a given layer.
  
  | __option__ | __description__ 
  | --- | --- 
  | layer | the layer instance whose legend you wish to add to the map
  | upperleft | the upperleft corner of the legend as a list or tuple of the relative x and y position, each a float between 0-1
  | bottomright | the bottomright corner of the legend as a list or tuple of the relative x and y position, each a float between 0-1
  | legendtitle | the title of the legend as a string, by default uses the filename of the underlying shapefile
  | boxcolor | the hex color of the rectangle box that contains the legend, set to None to not render the box, default is a lightgray.
  | boxoutlinecolor | the hex color of the outline of the rectangle box that contains the legend, set to None to not render the outline, default is black.
  | boxoutlinewidth | the thickness of the boxoutline color relative to the box size, so 0.10 is 10 percent of the box size

  - #### .AddShape(...):
  This adds an individual shape instead of an entire file.
  
  | __option__ | __description__ 
  | --- | --- 
  | shapeobj | a shape instance, currently it only works with the PyShpShape instances that are returned when looping through the geovis Shapefile instance
  | **customoptions | any number of named arguments to style the shape

  - #### .AddText(...):
  Writes text on the map.
  
  | __option__ | __description__ 
  | --- | --- 
  | relx | the relative x position of the text's centerpoint, a float between 0-1
  | rely | the relative y position of the text's centerpoint, a float between 0-1
  | text | the text to add to the map, as a string
  | **customoptions | any number of named arguments to style the text

  - #### .AddToMap(...):
  Add and render a layer instance to the map.
  
  | __option__ | __description__ 
  | --- | --- 
  | layer | the layer instance that you wish to add to the map

  - #### .DrawCircle(...):
  Draws a circle on the map.
  
  | __option__ | __description__ 
  | --- | --- 
  | relx | the relative x position of the circle's centerpoint, a float between 0-1
  | rely | the relative y position of the circle's centerpoint, a float between 0-1
  | **customoptions | any number of named arguments to style the line

  - #### .DrawLine(...):
  Draws a line on the map.
  
  | __option__ | __description__ 
  | --- | --- 
  | startpos | a list or tuple of the relative x and y position where the line should start, each a float between 0-1
  | stoppos | a list or tuple of the relative x and y position where the line should end, each a float between 0-1
  | **customoptions | any number of named arguments to style the line

  - #### .DrawRectangle(...):
  Draws a rectangle on the map.
  
  | __option__ | __description__ 
  | --- | --- 
  | upperleft | the upperleft corner of the rectangle as a list or tuple of the relative x and y position, each a float between 0-1
  | bottomright | the bottomright corner of the rectangle as a list or tuple of the relative x and y position, each a float between 0-1
  | **customoptions | any number of named arguments to style the rectangle

  - #### .SaveMap(...):
  Save the map to an image file.
  
  | __option__ | __description__ 
  | --- | --- 
  | savepath | the string path for where you wish to save the map image. Image type extension must be specified ('.png','.gif',...)

  - #### .ViewMap(...):
  View the created map embedded in a Tkinter window. Map image can be panned, but not zoomed. Offers a 'save image' button to allow to interactively save the image.
  
  *Takes no arguments*

### geovis.SaveShapefileImage(...):
Quick task to save a shapefile to an image.

| __option__    | __description__ 
| --- | --- 
| shapefilepath | the path string of the shapefile.
| savepath      | the path string of where to save the image, including the image type extension.
| **customoptions | any series of named arguments of how to style the shapefile visualization (optional). Valid arguments are: fillcolor, fillsize (determines the circle size for point shapefiles, line width for line shapefiles, and has no effect for polygon shapefiles), outlinecolor, outlinewidth.

### geovis.SetMapBackground(...):
Sets the mapbackground of the next map to be made. At startup the mapbackground is transparent (None).

| __option__ | __description__ 
| --- | --- 
| mapbackground | takes a hex color string, as can be created with the Color function. It can also be None for a transparent background (default).

### geovis.SetMapDimensions(...):
Sets the width and height of the next map image. At startup the width and height are set to the dimensions of the window screen.

| __option__ | __description__ 
| --- | --- 
| width | the pixel width of the final map image to be rendered, an integer.
| height | the pixel height of the final map image to be rendered, an integer.

### geovis.SetMapZoom(...):
Zooms the map to the given mapextents.

| __option__ | __description__ 
| --- | --- 
| x2x | a two-item list of the x-extents in longitude format, from the leftmost to the rightmost longitude, default is full extent [-180, 180]
| y2y | a two-item list of the y-extents in latitude format, from the bottommost to the topmost latitude, default is full extent [-90, 90]

### geovis.SetRenderingOptions(...):
Sets certain rendering options that apply to all visualizations or map images.

| __option__    | __description__
| --- | --- 
| *renderer | a string describing which Python module will be used for rendering. This means you need to have the specified module installed. Valid renderer values are 'aggdraw' (default), 'PIL', 'pycairo', 'tkinter'. Notes: If you have no renderers installed, then use Tkinter which comes with all Python installations, be aware that it is significantly slow, memory-limited, and cannot be used to save images. Currently PyCairo is not very well optimized, and is particularly slow to render line shapefiles. 
| *numpyspeed | specifies whether to use numpy to speed up shapefile reading and coordinate-to-pixel conversion. Must be True (default) or False.
| *reducevectors | specifies whether to reduce the number of vectors to be rendered. This can speed up rendering time, but may lower the quality of the rendered image, especially for line shapefiles. Must be True or False (default).

### geovis.Shapefile(...) --> class object
Opens and reads a shapefile. Supports looping through it to extract one PyShpShape instance at a time. Using it with a print() function passes the filename, and measuring its len() returns the number of rows.

| __options__ | __description__ 
| --- | --- 
| shapefilepath | the filepath of the shapefile, including the .shp extension
| showprogress | True if wanting to display a progressbar while looping through the shapefile (default), otherwise False (default)
| progresstext | a textstring to print alongside the progressbar to help identify why it is being looped

  - #### .ClearSelection(...):
  Clears the current selection so that all shapes will be looped

  - #### .InvertSelection(...):
  Inverts the current selection

  - #### .SelectByQuery(...):
  Make a query selection on the shapefile so that only those features where the query evaluates to True are returned.
  
  | __option__    | __description__ 
  | --- | --- 
  | query | a string containing Python-like syntax (required). Feature values for fieldnames can be grabbed by specifying the fieldname as if it were a variable (case-sensitive). Note that evaluating string expressions is currently case-sensitive, which becomes particularly unintuitive for less-than/more-than alphabetic queries.
  | *inverted | a boolean specifying whether to invert the selection (default is False).

### geovis.ShapefileFolder(...):
A generator that will loop through a folder and all its subfolder and return information of every shapefile it finds. Information returned is a tuple with the following elements (string name of current subfolder, string name of shapefile found, string of the shapefile's file extension(will always be '.shp'))

| __option__ | __description__ 
| --- | --- 
| folder | a path string of the folder to check for shapefiles.

### geovis.ViewShapefile(...):
Quick task to visualize a shapefile and show it in a Tkinter window.

| __option__    | __description__ 
| --- | --- 
| shapefilepath | the path string of the shapefile.
| **customoptions | any series of named arguments of how to style the shapefile visualization (optional). Valid arguments are: fillcolor, fillsize (determines the circle size for point shapefiles, line width for line shapefiles, and has no effect for polygon shapefiles), outlinecolor, outlinewidth.

