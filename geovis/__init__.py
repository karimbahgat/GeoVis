"""
Python Geographic Visualizer (GeoVis)

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

"""

# IMPORTS
#builtins
import sys, os, itertools, array, random, math, platform, operator
import threading, Queue, multiprocessing
import Tkinter as tk
import tkFileDialog, tkColorChooser
#customized
import messages, listy, guihelper
#third party modules
import shapefile_fork as pyshp
import colour

# GLOBAL VARS
OSSYSTEM = platform.system().lower()
#PyShp shapetype constants
NULL = 0
POINT = 1
POLYLINE = 3
POLYGON = 5
MULTIPOINT = 8
POINTZ = 11
POLYLINEZ = 13
POLYGONZ = 15
MULTIPOINTZ = 18
POINTM = 21
POLYLINEM = 23
POLYGONM = 25
MULTIPOINTM = 28
MULTIPATCH = 31
#PyShp shapetypes as text
PYSHPTYPE_AS_TEXT = {\
    NULL:"Null",
    POINT:"Point",
    POINTZ:"PointZ",
    POINTM:"PointM",
    POLYLINE:"PolyLine",
    POLYLINEZ:"PolyLineZ",
    POLYLINEM:"PolyLineM",
    POLYGON:"Polygon",
    POLYGONZ:"PolygonZ",
    POLYGONM:"PolygonM",
    MULTIPOINT:"MultiPoint",
    MULTIPOINTZ:"MultiPointZ",
    MULTIPOINTM:"MultiPointM",
    MULTIPATCH:"MultiPatch"}
#default rendering options
try:
    import numpy
    NUMPYSPEED = True
except:
    NUMPYSPEED = False
REDUCEVECTORS = False
SHOWPROGRESS = True
#some map stuff
MAPBACKGROUND = None
try:
    import aggdraw
    RENDERER = "aggdraw"
except:
    try:
        import PIL
        RENDERER = "PIL"
    except:
        try:
            import cairo
            RENDERER = "pycairo"
        except:
            RENDERER = "tkinter"
#setup coordinate system (this can be done by user too, see SetMapZoom function towards the bottom)
PROJ_XYRATIO = 2.0
XMIN,XMAX = (-180,180)
YMIN,YMAX = (-90,90)
x2x = (XMIN,XMAX)
y2y = (YMIN,YMAX)
nw = (-1*min(x2x),max(y2y)) #northwest corner of zoomextent
XWIDTH = x2x[1]-x2x[0]
YHEIGHT = y2y[1]-y2y[0]
XOFFSET = nw[0]
YOFFSET = nw[1]
#set mapdims to window size
mapdimstest = tk.Tk()
width = int(mapdimstest.winfo_screenwidth())
height = int(mapdimstest.winfo_screenheight())
if width/float(height) < PROJ_XYRATIO:
    #snap to world ratio in case screenratio is different
    height = width/PROJ_XYRATIO
MAPWIDTH = width
MAPHEIGHT = height
mapdimstest.destroy()
del mapdimstest
#update mapdims
def _UpdateMapDims():
    if NUMPYSPEED:
        global ZOOMDIM, OFFSET, TRANSLATION, RENDERAREA, SCALING        
        ZOOMDIM = numpy.array([XWIDTH,YHEIGHT])
        OFFSET = numpy.array([0.0,0.0])*-1 #move x or y by normal +- coordinates (not compat with zoom yet
        TRANSLATION = numpy.array([XOFFSET, -YOFFSET]) + OFFSET
        RENDERAREA = numpy.array([MAPWIDTH, -MAPWIDTH/PROJ_XYRATIO])
        SCALING = RENDERAREA / ZOOMDIM
    else:
        #?? evrything is done with set zoom...?
        pass
_UpdateMapDims()
#define colorstyles
COLORSTYLES = dict([("strong", dict( [("intensity",1), ("brightness",0.5)]) ),
                    ("dark", dict( [("intensity",0.8), ("brightness",0.2)]) ),
                    ("matte", dict( [("intensity",0.4), ("brightness",0.2)]) ),
                ("bright", dict( [("intensity",0.8), ("brightness",0.7)] ) ),
                    ("weak", dict( [("intensity",0.3), ("brightness",0.5)] ) ),
                ("pastelle", dict( [("intensity",0.5), ("brightness",0.6)] ) )
                    ])


# INTERNAL CLASSES
class _PyShpShape:
    def __init__(self, shapefile, fieldnames, uniqid, coords, shapetype, bbox=None):
        """
every shapetype is always multi (upon entry) so have to be looped through when retrieved.
"""
        self._shapefile = shapefile
        self.fieldnames = fieldnames
        self.id = uniqid
        self.coords = coords
        #print coords
        if not bbox:
            #this is only needed for single points
            x,y = coords[0][0]
            bbox = [x,y,x,y]
        self.bbox = bbox
        self.type = shapetype
    def to_tkinter(self):
        convertedcoords = (self._MapCoords(eachmulti) for eachmulti in self.coords)
        formattedcoords = convertedcoords
        return (eachmulti for eachmulti in formattedcoords)
    def to_PIL(self):
        convertedcoords = (self._MapCoords(eachmulti) for eachmulti in self.coords)
        formattedcoords = convertedcoords
        return (array.array("f",eachmulti) for eachmulti in formattedcoords)
    def to_aggdraw(self):
        convertedcoords = (self._MapCoords(eachmulti) for eachmulti in self.coords)
        formattedcoords = convertedcoords
        return (array.array("f",eachmulti) for eachmulti in formattedcoords)
    def to_pycairo(self):
        convertedcoords = (self._MapCoords(eachmulti) for eachmulti in self.coords)
        formattedcoords = (self.__pairwise(eachmulti) for eachmulti in convertedcoords)
        return (eachmulti for eachmulti in formattedcoords)
    def GetAttributes(self, fieldname=None):
        if fieldname:
            rowdict = dict(zip(self.fieldnames, self._shapefile.record(self.id)))
            fieldvalue = rowdict[fieldname]
            return fieldvalue
        else:
            entirerow = self._shapefile.record(self.id)
            return entirerow
    def GetAvgCenter(self):
        """
so far only simple nonnumpy
"""
        if "point" in self.type:
            xs,ys = itertools.izip(*self.coords)
            avgx = sum(xs)/float(len(xs))
            avgy = sum(ys)/float(len(ys))
        else:
            x1,y1,x2,y2 = self.bbox
            avgx = (x1+x2)/2.0
            avgy = (y1+y2)/2.0
        avgcenter = [(avgx,avgy)]
        avgcenter = self._MapCoords(avgcenter)
        return avgcenter
    def GetMultiCenters(self):
        """
so far only simple nonnumpy
"""
        for single in self.coords:
            xs = [xy[0] for xy in single]
            xmid = sum(xs)/float(len(xs))
            xmid = self._MapCoords(xmid)
            ys = [xy[1] for xy in single]
            ymid = sum(ys)/float(len(ys))
            ymid = self._MapCoords(ymid)
            yield (xmid,ymid)
    #internal use only
    def __pairwise(self, coords, batchsize=2):
        """
only used when sending coordinates to pycairo, bc can only draw as a path one xy point at a time
"""
        return [pair for pair in itertools.izip(*[iter(coords)] * batchsize)]
    def _MapCoords(self, incoords):
        """
takes single set of coords, not multicoords
"""
        if NUMPYSPEED:
            converted = (incoords + TRANSLATION) * SCALING
            #for smoother drawings comment out the rint and vstack commands below
            if REDUCEVECTORS:
                converted = numpy.rint(converted).astype(int)
                converted = numpy.vstack((converted[0], converted[1:][numpy.any(converted[1:]!=converted[:-1], axis=1)]))
            aslist = converted.flatten()
            return aslist
        else:
            outcoords = []
            previous = None
            for point in incoords:
                inx, iny = point
                newx = (XOFFSET+inx)/XWIDTH*MAPWIDTH
                newy = MAPHEIGHT-(YOFFSET+iny)/YHEIGHT*MAPHEIGHT
                if REDUCEVECTORS:
                    newpoint = (int(newx),int(newy))
                    if newpoint != previous:
                        outcoords.extend(newpoint)
                        previous = newpoint
                else:
                    newpoint = [newx,newy]
                    outcoords.extend(newpoint)
            return outcoords
        

class Shapefile:
    #builtins
    """
Opens and reads a shapefile. Supports looping through it to extract one PyShpShape instance at a time. Using it with a print() function passes the filename, and measuring its len() returns the number of rows.

| __options__ | __description__ 
| --- | --- 
| shapefilepath | the filepath of the shapefile, including the .shp extension
| showprogress | True if wanting to display a progressbar while looping through the shapefile (default), otherwise False (default)
| progresstext | a textstring to print alongside the progressbar to help identify why it is being looped
"""
    def __init__(self, shapefilepath=None, showprogress="not specified", progresstext="looping shapefile"):
        self.showprogress = showprogress
        self.progresstext = progresstext
        self.selection = False
        if shapefilepath:
            self.shapefile = pyshp.Reader(shapefilepath)
            name = ".".join(shapefilepath.split(".")[:-1])
            name = name.split("\\")[-1]
            self.filename = name
            self.fieldnames = [fieldinfo[0] for fieldinfo in self.shapefile.fields[1:]]
        else:
            self.shapefile = None
            self.filename = "empty_shapefile"
            self.fieldnames = []
            self.writer = pyshp.Writer()
    def __len__(self):
        self._UpdateShapefile()
        return self.shapefile.numRecords
    def __str__(self):
        return self.filename
    def __iter__(self):
        self._UpdateShapefile()
        #prepare progressreporting
        if self.showprogress == "not specified":
            if SHOWPROGRESS:
                shellreport = "progressbar"
            else:
                shellreport = None
        else:
            shellreport = self.showprogress
        SHAPEFILELOOP = messages.ProgressReport(self.shapefile.iterShapes(numpyspeed=NUMPYSPEED), text=self.progresstext+" "+self.filename, shellreport=shellreport, countmethod="manual", genlength=self.shapefile.numRecords)
        if NUMPYSPEED:
            #loop
            for shapeindex, shape in enumerate(SHAPEFILELOOP):
                SHAPEFILELOOP.Increment()
                if self.selection:
                    if shapeindex in self.selection:
                        pyshpshape = self._PrepShape(shapeindex, shape)
                        xmin,ymin,xmax,ymax = pyshpshape.bbox
                        if (xmin < XMAX and xmax > XMIN) or (ymin < YMAX and ymax > YMIN):
                            yield pyshpshape
                else:
                    pyshpshape = self._PrepShape(shapeindex, shape)
                    xmin,ymin,xmax,ymax = pyshpshape.bbox
                    if (xmin < XMAX and xmax > XMIN) or (ymin < YMAX and ymax > YMIN):
                        yield pyshpshape
        else:
            for shapeindex, shape in enumerate(SHAPEFILELOOP):
                SHAPEFILELOOP.Increment()
                if self.selection:
                    if shapeindex in self.selection:
                        pyshpshape = self._PrepShape(shapeindex, shape)
                        xmin,ymin,xmax,ymax = pyshpshape.bbox
                        if (xmin < XMAX and xmax > XMIN) or (ymin < YMAX and ymax > YMIN):
                            yield pyshpshape
                else:
                    pyshpshape = self._PrepShape(shapeindex, shape)
                    xmin,ymin,xmax,ymax = pyshpshape.bbox
                    if (xmin < XMAX and xmax > XMIN) or (ymin < YMAX and ymax > YMIN):
                        yield pyshpshape
    #BASICS
##    def SetFields(self, fieldnames):
##        self.fieldnames = fieldnames
##    def GetFeature(self, shapeindex):
##        self._UpdateShapefile()
##        shape = self.shapefile.shape(shapeindex, numpyspeed=NUMPYSPEED)
##        return self._PrepShape(shapeindex, shape)
##    def AddFeature(self, shape, record, shapetype=None):
##        #first process inshape somehow
##        #...
##        self.writer._shapes.append(shapeinput)
##        self.writer.records.append(attributes)
##    def ChangeFeature(self, shapeid=None, shape=None, recordid=None, record=None):
##        #first process inshape somehow
##        #...
##        if shapeid and shape:
##            self.writer._shapes[shapeid] = shape
##        if recordid and record:
##            self.writer.records[recordid] = attributes
    #USEFUL
##    def Save(self, savepath):
##        "work in progress..."
##        # create writer
##        shapewriter = pyshp.Writer()
##        shapewriter.autoBalance = 1
##        # add fields in correct fieldtype
##        self.progresstext = "checking fieldtypes for"
##        for fieldname in self.fieldnames:
##            if not fieldname.startswith(tuple(shapetable.invisiblefields)):
##                # write field
##                fieldinfo = self._ShapefileFieldInfo(shapetable, fieldname)
##                shapewriter.field(*fieldinfo)
##        self.progresstext = "saving"
##        for shape in self:
##            attributes = dict(zip(self.fieldnames, shape.GetAttributes()))
##        self.writer.save(savepath)
        ##
##        """shapefilename: shapefile to be saved, name given to shapefile when loaded into shapeholder, type str; savepath: path of where to save, type str, use double backslash"""
##        # create writer
##        shapewriter = shapefile.Writer()
##        shapewriter.autoBalance = 1
##        # add fields in correct fieldtype
##        shapetable = self.filenames[shapefilename].table
##        for fieldname in shapetable.fields:
##            if not fieldname.startswith(tuple(shapetable.invisiblefields)):
##                # write field
##                fieldinfo = self._ShapefileFieldInfo(shapetable, fieldname)
##                shapewriter.field(*fieldinfo)
##        # convert shapely shapetypes to shapefile points/parts format, and then match shapeid rows to each shape and write to output
##        origshapes = self.filenames[shapefilename].shapes
##        for eachshapeid in origshapes:
##            points, shapetype = self._ShapelyToShapeparts(origshapes[eachshapeid]["shape"])
##            shapewriter.poly(parts=points, shapeType=shapetype)
##            rowinfo = [encode(eachcell, strlen=250, floatlen=16, floatprec=6) for index, eachcell in enumerate(shapetable.FetchEntireRow(eachshapeid)) if not shapetable.fields[index].startswith(tuple(shapetable.invisiblefields))]
##            shapewriter.record(*rowinfo)
##        # save
##        shapewriter.save(savepath)
##        # finally copy prj file from original if exists
##        self._SaveProjection(shapefilename, savepath)
    def SelectByQuery(self, query, inverted=False):
        """
Make a query selection on the shapefile so that only those features where the query evaluates to True are returned.

| __option__    | __description__ 
| --- | --- 
| query | a string containing Python-like syntax (required). Feature values for fieldnames can be grabbed by specifying the fieldname as if it were a variable (case-sensitive). Note that evaluating string expressions is currently case-sensitive, which becomes particularly unintuitive for less-than/more-than alphabetic queries.
| *inverted | a boolean specifying whether to invert the selection (default is False).
"""
        self._UpdateShapefile()
        self.ClearSelection()
        self.progresstext = "making selection for"
        tempselection = []
        for shape in self:
            attributes = dict(zip(self.fieldnames, shape.GetAttributes()))
            #first make temp variables out of all fieldnames
            for field in self.fieldnames:
                value = attributes[field]
                if isinstance(value, basestring):
                    value = '"""'+str(value)+'"""'
                elif isinstance(value, (int,float)):
                    value = str(value)
                code = str(field)+" = "+value
                exec(code)
            #then run query
            queryresult = eval(query)
            if queryresult:
                tempselection.append(shape.id)
        self.selection = tempselection
        if inverted:
            self.InvertSelection()
        return self.selection
    def InvertSelection(self):
        """
Inverts the current selection
"""
        self.progresstext = "inverting selection for"
        oldselection = self.selection
        self.ClearSelection()
        tempselection = [shape.id for shape in self if shape.id not in oldselection]
        self.selection = tempselection
    def ClearSelection(self):
        """
Clears the current selection so that all shapes will be looped
"""
        self.selection = False
##    def SplitByAttribute(self, fieldname):
##        self._UpdateShapefile()
##        pass
    #
    #INTERNAL USE ONLY
    def _UpdateShapefile(self):
        #first check that a few essentials have been set...
        #...
        #then activate
        #self.shapefile = pyshp.Reader(self.writer)
        if self.filename == "empty_shapefile":
            #only do this first time done on a previously empty shapefile
            self.filename = "custom_shapefile"
            self.fieldnames = [fieldinfo[0] for fieldinfo in self.shapefile.fields[1:]]
    def _PrepShape(self, shapeindex, shape):
        if NUMPYSPEED:
            shapetype = PYSHPTYPE_AS_TEXT[shape.shapeType].lower()
            if "polygon" in shapetype:
                if not numpy.any(shape.parts):
                    nestedcoords = [shape.points]
                    return _PyShpShape(self.shapefile, self.fieldnames, shapeindex, nestedcoords, shapetype, bbox=shape.bbox)
                else:
                    coords = numpy.split(shape.points, shape.parts[1:])
                    return _PyShpShape(self.shapefile, self.fieldnames, shapeindex, coords, "polygon", bbox=shape.bbox)
            elif "line" in shapetype:
                if not numpy.any(shape.parts):
                    nestedcoords = [shape.points]
                    return _PyShpShape(self.shapefile, self.fieldnames, shapeindex, nestedcoords, shapetype, bbox=shape.bbox)
                else:
                    coords = numpy.split(shape.points, shape.parts[1:])
                    return _PyShpShape(self.shapefile, self.fieldnames, shapeindex, coords, "line", bbox=shape.bbox)
            elif "point" in shapetype:
                if "multi" in shapetype:
                    return _PyShpShape(self.shapefile, self.fieldnames, shapeindex, shape.points, "point", bbox=shape.bbox)
                else:
                    nestedcoords = [shape.points]
                    return _PyShpShape(self.shapefile, self.fieldnames, shapeindex, nestedcoords, "point")
        else:
            #first set new shapetype to pass on
            shapetype = PYSHPTYPE_AS_TEXT[shape.shapeType].lower()
            if "polygon" in shapetype:
                newshapetype = "polygon"
            if "line" in shapetype:
                newshapetype = "line"
            if "point" in shapetype:
                newshapetype = "point"
            #then serve up points universal for all shapetypes
            if "point" in shapetype:
                nestedcoords = [shape.points]
                return _PyShpShape(self.shapefile, self.fieldnames, shapeindex, nestedcoords, newshapetype)
            elif len(shape.parts) == 1:
                nestedcoords = [shape.points]
                return _PyShpShape(self.shapefile, self.fieldnames, shapeindex, nestedcoords, newshapetype)
            else:
                nestedcoords = []
                shapeparts = list(shape.parts)
                shapeparts.append(len(shape.points))
                startindex = shapeparts[0]
                for endindex in shapeparts[1:]:
                    eachmulti = shape.points[startindex:endindex]
                    nestedcoords.append(eachmulti)
                    startindex = endindex
                return _PyShpShape(self.shapefile, self.fieldnames, shapeindex, nestedcoords, newshapetype)


class _TkCanvas_Renderer:
    def __init__(self):
        global tkFont
        import tkFont
        self.fontnames = dict([("default", "Times"),
                       ("times new roman", "Times"),
                       ("courier", "Courier"),
                       ("helvetica","Helvetica") ])
    def NewImage(self):
        """
this must be called before doing any rendering.
Note: this replaces any previous image drawn on so be sure to
retrieve the old image before calling it again to avoid losing work
"""
        width = MAPWIDTH
        height = MAPHEIGHT
        background = MAPBACKGROUND
        self.img = None
        self.window = tk.Tk()
        self.window_frame = tk.Frame(self.window)
        self.window_frame.pack()
        screenwidth = self.window.winfo_screenwidth()
        if MAPWIDTH >= screenwidth:
            self.window.wm_state('zoomed')
        self.drawer = tk.Canvas(self.window_frame, width=width, height=height, bg="white")
        self.drawer.pack()
        #place the shadow
        if background:
            x0,y0,x1,y1 = ( -int(width/50.0), int(width/50.0), width-int(width/50.0), height+int(width/50.0) )
            self.drawer.create_rectangle(x0,y0,x1,y1, fill="Gray80", outline="")
        #place background
        x0,y0,x1,y1 = ( 0, 0, width, height )
        self.drawer.create_rectangle(x0,y0,x1,y1, fill=background, outline="")
        #make image pannable
        def mouseovermap(event):
            global mouseovermapvar
            self.window.config(cursor="fleur") #draft_large
            mouseovermapvar = True
        def mouseoutofmap(event):
            global mouseovermapvar
            self.window.config(cursor="")
            mouseovermapvar = False
        def activatedrag(event):
            global mouseclicked
            if mouseovermapvar == True:
                mouseclicked = True
        def deactivatedrag(event):
            global mouseclicked
            mouseclicked = False
        def mark(event):
            self.drawer.scan_mark(event.x, event.y)
        def dragto(event):
            try:
                if mouseclicked == True:
                    self.drawer.scan_dragto(event.x, event.y, 1)
            except:
                pass
        self.drawer.bind("<Enter>", mouseovermap, "+")
        self.drawer.bind("<Leave>", mouseoutofmap, "+")
        self.window.bind("<Button-1>", mark, "+")
        self.window.bind("<Motion>", dragto, "+")
        self.window.bind("<Button-1>", activatedrag, "+")
        self.window.bind("<ButtonRelease-1>", deactivatedrag, "+")
    def RenderText(self, relx, rely, text, options):
        if not options.get("texteffect"):
            self._BasicText(relx, rely, text, options)
    def RenderRectangle(self, upperleft, bottomright, customoptions):
        self.__FixHollowPolyError(customoptions)
        leftrelx, uprely = upperleft
        leftx,upy = (int(MAPWIDTH*leftrelx), int(MAPHEIGHT*uprely))
        rightrelx, downrely = bottomright
        rightx,downy = (int(MAPWIDTH*rightrelx), int(MAPHEIGHT*downrely))
        rectanglecoords = [leftx,upy, rightx,upy, rightx,downy, leftx,downy, leftx,upy]
        self._BasicPolygon(rectanglecoords, customoptions)
    def RenderCircle(self, relx, rely, fillsize, customoptions):
        customoptions["fillsize"] = fillsize
        x = int(MAPWIDTH*relx)
        y = int(MAPHEIGHT*rely)
        self._BasicCircle((x,y), customoptions)
    def RenderLine(self, startpos, stoppos, customoptions):
        startrelx, startrely = startpos
        startxy = [int(MAPWIDTH*startrelx), int(MAPHEIGHT*startrely)]
        stoprelx, stoprely = stoppos
        stopxy = [int(MAPWIDTH*stoprelx), int(MAPHEIGHT*stoprely)]
        linecoords = startxy
        linecoords.extend(stopxy)
        self._BasicLine(linecoords, customoptions)
    def RenderShape(self, shapeobj, options):
        """
looks at instructions in options to decide which draw method to use
"""
        self.__FixHollowPolyError(options)
        multishapes = shapeobj.to_tkinter()
        symbolizer = options.get("symbolizer")
        if shapeobj.type == "polygon":
            if symbolizer:
                if symbolizer == "circle":
                    coords = shapeobj.GetAvgCenter()
                    self._BasicCircle(coords, options)
                elif symbolizer == "square":
                    coords = shapeobj.GetAvgCenter()
                    self._BasicSquare(coords, options)
                elif symbolizer == "pyramid":
                    coords = shapeobj.GetAvgCenter()
                    self._Pyramid(coords, options)
            else:
                for coords in multishapes:
                    self._BasicPolygon(coords, options)
        elif shapeobj.type == "line":
            if symbolizer:
                if symbolizer == "circle":
                    coords = shapeobj.GetAvgCenter()
                    self._BasicCircle(coords, options)
                elif symbolizer == "square":
                    coords = shapeobj.GetAvgCenter()
                    self._BasicSquare(coords, options)
                elif symbolizer == "pyramid":
                    coords = shapeobj.GetAvgCenter()
                    self._Pyramid(coords, options)
            else:
                for coords in multishapes:
                    self._BasicLine(coords, options)
        elif shapeobj.type == "point":
            if symbolizer:
                if symbolizer == "circle":
                    for coords in multishapes:
                        self._BasicCircle(coords, options)
                elif symbolizer == "square":
                    for coords in multishapes:
                        self._BasicSquare(coords, options)
                elif symbolizer == "pyramid":
                    for coords in multishapes:
                        self._Pyramid(coords, options)
            else:
                for coords in multishapes:
                    self._BasicCircle(coords, options)
    def RunTk(self):
        self.drawer.create_rectangle(0,0,MAPWIDTH,MAPHEIGHT, fill="", outline=Color("black")) #this is the map outline edge
        self.window.mainloop()

    #Internal use only
    def __FixHollowPolyError(self, options):
        if not options.get("fillcolor"):
            options["fillcolor"] = ""
        if not options.get("outlinecolor"):
            options["outlinecolor"] = ""
    def _BasicText(self, relx, rely, text, options):
        """
draws basic text, no effects
"""
        font = tkFont.Font(family=self.fontnames[options["textfont"]], size=options["textsize"])
        fontwidth, fontheight = (font.measure(text), font.metrics("ascent"))
        textanchor = options.get("textanchor")
        if textanchor:
            textanchor = textanchor.lower()
            if textanchor == "center":
                x = int(MAPWIDTH*relx) - int(fontwidth/2.0)
                y = int(MAPHEIGHT*rely) - int(fontheight/2.0)
            else:
                x = int(MAPWIDTH*relx) - int(fontwidth/2.0)
                y = int(MAPHEIGHT*rely) - int(fontheight/2.0)
                if "n" in textanchor:
                    y = int(MAPHEIGHT*rely)
                elif "s" in textanchor:
                    y = int(MAPHEIGHT*rely) - int(fontheight)
                if "e" in textanchor:
                    x = int(MAPWIDTH*relx) - int(fontwidth)
                elif "w" in textanchor:
                    x = int(MAPWIDTH*relx)
        if options.get("textboxfillcolor") or options.get("textboxoutlinecolor"):
            relfontwidth, relfontheight = (fontwidth/float(MAPWIDTH), fontheight/float(MAPHEIGHT))
            relxmid,relymid = (x/float(MAPWIDTH)+relfontwidth/2.0,y/float(MAPHEIGHT)+relfontheight/2.0)
            relupperleft = (relxmid-relfontwidth*options["textboxfillsize"]/2.0, relymid-relfontheight*options["textboxfillsize"]/2.0)
            relbottomright = (relxmid+relfontwidth*options["textboxfillsize"]/2.0, relymid+relfontheight*options["textboxfillsize"]/2.0)
            options["fillcolor"] = options["textboxfillcolor"]
            options["outlinecolor"] = options["textboxoutlinecolor"]
            options["outlinewidth"] = options["textboxoutlinewidth"]
            self.RenderRectangle(relupperleft, relbottomright, options)       
        self.drawer.create_text((x,y), text=text, font=font, fill=options["textcolor"], anchor="nw")
    def _BasicLine(self, coords, options):
        """
draw basic lines with outline, but nothing at start and end
"""
        if len(coords) < 4:
            return
        #first draw outline line
        if options["outlinecolor"]:
            self.drawer.create_line(*coords, fill=options.get("outlinecolor"), width=int(options.get("fillsize")+(options.get("outlinewidth")*2)))
        #then draw fill line which is thinner
        self.drawer.create_line(*coords, fill=options.get("fillcolor"), width=int(options.get("fillsize")))
    def _BasicPolygon(self, coords, options):
        """
draw polygon with color fill
"""
        if len(coords) > 6:
            self.drawer.create_polygon(*coords, fill=options["fillcolor"], outline=options["outlinecolor"])
    def _BasicCircle(self, coords, options):
        """
draw points with a symbol path representing a circle
"""
        size = int(options["fillsize"]/2.0)
        x,y = coords
        circlecoords = (x-size, y-size, x+size, y+size)
        self.drawer.create_oval(circlecoords, fill=options["fillcolor"], outline=options["outlinecolor"])
    def _BasicSquare(self, coords, options):
        """
draw points with a symbol path representing a square
"""
        #build circle
        size = int(options["fillsize"]/2.0)
        x,y = coords
        squarecoords = [x-size,y-size, x+size,y-size, x+size,y+size, x-size,y+size, x-size,y-size]
        #draw
        self.drawer.create_polygon(*squarecoords, fill=options["fillcolor"], outline=options["outlinecolor"])
    def _Pyramid(self, coords, options):
        """
draw basic lines with outline, but nothing at start and end
"""
        size = int(options["fillsize"])
        width = int(options["fillwidth"]) #pxls
        #calculate three pyramid coords
        x,y = coords
        leftbase = [x-int(width/2.0), y]
        peak = [x, y-size]
        rightbase = [x+int(width/2.0), y]
        #first draw left line
        leftlinecoords = list(leftbase)
        leftlinecoords.extend(peak)
        self.drawer.create_line(*leftlinecoords, fill=options["outlinecolor"], width=options["outlinewidth"])
        #then draw right line
        rightlinecoords = list(rightbase)
        rightlinecoords.extend(peak)
        self.drawer.create_line(*rightlinecoords, fill=options["outlinecolor"], width=options["outlinewidth"])

class _PIL_Renderer:
    """
this class can be called on to draw each feature with PIL as long as
it is given instructions via a color/size/options dictionary
"""
    #NEED TO RECEIVE GENERATOR OF TRANSFORMED COORDS FROM MAPCANVAS
    #ALSO NEEDS THE Aggdraw.Draw(img) OBJECT
    def __init__(self):
        global PIL
        import PIL, PIL.Image, PIL.ImageDraw, PIL.ImageTk, PIL.ImageFont
        self.upscaled = False
        self.sysfontfolders = dict([("windows","C:/Windows/Fonts/")])
        self.fontfilenames = dict([("default", "TIMES.TTF"),
                                   ("times new roman","TIMES.TTF"),
                                   ("arial","ARIAL.TTF")])
    def NewImage(self):
        """
this must be called before doing any rendering.
Note: this replaces any previous image drawn on so be sure to
retrieve the old image before calling it again to avoid losing work
"""
        #first mode
        mode = "RGBA"
        #then other specs
        if not self.upscaled:
            global MAPWIDTH, MAPHEIGHT
            MAPWIDTH = MAPWIDTH*2
            MAPHEIGHT = MAPHEIGHT*2
            _UpdateMapDims()
            self.upscaled = True
        width = MAPWIDTH
        height = MAPHEIGHT
        background = MAPBACKGROUND
        dimensions = (width, height)
        self.img = PIL.Image.new(mode, dimensions, background)
        self.drawer = PIL.ImageDraw.Draw(self.img)
    def RenderText(self, relx, rely, text, options):
        options = options.copy()
        options["textsize"] = options["textsize"]*2
        if not options.get("texteffect"):
            self._BasicText(relx, rely, text, options)
    def RenderRectangle(self, upperleft, bottomright, customoptions):
        leftrelx, uprely = upperleft
        leftx,upy = (int(MAPWIDTH*leftrelx), int(MAPHEIGHT*uprely))
        rightrelx, downrely = bottomright
        rightx,downy = (int(MAPWIDTH*rightrelx), int(MAPHEIGHT*downrely))
        rectanglecoords = [leftx,upy, rightx,upy, rightx,downy, leftx,downy, leftx,upy]
        self._BasicPolygon(rectanglecoords, customoptions)
    def RenderCircle(self, relx, rely, fillsize, customoptions):
        customoptions["fillsize"] = fillsize
        x = int(MAPWIDTH*relx)
        y = int(MAPHEIGHT*rely)
        self._BasicCircle((x,y), customoptions)
    def RenderLine(self, startpos, stoppos, customoptions):
        startrelx, startrely = startpos
        startxy = [int(MAPWIDTH*startrelx), int(MAPHEIGHT*startrely)]
        stoprelx, stoprely = stoppos
        stopxy = [int(MAPWIDTH*stoprelx), int(MAPHEIGHT*stoprely)]
        linecoords = startxy
        linecoords.extend(stopxy)
        self._BasicLine(linecoords, customoptions)
    def RenderShape(self, shapeobj, options):
        """
looks at instructions in options to decide which draw method to use
"""
        #possibly use an options filterer here to enure all needed options
        #are given, otherwise snap to default
        #............
        multishapes = shapeobj.to_PIL()
        symbolizer = options.get("symbolizer")
        if shapeobj.type == "polygon":
            if symbolizer:
                if symbolizer == "circle":
                    coords = shapeobj.GetAvgCenter()
                    self._BasicCircle(coords, options)
                elif symbolizer == "square":
                    coords = shapeobj.GetAvgCenter()
                    self._BasicSquare(coords, options)
                elif symbolizer == "pyramid":
                    coords = shapeobj.GetAvgCenter()
                    self._Pyramid(coords, options)
            else:
                for coords in multishapes:
                    self._BasicPolygon(coords, options)
        elif shapeobj.type == "line":
            if symbolizer:
                if symbolizer == "circle":
                    coords = shapeobj.GetAvgCenter()
                    self._BasicCircle(coords, options)
                elif symbolizer == "square":
                    coords = shapeobj.GetAvgCenter()
                    self._BasicSquare(coords, options)
                elif symbolizer == "pyramid":
                    coords = shapeobj.GetAvgCenter()
                    self._Pyramid(coords, options)
            else:
                for coords in multishapes:
                    self._BasicLine(coords, options)
        elif shapeobj.type == "point":
            if symbolizer:
                if symbolizer == "circle":
                    for coords in multishapes:
                        self._BasicCircle(coords, options)
                elif symbolizer == "square":
                    for coords in multishapes:
                        self._BasicSquare(coords, options)
                elif symbolizer == "pyramid":
                    for coords in multishapes:
                        self._Pyramid(coords, options)
            else:
                for coords in multishapes:
                    self._BasicCircle(coords, options)
    def GetImage(self):
        if self.upscaled:
            global MAPWIDTH, MAPHEIGHT
            MAPWIDTH = int(round(MAPWIDTH/2.0))
            MAPHEIGHT = int(round(MAPHEIGHT/2.0))
            _UpdateMapDims()
            width,height = self.img.size
            self.img = self.img.resize((int(round(width/2.0)),int(round(height/2.0))), PIL.Image.ANTIALIAS)
            self.upscaled = False
        return PIL.ImageTk.PhotoImage(self.img)
    def SaveImage(self, savepath):
        if self.upscaled:
            global MAPWIDTH, MAPHEIGHT
            MAPWIDTH = int(round(MAPWIDTH/2.0))
            MAPHEIGHT = int(round(MAPHEIGHT/2.0))
            _UpdateMapDims()
            width,height = self.img.size
            self.img = self.img.resize((int(round(width/2.0)),int(round(height/2.0))), PIL.Image.ANTIALIAS)
            self.upscaled = False
        self.img.save(savepath)

    #Internal use only
    def __DoubleSizeOptions(self, options):
        """
NO LONGER USED BC SIZE VALUES WERE CHANGED TO PERCENTAGES INSTEAD OF ACTUAL PIXELS. ORIGINAL DESCRIPTION: doubles and returns all size related options, since PIL draws on a 2x larger image so that it can be reduced to normal size using Antialias later.
"""
        #remove soon...
        options = options.copy()
        options["fillsize"] = options["fillsize"]*2
        options["outlinewidth"] = options["outlinewidth"]*2
        options["fillwidth"] = options["fillwidth"]*2
        options["fillheight"] = options["fillheight"]*2
        return options
    def _BasicText(self, relx, rely, text, options):
        """
draws basic text, no effects
"""
        fontlocation = self.sysfontfolders[OSSYSTEM]+self.fontfilenames[options["textfont"]]
        font = PIL.ImageFont.truetype(fontlocation, size=options["textsize"])
        fontwidth, fontheight = self.drawer.textsize(text, font)
        textanchor = options.get("textanchor")
        if textanchor:
            textanchor = textanchor.lower()
            if textanchor == "center":
                x = int(MAPWIDTH*relx) - int(fontwidth/2.0)
                y = int(MAPHEIGHT*rely) - int(fontheight/2.0)
            else:
                x = int(MAPWIDTH*relx) - int(fontwidth/2.0)
                y = int(MAPHEIGHT*rely) - int(fontheight/2.0)
                if "n" in textanchor:
                    y = int(MAPHEIGHT*rely)
                elif "s" in textanchor:
                    y = int(MAPHEIGHT*rely) - int(fontheight)
                if "e" in textanchor:
                    x = int(MAPWIDTH*relx) - int(fontwidth)
                elif "w" in textanchor:
                    x = int(MAPWIDTH*relx)
        if options.get("textboxfillcolor") or options.get("textboxoutlinecolor"):
            relfontwidth, relfontheight = (fontwidth/float(MAPWIDTH), fontheight/float(MAPHEIGHT))
            relxmid,relymid = (x/float(MAPWIDTH)+relfontwidth/2.0,y/float(MAPHEIGHT)+relfontheight/2.0)
            relupperleft = (relxmid-relfontwidth*options["textboxfillsize"]/2.0, relymid-relfontheight*options["textboxfillsize"]/2.0)
            relbottomright = (relxmid+relfontwidth*options["textboxfillsize"]/2.0, relymid+relfontheight*options["textboxfillsize"]/2.0)
            options["fillcolor"] = options["textboxfillcolor"]
            options["outlinecolor"] = options["textboxoutlinecolor"]
            options["outlinewidth"] = options["textboxoutlinewidth"]
            self.RenderRectangle(relupperleft, relbottomright, options)
        self.drawer.text((x,y), text=text, font=font, fill=options["textcolor"])
    def _BasicLine(self, coords, options):
        """
draw basic lines with outline, but nothing at start and end
"""
        #first draw outline line
        if options["outlinecolor"]:
            self.drawer.line(coords, fill=options.get("outlinecolor"), width=int(options.get("fillsize")+(options.get("outlinewidth")*2)))
        #then draw fill line which is thinner
        self.drawer.line(coords, fill=options.get("fillcolor"), width=int(options.get("fillsize")))
    def _BasicPolygon(self, coords, options):
        """
draw polygon with color fill
"""
        if len(coords) > 6:
            self.drawer.polygon(coords, fill=options["fillcolor"], outline=options["outlinecolor"])
    def _BasicCircle(self, coords, options):
        """
draw points with a symbol path representing a circle
"""
        size = int(options["fillsize"]/2.0)
        x,y = coords
        circlecoords = (x-size, y-size, x+size, y+size)
        self.drawer.ellipse(circlecoords, fill=options["fillcolor"], outline=options["outlinecolor"])
    def _BasicSquare(self, coords, options):
        """
draw points with a symbol path representing a square
"""
        #build circle
        size = int(options["fillsize"]/2.0)
        x,y = coords
        squarecoords = (x-size, y-size, x+size, y+size)
        #draw
        self.drawer.rectangle(squarecoords, fill=options["fillcolor"], outline=options["outlinecolor"])
    def _Pyramid(self, coords, options):
        """
draw basic lines with outline, but nothing at start and end
"""
        size = int(options["fillsize"])
        width = int(options["fillwidth"]) #pxls
        #calculate three pyramid coords
        x,y = coords
        leftbase = [x-int(width/2.0), y]
        peak = [x, y-size]
        rightbase = [x+int(width/2.0), y]
        #first draw left line
        leftlinecoords = list(leftbase)
        leftlinecoords.extend(peak)
        self.drawer.line(leftlinecoords, fill=options["outlinecolor"], width=options["outlinewidth"])
        #then draw right line
        rightlinecoords = list(rightbase)
        rightlinecoords.extend(peak)
        self.drawer.line(rightlinecoords, fill=options["outlinecolor"], width=options["outlinewidth"])

class _Aggdraw_Renderer:
    """
this class can be called on to draw each feature with aggdraw as long as 
it is given instructions via a color/size/options dictionary
"""
    #NEED TO RECEIVE GENERATOR OF TRANSFORMED COORDS FROM MAPCANVAS
    #ALSO NEEDS THE Aggdraw.Draw(img) OBJECT
    def __init__(self):
        global aggdraw, PIL
        import aggdraw, PIL, PIL.Image, PIL.ImageDraw, PIL.ImageTk
        self.sysfontfolders = dict([("windows","C:/Windows/Fonts/")])
        self.fontfilenames = dict([("default", "TIMES.TTF"),
                                   ("times new roman","TIMES.TTF"),
                                   ("arial","ARIAL.TTF")])
    def NewImage(self):
        """
this must be called before doing any rendering.
Note: this replaces any previous image drawn on so be sure to
retrieve the old image before calling it again to avoid losing work
"""
        #first mode
        mode = "RGBA"
        #then other specs
        width = MAPWIDTH
        height = MAPHEIGHT
        background = MAPBACKGROUND
        dimensions = (width, height)
        self.img = PIL.Image.new(mode, dimensions, background)
        self.drawer = aggdraw.Draw(self.img)
    def RenderShape(self, shapeobj, options):
        """
looks at instructions in options to decide which draw method to use
"""
        multishapes = shapeobj.to_aggdraw()
        symbolizer = options.get("symbolizer")
        if shapeobj.type == "polygon":
            if symbolizer:
                if symbolizer == "circle":
                    centercoords = shapeobj.GetAvgCenter()
                    self._BasicCircle(centercoords, options)
                elif symbolizer == "square":
                    centercoords = shapeobj.GetAvgCenter()
                    self._BasicSquare(centercoords, options)
                elif symbolizer == "pyramid":
                    centercoords = shapeobj.GetAvgCenter()
                    self._Pyramid(centercoords, options)
            else:
                for coords in multishapes:
                    self._BasicPolygon(coords, options)
        elif shapeobj.type == "line":
            if symbolizer:
                if symbolizer == "circle":
                    centercoords = shapeobj.GetAvgCenter()
                    self._BasicCircle(centercoords, options)
                elif symbolizer == "square":
                    centercoords = shapeobj.GetAvgCenter()
                    self._BasicSquare(centercoords, options)
                elif symbolizer == "pyramid":
                    centercoords = shapeobj.GetAvgCenter()
                    self._Pyramid(centercoords, options)
            else:
                for coords in multishapes:
                    self._BasicLine(coords, options)
        elif shapeobj.type == "point":
            if symbolizer:
                if symbolizer == "circle":
                    for coords in multishapes:
                        self._BasicCircle(coords, options)
                elif symbolizer == "square":
                    for coords in multishapes:
                        self._BasicSquare(coords, options)
                elif symbolizer == "pyramid":
                    for coords in multishapes:
                        self._Pyramid(coords, options)
            else:
                for coords in multishapes:
                    self._BasicCircle(coords, options)
    def RenderText(self, relx, rely, text, options):
        if not options.get("texteffect"):
            self._BasicText(relx, rely, text, options)
    def RenderRectangle(self, upperleft, bottomright, customoptions):
        leftrelx, uprely = upperleft
        leftx,upy = (int(MAPWIDTH*leftrelx), int(MAPHEIGHT*uprely))
        rightrelx, downrely = bottomright
        rightx,downy = (int(MAPWIDTH*rightrelx), int(MAPHEIGHT*downrely))
        rectanglecoords = [leftx,upy, rightx,upy, rightx,downy, leftx,downy, leftx,upy]
        self._BasicPolygon(rectanglecoords, customoptions)
    def RenderCircle(self, relx, rely, fillsize, customoptions):
        customoptions["fillsize"] = fillsize
        x = int(MAPWIDTH*relx)
        y = int(MAPHEIGHT*rely)
        self._BasicCircle((x,y), customoptions)
    def RenderLine(self, startpos, stoppos, customoptions):
        startrelx, startrely = startpos
        startxy = [int(MAPWIDTH*startrelx), int(MAPHEIGHT*startrely)]
        stoprelx, stoprely = stoppos
        stopxy = [int(MAPWIDTH*stoprelx), int(MAPHEIGHT*stoprely)]
        linecoords = startxy
        linecoords.extend(stopxy)
        self._BasicLine(linecoords, customoptions)
    def GetImage(self):
        self.drawer.flush()
        return PIL.ImageTk.PhotoImage(self.img)
    def SaveImage(self, savepath):
        self.drawer.flush()
        self.img.save(savepath)

    #Internal use only
    def _BasicText(self, relx, rely, text, options):
        """
draws basic text, no effects
"""
        fontlocation = self.sysfontfolders[OSSYSTEM]+self.fontfilenames[options["textfont"]]
        font = aggdraw.Font(color=options["textcolor"], file=fontlocation, size=options["textsize"], opacity=options["textopacity"])
        fontwidth, fontheight = self.drawer.textsize(text, font)
        textanchor = options.get("textanchor")
        if textanchor:
            textanchor = textanchor.lower()
            if textanchor == "center":
                x = int(MAPWIDTH*relx) - int(fontwidth/2.0)
                y = int(MAPHEIGHT*rely) - int(fontheight/2.0)
            else:
                x = int(MAPWIDTH*relx) - int(fontwidth/2.0)
                y = int(MAPHEIGHT*rely) - int(fontheight/2.0)
                if "n" in textanchor:
                    y = int(MAPHEIGHT*rely)
                elif "s" in textanchor:
                    y = int(MAPHEIGHT*rely) - int(fontheight)
                if "e" in textanchor:
                    x = int(MAPWIDTH*relx) - int(fontwidth)
                elif "w" in textanchor:
                    x = int(MAPWIDTH*relx)
        if options.get("textboxfillcolor") or options.get("textboxoutlinecolor"):
            relfontwidth, relfontheight = (fontwidth/float(MAPWIDTH), fontheight/float(MAPHEIGHT))
            relxmid,relymid = (x/float(MAPWIDTH)+relfontwidth/2.0,y/float(MAPHEIGHT)+relfontheight/2.0)
            relupperleft = (relxmid-relfontwidth*options["textboxfillsize"]/2.0, relymid-relfontheight*options["textboxfillsize"]/2.0)
            relbottomright = (relxmid+relfontwidth*options["textboxfillsize"]/2.0, relymid+relfontheight*options["textboxfillsize"]/2.0)
            options["fillcolor"] = options["textboxfillcolor"]
            options["outlinecolor"] = options["textboxoutlinecolor"]
            options["outlinewidth"] = options["textboxoutlinewidth"]
            self.RenderRectangle(relupperleft, relbottomright, options)
        self.drawer.text((x,y), text, font)
    def _BasicLine(self, coords, options):
        """
draw basic lines with outline, but nothing at start and end
"""
        #first draw outline line
        if options["outlinecolor"]:
            outlinepen = aggdraw.Pen(options["outlinecolor"], options["fillsize"]+options["outlinewidth"])
            self.drawer.line(coords, outlinepen)
        #then draw fill line which is thinner
        if options["fillcolor"]:
            fillpen = aggdraw.Pen(options["fillcolor"], options["fillsize"])
            self.drawer.line(coords, fillpen)
    def _BasicPolygon(self, coords, options):
        """
draw polygon with color fill
"""
        args = []
        if options["fillcolor"]:
            fillbrush = aggdraw.Brush(options["fillcolor"])
            args.append(fillbrush)
        if options["outlinecolor"]:
            outlinepen = aggdraw.Pen(options["outlinecolor"], options["outlinewidth"])
            args.append(outlinepen)
        self.drawer.polygon(coords, *args)
        pass
    def _BasicCircle(self, coords, options):
        """
draw points with a symbol path representing a circle
"""
        #build circle
        size = int(options["fillsize"]/2.0)
        x,y = coords
        circlecoords = (x-size, y-size, x+size, y+size)
        #set symbol options
        args = []
        if options["fillcolor"]:
            fillbrush = aggdraw.Brush(options["fillcolor"])
            args.append(fillbrush)
        if options["outlinecolor"]:
            outlinepen = aggdraw.Pen(options["outlinecolor"], options["outlinewidth"])
            args.append(outlinepen)
        #draw
        self.drawer.ellipse(circlecoords, *args)
    def _BasicSquare(self, coords, options):
        """
draw points with a symbol path representing a square
"""
        #build circle
        size = int(options["fillsize"]/2.0)
        x,y = coords
        squarecoords = (x-size, y-size, x+size, y+size)
        #set symbol options
        args = []
        if options["fillcolor"]:
            fillbrush = aggdraw.Brush(options["fillcolor"])
            args.append(fillbrush)
        if options["outlinecolor"]:
            outlinepen = aggdraw.Pen(options["outlinecolor"], options["outlinewidth"])
            args.append(outlinepen)
        #draw
        self.drawer.rectangle(squarecoords, *args)
    def _Pyramid(self, coords, options):
        """
draw basic lines with outline, but nothing at start and end.
"""
        if options["outlinecolor"]:
            size = int(options["fillsize"])
            width = int(options["fillwidth"]) #pxls
            #calculate three pyramid coords
            x,y = coords
            leftbase = [x-int(width/2.0), y]
            peak = [x, y-size]
            rightbase = [x+int(width/2.0), y]
            #first draw left line
            leftlinecoords = list(leftbase)
            leftlinecoords.extend(peak)
            outlinepen = aggdraw.Pen(options["outlinecolor"], options["outlinewidth"])
            self.drawer.line(leftlinecoords, outlinepen)
            #then draw right line
            rightlinecoords = list(rightbase)
            rightlinecoords.extend(peak)
            outlinepen = aggdraw.Pen(options["outlinecolor"], options["outlinewidth"])
            self.drawer.line(rightlinecoords, outlinepen)
    def _PyramidScape(self, coords, options):
        """
similar to pyramid, except pyramids stretch across all of map horizontally at specified y interval, and goes up and down by aggregating all values in each x area of its respective y range.
"""
        pass

class _PyCairo_Renderer:
    """
This class can be called on to draw each feature with PyCairo as long as
it is given instructions via a color/size/options dictionary
"""
    #NEED TO RECEIVE GENERATOR OF TRANSFORMED COORDS FROM MAPCANVAS
    #ALSO NEEDS THE Aggdraw.Draw(img) OBJECT
    def __init__(self):
        global cairo
        import cairo
        self.fontnames = dict([("default", "cursive"),
                               ("serif", "serif"),
                               ("sans-serif", "sans-serif"),
                               ("cursive","cursive"),
                               ("fantasy", "fantasy"),
                               ("monospace","monospace") ])
    def NewImage(self):
        """
This must be called before doing any rendering.
Note: this replaces any previous image drawn on so be sure to
retrieve the old image before calling it again to avoid losing work
"""
        #first mode
        mode = cairo.FORMAT_ARGB32
        #then other specs
        width = MAPWIDTH
        height = MAPHEIGHT
        background = MAPBACKGROUND
        self.img = cairo.ImageSurface(mode, int(MAPWIDTH), int(MAPHEIGHT))
        self.drawer = cairo.Context(self.img)
        if background:
            backgroundcolor = self.__hex_to_rgb(background)
            self.drawer.set_source_rgb(*backgroundcolor)
            self.drawer.rectangle(0,0,MAPWIDTH,MAPHEIGHT)
            self.drawer.fill()
    def RenderText(self, relx, rely, text, options):
        if not options.get("texteffect"):
            self._BasicText(relx, rely, text, options)
    def RenderRectangle(self, upperleft, bottomright, customoptions):
        leftrelx, uprely = upperleft
        leftx,upy = (int(MAPWIDTH*leftrelx), int(MAPHEIGHT*uprely))
        rightrelx, downrely = bottomright
        rightx,downy = (int(MAPWIDTH*rightrelx), int(MAPHEIGHT*downrely))
        rectanglecoords = [(leftx,upy), (rightx,upy), (rightx,downy), (leftx,downy), (leftx,upy)]        
        self._BasicPolygon(rectanglecoords, customoptions)
    def RenderCircle(self, relx, rely, fillsize, customoptions):
        customoptions["fillsize"] = fillsize
        x = int(MAPWIDTH*relx)
        y = int(MAPHEIGHT*rely)
        self._BasicCircle([(x,y)], customoptions)
    def RenderLine(self, startpos, stoppos, customoptions):
        startrelx, startrely = startpos
        startxy = (int(MAPWIDTH*startrelx), int(MAPHEIGHT*startrely))
        stoprelx, stoprely = stoppos
        stopxy = (int(MAPWIDTH*stoprelx), int(MAPHEIGHT*stoprely))
        linecoords = [startxy, stopxy]
        self._BasicLine(linecoords, customoptions)
    def RenderShape(self, shapeobj, options):
        """
looks at instructions in options to decide which draw method to use
"""
        #possibly use an options filterer here to enure all needed options
        #are given, otherwise snap to default
        #............
        multishapes = shapeobj.to_pycairo()
        for coords in multishapes:
            if shapeobj.type == "polygon":
                self._BasicPolygon(coords, options)
            elif shapeobj.type == "line":
                self._BasicLine(coords, options)
            elif shapeobj.type == "point":
                self._BasicCircle(coords, options)
    def GetImage(self):
        self.img.write_to_png("tempgif.gif")
        gifimg = tk.PhotoImage(file="tempgif.gif")
        os.remove("tempgif.gif")
        return gifimg
    def SaveImage(self, savepath):
        if savepath.endswith(".png"):
            self.img.write_to_png(savepath)

    #Internal use only
    def __hex_to_rgb(self, hexcolor):
        return colour.Color(hexcolor).rgb
    def _BasicText(self, relx, rely, text, options):
        """
Draws basic text, no effects
"""
        self.drawer.select_font_face(self.fontnames[options["textfont"]])
        self.drawer.set_font_size(options["textsize"]) # em-square height is 90 pixels
        _, _, fontwidth, fontheight, _, _ = self.drawer.text_extents(text)
        x = int(MAPWIDTH*relx) - int(fontwidth/2.0)
        y = int(MAPHEIGHT*rely) + int(fontheight/2.0) #NOTICE: for some odd reason height has to be plussed, not minused
        self.drawer.move_to(x, y) # move to point (x, y) = (10, 90)
        textcolor = self.__hex_to_rgb(options["textcolor"])
        self.drawer.set_source_rgb(*textcolor) # yellow
        self.drawer.show_text(text)
        self.drawer.stroke()
    def _BasicLine(self, coords, options):
        """
Draw basic lines with outline, but nothing at start and end
"""
        if len(coords) >= 2:
            #outline symbolics
            outlinecolor = self.__hex_to_rgb(options["outlinecolor"])
            self.drawer.set_source_rgb(*outlinecolor) # Solid color
            self.drawer.set_line_width(options.get("fillsize")+(options.get("outlinewidth")*2))
            #draw outline
            xy = coords[0]
            self.drawer.move_to(*xy)
            for xy in coords[1:]:
                self.drawer.line_to(*xy)
            self.drawer.stroke_preserve()
            #fill symbolics
            fillcolor = self.__hex_to_rgb(options["fillcolor"])
            self.drawer.set_source_rgb(*fillcolor) # Solid color
            self.drawer.set_line_width(options.get("fillsize"))
            #then draw fill line which is thinner
            xy = coords[0]
            self.drawer.move_to(*xy)
            for xy in coords[1:]:
                self.drawer.line_to(*xy)
            self.drawer.stroke_preserve()
    def _BasicPolygon(self, coords, options):
        """
Draw polygon with color fill
"""
        if len(coords) >= 3:
            #define outline symbolics
            outlinecolor = self.__hex_to_rgb(options["outlinecolor"])
            self.drawer.set_source_rgb(*outlinecolor) # Solid color
            self.drawer.set_line_width(options["outlinewidth"])
            #...self.drawer.set_line_join(cairo.LINE_JOIN_ROUND)
            #first starting point
            xy = coords[0]
            self.drawer.move_to(*xy)
            #then add path for each new vertex
            for xy in coords[1:]:
                self.drawer.line_to(*xy)
            self.drawer.close_path()
            self.drawer.stroke_preserve()
            #then fill insides
            fillcolor = self.__hex_to_rgb(options["fillcolor"])
            self.drawer.set_source_rgb(*fillcolor)
            self.drawer.fill()
    def _BasicCircle(self, coords, options):
        "draw points with a symbol path representing a circle"
        #define outline symbolics
        outlinecolor = self.__hex_to_rgb(options["outlinecolor"])
        self.drawer.set_source_rgb(*outlinecolor) # Solid color
        self.drawer.set_line_width(options["outlinewidth"])
        #draw circle
        size = int(options["fillsize"]/2.0)
        x,y = coords[0] #0 necessary bc pycairo receives a list of coordinate pairs, and with points there is only one pair
        self.drawer.arc(x, y, size, 0, 2*math.pi)
        self.drawer.stroke_preserve()
        #fill circle
        fillcolor = self.__hex_to_rgb(options["fillcolor"])
        self.drawer.set_source_rgb(*fillcolor)
        self.drawer.fill()

class _Renderer:
    #builtins
    def __init__(self):
        if RENDERER == "tkinter":
            self.renderer = _TkCanvas_Renderer()
        elif RENDERER == "PIL":
            self.renderer = _PIL_Renderer()
        elif RENDERER == "aggdraw":
            self.renderer = _Aggdraw_Renderer()
        elif RENDERER == "pycairo":
            self.renderer = _PyCairo_Renderer()
        #automatically create blank image
        self.NewImage()
        self.layers = dict()
    #custom methods
    def NewImage(self):
        self.renderer.NewImage()
    def ViewShapefile(self, shapefilepath, customoptions):
        self._RenderShapefile(shapefilepath, customoptions)
        self._RenderMapTitle(shapefilepath, customoptions)
        self._ViewRenderedShapefile()
    def SaveShapefileImage(self, shapefilepath, savepath, customoptions):
        self._RenderShapefile(shapefilepath, customoptions)
        self._RenderMapTitle(shapefilepath, customoptions)
        self._SaveRenderedShapefile(savepath)
    #internal use only
    def _RelSizesToPixels(self, customoptions):
        customoptions = customoptions.copy()
        customoptions["fillsize"] = MAPWIDTH*customoptions["fillsize"]/100.0
        customoptions["fillwidth"] = MAPWIDTH*customoptions["fillwidth"]/100.0
        customoptions["fillheight"] = MAPHEIGHT*customoptions["fillheight"]/100.0
        customoptions["outlinewidth"] = MAPWIDTH*customoptions["outlinewidth"]/100.0
        return customoptions
    def _RenderMapTitle(self, shapefilepath, customoptions):
        #unless not specified, default maptitle is set to name of shapefile
        if customoptions.get("maptitle", "not set") == "not set":
            shapefilename = shapefilepath.split("\\")[-1]
            shapefilename = ".".join(shapefilename.split(".")[:-1])
            customoptions["maptitle"] = shapefilename
        #unless asked not to show maptitle, generate default textoptions except large text size
        if customoptions.get("maptitle"):
            textoptions = _CheckTextOptions(dict([("textsize",0.0452)]))
            self._RenderText(0.5, 0.05, customoptions["maptitle"], textoptions)
    def _RenderText(self, relx, rely, text, textoptions):
        self.renderer.RenderText(relx, rely, text, textoptions)
    def _RenderRectangle(self, upperleft, bottomright, customoptions):
        customoptions = self._RelSizesToPixels(customoptions)
        self.renderer.RenderRectangle(upperleft, bottomright, customoptions)
    def _RenderCircle(self, relx, rely, fillsize, customoptions):
        customoptions["fillsize"] = fillsize
        customoptions = self._RelSizesToPixels(customoptions)
        fillsize = customoptions["fillsize"]
        self.renderer.RenderCircle(relx, rely, fillsize, customoptions)
    def _RenderLine(self, startpos, stoppos, customoptions):
        #NOTE: TO ADD BETTER LINES DRAWING, DRAW AS POLYGON.
        #CALCULTE POLYCOORDS OF LINEWIDTH BASED ON:
        #http://mathforum.org/library/drmath/view/68285.html

        #hmm...
        
        customoptions = self._RelSizesToPixels(customoptions)
        self.renderer.RenderLine(startpos, stoppos, customoptions)
    def _RenderShape(self, shape, customoptions):
        customoptions = self._RelSizesToPixels(customoptions)
        self.renderer.RenderShape(shape, customoptions)
    def _RenderShapefile(self, shapefilepath, customoptions):
        "this one loads a filepath from scratch, does not take preloaded layers"
        #create shapefile generator
        shapefile = Shapefile(shapefilepath)
        #exclude values if specified
        excludequery = customoptions.get("excludequery")
        if excludequery:
            shapefile.SelectByQuery(excludequery, inverted=True)
        #then iterate through shapes and render each
        shapefile.progresstext = "rendering"
        for eachshape in shapefile:
            #then send to be rendered
            self._RenderShape(eachshape, customoptions)
    def _RenderLayer(self, layer):
        "renders a preloaded layer"
        #create shapefile generator
        shapefile = layer.fileobj
        customoptions = layer.customoptions
        #exclude values if specified
        excludequery = customoptions.get("excludequery")
        if excludequery:
            shapefile.SelectByQuery(excludequery, inverted=True)
        #then iterate through shapes and render each
        shapefile.progresstext = "rendering"
        for eachshape in shapefile:
            #then send to be rendered
            self._RenderShape(eachshape, customoptions)
    def _AddLayerInfo(self, layername, allclassifications):
        self.layers[layername] = allclassifications
    def _ViewRenderedShapefile(self):
        #finally open image in tkinter
        if RENDERER == "tkinter":
            #if tkinter is the renderer then all that is needed is to run the mainloop
            self.renderer.RunTk()
        else:
            def ViewInTkinter():
                #setup GUI
                window = tk.Tk()
                window.wm_title("Static MapCanvas Viewer")
                window_frame = tk.Frame(window)
                window_frame.pack()
                #embed image in a canvas
                tkimg = self.renderer.GetImage()
                screenwidth = window.winfo_screenwidth()
                viewimgwidth,viewimgheight = (MAPWIDTH,MAPHEIGHT)
                if MAPWIDTH >= screenwidth:
                    viewimgwidth,viewimgheight = (screenwidth,int(screenwidth/2.0))
                    resizedimg = self.renderer.img.resize((viewimgwidth,viewimgheight), PIL.Image.ANTIALIAS)
                    tkimg = PIL.ImageTk.PhotoImage(image=resizedimg)
                    window.wm_state('zoomed')
                canvas = tk.Canvas(window_frame, width=viewimgwidth, height=viewimgheight, bg="white")
                canvas.pack()
                x0,y0,x1,y1 = ( -int(viewimgwidth/50.0), int(viewimgwidth/50.0), viewimgwidth-int(viewimgwidth/50.0), viewimgheight+int(viewimgwidth/50.0) )
                if MAPBACKGROUND:
                    canvas.create_rectangle(x0,y0,x1,y1, fill="Gray80", outline="") #this is the shadow
                canvas.create_image(0,0, anchor="nw", image=tkimg)
                canvas.create_rectangle(0,0,viewimgwidth,viewimgheight, fill="", outline=Color("black")) #this is the map outline edge
                #make image pannable
                def mouseovermap(event):
                    global mouseovermapvar
                    window.config(cursor="fleur") #draft_large
                    mouseovermapvar = True
                def mouseoutofmap(event):
                    global mouseovermapvar
                    window.config(cursor="")
                    mouseovermapvar = False
                def activatedrag(event):
                    global mouseclicked
                    if mouseovermapvar == True:
                        mouseclicked = True
                def deactivatedrag(event):
                    global mouseclicked
                    mouseclicked = False
                def mark(event):
                    canvas.scan_mark(event.x, event.y)
                def dragto(event):
                    try:
                        if mouseclicked == True:
                            canvas.scan_dragto(event.x, event.y, 1)
                    except:
                        pass
                canvas.bind("<Enter>", mouseovermap, "+")
                canvas.bind("<Leave>", mouseoutofmap, "+")
                window.bind("<Button-1>", mark, "+")
                window.bind("<Motion>", dragto, "+")
                window.bind("<Button-1>", activatedrag, "+")
                window.bind("<ButtonRelease-1>", deactivatedrag, "+")
                #place save button to enable saving map image
                def imagesavefiledialog():
                    savepath = tkFileDialog.asksaveasfilename(defaultextension=".png", initialfile="unnamed_map")
                    self._SaveRenderedShapefile(savepath)
                saveimg = "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"
                savebutton = tk.Button(window_frame, command=imagesavefiledialog, relief="solid")
                savebutton.img = tk.PhotoImage(data=saveimg).subsample(8,8)
                savebutton["image"] = savebutton.img
                savebutton.place(x=5, y=5, anchor="nw")
                #open window
                window.mainloop()
            tkthread = threading.Thread(target=ViewInTkinter)
            tkthread.start()
    def _SaveRenderedShapefile(self, savepath):
        if RENDERER == "tkinter":
            raise AttributeError("The Tkinter map renderer does not have a function to save the map as an image \
due to the limited options of the Tkinter Canvas. If possible try using any of the other renderers instead")
        else:
            self.renderer.SaveImage(savepath)







############## FINALLY, DEFINE FRONT-END USER FUNCTIONS

#INTERACTIVE INPUT HELPERS
def AskNumber(text="unknown task"):
    """
Asks the user to interactively input a number (float or int) at any point in the script, and returns the input number.

| __option__ | __description__ 
| --- | --- 
| *text | an optional string to identify for what purpose the chosen number will be used.
"""
    def ValidateNumber(text):
        try:
            innumber = input("\n\nwrite a comma or integer number to use for "+str(text)+" (example: 15 or 15.83)\nnumber = ")
        except NameError:
            print("""\n---> unknown error""")
            return ValidateNumber(text)
        if not isinstance(innumber,(float,int)):
            print("""\n---> error: the number must be either a floating point comma or integer number""")
            return ValidateNumber(text)
        return innumber
    return ValidateNumber(text)
def AskString(text="unknown task"):
    """
Asks the user to interactively input a string at any point in the script, and returns the input string.

| __option__ | __description__ 
| --- | --- 
| *text | an optional string to identify for what purpose the chosen string will be used.
"""
    def ValidateString(text):
        try:
            instring = input("\n\nwrite a string to use for "+str(text)+", enclosed in quoatation marks (example: 'this is my string')\nstring = ")
        except NameError:
            print("""\n---> error: the string must be enclosed by quotation marks""")
            return ValidateString(text)
        if not isinstance(instring,basestring):
            print("""\n---> error: the string must be enclosed by quotation marks""")
            return ValidateString(text)
        return instring
    return ValidateString(text)
def AskShapefilePath(text="unknown task"):
    """
Pops up a temporary tk window asking user to visually choose a shapefile.
Returns the chosen shapefile path as a text string. Also prints it as text in case
the user wants to remember which shapefile was picked and hardcode it in the script.

| __option__ | __description__ 
| --- | --- 
| *text | an optional string to identify what purpose the shapefile was chosen for when printing the result as text.
"""
    tempwindow = tk.Tk()
    tempwindow.state("withdrawn")
    shapefilepath = tkFileDialog.askopenfilename(parent=tempwindow, filetypes=[("shapefile",".shp")], title="choose shapefile for "+text)
    tempwindow.destroy()
    print("you picked the following shapefile for <"+str(text)+">:\n"+str(shapefilepath)+"\n\n")
    return shapefilepath
def AskFieldName(shapefilepath, text="unknown task"):
    """
Loads and prints the available fieldnames of a shapefile, and asks the user which one to choose.
Returns the chosen fieldname as a string.

| __option__ | __description__ 
| --- | --- 
| *text | an optional string to identify for what purpose the chosen fieldname will be used.
"""
    tempshapefile = Shapefile(shapefilepath)
    print("valid fieldnames:")
    for fieldname in tempshapefile.fieldnames:
        print("  %s" % fieldname)
    def ValidateFieldName(tempshapefile, text):
        try:
            fieldname = input("\n\nselecting fieldname for "+str(text)+"\nchoose from the above fieldnames (and surround by quotation marks)\nfield = ")
        except NameError:
            print("""\n---> error: the fieldname must be given as a string enclosed by quotation marks (example "field1" or 'field1')""")
            return ValidateFieldName(tempshapefile, text)
        if not isinstance(fieldname,basestring):
            print("""\n---> error: the fieldname must be given as a string enclosed by quotation marks (example "field1" or 'field1')""")
            return ValidateFieldName(tempshapefile, text)
        if fieldname in tempshapefile.fieldnames:
            del tempshapefile
            return fieldname
        else:
            print("\n---> error: the specified fieldname does not match any of the valid fieldnames, try again")
            return ValidateFieldName(tempshapefile, text)
    return ValidateFieldName(tempshapefile, text)
def AskColor(text="unknown graphics"):
    """
Pops up a temporary tk window asking user to visually choose a color.
Returns the chosen color as a hex string. Also prints it as text in case
the user wants to remember which color was picked and hardcode it in the script.

| __option__ | __description__ 
| --- | --- 
| *text | an optional string to identify what purpose the color was chosen for when printing the result as text.
"""
    def askcolor():
        tempwindow = tk.Tk()
        tempwindow.state("withdrawn")
        rgb,hexcolor = tkColorChooser.askcolor(parent=tempwindow, title="choose color for "+text) ;
        tempwindow.destroy()
        print("you picked the following color for "+str(text)+": "+str(hexcolor))
        return hexcolor
    hexcolor = askcolor()
    return colour.Color(hexcolor).hex

#GENERAL UTILITIES
def _FolderLoop(folder, filetype=""):
    """
A generator that iterates through all files in a folder tree, either in a for loop or by using next() on it.
Filetype can be set to only grab files that have the specified file-extension. If filetype is a tuple then grabs all filetypes listed within it.
"""
    alldirs = os.walk(folder)
    # loop through and run unzip function
    for eachdirinfo in alldirs:
        eachdir = eachdirinfo[0]+"\\"
        dirfiles = eachdirinfo[2]
        for eachfile in dirfiles:
            if eachfile.endswith(filetype):
                eachfilename = ".".join(eachfile.split(".")[:-1])
                eachfiletype = "." + eachfile.split(".")[-1]
                yield (eachdir, eachfilename, eachfiletype)
def ShapefileFolder(folder):
    """
A generator that will loop through a folder and all its subfolder and return information of every shapefile it finds. Information returned is a tuple with the following elements (string name of current subfolder, string name of shapefile found, string of the shapefile's file extension(will always be '.shp'))

| __option__ | __description__ 
| --- | --- 
| folder | a path string of the folder to check for shapefiles.
"""
    for eachfolder, eachshapefile, eachfiletype in _FolderLoop(folder, filetype=".shp"):
        yield (eachfolder, eachshapefile, eachfiletype)

class Layer:
    """
Creates and returns a thematic layer instance (a visual representation of a geographic file) that can be symbolized and used to add to a map.

| __option__ | __description__ 
| --- | --- 
| filepath | the path string of the geographic file to add, including the file extension.
| **customoptions | any series of named arguments of how to style the shapefile visualization (optional). Valid arguments are: fillcolor, fillsize (determines the circle size for point shapefiles, line width for line shapefiles, and has no effect for polygon shapefiles), outlinecolor, outlinewidth. For more info see the special section on how to stylize a layer. 
"""
    def __init__(self, filepath, **customoptions):
        self.filepath = filepath
        self.fileobj = Shapefile(shapefilepath=filepath, progresstext="loading layer")
        self.customoptions = _CheckOptions(customoptions)
        self.classifier = None
    def AddClassification(self, symboltype, valuefield, symbolrange=None, classifytype="equal interval", nrclasses=5):
        """
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

"""
        if not self.classifier:
            #create classifier if this is the first classification being added
            self.classifier = _Classifier()
        self.classifier.AddClassification(symboltype, valuefield, symbolrange=symbolrange, classifytype=classifytype, nrclasses=nrclasses)
        
        
#RENDERING OPTIONS
def SetRenderingOptions(renderer="not set", numpyspeed="not set", reducevectors="not set"):
    """
Sets certain rendering options that apply to all visualizations or map images.

| __option__    | __description__
| --- | --- 
| *renderer | a string describing which Python module will be used for rendering. This means you need to have the specified module installed. Valid renderer values are 'aggdraw' (default), 'PIL', 'pycairo', 'tkinter'. Notes: If you have no renderers installed, then use Tkinter which comes with all Python installations, be aware that it is significantly slow, memory-limited, and cannot be used to save images. Currently PyCairo is not very well optimized, and is particularly slow to render line shapefiles. 
| *numpyspeed | specifies whether to use numpy to speed up shapefile reading and coordinate-to-pixel conversion. Must be True (default) or False.
| *reducevectors | specifies whether to reduce the number of vectors to be rendered. This can speed up rendering time, but may lower the quality of the rendered image, especially for line shapefiles. Must be True or False (default).
"""
    if renderer != "not set":
        global RENDERER
        RENDERER = renderer
    if numpyspeed != "not set":
        global NUMPYSPEED
        NUMPYSPEED = numpyspeed
        _UpdateMapDims() #this bc map dimensions have to be recalculated to/from numpyspeed format
    if reducevectors != "not set":
        global REDUCEVECTORS
        REDUCEVECTORS = reducevectors
        
#STYLE CUSTOMIZING
def Color(basecolor, intensity="not specified", brightness="not specified", style=None):
    """
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
"""
    #first check on intens/bright
    if style and basecolor not in ("black","white","gray"):
        #style overrides manual intensity and brightness options
        intensity = COLORSTYLES[style]["intensity"]
        brightness = COLORSTYLES[style]["brightness"]
    else:
        #special black,white,gray mode, bc random intens/bright starts creating colors, so have to be ignored
        if basecolor in ("black","white","gray"):
            if brightness == "random":
                brightness = random.randrange(20,80)/100.0
        #or normal
        else:
            if intensity == "random":
                intensity = random.randrange(20,80)/100.0
            elif intensity == "not specified":
                intensity = 0.7
            if brightness == "random":
                brightness = random.randrange(20,80)/100.0
            elif brightness == "not specified":
                brightness = 0.5
    #then assign colors
    if basecolor in ("black","white","gray"):
        #graymode
        if brightness == "not specified":
            return colour.Color(color=basecolor).hex
        else:
            #only listen to gray brightness if was specified by user or randomized
            return colour.Color(color=basecolor, luminance=brightness).hex
    elif basecolor == "random":
        #random colormode
        basecolor = random.randrange(300)
        return colour.Color(pick_for=basecolor, saturation=intensity, luminance=brightness).hex
    else:
        #custom made color
        return colour.Color(color=basecolor, saturation=intensity, luminance=brightness).hex

class _SymbolClass:
    def __init__(self, classmin, classmax, minvalue, maxvalue, classvalue, classsymbol):
        "_min and _max are not attr values meant for user, but used for membership determination internally and can be different from attr"
        self._min = classmin
        self._max = classmax
        self.min = minvalue
        self.max = maxvalue
        self.classvalue = classvalue
        self.classsymbol = classsymbol

class _Classifier:
    """
Internal use only
A classifier that holds a set of instructions on how to classify a shapefile's visual symbols based on its attribute values. 
The classifier can hold multiple classifications, one for each symbol (e.g. fillsize and fillcolor), and these are added with the AddClassification method. 
When a layer is passed to a rendering operations its classifier is used as the recipe on how to symbolize the shapefile. 
This classifier is also needed to render a shapefile's legend.

*Takes no arguments*

"""
    def __init__(self):
        self.values = dict()
        self.symbols = dict()
        self.allclassifications = []
        self.name = "unnamed classifier"
    def AddClassification(self, symboltype, valuefield, symbolrange=None, classifytype="equal interval", nrclasses=5):        
        if not symbolrange and classifytype!="categorical":
            raise TypeError("since you have chosen a gradual classification you must specify a range of symbol values to choose from")
        classification = dict([("symboltype",symboltype),
                               ("valuefield",valuefield),
                               ("symbolrange",symbolrange),
                               ("classifytype",classifytype),
                               ("nrclasses",nrclasses) ])
        self.allclassifications.append(classification)
    def AddCustomClass(self, symboltype, valuefield, valuemin, valuemax):
        #first loop through existing classes and delete/reset maxmin values to make room for the new class value range
        #then create and insert class at appropriate position
        pass
    def AddValue(self, index, symboltype, value):
        if self.values.get(index):
            #add to dict if already exits
            self.values[index][symboltype] = value
        else:
            #or create new dict if not
            self.values[index] = dict([(symboltype, value)])
        self.symbols[index] = dict()
    def CalculateClasses(self, classification):
        classifytype = classification.get("classifytype")
        #calculate classes based on classifytype
        if classifytype.lower() == "categorical":
            self._UniqueCategories(classification)
            self.__AssignMembershipByUnique(classification)
        elif classifytype.lower() == "equal interval":
            self._EqualInterval(classification)
            self.__AssignMembershipByValue(classification)
        elif classifytype.lower() == "equal classes":
            self._EqualClasses(classification)
            self.__AssignMembershipByIndex(classification)
        elif classifytype.lower() == "natural breaks":
            self._NaturalBreaks(classification)
            self.__AssignMembershipByValue(classification)
        else:
            raise TypeError("classifytype must be one of: ...")
    def GetSymbol(self, uniqid, symboltype):
        #for each class test value for membership
        featuresymbols = self.symbols.get(uniqid)
        if featuresymbols:
            symbol = featuresymbols.get(symboltype)
            if symbol:
                return symbol
    def GetValues(self):
        return self.sortedvalues
    def GetClassifications(self):
        return self.allclassifications

    # INTERNAL USE ONLY
    def __AssignMembershipByValue(self, classification):
        symboltype = classification.get("symboltype")
        classes = classification.get("classes")
        #loop through values and assign class symbol to each for the specified symboltype
        for uniqid, value in self.sortedvalues:
            value = value[symboltype]
            #for each class test value for membership
            for eachclass in classes:
                #membership true if within minmax range of that class
                if value >= eachclass._min and value <= eachclass._max:
                    #assign classsymbol
                    self.symbols[uniqid][symboltype] = eachclass.classsymbol
                    break
    def __AssignMembershipByIndex(self, classification):
        symboltype = classification.get("symboltype")
        classes = classification.get("classes")
        #loop through values and assign class symbol to each for the specified symboltype
        for index, (uniqid, value) in enumerate(self.sortedvalues):
            value = value[symboltype]
            #for each class test value for membership
            for eachclass in classes:
                #membership true if within minmax range of that class
                if index >= eachclass._min and index <= eachclass._max:
                    #assign classsymbol
                    self.symbols[uniqid][symboltype] = eachclass.classsymbol
                    break
    def __AssignMembershipByUnique(self, classification):
        symboltype = classification.get("symboltype")
        classes = (each for each in classification.get("classes"))
        #loop through values and assign class symbol to each for the specified symboltype
        oldvalue = None
        for index, (uniqid, value) in enumerate(self.sortedvalues):
            value = value[symboltype]
            if value != oldvalue:
                eachclass = next(classes)
            self.symbols[uniqid][symboltype] = eachclass.classsymbol
            oldvalue = value
    def __CustomSymbolRange(self, classification):
        symbolrange = classification.get("symbolrange")
        nrclasses = classification.get("nrclasses")
        #first create pool of possible symbols from raw inputted symbolrange
        if isinstance(symbolrange[0], (int,float)):
            #create interpolated or shrinked nr range
            symbolrange = listy.Resize(symbolrange, nrclasses)
        elif isinstance(symbolrange[0], basestring):
            #create color gradient by blending color rgb values
            rgbcolors = [colour.hex2rgb(eachhex) for eachhex in symbolrange]
            rgbgradient = listy.Resize(rgbcolors, nrclasses)
            symbolrange = [colour.rgb2hex(eachrgb) for eachrgb in rgbgradient]
            #alternative color spectrum hsl interpolation
            ###rgbcolors = [colour.rgb2hsl(colour.hex2rgb(eachhex)) for eachhex in symbolrange]
            ###rgbgradient = listy.Resize(rgbcolors, nrclasses)
            ###symbolrange = [colour.rgb2hex(colour.hsl2rgb(eachrgb
        #update classification with new symbolrange
        classification["symbolrange"] = symbolrange
    def _UniqueCategories(self, classification):
        """
Remember, with unique categories the symbolrange doesn't matter, and only works for colors
"""
        symboltype = classification.get("symboltype")
        classifytype = classification.get("classifytype")
        if not "color" in symboltype:
            raise TypeError("the categorical classification can only be used with color related symboltypes")
        #initiate
        self.sortedvalues = sorted([(uniqid, value) for uniqid, value in self.values.iteritems()], key=operator.itemgetter(1))
        sortedvalues = [value[symboltype] for uniqid,value in self.sortedvalues]
        #populate classes
        classes = []
        #then set symbols
        olduniq = None
        for index, uniq in enumerate(sortedvalues):
            if uniq != olduniq:
                classsymbol = Color("random")
                classmin = uniq
                classmax = uniq
                minvalue = classmin
                maxvalue = classmax
                #create and add class
                classes.append( _SymbolClass(classmin, classmax, minvalue, maxvalue, index, classsymbol) )
                olduniq = uniq
        classification["classes"] = classes
    def _EqualInterval(self, classification):
        symboltype = classification.get("symboltype")
        symbolrange = classification.get("symbolrange")
        classifytype = classification.get("classifytype")
        nrclasses = classification.get("nrclasses")
        #initiate
        self.__CustomSymbolRange(classification)
        symbolrange = classification["symbolrange"]
        self.sortedvalues = sorted([(uniqid, value) for uniqid, value in self.values.iteritems()], key=operator.itemgetter(1))
        sortedvalues = [value[symboltype] for uniqid,value in self.sortedvalues]
        lowerbound = sortedvalues[0]
        upperbound = sortedvalues[-1]
        intervalsize = int( (upperbound-lowerbound)/float(nrclasses) )        
        #populate classes
        classmin = lowerbound
        classes = []
        for index, classsymbol in enumerate(symbolrange):
            if index == nrclasses-1:
                classmax = upperbound
            else:
                classmax = classmin+intervalsize
            #determine min and max value
            minvalue = classmin
            maxvalue = classmax
            #create and add class
            classes.append( _SymbolClass(classmin, classmax, minvalue, maxvalue, index, classsymbol) )
            #prep for next
            classmin = classmax
        classification["classes"] = classes
    def _EqualClasses(self, classification):
        symboltype = classification.get("symboltype")
        symbolrange = classification.get("symbolrange")
        classifytype = classification.get("classifytype")
        nrclasses = classification.get("nrclasses")
        #initiate
        self.__CustomSymbolRange(classification)
        symbolrange = classification["symbolrange"]
        self.sortedvalues = sorted([(uniqid, value) for uniqid, value in self.values.iteritems()], key=operator.itemgetter(1))
        sortedvalues = [value[symboltype] for uniqid,value in self.sortedvalues]
        classsize = int( len(sortedvalues)/float(nrclasses) )
        #populate classes
        classmin = 0
        classes = []
        for index, classsymbol in enumerate(symbolrange):
            if index == nrclasses-1:
                classmax = len(sortedvalues)-1
            else:
                classmax = classmin+classsize
            #determine min and max value
            minvalue = sortedvalues[classmin]
            maxvalue = sortedvalues[classmax]
            #create and add class
            classes.append( _SymbolClass(classmin, classmax, minvalue, maxvalue, index, classsymbol) )
            #prep for next
            classmin = classmax
        classification["classes"] = classes
    def _NaturalBreaks(self, classification):
        symboltype = classification.get("symboltype")
        symbolrange = classification.get("symbolrange")
        classifytype = classification.get("classifytype")
        nrclasses = classification.get("nrclasses")
        #initiate
        self.__CustomSymbolRange(classification)
        symbolrange = classification["symbolrange"]
        self.sortedvalues = sorted([(uniqid, value) for uniqid, value in self.values.iteritems()], key=operator.itemgetter(1))
        sortedvalues = [value[symboltype] for uniqid,value in self.sortedvalues]
        lowerbound = sortedvalues[0]
        upperbound = sortedvalues[-1]
        def getJenksBreaks(dataList, numClass ):
            "taken from http://danieljlewis.org/files/2010/06/Jenks.pdf"
            dataList = sorted(dataList)
            #in mat1, populate empty classlists of zeros
            zeros = [0 for j in xrange(0,numClass+1)]
            zeroandones = [0]
            zeroandones.extend([1 for i in xrange(1,numClass+1)])
            mat1 = [list(zeros), zeroandones]
            mat1.extend([list(zeros) for i in xrange(2,len(dataList)+1)])
            #...while classes in element 1 are set to 1, except for first class which remains zero
            for i in xrange(1,numClass+1):
                mat1[1][i] = 1
            #in mat2, classes in element 0 and 1 are set to 0
            mat2 = [list(zeros),list(zeros)]
            #...while the classes in elements 2 and up are set to infinity, except for first class which is a zero
            mat2classes = [0]
            mat2classes.extend([float('inf') for i in xrange(1,numClass+1)])
            mat2ext = [list(mat2classes) for j in xrange(2,len(dataList)+1)]
            mat2.extend(mat2ext)
            #then the main work (everything prior to this has been optimized/changed from original code)
            v = 0.0
            for l in xrange(2,len(dataList)+1):
                s1 = 0.0
                s2 = 0.0
                w = 0.0
                for m in xrange(1,l+1):
                    i3 = l - m + 1
                    val = float(dataList[i3-1])
                    s2 += val * val
                    s1 += val
                    w += 1
                    v = s2 - (s1 * s1) / w
                    i4 = i3 - 1
                    if i4 != 0:
                        for j in xrange(2,numClass+1):
                            if mat2[l][j] >= (v + mat2[i4][j - 1]):
                                mat1[l][j] = i3
                                mat2[l][j] = v + mat2[i4][j - 1]  
                mat1[l][1] = 1
                mat2[l][1] = v         
            k = len(dataList)
            kclass = []
            for i in xrange(0,numClass+1):
                kclass.append(dataList[0])
            kclass[numClass] = float(dataList[-1])
            countNum = numClass
            while countNum >= 2:
                #print "rank = " + str(mat1[k][countNum])
                id = int((mat1[k][countNum]) - 2)
                #print "val = " + str(dataList[id])
                kclass[countNum - 1] = dataList[id]
                k = int((mat1[k][countNum] - 1))
                countNum -= 1
            return kclass
        #populate classes
        highthresh = 1000
        if len(sortedvalues) > highthresh:
            #the idea of using random sampling for large datasets came from a blogpost by Carson Farmer. I just added the idea of calculating the breaks several times and using the sample means for the final break values.
            #see: http://www.carsonfarmer.com/2010/09/adding-a-bit-of-classification-to-qgis/
            allrandomsamples = []
            samplestotake = 6
            for _ in xrange(samplestotake):
                randomsample = sorted(random.sample(sortedvalues, highthresh))
                randomsample[0] = lowerbound
                randomsample[-1] = upperbound
                tempbreaks = getJenksBreaks(randomsample, nrclasses)
                allrandomsamples.append(tempbreaks)
            jenksbreaks = [sum(allbreakvalues)/float(len(allbreakvalues)) for allbreakvalues in itertools.izip(*allrandomsamples)]
        else:
            jenksbreaks = getJenksBreaks(sortedvalues, nrclasses)
        breaksgen = (each for each in jenksbreaks[1:])
        classmin = lowerbound
        classes = []
        for index, classsymbol in enumerate(symbolrange):
            classmax = next(breaksgen)
            #determine min and max value
            minvalue = classmin
            maxvalue = classmax
            #create and add class
            classes.append( _SymbolClass(classmin, classmax, minvalue, maxvalue, index, classsymbol) )
            #prep for next
            classmin = classmax
        classification["classes"] = classes


def _CheckOptions(customoptions):
    #types
    customoptions = customoptions.copy()
    #paramaters
    if customoptions.get("fillcolor", "not specified") == "not specified":
        customoptions["fillcolor"] = Color("random")
    if not customoptions.get("fillsize"):
        customoptions["fillsize"] = 0.4
    if not customoptions.get("fillwidth"):
        customoptions["fillwidth"] = 1.2
    if not customoptions.get("fillheight"):
        customoptions["fillheight"] = 0.8
    if customoptions.get("outlinecolor", "not specified") == "not specified":
        customoptions["outlinecolor"] = Color("black")
    if not customoptions.get("outlinewidth"):
        customoptions["outlinewidth"] = 0.09 #percent of map
    return customoptions
def _CheckTextOptions(customoptions):
    customoptions = customoptions.copy()
    #text and font
    if not customoptions.get("textfont"):
        customoptions["textfont"] = "default"
    if not customoptions.get("textsize"):
        customoptions["textsize"] = MAPWIDTH*0.0055 #equivalent to textsize 7
    else:
        #input is percent textheight of MAPWIDTH
        percentheight = customoptions["textsize"]
        #so first get pixel height
        pixelheight = MAPWIDTH*percentheight
        #to get textsize
        textsize = int(round(pixelheight*0.86))
        customoptions["textsize"] = textsize
    if not customoptions.get("textcolor"):
        customoptions["textcolor"] = Color("black")
    if not customoptions.get("textopacity"):
        customoptions["textopacity"] = 255
    if not customoptions.get("texteffect"):
        customoptions["texteffect"] = None
    if not customoptions.get("textanchor"):
        customoptions["textanchor"] = "center"
    #text background box
    if not customoptions.get("textboxfillcolor"):
        customoptions["textboxfillcolor"] = None
    else:
        if customoptions.get("textboxoutlinecolor","not specified") == "not specified":
            customoptions["textboxoutlinecolor"] = Color("black")
    if not customoptions.get("textboxfillsize"):
        customoptions["textboxfillsize"] = 1.1 #proportion size of text bounding box
    if not customoptions.get("textboxoutlinecolor"):
        customoptions["textboxoutlinecolor"] = None
    if not customoptions.get("textboxoutlinewidth"):
        customoptions["textboxoutlinewidth"] = 1.0 #percent of fill, not of map
    if not customoptions.get("textboxopacity"):
        customoptions["textboxopacity"] = 0 #both fill and outline
    return customoptions
def _ScreenToWorldCoords(xy):
    """
Internal use only.
Converts a screen pixel coordinate to world coordinate, takes only a single pixel point
"""
    x,y = xy
    relx = x/float(MAPWIDTH)
    rely = y/float(MAPHEIGHT)
    worldxy = (XMIN+relx*XWIDTH, YMIN+(1-rely)*YHEIGHT)
    return worldxy

#QUICK TASKS
def ViewShapefile(shapefilepath, **customoptions):
    """
Quick task to visualize a shapefile and show it in a Tkinter window.

| __option__    | __description__ 
| --- | --- 
| shapefilepath | the path string of the shapefile.
| **customoptions | any series of named arguments of how to style the shapefile visualization (optional). Valid arguments are: fillcolor, fillsize (determines the circle size for point shapefiles, line width for line shapefiles, and has no effect for polygon shapefiles), outlinecolor, outlinewidth.
"""
    customoptions = _CheckOptions(customoptions)
    renderer = _Renderer()
    renderer.ViewShapefile(shapefilepath, customoptions)
def SaveShapefileImage(shapefilepath, savepath, **customoptions):
    """
Quick task to save a shapefile to an image.

| __option__    | __description__ 
| --- | --- 
| shapefilepath | the path string of the shapefile.
| savepath      | the path string of where to save the image, including the image type extension.
| **customoptions | any series of named arguments of how to style the shapefile visualization (optional). Valid arguments are: fillcolor, fillsize (determines the circle size for point shapefiles, line width for line shapefiles, and has no effect for polygon shapefiles), outlinecolor, outlinewidth.
"""
    customoptions = _CheckOptions(customoptions)
    renderer = _Renderer()
    renderer.SaveShapefileImage(shapefilepath, savepath, customoptions)

#MAP BUILDING
class NewMap:
    """
Creates and returns a new map based on previously defined mapsettings.

*Takes no arguments*
"""
    def __init__(self):
        self.renderer = _Renderer()
    def AddShape(self, shapeobj, **customoptions):
        """
This adds an individual shape instead of an entire file.

| __option__ | __description__ 
| --- | --- 
| shapeobj | a shape instance, currently it only works with the PyShpShape instances that are returned when looping through the geovis Shapefile instance
| **customoptions | any number of named arguments to style the shape
"""
        customoptions = _CheckOptions(customoptions)
        self.renderer._RenderShape(shapeobj, customoptions)
    def AddToMap(self, layer):
        """
Add and render a layer instance to the map.

| __option__ | __description__ 
| --- | --- 
| layer | the layer instance that you wish to add to the map
"""
        if layer.classifier:
            self._AutoClassifyShapefile(layer)
        else:
            self.renderer._RenderLayer(layer)
    def AddLegend(self, layer, upperleft, bottomright, legendtitle="not specified", boxcolor=Color("gray",brightness=0.8), boxoutlinecolor=Color("black"), boxoutlinewidth=0.08):
        """
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
"""
        classifier = layer.classifier
        #first set positions
        relx1,rely1 = upperleft
        relx2,rely2 = bottomright
        relxcenter = sum([relx1,relx2])/2.0
        relycenter = sum([rely1,rely2])/2.0
        xpad = 0.1
        ypad = 0.2
        legendwidth = (relx2-relx1)#*(1-xpad)
        legendheight = (rely2-rely1)#*(1-ypad)
        #multiple classifications are placed side by side
        allclassifications = classifier.GetClassifications()
        relxincr = legendwidth/float(len(allclassifications))
        #draw legendbox and title if any
        if boxcolor or boxoutlinecolor:
            boxoptions = dict([("fillcolor",boxcolor),
                               ("outlinecolor",boxoutlinecolor),
                               ("outlinewidth",boxoutlinewidth)])
            boxoptions = _CheckOptions(boxoptions)
            self.DrawRectangle(upperleft, bottomright, **boxoptions)
        if legendtitle:
            if legendtitle == "not specified":
                legendtitle = classifier.name
            titleoptions = dict([("textsize",0.023),
                                 ("textboxfillcolor",Color("white")),
                                 ("textboxfillsize",1.2),
                                 ("textanchor","s")])
            print("") #to fix weird tk text positioning error
            self.AddText(relxcenter, rely1, legendtitle, **titleoptions)
        #then...
        symbolizer = classifier.symbolizer
        relx = relx1+relxincr/2.0
        for classification in allclassifications:
            classes = classification.get("classes")
            symboltype = classification.get("symboltype")
            #classes are placed under each other
            relyincr = legendheight/float(len(classes)+2)
            #place symbol fieldname source
            rely = rely1+(relyincr/2.0)
            self.AddText(relx, rely, text=classification.get("valuefield"), textsize=0.0127, textboxfillcolor=None, textboxoutlinecolor=None)
            #place symboltype text
            rely += relyincr/2.0
            self.AddText(relx, rely, text="(%s)"%symboltype, textsize=0.0127, textboxfillcolor=None, textboxoutlinecolor=None)
            rely += relyincr/2.0
            tempwidth = relxincr
            xtox = (relx-tempwidth/2.0,relx+tempwidth/2.0)
            ytoy = (rely,rely+relyincr)
            partitions = guihelper.PartitionSpace(xtox,ytoy,partitions=2,padx=0.02,pady=0,direction="horizontal")
            leftpart,rightpart = partitions
            #place each class symbol and label text
            for eachclass in reversed(classes):
                symbol = eachclass.classsymbol
                if symboltype == "fillcolor":
                    tempwidth = (relx+relxincr-relx)
                    classupperleft = (leftpart.w[0],rely)
                    classbottomright = (leftpart.e[0],rely+relyincr)
                    self.DrawRectangle(classupperleft, classbottomright, fillcolor=symbol)
                    #place label text
                    if eachclass.min != eachclass.max:
                        textlabel = "%s - %s" %(eachclass.min,eachclass.max)
                    else:
                        textlabel = "%s" %eachclass.min
                    self.AddText(rightpart.center[0],rely+relyincr/2.0,text=textlabel, textsize=0.0111)
                elif symboltype == "fillsize":
                    if symbolizer:
                        if symbolizer == "circle":
                            tempoptions = _CheckOptions(dict(fillsize=symbol, fillcolor=None, symbolizer=symbolizer))
                            symbolheight = self.renderer._RelSizesToPixels(tempoptions)["fillsize"]/float(MAPHEIGHT)
                            temprelx,temprely = (leftpart.center[0], rely+relyincr*len(classes)-symbolheight/2.0)
                            xy = [[_ScreenToWorldCoords((temprelx*MAPWIDTH, temprely*MAPHEIGHT))]]
                            shape = _PyShpShape(shapefile=None, fieldnames=None, uniqid=None, coords=xy, shapetype="point")
                            self.renderer._RenderShape(shape, tempoptions)
                            rely -= relyincr
                            #place label text
                            if eachclass.min != eachclass.max:
                                textlabel = "%s - %s" %(eachclass.min,eachclass.max)
                            else:
                                textlabel = "%s" %eachclass.min
                            self.AddText(rightpart.center[0], rely+relyincr*(len(classes)+1)-symbolheight, text=textlabel, textsize=0.0111)
                        elif symbolizer == "square":
                            tempoptions = _CheckOptions(dict(fillsize=symbol, fillcolor=None, symbolizer=symbolizer))
                            symbolheight = self.renderer._RelSizesToPixels(tempoptions)["fillsize"]/float(MAPHEIGHT)
                            temprelx,temprely = (leftpart.center[0], rely+relyincr*len(classes)-symbolheight/2.0)
                            xy = [[_ScreenToWorldCoords((temprelx*MAPWIDTH, temprely*MAPHEIGHT))]]
                            shape = _PyShpShape(shapefile=None, fieldnames=None, uniqid=None, coords=xy, shapetype="point")
                            self.renderer._RenderShape(shape, tempoptions)
                            rely -= relyincr
                            #place label text
                            if eachclass.min != eachclass.max:
                                textlabel = "%s - %s" %(eachclass.min,eachclass.max)
                            else:
                                textlabel = "%s" %eachclass.min
                            self.AddText(rightpart.center[0], rely+relyincr*(len(classes)+1)-symbolheight, text=textlabel, textsize=0.0111)
                        elif symbolizer == "pyramid":
                            tempoptions = _CheckOptions(dict(fillsize=symbol, fillcolor=None, symbolizer=symbolizer))
                            symbolheight = self.renderer._RelSizesToPixels(tempoptions)["fillsize"]/float(MAPHEIGHT)
                            temprelx,temprely = (leftpart.center[0], rely+relyincr*len(classes))
                            xy = [[_ScreenToWorldCoords((temprelx*MAPWIDTH, temprely*MAPHEIGHT))]]
                            shape = _PyShpShape(shapefile=None, fieldnames=None, uniqid=None, coords=xy, shapetype="point")
                            self.renderer._RenderShape(shape, tempoptions)
                            rely -= relyincr
                            #place label text
                            if eachclass.min != eachclass.max:
                                textlabel = "%s - %s" %(eachclass.min,eachclass.max)
                            else:
                                textlabel = "%s" %eachclass.min
                            self.AddText(rightpart.center[0], rely+relyincr*(len(classes)+1)-symbolheight, text=textlabel, textsize=0.0111)
                    else:
                        tempoptions = _CheckOptions(dict(fillsize=symbol, fillcolor=None, symbolizer=symbolizer))
                        symbolheight = self.renderer._RelSizesToPixels(tempoptions)["fillsize"]/float(MAPHEIGHT)
                        temprelx,temprely = (leftpart.center[0], rely+relyincr*len(classes)-symbolheight/2.0)
                        xy = [[_ScreenToWorldCoords((temprelx*MAPWIDTH, temprely*MAPHEIGHT))]]
                        shape = _PyShpShape(shapefile=None, fieldnames=None, uniqid=None, coords=xy, shapetype="point")
                        self.renderer._RenderShape(shape, tempoptions)
                        rely -= relyincr
                        #place label text
                        if eachclass.min != eachclass.max:
                            textlabel = "%s - %s" %(eachclass.min,eachclass.max)
                        else:
                            textlabel = "%s" %eachclass.min
                        self.AddText(rightpart.center[0], rely+relyincr*(len(classes)+1)-symbolheight, text=textlabel, textsize=0.0111)
                elif symboltype == "outlinecolor":
                    tempwidth = (relx+relxincr-relx)/3.0
                    startpos, endpos = ((leftpart.w[0],rely+relyincr/2.0),(leftpart.e[0],rely+relyincr/2.0))
                    self.DrawLine(startpos, endpos, fillcolor=symbol)
                    #place label text
                    if eachclass.min != eachclass.max:
                        textlabel = "%s - %s" %(eachclass.min,eachclass.max)
                    else:
                        textlabel = "%s" %eachclass.min
                    self.AddText(rightpart.center[0],rely+relyincr/2.0,text=textlabel, textsize=0.0111)
                elif symboltype == "outlinewidth":
                    tempwidth = (relx+relxincr-relx)/3.0
                    startpos, endpos = ((leftpart.w[0],rely+relyincr/2.0),(leftpart.e[0],rely+relyincr/2.0))
                    self.DrawLine(startpos, endpos, fillcolor=Color("black"), fillsize=symbol)
                    #place label text
                    if eachclass.min != eachclass.max:
                        textlabel = "%s - %s" %(eachclass.min,eachclass.max)
                    else:
                        textlabel = "%s" %eachclass.min
                    self.AddText(rightpart.center[0],rely+relyincr/2.0,text=textlabel, textsize=0.0111)
                rely += relyincr
            relx += relxincr
    def AddText(self, relx, rely, text, **textoptions):
        """
Writes text on the map.

| __option__ | __description__ 
| --- | --- 
| relx | the relative x position of the text's centerpoint, a float between 0-1
| rely | the relative y position of the text's centerpoint, a float between 0-1
| text | the text to add to the map, as a string
| **customoptions | any number of named arguments to style the text
"""
        textoptions = _CheckTextOptions(textoptions)
        self.renderer._RenderText(relx, rely, text, textoptions)
    def DrawRectangle(self, upperleft, bottomright, **customoptions):
        """
Draws a rectangle on the map.

| __option__ | __description__ 
| --- | --- 
| upperleft | the upperleft corner of the rectangle as a list or tuple of the relative x and y position, each a float between 0-1
| bottomright | the bottomright corner of the rectangle as a list or tuple of the relative x and y position, each a float between 0-1
| **customoptions | any number of named arguments to style the rectangle
"""
        customoptions = _CheckOptions(customoptions)
        self.renderer._RenderRectangle(upperleft, bottomright, customoptions)
    def DrawCircle(self, relx, rely, fillsize, **customoptions):
        """
Draws a circle on the map.

| __option__ | __description__ 
| --- | --- 
| relx | the relative x position of the circle's centerpoint, a float between 0-1
| rely | the relative y position of the circle's centerpoint, a float between 0-1
| **customoptions | any number of named arguments to style the line
"""
        customoptions = _CheckOptions(customoptions)
        self.renderer._RenderCircle(relx, rely, fillsize, customoptions)
    def DrawLine(self, startpos, stoppos, **customoptions):
        """
Draws a line on the map.

| __option__ | __description__ 
| --- | --- 
| startpos | a list or tuple of the relative x and y position where the line should start, each a float between 0-1
| stoppos | a list or tuple of the relative x and y position where the line should end, each a float between 0-1
| **customoptions | any number of named arguments to style the line
"""
        customoptions = _CheckOptions(customoptions)
        self.renderer._RenderLine(startpos, stoppos, customoptions)
    def ViewMap(self):
        """
View the created map embedded in a Tkinter window. Map image can be panned, but not zoomed. Offers a 'save image' button to allow to interactively save the image.

*Takes no arguments*
"""
        self.renderer._ViewRenderedShapefile()
    def SaveMap(self, savepath):
        """
Save the map to an image file.

| __option__ | __description__ 
| --- | --- 
| savepath | the string path for where you wish to save the map image. Image type extension must be specified ('.png','.gif',...)
"""
        self.renderer._SaveRenderedShapefile(savepath)
    ###INTERNAL USE ONLY
    def _AutoClassifyShapefile(self, layer):
        shapefilepath = layer.filepath
        classifier = layer.classifier
        options = layer.customoptions
        ####CLASSIFY ONE SHAPEFILE OPTION
        allclassifications = classifier.allclassifications
        #create shapefile
        shapefile = layer.fileobj
        classifier.name = shapefile.filename
        classifier.symbolizer = options.get("symbolizer")
        #exclude values if specified
        excludequery = options.get("excludequery")
        if excludequery:
            shapefile.SelectByQuery(excludequery, inverted=True)
        #classify values into symbols
        shapefile.progresstext = "classifying"
        #first populate values from classification fields
        for eachshape in shapefile:
            row = dict(zip(shapefile.fieldnames, eachshape.GetAttributes()))
            for classification in allclassifications:
                field_to_classify = classification["valuefield"]
                attributevalue = row[field_to_classify]
                classifier.AddValue(eachshape.id, classification["symboltype"], attributevalue)
        #then calculate classes
        for classification in allclassifications:
            classifier.CalculateClasses(classification)
        #then send classifier to renderer so can remember its layer and legend properties
        self.renderer._AddLayerInfo(shapefile.filename, classifier)
        ####RENDER THAT CLASSIFIED SHAPEFILE
        #loop sorted/classified ids and get and render each
        shapefile.progresstext = "rendering shapes"
        for shape in shapefile:
            classificationsuccess = False
            #populate a custom options dict based on classifications
            for classification in allclassifications:
                symboltype = classification["symboltype"]
                #retrieve class color for each shape id
                symbol = classifier.GetSymbol(shape.id, symboltype)
                if symbol:
                    options[symboltype] = symbol
                    classificationsuccess = True #as long as at least one classification was successful it will display it later, but only those shapes that were not excluded will be given symbols based on classification algorithm (the rest will only use default)
            #render only if at least one of the options were successful
            if classificationsuccess:
                self.renderer._RenderShape(shape, options)

        ####OR RENDER IN SORTED ORDER (NEED TO ADD CUSTOM SHAPE RENDERING ORDER AND SPECIAL SHAPE CACHING TO FILE BEFORE USING THIS BC GRABBING ONE SHAPE AT A TIME IS CURRENTLY QUITE SLOW)
        "finish this later..."
##        #loop sorted/classified ids and get and render each
##        for uniqid, value in messages.ProgressReport(classifier.GetValues(), text="rendering shapes"):
##            #populate a custom options dict based on classifications
##            for classification in allclassifications:
##                symboltype = classification["symboltype"]
##                #retrieve class color for each shape id
##                symbol = classifier.GetSymbol(uniqid, symboltype)
##                if symbol:
##                    options[symboltype] = symbol
##            #render only if at least one of the options were successful
##            if options:
##                shape = shapefile.GetShape(uniqid)
##                self.renderer._RenderShape(shape, options)

        ####FINALLY ADD LABELS FOR THAT SHAPEFILE
        "need more work here........."
##        #loop through shapefile
##        shapefile.progresstext = "adding labels"
##        for eachshape in shapefile:
##            #populate a custom options dict based on classifications
##            for classification in allclassifications:
##                symboltype = classification["symboltype"]
##                #retrieve class color for each shape id
##                symbol = classifier.GetSymbol(eachshape.id, symboltype)
##                if symbol:
##                    options[symboltype] = symbol
##            #render only if at least one of the options were successful
##            if options:
##                #LABEL TEXT
##                textoptions = _CheckTextOptions(dict([("textsize",20)]))
##                x,y = eachshape._MapCoords([eachshape.GetCenter()])
##                relx, rely = (x/float(MAPWIDTH), y/float(MAPHEIGHT))
##                self.AddText(relx, rely, str(eachshape.id), **textoptions)


#MAP SPECS
def SetMapDimensions(width, height):
    """
Sets the width and height of the next map image. At startup the width and height are set to the dimensions of the window screen.

| __option__ | __description__ 
| --- | --- 
| width | the pixel width of the final map image to be rendered, an integer.
| height | the pixel height of the final map image to be rendered, an integer.
"""
    global MAPWIDTH, MAPHEIGHT
    MAPWIDTH = width
    MAPHEIGHT = height
    _UpdateMapDims()
def SetMapBackground(mapbackground):
    """
Sets the mapbackground of the next map to be made. At startup the mapbackground is transparent (None).

| __option__ | __description__ 
| --- | --- 
| mapbackground | takes a hex color string, as can be created with the Color function. It can also be None for a transparent background (default).
"""
    global MAPBACKGROUND
    MAPBACKGROUND = mapbackground
def SetMapZoom(x2x, y2y):
    """
Zooms the map to the given mapextents.

| __option__ | __description__ 
| --- | --- 
| x2x | a two-item list of the x-extents in longitude format, from the leftmost to the rightmost longitude, default is full extent [-180, 180]
| y2y | a two-item list of the y-extents in latitude format, from the bottommost to the topmost latitude, default is full extent [-90, 90]
"""
    global XMIN,XMAX,YMIN,YMAX
    XMIN,XMAX = (x2x[0],x2x[1])
    YMIN,YMAX = (y2y[0],y2y[1])
    global XWIDTH,YHEIGHT,XOFFSET,YOFFSET
    inxwidth = XMAX-XMIN
    inyheight = YMAX-YMIN
    #SUMTIN WEIRD, BOTH ZOOMS NEED TO BE TRUE AND MAYBE CHANGED, NOT JUST ONE, SO MAYBE ALWAYS TIMES UP AND NEVER DIVIDE DOWN
    if inxwidth > inyheight*PROJ_XYRATIO:
        #automatically override xlimits to be centered middle of given extents, but with a new width thats proportional to the projection widt/height ratio
        midx = sum(x2x)/float(len(x2x))
        halfxwidth = inyheight/PROJ_XYRATIO/2.0
        XMIN,XMAX = (midx-halfxwidth, midx+halfxwidth)
    elif inyheight*PROJ_XYRATIO > inxwidth:
        #automatically override ylimits to be centered middle of given extents, but with a new height thats proportional to the projection widt/height ratio
        midy = sum(y2y)/float(len(y2y))
        halfyheight = inxwidth/PROJ_XYRATIO/2.0
        YMIN,YMAX = (midy-halfyheight, midy+halfyheight)
    nw = (-1*min(x2x),max(y2y))
    #cant use old width/height from original input but instead recalculate using the updated X/YMAX/MIN bc they were changed to preserve a certain ratio
    XWIDTH = XMAX-XMIN
    YHEIGHT = YMAX-YMIN
    XOFFSET = nw[0]
    YOFFSET = nw[1]
    _UpdateMapDims()


### END OF SCRIPT ###

    
