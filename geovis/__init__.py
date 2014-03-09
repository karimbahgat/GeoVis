"""
Python Geographic Visualizer (GeoVis)

A complete geographic visualization module for the Python programming language
intended for easy everyday-use by novices and power-programmers alike.
It has one-liners for quickly visualizing a shapefile,
building and styling basic maps with multiple shapefile layers,
and/or saving to imagefiles. Uses the built-in Tkinter
or other third-party rendering modules to do its main work.
The current version is functional, but should be considered
a work in progress with potential bugs, so use with care.

Dependencies: None, but it is recommended to have Aggdraw, PIL, or PyCairo.
System Compatibility: Python version 2.x and Windows. 
License: Creative Commons Attribution-ShareAlike (CC BY-SA). For more details see: http://creativecommons.org/licenses/by-sa/4.0/

Author: Karim Bahgat (karim.bahgat.norway<at>gmail.com)
Homepage: https://github.com/karimbahgat/geovis
Date: February 21, 2014
"""
__version__ = "0.2.0"

# IMPORTS
#builtins
import sys, os, itertools, array, threading, random, math, platform, operator
import Tkinter as tk
#customized
import messages, listy
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
#set mapdims to window size
mapdimstest = tk.Tk()
MAPWIDTH = int(mapdimstest.winfo_screenwidth())
MAPHEIGHT = int(mapdimstest.winfo_screenheight())
mapdimstest.destroy()
del mapdimstest
#update mapdims
def _UpdateMapDims():
    if NUMPYSPEED:
        global ZOOMDIM, OFFSET, TRANSLATION, RENDERAREA, SCALING
        ZOOMDIM = numpy.array([360.0,180.0])
        OFFSET = numpy.array([0.0,0.0])*-1 #move x or y by normal +- coordinates (not compat with zoom yet
        TRANSLATION = numpy.array([180.0, -90.0]) + OFFSET
        RENDERAREA = numpy.array([MAPWIDTH, -MAPHEIGHT])
        SCALING = RENDERAREA / ZOOMDIM
    else:
        global XOFFSET, YOFFSET, XWIDTH, YHEIGHT
        XOFFSET = 180
        YOFFSET = 90
        XWIDTH = 360
        YHEIGHT = 180
_UpdateMapDims()
#define colorstyles
COLORSTYLES = dict([("strong", dict( [("intensity",1), ("brightness",0.5)]) ),
                    ("dark", dict( [("intensity",0.8), ("brightness",0.2)]) ),
                    ("matte", dict( [("intensity",0.4), ("brightness",0.2)]) ),
                ("bright", dict( [("intensity",0.8), ("brightness",0.7)] ) ),
                ("pastelle", dict( [("intensity",0.5), ("brightness",0.6)] ) )
                    ])


# INTERNAL CLASSES
class _PyShpShape:
    def __init__(self, shapefile, fieldnames, uniqid, coords, shapetype):
        "every shapetype is always multi (upon entry) so have to be looped through when retrieved."
        self._shapefile = shapefile
        self.fieldnames = fieldnames
        self.id = uniqid
        self.coords = coords
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
    def GetCenter(self):
        "so far only simple nonnumpy"
        for single in self.coords:
            xs = [xy[0] for xy in single]
            xmid = sum(xs)/float(len(xs))
            ys = [xy[1] for xy in single]
            ymid = sum(ys)/float(len(ys))
            return (xmid,ymid)
    #internal use only
    def __pairwise(self, coords, batchsize=2):
        "only used when sending coordinates to pycairo, bc can only draw as a path one xy point at a time"
        return [pair for pair in itertools.izip(*[iter(coords)] * batchsize)]
    def _MapCoords(self, incoords):
        "takes single set of coords, not multicoords"
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
    def __init__(self, shapefilepath, showprogress="not specified", progresstext="looping shapefile"):
        self.shapefile = pyshp.Reader(shapefilepath)
        self.showprogress = showprogress
        self.progresstext = progresstext
        name = ".".join(shapefilepath.split(".")[:-1])
        name = name.split("\\")[-1]
        self.filename = name
        self.fieldnames = [fieldinfo[0] for fieldinfo in self.shapefile.fields[1:]]
    def __len__(self):
        return self.shapefile.numRecords
    def __iter__(self):
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
                yield self._PrepShape(shapeindex, shape)
        else:
            for shapeindex, shape in enumerate(SHAPEFILELOOP):
                SHAPEFILELOOP.Increment()
                yield self._PrepShape(shapeindex, shape)
    def GetShape(self, shapeindex):
        shape = self.shapefile.shape(shapeindex, numpyspeed=NUMPYSPEED)
        return self._PrepShape(shapeindex, shape)
    def _PrepShape(self, shapeindex, shape):
        if NUMPYSPEED:
            shapetype = PYSHPTYPE_AS_TEXT[shape.shapeType].lower()
            if "polygon" in shapetype:
                if not numpy.any(shape.parts):
                    nestedcoords = [shape.points]
                    return _PyShpShape(self.shapefile, self.fieldnames, shapeindex, nestedcoords, shapetype)
                else:
                    coords = numpy.split(shape.points, shape.parts[1:])
                    return _PyShpShape(self.shapefile, self.fieldnames, shapeindex, coords, "polygon")
            elif "line" in shapetype:
                if not numpy.any(shape.parts):
                    nestedcoords = [shape.points]
                    return _PyShpShape(self.shapefile, self.fieldnames, shapeindex, nestedcoords, shapetype)
                else:
                    coords = numpy.split(shape.points, shape.parts[1:])
                    return _PyShpShape(self.shapefile, self.fieldnames, shapeindex, coords, "line")
            elif "point" in shapetype:
                if "multi" in shapetype:
                    return _PyShpShape(self.shapefile, self.fieldnames, shapeindex, shape.points, "point")
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
        """this must be called before doing any rendering.\
        Note: this replaces any previous image drawn on so be sure to
        retrieve the old image before calling it again to avoid losing work"""
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
            x0,y0,x1,y1 = ( -int(width/50.0), int(height/50.0), width-int(width/50.0), height+int(height/50.0) )
            self.drawer.create_rectangle(x0,y0,x1,y1, fill="Gray18", outline="")
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
    def RenderShape(self, shapeobj, options):
        "looks at instructions in options to decide which draw method to use"
        multishapes = shapeobj.to_tkinter()
        for coords in multishapes:
            if shapeobj.type == "polygon":
                self._BasicPolygon(coords, options)
            elif shapeobj.type == "line":
                self._BasicLine(coords, options)
            elif shapeobj.type == "point":
                self._BasicCircle(coords, options)
    def RunTk(self):
        self.window.mainloop()

    #Internal use only
    def _BasicText(self, relx, rely, text, options):
        "draws basic text, no effects"
        font = tkFont.Font(family=self.fontnames[options["textfont"]], size=options["textsize"])
        x = int(MAPWIDTH*relx)
        y = int(MAPHEIGHT*rely)
        self.drawer.create_text((x,y), text=text, font=font, fill=options["textcolor"], anchor="center")
    def _BasicLine(self, coords, options):
        "draw basic lines with outline, but nothing at start and end"
        if len(coords) < 4:
            return
        #first draw outline line
        self.drawer.create_line(*coords, fill=options.get("outlinecolor"), width=int(options.get("fillsize")+(options.get("outlinewidth")*2)))
        #then draw fill line which is thinner
        self.drawer.create_line(*coords, fill=options.get("fillcolor"), width=int(options.get("fillsize")))
    def _BasicPolygon(self, coords, options):
        "draw polygon with color fill"
        if len(coords) > 6:
            self.drawer.create_polygon(*coords, fill=options["fillcolor"], outline=options["outlinecolor"])
    def _BasicCircle(self, coords, options):
        "draw points with a symbol path representing a circle"
        size = int(options["fillsize"]/2.0)
        x,y = coords
        circlecoords = (x-size, y-size, x+size, y+size)
        self.drawer.create_oval(circlecoords, fill=options["fillcolor"], outline=options["outlinecolor"])

class _PIL_Renderer:
    "this class can be called on to draw each feature with PIL as long as \
    it is given instructions via a color/size/options dictionary"
    #NEED TO RECEIVE GENERATOR OF TRANSFORMED COORDS FROM MAPCANVAS
    #ALSO NEEDS THE Aggdraw.Draw(img) OBJECT
    def __init__(self):
        global PIL
        import PIL, PIL.Image, PIL.ImageDraw, PIL.ImageTk, PIL.ImageFont
        self.sysfontfolders = dict([("windows","C:/Windows/Fonts/")])
        self.fontfilenames = dict([("default", "TIMES.TTF"),
                                   ("times new roman","TIMES.TTF"),
                                   ("arial","ARIAL.TTF")])
    def NewImage(self):
        """this must be called before doing any rendering.\
        Note: this replaces any previous image drawn on so be sure to
        retrieve the old image before calling it again to avoid losing work"""
        #first mode
        mode = "RGBA"
        #then other specs
        width = MAPWIDTH
        height = MAPHEIGHT
        background = MAPBACKGROUND
        dimensions = (width, height)
        self.img = PIL.Image.new(mode, dimensions, background)
        self.drawer = PIL.ImageDraw.Draw(self.img)
    def RenderText(self, relx, rely, text, options):
        if not options.get("texteffect"):
            self._BasicText(relx, rely, text, options)
    def RenderShape(self, shapeobj, options):
        "looks at instructions in options to decide which draw method to use"
        #possibly use an options filterer here to enure all needed options
        #are given, otherwise snap to default
        #............
        multishapes = shapeobj.to_PIL()
        for coords in multishapes:
            if shapeobj.type == "polygon":
                self._BasicPolygon(coords, options)
            elif shapeobj.type == "line":
                self._BasicLine(coords, options)
            elif shapeobj.type == "point":
                self._BasicCircle(coords, options)
    def GetImage(self):
        return PIL.ImageTk.PhotoImage(self.img)
    def SaveImage(self, savepath):
        self.img.save(savepath)

    #Internal use only
    def _BasicText(self, relx, rely, text, options):
        "draws basic text, no effects"
        fontlocation = self.sysfontfolders[OSSYSTEM]+self.fontfilenames[options["textfont"]]
        font = PIL.ImageFont.truetype(fontlocation, size=options["textsize"])
        fontwidth, fontheight = self.drawer.textsize(text, font)
        x = int(MAPWIDTH*relx) - int(fontwidth/2.0)
        y = int(MAPHEIGHT*rely) - int(fontheight/2.0)
        self.drawer.text((x,y), text=text, font=font, fill=options["textcolor"])
    def _BasicLine(self, coords, options):
        "draw basic lines with outline, but nothing at start and end"
        #first draw outline line
        self.drawer.line(coords, fill=options.get("outlinecolor"), width=int(options.get("fillsize")+(options.get("outlinewidth")*2)))
        #then draw fill line which is thinner
        self.drawer.line(coords, fill=options.get("fillcolor"), width=int(options.get("fillsize")))
    def _BasicPolygon(self, coords, options):
        "draw polygon with color fill"
        if len(coords) > 6:
            self.drawer.polygon(coords, fill=options["fillcolor"], outline=options["outlinecolor"])
    def _BasicCircle(self, coords, options):
        "draw points with a symbol path representing a circle"
        size = int(options["fillsize"]/2.0)
        x,y = coords
        circlecoords = (x-size, y-size, x+size, y+size)
        self.drawer.ellipse(circlecoords, fill=options["fillcolor"], outline=options["outlinecolor"])
    def _Dot(self, coords):
        self.drawer.point(coords, "black")

class _Aggdraw_Renderer:
    "this class can be called on to draw each feature with aggdraw as long as \
    it is given instructions via a color/size/options dictionary"
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
        """this must be called before doing any rendering.\
        Note: this replaces any previous image drawn on so be sure to
        retrieve the old image before calling it again to avoid losing work"""
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
        "looks at instructions in options to decide which draw method to use"
        multishapes = shapeobj.to_aggdraw()
        for coords in multishapes:
            if shapeobj.type == "polygon":
                self._BasicPolygon(coords, options)
            elif shapeobj.type == "line":
                self._BasicLine(coords, options)
            elif shapeobj.type == "point":
                self._BasicCircle(coords, options)
    def RenderText(self, relx, rely, text, options):
        if not options.get("texteffect"):
            self._BasicText(relx, rely, text, options)
    def GetImage(self):
        self.drawer.flush()
        return PIL.ImageTk.PhotoImage(self.img)
    def SaveImage(self, savepath):
        self.drawer.flush()
        self.img.save(savepath)

    #Internal use only
    def _BasicText(self, relx, rely, text, options):
        "draws basic text, no effects"
        fontlocation = self.sysfontfolders[OSSYSTEM]+self.fontfilenames[options["textfont"]]
        font = aggdraw.Font(color=options["textcolor"], file=fontlocation, size=options["textsize"], opacity=options["textopacity"])
        fontwidth, fontheight = self.drawer.textsize(text, font)
        x = int(MAPWIDTH*relx) - int(fontwidth/2.0)
        y = int(MAPHEIGHT*rely) - int(fontheight/2.0)
        self.drawer.text((x,y), text, font)
    def _BasicLine(self, coords, options):
        "draw basic lines with outline, but nothing at start and end"
        #first draw outline line
        outlinepen = aggdraw.Pen(options["outlinecolor"], options["fillsize"]+options["outlinewidth"])
        self.drawer.line(coords, outlinepen)
        #then draw fill line which is thinner
        fillpen = aggdraw.Pen(options["fillcolor"], options["fillsize"])
        self.drawer.line(coords, fillpen)
    def _BasicPolygon(self, coords, options):
        "draw polygon with color fill"
        outlinepen = aggdraw.Pen(options["outlinecolor"], options["outlinewidth"])
        fillbrush = aggdraw.Brush(options["fillcolor"])
        self.drawer.polygon(coords, fillbrush, outlinepen)
        pass
    def _BasicCircle(self, coords, options):
        "draw points with a symbol path representing a circle"
        #build circle
        size = int(options["fillsize"]/2.0)
        x,y = coords
        circlecoords = (x-size, y-size, x+size, y+size)
        #set symbol options
        outlinepen = aggdraw.Pen(options["outlinecolor"], options["outlinewidth"])
        fillbrush = aggdraw.Brush(options["fillcolor"])
        #draw
        self.drawer.ellipse(circlecoords, fillbrush, outlinepen)

class _PyCairo_Renderer:
    "this class can be called on to draw each feature with PIL as long as \
    it is given instructions via a color/size/options dictionary"
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
        """this must be called before doing any rendering.\
        Note: this replaces any previous image drawn on so be sure to
        retrieve the old image before calling it again to avoid losing work"""
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
    def RenderShape(self, shapeobj, options):
        "looks at instructions in options to decide which draw method to use"
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
        self.img.write_to_gif("tempgif.gif")
        gifimg = tk.PhotoImage("tempgif.gif")
        os.remove("tempgif.gif")
        return gifimg
    def SaveImage(self, savepath):
        if savepath.endswith(".png"):
            self.img.write_to_png(savepath)

    #Internal use only
    def __hex_to_rgb(self, hexcolor):
        return colour.Color(hexcolor).rgb
    def _BasicText(self, relx, rely, text, options):
        "draws basic text, no effects"
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
        "draw basic lines with outline, but nothing at start and end"
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
            outlinecolor = self.__hex_to_rgb(options["fillcolor"])
            self.drawer.set_source_rgb(*outlinecolor) # Solid color
            self.drawer.set_line_width(options.get("fillsize"))
            #then draw fill line which is thinner
            xy = coords[0]
            self.drawer.move_to(*xy)
            for xy in coords[1:]:
                self.drawer.line_to(*xy)
            self.drawer.stroke_preserve()
    def _BasicPolygon(self, coords, options):
        "draw polygon with color fill"
        if len(coords) >= 6:
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
    def _RenderMapTitle(self, shapefilepath, customoptions):
        #unless not specified, default maptitle is set to name of shapefile
        if customoptions.get("maptitle", "not set") == "not set":
            shapefilename = shapefilepath.split("\\")[-1]
            shapefilename = ".".join(shapefilename.split(".")[:-1])
            customoptions["maptitle"] = shapefilename
        #unless asked not to show maptitle, generate default textoptions except large text size
        if customoptions.get("maptitle"):
            textoptions = _CheckTextOptions(dict([("textsize",50)]))
            self._RenderText(0.5, 0.05, customoptions["maptitle"], textoptions)
    def _RenderText(self, relx, rely, text, textoptions):
        self.renderer.RenderText(relx, rely, text, textoptions)
    def _RenderShape(self, shape, customoptions):
        self.renderer.RenderShape(shape, customoptions)
    def _RenderShapefile(self, shapefilepath, customoptions):
        #create shapefile generator
        shapefile = Shapefile(shapefilepath, progresstext="rendering")
        #then iterate through shapes and render each
        for eachshape in shapefile:
            #then send to be rendered
            self._RenderShape(eachshape, customoptions)
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
                screenwidth = window.winfo_screenwidth()
                if MAPWIDTH >= screenwidth:
                    window.wm_state('zoomed')
                #embed image in a canvas
                tkimg = self.renderer.GetImage()
                canvas = tk.Canvas(window_frame, width=MAPWIDTH, height=MAPHEIGHT, bg="white")
                canvas.pack()
                x0,y0,x1,y1 = ( -int(MAPWIDTH/50.0), int(MAPHEIGHT/50.0), MAPWIDTH-int(MAPWIDTH/50.0), MAPHEIGHT+int(MAPHEIGHT/50.0) )
                if MAPBACKGROUND:
                    canvas.create_rectangle(x0,y0,x1,y1, fill="Gray15", outline="") #this is the shadow
                canvas.create_image(0,0, anchor="nw", image=tkimg)
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
                import tkFileDialog
                def imagesavefiledialog():
                    savepath = tkFileDialog.asksaveasfilename()
                    self._SaveRenderedShapefile(savepath)
                savebutton = tk.Button(window_frame, text="Save Image", command=imagesavefiledialog)
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

#GENERAL UTILITIES
def _FolderLoop(folder, filetype=""):
    "a generator that iterates through all files in a folder tree, either in a for loop or by using next() on it.\
    Filetype can be set to only grab files that have the specified file-extension. If filetype is a tuple then grabs all filetypes listed within it."
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
    """A generator that will loop through a folder and all its subfolder and return information of every shapefile it finds. Information returned is a tuple with the following elements (string name of current subfolder, string name of shapefile found, string of the shapefile's file extension(will always be '.shp'))\
    -folder is a path string of the folder to check for shapefiles."""
    for eachfolder, eachshapefile, eachfiletype in _FolderLoop(folder, filetype=".shp"):
        yield (eachfolder, eachshapefile, eachfiletype)
        
#RENDERING OPTIONS
def SetRenderingOptions(renderer="not set", numpyspeed="not set", reducevectors="not set"):
    """Sets certain rendering options that apply to all visualizations or map images.
    -renderer is a string describing which Python module will be used for rendering. This means you need to have the specified module installed. Valid renderer values are 'aggdraw' (default), 'PIL', 'pycairo', 'tkinter'. Notes: If you have no renderers installed, then use Tkinter which comes with all Python installations, be aware that it is significantly slow, memory-limited, and cannot be used to save images. Currently PyCairo is not very well optimized, and is particularly slow to render line shapefiles. 
    -numpyspeed specifies whether to use numpy to speed up shapefile reading and coordinate-to-pixel conversion. Must be True (default) or False.
    -reducevectors specifies whether to reduce the number of vectors to be rendered. This can speed up rendering time, but may lower the quality of the rendered image, especially for line shapefiles. Must be True or False (default)."""
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
def Color(basecolor="random", intensity="not specified", brightness="not specified", style=None):
    """Returns a hex color string of the color options specified.
    NOTE: changes with randomizing colors...
    -basecolor is the human-like name of a color.
    -intensity of how strong the color should be. Must be a float between 0 and 1 (default is random).
    -brightness of how light or dark the color should be. Must be a float between 0 and 1 (default is random).
    -style is a named style that overrides the brightness and intensity options (optional). Valid style names are: strong', 'dark', 'matte', 'bright', 'pastelle'."""
    #first check on intens/bright
    if style:
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
        basecolor = random.randrange(100)
        return colour.Color(pick_for=basecolor, saturation=intensity, luminance=brightness).hex
    else:
        #custom made color
        return colour.Color(color=basecolor, saturation=intensity, luminance=brightness).hex

class _ColorGradient:
    """A generator that yields n colors between N end-points.
    Each colorstop must be a hex color as made by the Color() function"""
    def __init__(self, *colorstops):
        #convert colorstops from hex to rgb to hsl
        self.colorstops = [colour.rgb2hsl(colour.hex2rgb(eachcolor)) for eachcolor in colorstops]
    def GetColors(self, nrcolors):
        #then build final colorrange
        hsl_colorrange = listy.Resize(self.colorstops, nrcolors, dtype="hsl")
        #then iterate through results
        for hsl in hsl_colorrange:
            to_hex = colour.rgb2hex(colour.hsl2rgb(hsl))
            yield to_hex

class _SymbolClass:
    def __init__(self, classmin, classmax, minvalue, maxvalue, classvalue, classsymbol):
        "_min and _max are not attr values meant for user, but used for membership determination internally and can be different from attr"
        self._min = classmin
        self._max = classmax
        self.min = minvalue
        self.max = maxvalue
        self.classvalue = classvalue
        self.classsymbol = classsymbol

class Classifier:
    def __init__(self):
        self.values = dict()
        self.symbols = dict()
        self.allclassifications = []
    def AddClassification(self, symboltype, valuefield, symbolrange, classifytype="equal interval", nrclasses=5, excludevalues=[]):
        classification = dict([("symboltype",symboltype),
                               ("valuefield",valuefield),
                               ("symbolrange",symbolrange),
                               ("classifytype",classifytype),
                               ("nrclasses",nrclasses),
                               ("excludevalues",excludevalues) ])
        self.allclassifications.append(classification)
    def AddValue(self, index, symboltype, value):
        if self.values.get(index):
            #add to dict if already exits
            self.values[index][symboltype] = value
        else:
            #or create new dict if not
            self.values[index] = dict([(symboltype, value)])
        self.symbols[index] = dict()
    def CalculateClasses(self, symboltype, symbolrange, classifytype="equal interval", nrclasses=5, excludevalues=[]):
        #first create pool of possible symbols from raw inputted symbolrange
        if isinstance(symbolrange[0], (int,float)):
            #create nr range
            symbolrange = listy.Resize(symbolrange, nrclasses, dtype="numbers")
        else:
            #create colorrange
            gradient = _ColorGradient(*symbolrange)
            symbolrange = gradient.GetColors(nrcolors=nrclasses)
        #calculate classes based on classifytype
        self.classes = []
        if classifytype.lower() == "equal interval":
            self._EqualInterval(symboltype, symbolrange, classifytype, nrclasses, excludevalues)
            self.__AssignMembershipByValue(symboltype)
        elif classifytype.lower() == "equal classes":
            self._EqualClasses(symboltype, symbolrange, classifytype, nrclasses, excludevalues)
            self.__AssignMembershipByIndex(symboltype, excludevalues)
        elif classifytype.lower() == "natural breaks":
            self._NaturalBreaks(symboltype, symbolrange, classifytype, nrclasses, excludevalues)
            self.__AssignMembershipByValue(symboltype)
    def GetSymbol(self, uniqid, symboltype):
        #for each class test value for membership
        symbol = self.symbols[uniqid].get(symboltype)
        if symbol:
            return symbol
    def GetValues(self):
        return self.sortedvalues
##    def ViewLegend(self, rootwindow=None):
##        """
##        ...workinprogress...
##        Views the classes as a legend in a separate tkinter window.
##        - rootwindow is a tkinter mainloop window, which, if given, will display the label simply as a sub/topwindow part of the mainloop."
##        """
##        #first create legend window
##        if rootwindow:
##            legendwin = tk.TopWindow(rootwindow)
##        else:
##            legendwin = tk.Tk()
##        #then add class widgets
##        for eachclass in self.classes:
##            symbol = eachclass.classsymbol
##            valuerange = str(eachclass.min)+" - "+str(eachclass.max)
##            #so far only color bg supported, no size, shape, or outline
##            if isinstance(symbol, basestring):
##                lbl = tk.Label(bg=symbol, text=valuerange)
##            else:
##                raise TypeError()
##            lbl.pack(fill="x")
##        #then view
##        if rootwindow:
##            pass
##        else:
##            legendwin.mainloop()

    # INTERNAL USE ONLY
    def __AssignMembershipByValue(self, symboltype):
        #loop through values and assign class symbol to each for the specified symboltype
        for uniqid, value in self.sortedvalues:
            value = value[symboltype]
            #for each class test value for membership
            for eachclass in self.classes:
                ### print uniqid, value, eachclass.min, eachclass.max, eachclass.classsymbol
                #membership true if within minmax range of that class
                if value >= eachclass._min and value <= eachclass._max:
                    #assign classsymbol
                    self.symbols[uniqid][symboltype] = eachclass.classsymbol
                    ### print uniqid, value, eachclass.classsymbol
                    break
    def __AssignMembershipByIndex(self, symboltype, excludevalues):
        "still not working properly..."
        #loop through values and assign class symbol to each for the specified symboltype
        for index, (uniqid, value) in enumerate(self.sortedvalues):
            value = value[symboltype]
            #for each class test value for membership
            for eachclass in self.classes:
                ### print uniqid, value, eachclass.min, eachclass.max, eachclass.classsymbol
                #membership true if within minmax range of that class
                if index >= eachclass._min and index <= eachclass._max:
                    #assign classsymbol
                    self.symbols[uniqid][symboltype] = eachclass.classsymbol
                    ### print uniqid, value, eachclass.classsymbol
                    break
    def _EqualInterval(self, symboltype, symbolrange, classifytype, nrclasses, excludevalues):
        self.sortedvalues = sorted([(uniqid, value) for uniqid, value in self.values.iteritems() if value[symboltype] not in excludevalues], key=operator.itemgetter(1))
        sortedvalues = [value[symboltype] for uniqid,value in self.sortedvalues]
        lowerbound = sortedvalues[0]
        upperbound = sortedvalues[-1]
        intervalsize = int( (upperbound-lowerbound)/float(nrclasses) )        
        #populate classes
        classmin = lowerbound
        print symboltype, classifytype
        for index, classsymbol in enumerate(symbolrange):
            if index == nrclasses-1:
                classmax = upperbound
            else:
                classmax = classmin+intervalsize
            print classmin, classmax, len(sortedvalues)
            #determine min and max value
            minvalue = classmin
            maxvalue = classmax
            #create and add class
            self.classes.append( _SymbolClass(classmin, classmax, minvalue, maxvalue, index, classsymbol) )
            #prep for next
            classmin = classmax
    def _EqualClasses(self, symboltype, symbolrange, classifytype, nrclasses, excludevalues):
        self.sortedvalues = sorted([(uniqid, value) for uniqid, value in self.values.iteritems() if value[symboltype] not in excludevalues], key=operator.itemgetter(1))
        sortedvalues = [value[symboltype] for uniqid,value in self.sortedvalues]
        classsize = int( len(sortedvalues)/float(nrclasses) )
        #populate classes
        classmin = 0
        print symboltype, classifytype
        for index, classsymbol in enumerate(symbolrange):
            if index == nrclasses-1:
                classmax = len(sortedvalues)-1
            else:
                classmax = classmin+classsize
            print classmin, classmax, len(sortedvalues)
            #determine min and max value
            minvalue = sortedvalues[classmin]
            maxvalue = sortedvalues[classmax]
            #create and add class
            self.classes.append( _SymbolClass(classmin, classmax, minvalue, maxvalue, index, classsymbol) )
            #prep for next
            classmin = classmax
    def _NaturalBreaks(self, symboltype, symbolrange, classifytype, nrclasses, excludevalues):
        "taken from http://danieljlewis.org/files/2010/06/Jenks.pdf"
        self.sortedvalues = sorted([(uniqid, value) for uniqid, value in self.values.iteritems() if value[symboltype] not in excludevalues], key=operator.itemgetter(1))
        sortedvalues = [value[symboltype] for uniqid,value in self.sortedvalues]
        lowerbound = sortedvalues[0]
        upperbound = sortedvalues[-1]
        def getJenksBreaks( dataList, numClass ):
            "sorting is skipped, bc dataList is already sorted when getting the Jenks breaks"
            mat1 = []
            for i in range(0,len(dataList)+1):
                temp = []
                for j in range(0,numClass+1):
                    temp.append(0)
                mat1.append(temp)
            mat2 = []
            for i in range(0,len(dataList)+1):
                temp = []
                for j in range(0,numClass+1):
                    temp.append(0)
                mat2.append(temp)
            for i in range(1,numClass+1):
                mat1[1][i] = 1
                mat2[1][i] = 0
                for j in range(2,len(dataList)+1):
                    mat2[j][i] = float('inf')
            v = 0.0
            for l in range(2,len(dataList)+1):
                s1 = 0.0
                s2 = 0.0
                w = 0.0
                for m in range(1,l+1):
                    i3 = l - m + 1
                    val = float(dataList[i3-1])
                    s2 += val * val
                    s1 += val
                    w += 1
                    v = s2 - (s1 * s1) / w
                    i4 = i3 - 1
                    if i4 != 0:
                        for j in range(2,numClass+1):
                            if mat2[l][j] >= (v + mat2[i4][j - 1]):
                                mat1[l][j] = i3
                                mat2[l][j] = v + mat2[i4][j - 1]  
                mat1[l][1] = 1
                mat2[l][1] = v         
            k = len(dataList)
            kclass = []
            for i in range(0,numClass+1):
                kclass.append(0)
            kclass[numClass] = float(dataList[len(dataList) - 1])
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
        jenksbreaks = getJenksBreaks(sortedvalues, nrclasses)
        breaksgen = (each for each in jenksbreaks[1:-1]) #excluding first and last bc those are just endpoints
        classmin = lowerbound
        print symboltype, classifytype
        for index, classsymbol in enumerate(symbolrange):
            if index == nrclasses-1:
                classmax = upperbound
            else:
                classmax = next(breaksgen)
            print classmin, classmax, len(sortedvalues)
            #determine min and max value
            minvalue = classmin
            maxvalue = classmax
            #create and add class
            self.classes.append( _SymbolClass(classmin, classmax, minvalue, maxvalue, index, classsymbol) )
            #prep for next
            classmin = classmax


def _CheckOptions(customoptions):
    if not customoptions.get("fillcolor"):
        customoptions["fillcolor"] = Color()
    if not customoptions.get("fillsize"):
        customoptions["fillsize"] = 7
    if not customoptions.get("outlinecolor"):
        customoptions["outlinecolor"] = Color("black")
    if not customoptions.get("outlinewidth"):
        customoptions["outlinewidth"] = 1
    return customoptions
def _CheckTextOptions(customoptions):
    if not customoptions.get("textfont"):
        customoptions["textfont"] = "default"
    if not customoptions.get("textsize"):
        customoptions["textsize"] = 7
    if not customoptions.get("textcolor"):
        customoptions["textcolor"] = Color("black")
    if not customoptions.get("textopacity"):
        customoptions["textopacity"] = 255
    if not customoptions.get("texteffect"):
        customoptions["texteffect"] = None
    return customoptions

#QUICK TASKS
def ViewShapefile(shapefilepath, **customoptions):
    """Quick task to visualize a shapefile and show it in a Tkinter window.
    -shapefilepath is the path string of the shapefile.
    -customoptions is any series of named arguments of how to style the shapefile visualization (optional). Valid arguments are: fillcolor, fillsize (determines the circle size for point shapefiles, line width for line shapefiles, and has no effect for polygon shapefiles), outlinecolor, outlinewidth."""
    customoptions = _CheckOptions(customoptions)
    renderer = _Renderer()
    renderer.ViewShapefile(shapefilepath, customoptions)
def SaveShapefileImage(shapefilepath, savepath, **customoptions):
    """Quick task to save a shapefile to an image.
    -shapefilepath is the path string of the shapefile.
    -savepath is the path string of where to save the image, including the image type extension.
    -customoptions is any series of named arguments of how to style the shapefile visualization (optional). Valid arguments are: fillcolor, fillsize (determines the circle size for point shapefiles, line width for line shapefiles, and has no effect for polygon shapefiles), outlinecolor, outlinewidth."""
    customoptions = _CheckOptions(customoptions)
    renderer = _Renderer()
    renderer.SaveShapefileImage(shapefilepath, savepath, customoptions)

#MAP BUILDING
class NewMap:
    """Creates and returns a new map based on previously defined mapsettings."""
    def __init__(self):
        self.renderer = _Renderer()
    def AddShape(self, shapeobj, **customoptions):
        customoptions = _CheckOptions(customoptions)
        self.renderer._RenderShape(shapeobj, customoptions)
    def AddToMap(self, shapefilepath, **customoptions):
        """Add a shapefile to the map.
        -shapefilepath is the path string of the shapefile to add.
        -customoptions is any series of named arguments of how to style the shapefile visualization (optional). Valid arguments are: fillcolor, fillsize (determines the circle size for point shapefiles, line width for line shapefiles, and has no effect for polygon shapefiles), outlinecolor, outlinewidth."""
        customoptions = _CheckOptions(customoptions)
        if customoptions.get("classifier"):
            self._AutoClassifyShapefile(shapefilepath, customoptions.get("classifier"), customoptions)
        else:
            self.renderer._RenderShapefile(shapefilepath, customoptions)
    def AddText(self, relx, rely, text, **textoptions):
        textoptions = _CheckTextOptions(textoptions)
        self.renderer._RenderText(relx, rely, text, textoptions)
##    def AddLegend(self, relx, rely, classifier, text, **textoptions):
##        "under construction..."
##        textoptions = _CheckTextOptions(textoptions)
##        #first legend box
##        self.renderer._RenderRectangle(relNW, relSE, text, textoptions)
##        #then legend title
##        self.renderer._RenderText(relx, rely, text, textoptions)
##        #for each class
##        for eachclass in classifier:
##            #symbol color/size
##            #values text
##            pass

    def ViewMap(self):
        """View the created map embedded in a Tkinter window. Map image can be panned, but not zoomed. Offers a 'save image' button to allow to interactively save the image"""
        self.renderer._ViewRenderedShapefile()
    def SaveMap(self, savepath):
        """Save the map to an image file.
        -savepath is the string path for where you wish to save the map image. Image type extension must be specified ('.png','.gif',...)"""
        self.renderer._SaveRenderedShapefile(savepath)
    ###INTERNAL USE ONLY
    def _AutoClassifyShapefile(self, shapefilepath, classifier, options):
        allclassifications = classifier.allclassifications
        ####CLASSIFY ONE SHAPEFILE OPTION
        #create shapefile
        shapefile = Shapefile(shapefilepath)
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
            classifier.CalculateClasses(classification["symboltype"],
                                        classification["symbolrange"],
                                        classifytype=classification["classifytype"],
                                        nrclasses=classification["nrclasses"],
                                        excludevalues=classification["excludevalues"])
        ####RENDER THAT CLASSIFIED SHAPEFILE
        #loop sorted/classified ids and get and render each
        shapefile.progresstext = "rendering shapes"
        for shape in shapefile:
            #populate a custom options dict based on classifications
            for classification in allclassifications:
                symboltype = classification["symboltype"]
                #retrieve class color for each shape id
                symbol = classifier.GetSymbol(shape.id, symboltype)
                if symbol:
                    options[symboltype] = symbol
            #render only if at least one of the options were successful
            if options:
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
    """Sets the width and height of the next map. At startup the width and height are set to the dimensions of the window screen.
    -width/height must be integers."""
    global MAPWIDTH, MAPHEIGHT
    MAPWIDTH = width
    MAPHEIGHT = height
    _UpdateMapDims()
def SetMapBackground(mapbackground):
    """Sets the mapbackground of the next map to be made. At startup the mapbackground is transparent (None).
    -mapbackground takes a hex color string, as can be created with the Color function. It can also be None for a transparent background (default)."""
    global MAPBACKGROUND
    MAPBACKGROUND = mapbackground
def SetZoomExtent():
    """Not yet in use, and will not still create entire image..."""
    if NUMPYSPEED:
        pass
    else:
        pass
    _UpdateMapDims()


### END OF SCRIPT ###

    
