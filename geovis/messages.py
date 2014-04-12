# Import main modules
import sys, pickle, Queue
# Import custom modules
from textual import txt
import timetaker as timer

def SnapVars(onlyvars=[], excludevars=[]):
    """
not working yet bc only snaps local vars...
"""
    print ("snapshot of variables:")
    print ("----------------------")
    if onlyvars: allvars = onlyvars
    else: allvars = dir()
    for var in allvars:
        if not var.startswith("__"):
            if var in excludevars:
                continue
            val = eval(var)
            print ("%s = %s"%(var,val))

def Report(text, conditional=True):
    if isinstance(text, list):
        text = [txt(eachitem) for eachitem in text]
        text = ", ".join(text)
    if conditional == True:
        print text

class ProgressReport:
    """generator that is wrapped over an iterator in a for-loop (like enumerate)
and yields the same output as the iterator, except it also automatically checks
and reports back the progress of the loop. Does not currently work for generators
bc no way to assess length of a generator, unless it's a custom made one that has
the __len__ attribute or if you specify the generator length manually. NOTE: using this wrapper function does not significantly reduce
speed as long as you use it on loops that are large enough to make the difference neglible,
that is, try not to use it on small loops; although it makes a loop 5x slower. For
every 1 million loops this only amounts to a time punishment of about 0.6 seconds.
Also, it is not very accurate for small time amounts, and can only measure times larger
than 0.00005 seconds.
*reportincr = report progress every x percent
*genlength = if the iterator is a generator the iterator length has to be set manually in this variable"""
    def __init__(self, iterable, **kwargs):
        self.kwargs = kwargs
        self.iterable = iterable
        self.prog = 0
    def __iter__(self):
        iterable = self.iterable
        if not "shellreport" in self.kwargs:
            shellreport="progressbar"
        else:
            shellreport=self.kwargs["shellreport"]
        if not "text" in self.kwargs:
            text="unknown task"
        else:
            text=self.kwargs["text"]
        if not "tkwidget" in self.kwargs:
            tkwidget=None
        else:
            tkwidget=self.kwargs["tkwidget"]
        if not "queue" in self.kwargs:
            queue=None
        else:
            queue=self.kwargs["queue"]
        if not "picklepath" in self.kwargs:
            picklepath=None
        else:
            picklepath=self.kwargs["picklepath"]
        if not "reportincr" in self.kwargs:
            reportincr=1
        else:
            reportincr=self.kwargs["reportincr"]
        if not "genlength" in self.kwargs:
            genlength=None
        else:
            genlength=self.kwargs["genlength"]
        if not "countmethod" in self.kwargs:
            countmethod="auto"
        else:
            countmethod=self.kwargs["countmethod"]
        #some error checking
        if not hasattr(iterable, "__iter__"):
            raise TypeError("The iterable argument was not iterable")
        if not hasattr(iterable, "__len__") and not genlength:
            raise TypeError("The iterable argument must have a length in order to asses its progress")
        #determine report types
        if not shellreport:
            shellprogbar=False
            shellprint=False
        elif shellreport.lower() == "progressbar":
            shellprogbar=True
            shellprint=False
        elif shellreport.lower() == "print":
            shellprogbar=False
            shellprint=True
        #do some startup things
        if shellprogbar:
            reportincr = 2
            print "\n%s" %text
            print "0%"+","*50+"100%"
            sys.stdout.write("  ")
        #convert report incr percent to fraction of one
        reportincr = reportincr/100.0
        #measure total length
        if not genlength:
            total = float(len(iterable))
        else:
            total = float(genlength)
        nextthresh = reportincr
        self.prog = 0
        timer.start("task completed in")
        for index, each in enumerate(iterable):
            if countmethod == "auto":
                #only if countmethod is set to "auto" will progress increase automatically
                #otherwise, the user has to keep a reference to the ProgressReport obj
                #and manually increment self.prog at the correct pace
                self.prog = index
            percent = self.prog/total
            #report progress if reached threshold
            if percent >= nextthresh:
                nextthresh += reportincr
                #if progressbar is true this will ignore the shellprint option
                if shellprogbar:
                    sys.stdout.write("|")
                elif shellprint:
                    print "%i percent task completion: %s" %(int(percent*100),text)
                if queue:
                    queue.put({"percent":int(percent*100),"text":text})
                if tkwidget:
                    #tkwidget.set(int(percent*100))
                    tkwidget.update()
                if picklepath:
                    msgbox = open(picklepath,"wb")
                    pickle.dump({"percent":int(percent*100),"text":text}, msgbox)
                    msgbox.close()
                #check for finish
                if nextthresh >= 1:
                    if shellprogbar:
                        sys.stdout.write("\n"+" "*8)
                        timer.stop("task completed in")
                        sys.stdout.write("\n")
                    elif shellprint:
                        print "%i percent task completion: %s" %(100,text)
                    if queue:
                        queue.put({"percent":100,"text":text})
                    if tkwidget:
                        #tkwidget.set(int(percent*100))
                        tkwidget.update()
                    if picklepath:
                        msgbox = open(picklepath,"wb")
                        pickle.dump({"percent":100,"text":text}, msgbox)
                        msgbox.close()
            #yield next element from iterable
            yield each
    def Increment(self):
        self.prog += 1


# example testing
if __name__ == "__main__":
    import timetaker as timer
    l = xrange(1000000)
    timer.start()
    for each in ProgressReport(l):
        pass
    timer.stop()
    print "done"
        


        
        
