# timer module to easily measure time in any code
# works like a stopclock and reports back/prints the time taken
# when you call stop

import time
runningtimers = dict()

def start(name="unnamed"):
    starttime = time.clock()
    runningtimers.update([(name,starttime)])

def stop(name="unnamed"):
    endtime = time.clock()
    #obtain starttime based on name provided
    #but if no name was provided at starttime it will still get the time from the default
    starttime = runningtimers.get(name, None)
    if not starttime:
        starttime = runningtimers["unnamed"]
    timetaken = endtime-starttime
    if timetaken < 60.0:
        timeunit = "seconds"
    if timetaken > 60.0:
        timetaken = timetaken/60.0
        timeunit = "minutes"
        if timetaken > 60.0:
            timetaken = timetaken/60.0
            timeunit = "hours"
    #finally, print time taken
    print name, timetaken, timeunit
    if name in runningtimers:
        runningtimers.pop(name)
