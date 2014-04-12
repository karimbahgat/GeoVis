
"""
almost good
but not sure how useful all of this is
gets buggy/leans to one direction when using excessive padding isntead of just disappearing
and seems that same can be done using relx/rely and nested widgets...?
maybe the charm is to not use the subpartition (only if you really cant do nesting)
but instead call PartitionSpace simply as an aid when doing relx/rely inside a nested widget
"""

class Partition:
    def __init__(self, center, partitionwidth, partitionheight, direction):
        if direction == "vertical":
            center = (center[1],center[0])
            partitionwidth,partitionheight = partitionheight,partitionwidth
        self.center = center
        self.width = partitionwidth
        self.height = partitionheight
        midx,midy = center
        halfx = partitionwidth/2.0
        halfy = partitionheight/2.0
        self.nw = (midx-halfx, midy-halfy)
        self.n = (midx, midy-halfy)
        self.ne = (midx+halfx, midy-halfy)
        self.e = (midx+halfx, midy)
        self.se = (midx+halfx, midy+halfy)
        self.s = (midx, midy+halfy)
        self.sw = (midx-halfx, midy+halfy)
        self.w = (midx-halfx, midy)
    def __repr__(self):
        visualstring = "partition:\n"
        visualstring += "%s \t %s \t %s \n" % tuple([[str(nr)[:5] for nr in pair] for pair in (self.nw,self.n,self.ne)])
        visualstring += "%s \t %s \t %s \n" % tuple([[str(nr)[:5] for nr in pair] for pair in (self.w,self.center,self.e)])
        visualstring += "%s \t %s \t %s" % tuple([[str(nr)[:5] for nr in pair] for pair in (self.sw,self.s,self.se)])
        return visualstring
    def SubPartition(self, partitions, padx, pady, direction="horizontal"):
        "only use if you really need to avoid nested widgets, eg if you need to structure your widgets over a large background image bc a background widget to nest them in would cover up parts of the image"
        xtox = (self.w[0], self.e[0])
        ytoy = (self.n[1], self.s[1])
        return PartitionSpace(xtox, ytoy, partitions, padx, pady, direction)

def PartitionSpace(xtox, ytoy, partitions, padx, pady, direction="horizontal"):
    startx, endx = xtox
    starty, endy = ytoy
    if direction == "vertical":
        startx,starty = starty,startx
        endx,endy = endy,endx
        padx,pady = pady,padx
    #prep
    allwidth = endx-startx
    allheight = endy-starty
    widthafterpad = allwidth-padx*(partitions+1)
    heightafterpad = allheight-pady*2
    partitionwidth = widthafterpad/float(partitions)
    partitionheight = heightafterpad
    #calc
    outpartitions = []
    tempx = startx+padx+partitionwidth/2.0
    tempy = starty+pady+partitionheight/2.0
    for _ in xrange(partitions):
        center = (tempx, tempy)
        outpartitions.append( Partition(center, partitionwidth, partitionheight, direction) )
        tempx += partitionwidth/2.0+padx+partitionwidth/2.0
    return outpartitions

if __name__ == "__main__":
    import Tkinter as tk
    import random
    win = tk.Tk()
    testdims = (1100,500)
    testparts = 3

    #pixel positions test
##    testpadx,testpady = (90,20)
##    frame = tk.Frame(win, bg="red", width=testdims[0], height=testdims[1])
##    frame.pack()
##    hm = tk.Label(frame, bg="yellow")
##    hm.place(x=200,y=200)
##    for partition in PartitionSpace(200,testdims[0],0,testdims[1],testparts,testpadx,testpady):
##        but = tk.Label(frame, bg="blue")
##        x,y = partition.center
##        print partition.w, x, partition.e
##        but.place(x=x, y=y, width=round(partition.width), height=round(partition.height), anchor="center")

    #rel test
    testpadx,testpady = (0.01,0.01)
    frame = tk.Frame(win, bg="red", width=testdims[0], height=testdims[1])
    frame.pack(fill="both")
    hm = tk.Label(frame, bg="yellow")
    hm.place(relx=0.3,rely=0.5, anchor="ne")
    #horiz partitions
    partitions = PartitionSpace((0.3,1),(0.7,1),testparts,testpadx,testpady)
    subpart = partitions[0]
    for partition in partitions:
        but = tk.Label(frame, bg="blue")
        x,y = partition.center
        but.place(relx=x, rely=y, relwidth=partition.width, relheight=partition.height, anchor="center")
        #split each down the middle
        subpartitions = partition.SubPartition(2, 0.01, 0.02)
        #left side
        subpart = subpartitions[0]
        but = tk.Label(frame, bg="green")
        x,y = subpart.center
        but.place(relx=x, rely=y, relwidth=subpart.width, relheight=subpart.height, anchor="center")
        #then try downwards partition
        subsubpartitions = subpart.SubPartition(5, 0.006, 0.006, direction="vertical")
        for subpart in subsubpartitions:
            but = tk.Label(frame, bg="red")
            x,y = subpart.center
            but.place(relx=x, rely=y, relwidth=subpart.width, relheight=subpart.height, anchor="center")
        #right side
        subpart = subpartitions[1]
        but = tk.Label(frame, bg="green")
        x,y = subpart.center
        but.place(relx=x, rely=y, relwidth=subpart.width, relheight=subpart.height, anchor="center")
        #then try downwards partition
        subsubpartitions = subpart.SubPartition(5, 0.006, 0.006, direction="vertical")
        for subpart in subsubpartitions:
            but = tk.Label(frame, bg="white", text="text")
            x,y = subpart.center
            but.place(relx=x, rely=y, relwidth=subpart.width, relheight=subpart.height, anchor="center")
    #finalize window
    coordsdisplay = tk.Label(win, text="mousepos")
    coordsdisplay.place(relx=0.01, rely=0.01)
    def displaymousecoords(event):
        coordsdisplay["text"] = "%s,%s (%s,%s)" %(event.x,event.y, event.x/float(win.winfo_width()),event.y/float(win.winfo_height()))
    win.bind("<Motion>", displaymousecoords)
    win.mainloop()
        
