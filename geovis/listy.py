#IMPORTS
import sys, os, operator, itertools, random, math

#GLOBALS
NONEVALUE = None


"""
SEE ALSO
http://code.activestate.com/recipes/189971-basic-linear-algebra-matrix/
http://users.rcn.com/python/download/python.htm
"""


#FUNCTIONS
def Resize(rows, newlength, stretchmethod="not specified", gapvalue="not specified"):
    "front end used by user, determines if special nested list resizing or single list"
    if isinstance(rows[0], (list,tuple)):
        #input list is a sequence of list (but only the first item is checked)
        #needs to have same nr of list items in all sublists
        crosssection = itertools.izip(*rows)
        grad_crosssection = [ _Resize(spectrum,newlength,stretchmethod,gapvalue) for spectrum in crosssection ]
        gradient = [list(each) for each in itertools.izip(*grad_crosssection)]
        return gradient
    else:
        #just a single list of values
        return _Resize(rows, newlength, stretchmethod, gapvalue)
def Transpose(listoflists):
    "must get a 2d grid, ie a list of lists, with all sublists having equal lengths"
    transposed = [list(each) for each in itertools.izip(*listoflists)]
    return transposed

#BUILTINS    
def _Resize(rows, newlength, stretchmethod="not specified", gapvalue="not specified"):
    "behind the scenes, does the actual work, only for a single flat list"
    #return input as is if no difference in length
    if newlength == len(rows):
        return rows
    #set gap
    if gapvalue == "not specified":
        gapvalue = NONEVALUE
    #set auto stretchmode
    if stretchmethod == "not specified":
        if isinstance(rows[0], (int,float)):
            stretchmethod = "interpolate"
        else:
            stretchmethod = "duplicate"
    #reduce newlength 
    newlength -= 1
    #assign first value
    outlist = [rows[0]]
    relspreadindexgen = (index/float(len(rows)-1) for index in xrange(1,len(rows))) #warning a little hacky by skipping first index cus is assigned auto
    relspreadindex = next(relspreadindexgen)
    spreadflag = False
    for each in xrange(1, newlength):
        #relative positions
        rel = each/float(newlength)
        relindex = (len(rows)-1) * rel
        basenr,decimals = str(relindex).split(".")
        relbwindex = float("0."+decimals)
        #determine equivalent value
        if stretchmethod=="interpolate":
            maybecurrelval = rows[int(relindex)]
            if maybecurrelval != gapvalue:
                #ALMOST THERE BUT NOT QUITE
                #DOES SOME WEIRD BACKTRACKING
                #...
                currelval = rows[int(relindex)]
            #make sure next value to interpolate to is valid
            testindex = int(relindex)+1
            while testindex < len(rows)-1 and rows[testindex] == gapvalue:
                #if not then interpolate until next valid item
                testindex += 1
            nextrelval = rows[testindex]
            #assign value
            relbwval = currelval + (nextrelval - currelval) * relbwindex #basenr pluss interindex percent interpolation of diff to next item
        elif stretchmethod=="duplicate":
            relbwval = rows[int(round(relindex))] #no interpolation possible, so just copy each time
        elif stretchmethod=="spread":
            if rel >= relspreadindex:
                spreadindex = int(len(rows)*relspreadindex)
                relbwval = rows[spreadindex] #spread values further apart so as to leave gaps in between
                relspreadindex = next(relspreadindexgen)
            else:
                relbwval = gapvalue
        #assign each value
        outlist.append(relbwval)
    #assign last value
    outlist.append(rows[-1])
    return outlist
def _InterpolateValue(value, otherinput, method):
    "method can be linear, IDW, etc..."
    pass

#CLASSES
class _1dData:
    """
Most basic of all list types. Contains data values but is just a meaningless arbitrary list if not embedded in some other list type.
It can be embedded in a 2dsurfacegrid to represent a theme located along horizantal x lines.
Or embedded in a 4dtimegrid to represent a theme changing over time, without any spatial properties.
Maybe same as Listy below??
"""
    pass
class _Cell:
    def __init__(self, xpos, ypos, value):
        self.x = xpos
        self.y = ypos
        self.value = value
class _2dSurfaceGrid:
    "horizontal lines up and down along y axis"
    #BUILTINS
    def __init__(self, twoDlist=None, emptydims="not specified"):
        #add some error checking...
        #...
        if not twoDlist:
            if emptydims == "not specified":
                emptydims = (50,50)
            width,height = emptydims
            twoDlist = [[NONEVALUE for _ in xrange(width)] for _ in xrange(height)]
        self.grid = Listy(*twoDlist)
        self.height = len(self.grid.lists)
        self.width = len(self.grid.lists[0])
        self.knowncells = self._GetKnownCells()
    def __iter__(self):
        for ypos, horizline in enumerate(self.grid.lists):
            for xpos, xpoint in enumerate(horizline):
                yield _Cell(xpos, ypos, value=xpoint)
    def __str__(self):
        return str(self.grid)
    #FUNCTIONS
    def RandomPoints(self, value="random", valuerange="not specified", nrpoints="not specified"):
        if nrpoints == "not specified":
            nrpoints = int(self.width*self.height*0.10) #10 percent of all cells
        if valuerange == "not specified":
            valuerange = (0,250)
        randomvalue = False
        if value == "random":
            randomvalue = True
        for _ in xrange(nrpoints):
            if randomvalue:
                value = random.randrange(*valuerange)
            xindex = random.randrange(self.width)
            yindex = random.randrange(self.height)
            self.grid.lists[yindex][xindex] = value
        self.knowncells = self._GetKnownCells()
    def Interpolate(self, method="IDW", **options):
        "ie fill any gaps in grid with interpolation"
        if method == "IDW":
            self._IDW(options)
    def ChangeValues(self, expression):
        pass
    def SelectQuery(self, query):
        pass
    def Show(self):
        import numpy, PIL, PIL.Image, PIL.ImageTk, PIL.ImageDraw
        import Tkinter as tk
        import colour
        win = tk.Tk()
        nparr = numpy.array(self.grid.lists)
        npmin = numpy.min(nparr)
        npmax = numpy.max(nparr)
        minmaxdiff = npmax-npmin
        colorstops = [colour.Color("red").rgb,colour.Color("yellow").rgb,colour.Color("green").rgb]
        colorstops = [list(each) for each in colorstops]
        colorgrad = Listy(*colorstops)
        colorgrad.Convert("250*value")
        colorgrad.Resize(int(minmaxdiff))
        valuerange = range(int(npmin),int(npmax))
        colordict = dict(zip(valuerange,colorgrad.lists))
        print len(valuerange),len(colorgrad.lists),len(colordict)
        print "minmax",npmin,npmax
        for ypos,horizline in enumerate(self.grid.lists):
            for xpos,value in enumerate(horizline):
                relval = value/float(npmax)
                self.grid.lists[ypos][xpos] = colorgrad.lists[int((len(colorgrad.lists)-1)*relval)]
        nparr = numpy.array(self.grid.lists,"uint8")
        print "np shape",nparr.shape
        img = PIL.Image.fromarray(nparr)
        drawer = PIL.ImageDraw.ImageDraw(img)
        size = 3
        for knowncell in self.knowncells:
            x,y = (knowncell.x,knowncell.y)
            drawer.ellipse((x-size,y-size,x+size,y+size),fill="black")
        img.save("C:/Users/BIGKIMO/Desktop/test.png")
        tkimg = PIL.ImageTk.PhotoImage(img)
        lbl = tk.Label(win, image=tkimg)
        lbl.pack()
        win.mainloop()
    #INTERNAL USE ONLY
    def _GetKnownCells(self):
        knowncellslist = []
        for cell in self:
            if cell.value != NONEVALUE:
                knowncellslist.append(cell)
        return knowncellslist
    def _IDW(self, options):
        #retrieve input options
        neighbours = options.get("neighbours",int(len(self.knowncells)*0.10)) #default neighbours is 10 percent of known points
        sensitivity = options.get("sensitivity",3) #same as power, ie that high sensitivity means much more effect from far away points
        #some defs
        def _calcvalue(unknowncell, knowncells):
            weighted_values_sum = 0.0
            sum_of_weights = 0.0
            for knowncell in knowncells:
                weight = ((unknowncell.x-knowncell.x)**2 + (unknowncell.y-knowncell.y)**2)**(-sensitivity/2.0)
                sum_of_weights += weight
                weighted_values_sum += weight * knowncell.value
            return weighted_values_sum / sum_of_weights
        #calculate value
        for unknowncell in self:
            if unknowncell.value == NONEVALUE:
                #only calculate for unknown points
                self.grid.lists[unknowncell.y][unknowncell.x] = _calcvalue(unknowncell, self.knowncells)
            
class _3dSpaceGrid:
    """z axis.
Works by rendering one surface at a time, starting with lowest, that way rendering higher up/closer to the eye points on top of lower/further away points which gives a 3d effect.
Just need to find a way to transform each surface to the way it should look like from different angles.
Note: Link to a function to create the transform coeffs for PIL's perspective transform: http://stackoverflow.com/questions/14177744/how-does-perspective-transformation-work-in-pil
OR use ray tracing... http://scratchapixel.com/lessons/3d-basic-lessons/lesson-1-writing-a-simple-raytracer/source-code/
ALSO see basic 3d equations http://www.math.washington.edu/~king/coursedir/m445w04/notes/vector/equations.html
"""
    pass
class _4dTimeGrid:
    """time axis
example:
for 3dtime in 4dtimegrid:
    #loops all 3d spaces at different points in time
    for 2ddepth in 3dtime:
        #loops all 2d surfaces at different altitudes, from low to high
        for 1dheight in 2ddepth:
            #loops all leftright horizantal lines in a 2dgrid
            for datavalue in 1dheight:
                #loops all datavalues for whatever theme in a specific 1dline, in a 2dgrid, at a 3daltitude, at a 4d point in time
"""
    pass

class Listy(list):
    "A list-type class with extended functionality and methods. These extra features should only be bindings to functions alredy defined in the general listy module and can be used by anyone, not just the Listy class."
    def __init__(self, *sequences):
        self.lists = list(sequences)
        self.dtype = "numbers" #"maybe do some automatic dtype detection"
    def __str__(self):
        maxchar = 50
        printstr = "[\n"
        for eachlist in self.lists:
            if len(str(eachlist)) > maxchar:
                printstr += str(eachlist)[:int(maxchar/2.0)]+"..."+str(eachlist)[-int(maxchar/2.0):]+"\n"
            else:
                printstr += str(eachlist)+"\n"
        printstr += "]\n"
        return printstr
    #SHAPE AND ORIENTATION
    def Resize(self, newlength, listdim=None, stretchmethod="not specified", gapvalue="not specified"):
        if listdim:
            #resize only a certain dimension
            self.lists[listdim] = Resize(self.lists[listdim], newlength, stretchmethod, gapvalue)
        else:
            #resize all lists??? experimental...
            self.lists = Resize(self.lists, newlength, stretchmethod, gapvalue)
    def Transpose(self):
        self.lists = Transpose(self.lists)
    def Reshape(self, newshape):
        "not sure yet how to do..."
        pass
    def Split(self, groups_or_indexes):
        pass
    #TYPES
    def Convert(self, dataformat):
        "it does actually work...but floating values will never be shortened bc no exact precision"
        toplist = self.lists
        def execfunc(code, toplist, value, index):
            exec(code)
        def recurloop(toplist):
            for index, value in enumerate(toplist):
                if isinstance(value, list):
                    listfound = True
                    recurloop(value)
                else:
                    conversioncode = "toplist[index] = "+dataformat
                    execfunc(conversioncode, toplist, value, index)
        #begin
        recurloop(toplist)
    #ATTRIBUTES
    @property
    def minval(self):
        pass
    @property
    def maxval(self):
        pass
    @property
    def shape(self):
        return tuple([len(eachlist) for eachlist in self.lists])
    @property
    def structure(self):
        toplist = self.lists
        depth = 0
        spaces = "  "
        structstring = str(len(toplist))+"\n"
        def recurloop(toplist, structstring, depth, spaces):
            for item in toplist:
                if isinstance(item, list):
                    listfound = True
                    depth += 1
                    structstring += spaces*depth + str(len(item)) + "\n"
                    toplist, structstring, depth, spaces = recurloop(item, structstring, depth, spaces)
                    depth -= 1
            return toplist, structstring, depth, spaces
        #begin
        item, structstring, depth, spaces = recurloop(toplist, structstring, depth, spaces)
        return structstring

if __name__ == "__main__":

    print ""
    print "print and shape and resize test"
    testlist = [random.randrange(50) for e in xrange(random.randrange(31))]
    testlisty = Listy(testlist, testlist)
    print testlisty
    print testlisty.shape
    testlisty.Resize(22, listdim=0)
    print testlisty.shape
    print testlisty

    print ""
    print "hierarchical nested list structure test"
    nestedlists = [[["anything" for e in xrange(random.randrange(500))] for e in xrange(random.randrange(5))] for d in xrange(random.randrange(6))]
    nestedlisty = Listy(*nestedlists)
    print nestedlisty
    print nestedlisty.structure

    print ""
    print "transpose test"
    listoflists = [range(100) for _ in xrange(100)]
    gridlisty = Listy(*listoflists)
    print gridlisty
    gridlisty.Transpose()
    print gridlisty

    print ""
    print "fill in blanks test"
    listholes = [1,2,None,4,None,6]
    gridlisty = Listy(*listholes)
    print gridlisty
    gridlisty.Resize(12, stretchmethod="interpolate")
    print gridlisty

    print ""
    print "spread grid test"
    listoflists = [range(6) for _ in xrange(6)]
    gridlisty = Listy(*listoflists)
    print gridlisty
    #expand sideways (instead of downwards which is default for the multilist resize func)
    gridlisty.Transpose()
    gridlisty.Resize(11, stretchmethod="spread")
    gridlisty.Transpose()
    #resize again to also expand downwards
    gridlisty.Resize(11, stretchmethod="spread")
    print gridlisty
    #finally try interpolating in between
    #THIS PART NOT WORKING PROPERLY, GOING ZIGZAG OVER GAPS
##    gridlisty.Resize(22, stretchmethod="interpolate")
##    print gridlisty
##    gridlisty.Resize(11)
##    print gridlisty

    print ""
    print "gridpoints interpolate test"
    listoflists = [[random.randrange(200) for _ in xrange(10)] for _ in xrange(10)] #[range(10) for _ in xrange(10)]
    templisty = Listy(*listoflists)
    print templisty
    #spread to create holes
    templisty.Transpose()
    templisty.Resize(80, stretchmethod="spread")
    templisty.Transpose()
    templisty.Resize(80, stretchmethod="spread")
    #make into 2dgrid obj
    testgrid = _2dSurfaceGrid(templisty.lists)
    print "spread done"#,testgrid
    #interpolate
    testgrid.Interpolate("IDW")
    print "idw done"#,testgrid.grid.lists
    #reduce decimals
    ##testgrid.grid.Convert("str(round(value,2))")
    ##print testgrid
    #testgrid.Show()

    print ""
    print "randompoints interpolate test"
    #create empty 2dgrid obj
    testgrid = _2dSurfaceGrid(emptydims=(600,600))
    print "grid made"#,testgrid
    #put random points
    testgrid.RandomPoints(nrpoints=20)
    print "points placed"#,testgrid
    #interpolate
    import time
    t=time.clock()
    testgrid.Interpolate("IDW", sensitivity=4)
    print time.clock()-t
    print "idw done"#,testgrid.grid.lists
    testgrid.Show()


