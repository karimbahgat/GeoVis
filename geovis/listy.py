#IMPORTS
import sys, os, operator, itertools
try:
    import colour
except:
    pass

#FUNCTIONS
def Resize(rows, newlength, dtype=None):
    #return input as is if no difference in length
    if newlength == len(rows):
        return rows
    #determine mode
    if dtype:
        mode = dtype
    else:
        #not specified so try autodetecting
        if isinstance(rows[0], (int,float)):
            mode = "numbers"
        elif isinstance(rows[0], basestring):
            mode = "strings"
    #reduce newlength 
    newlength -= 1
    #assign first value
    outlist = [rows[0]] 
    for each in xrange(1, newlength):
        #relative positions
        rel = each/float(newlength)
        relindex = (len(rows)-1) * rel
        relbwindex = float("0."+str(relindex).split(".") [-1] )
        #determine equivalent value
        if mode == "numbers":
            relbwval = rows[int(relindex)] + (rows[int(relindex)+1] - rows[int(relindex)]) * relbwindex #basenr pluss interindex percent interpolation of diff to next item
        elif mode == "strings":
            relbwval = rows[int(round(relindex))] #no interpolation possible, so just copy each time
        elif mode == "hsl":
            colorrange =  colour.color_scale( rows[int(relindex)], rows[int(relindex)+1], 100)
            interpolatedcolorindex = 100 * relbwindex
            relbwval = colorrange[int(round(interpolatedcolorindex))]  #...colorrange(...) and then interpolate index
        #assign each value
        outlist.append(relbwval)
    #assign last value
    outlist.append(rows[-1])
    return outlist


#CLASSES
class Listy(list):
    "A list-type class with extended functionality and methods"
    def __init__(self, *sequences):
        self.lists = list(sequences)
        self.dtype = "numbers" #"maybe do some automatic dtype detection"
    def __str__(self):
        printstr = "[\n"
        for eachlist in self.lists:
            printstr += str(eachlist)+"\n"
        printstr += "]\n"
        return printstr
    def Resize(self, listdim, newlength):
        self.lists[listdim] = Resize(self.lists[listdim], newlength, dtype=self.dtype)
    @property        
    def shape(self):
        return tuple([len(eachlist) for eachlist in self.lists])

if __name__ == "__main__":
    testlist = [1,4,56,7,99]
    testlisty = Listy(testlist,testlist)
    print testlisty
    print testlisty.shape
    testlisty.Resize(0, 22)
    print testlisty.shape
    print testlisty
