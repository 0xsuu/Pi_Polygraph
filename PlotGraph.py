
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import random
from scipy import interpolate
import numpy as np
import csv

from DigitalFilter import *

#Global variable
WINDOWSIZE = 10
PERIOD = 0.125
Colour = {"SCR":"k","RR":"b", "HR":"r", "SST":"g"}
GRAPHWIDTH = 300
#plt is a global stuff

#plotter manual:
#  init with modes
class Plotter():
    def __init__(self, modes):
        #plt.title("Polygraph")
        #plt.axis([0, 300, -4096, 4096])
        
        self._windowSize = WINDOWSIZE
        self._currentWidth = GRAPHWIDTH
        
        #Set modes
        self._modes = modes
        
        #Plot switch
        self._doPlotting = False
        
        #Data storageimport csv
        self._dataSegment = {"SCR":[],"RR":[], "HR":[], "SST":[]}          #raw data
        self._filteredData = {"SCR":[],"RR":[], "HR":[], "SST":[]}         #filtered data
        self._changeRateData = {"SCR":[],"RR":[], "HR":[], "SST":[]}       #change rate data
        self._interpolatedData = {"SCR":[],"RR":[], "HR":[], "SST":[]}     #interpolated data
    
        self._dataSegmentX = {"SCR":[],"RR":[], "HR":[], "SST":[]}         #raw data X axis
        self._filteredDataX = {"SCR":[],"RR":[], "HR":[], "SST":[]}        #filtered data X axis
        self._changeRateDataX = {"SCR":[],"RR":[], "HR":[], "SST":[]}      #change rate data X axis
        self._interpolatedDataX = {"SCR":[],"RR":[], "HR":[], "SST":[]}    #interpolated data X axis

        self._dataSegmentTime = {"SCR":[],"RR":[], "HR":[], "SST":[]}         #raw data timestamps
        self._filteredDataTime = {"SCR":[],"RR":[], "HR":[], "SST":[]}        #filtered data timestamps
        self._changeRateDataTime = {"SCR":[],"RR":[], "HR":[], "SST":[]}      #change rate data timestamps
        self._interpolatedDataTime = {"SCR":[],"RR":[], "HR":[], "SST":[]}    #interpolated data timestamps
        
        self._usedData = {"SCR":[],"RR":[], "HR":[], "SST":[]}
        self._usedDataX = {"SCR":[],"RR":[], "HR":[], "SST":[]}

        self._yellowButton = []
        self._redButton = []

        self._firstPlot = True
        
        plt.ion()
        
        self._SCR, self._axSCR = plt.subplots(1,1)
        self._axSCR.axis([0, 300, -4096, 4096])
        SCRLine = self._axSCR.plot([],[],"k",label="SCR")
        RRLine = self._axSCR.plot([],[],"b",label="RR")
        HRLine = self._axSCR.plot([],[],"r",label="HR")
        SSTLine = self._axSCR.plot([],[],"g",label="SST")
        self._axSCR.legend(["SCR","RR","HR","SST"])
        self._axSCR.hold(True)
        plt.draw()
        self._background = self._SCR.canvas.copy_from_bbox(self._axSCR.bbox)

    def stopPlotting(self):
        self._yellowButton.append(str(time.localtime().tm_hour)+":"+
                                      str(time.localtime().tm_min)+":"+
                                      str(time.localtime().tm_sec))
        #Recording to file
        row = []

        if "INTERPOLATE" in self._modes["HR"]:
                points = self._axSCR.plot(self._interpolatedDataX["HR"], self._interpolatedData["HR"], "m")[0]
                # redraw just the points
                self._axSCR.draw_artist(points)
                # fill in the axes rectangle
                self._SCR.canvas.blit(self._axSCR.bbox)
                
        writer = csv.writer(open("../polygraph.csv", "wb"))
        writer.writerow(["SCR","Time","X","Y","RR","Time","X","Y","HR","Time","X","Y","SST","Time","X","Y","Yellow Button", "Red Button"])
        i=0
        iteration = 0
        while iteration<4:
            iteration = 0
            #SCR
            if "CHANGERATE" in self._modes["SCR"]:
                if i < len(self._changeRateDataX["SCR"]):
                    row.append("")
                    row.append(self._changeRateDataTime["SCR"][i])
                    row.append(self._changeRateDataX["SCR"][i])
                    row.append(self._changeRateData["SCR"][i])
                else:
                    iteration += 1
                    row.append("")
                    row.append("")
                    row.append("")
                    row.append("")
            elif "FILTER" in self._modes["SCR"]:
                if i < len(self._filteredDataX["SCR"]):
                    row.append("")
                    row.append(self._filteredDataTime["SCR"][i])
                    row.append(self._filteredDataX["SCR"][i])
                    row.append(self._filteredData["SCR"][i])
                else:
                    iteration += 1
                    row.append("")
                    row.append("")
                    row.append("")
                    row.append("")
            else:
                if i < len(self._dataSegmentX["SCR"]):
                    row.append("")
                    row.append(self._dataSegmentTime["SCR"][i])
                    row.append(self._dataSegmentX["SCR"][i])
                    row.append(self._dataSegment["SCR"][i])
                else:
                    iteration += 1
                    row.append("")
                    row.append("")
                    row.append("")
                    row.append("")
            
            #RR
            if "FILTER" in self._modes["RR"]:
                if i < len(self._filteredDataX["RR"]):
                    row.append("")
                    row.append(self._filteredDataTime["RR"][i])
                    row.append(self._filteredDataX["RR"][i])
                    row.append(self._filteredData["RR"][i])
                else:
                    iteration += 1
                    row.append("")
                    row.append("")
                    row.append("")
                    row.append("")
            else:
                if i < len(self._dataSegmentX["RR"]):
                    row.append("")
                    row.append(self._dataSegmentTime["RR"][i])
                    row.append(self._dataSegmentX["RR"][i])
                    row.append(self._dataSegment["RR"][i])
                else:
                    iteration += 1
                    row.append("")
                    row.append("")
                    row.append("")
                    row.append("")
            
            #HR
            if "INTERPOLATE" in self._modes["HR"]:
                if i < len(self._interpolatedDataX["HR"]):
                    row.append("")
                    row.append("")
                    row.append(self._interpolatedDataX["HR"][i])
                    row.append(self._interpolatedData["HR"][i])
                else:
                    iteration += 1
                    row.append("")
                    row.append("")
                    row.append("")
                    row.append("")
            else:
                if i < len(self._dataSegmentX["HR"]):
                    row.append("")
                    row.append(self._dataSegmentTime["HR"][i])
                    row.append(self._dataSegmentX["HR"][i])
                    row.append(self._dataSegment["HR"][i])
                else:
                    iteration += 1
                    row.append("")
                    row.append("")
                    row.append("")
                    row.append("")
            
            #SST
            if "FILTER" in self._modes["SST"]:
                if i < len(self._filteredDataX["SST"]):
                    row.append("")
                    row.append(self._filteredDataTime["SST"][i])
                    row.append(self._filteredDataX["SST"][i])
                    row.append(self._filteredData["SST"][i])
                else:
                    iteration += 1
                    row.append("")
                    row.append("")
                    row.append("")
                    row.append("")
            else:
                if i < len(self._dataSegmentX["SST"]):
                    row.append("")
                    row.append(self._dataSegmentTime["SST"][i])
                    row.append(self._dataSegmentX["SST"][i])
                    row.append(self._dataSegment["SST"][i])
                else:
                    iteration += 1
                    row.append("")
                    row.append("")
                    row.append("")
                    row.append("")

            #Buttons
            if i < len(self._yellowButton):
                row.append(self._yellowButton[i])
            else:
                row.append("")

            if i < len(self._redButton):
                row.append(self._redButton[i])
            else:
                row.append("")
                
            writer.writerow(row)
            row = []
            i += 1
            
        plt.show(block=True)
        
    def addData(self, data, title):
        if self._firstPlot:
            self._redButton.append(str(time.localtime().tm_hour)+":"+
                                      str(time.localtime().tm_min)+":"+
                                      str(time.localtime().tm_sec))
            self._firstPlot = False
        #Take raw data
        self._dataSegment[title].append(data)
        self._dataSegmentX[title].append(len(self._dataSegment[title]))
        self._dataSegmentTime[title].append(str(time.localtime().tm_hour)+":"+
                                      str(time.localtime().tm_min)+":"+
                                      str(time.localtime().tm_sec))
        
        #filter mode
        if "FILTER" in self._modes[title] and len(self._dataSegment[title]) % self._windowSize == 0:
            self._filteredDataX[title].append(len(self._filteredData[title]))
            self._filteredData[title].append(processFilter(self._dataSegment[title][-10:]))
            self._filteredDataTime[title].append(str(time.localtime().tm_hour)+":"+
                                                 str(time.localtime().tm_min)+":"+
                                                 str(time.localtime().tm_sec))
        
        if "CHANGERATE" in self._modes[title]:
            if "FILTER" in self._modes[title]:
                dataX = self._filteredDataX[title]
                data = self._filteredData[title]
            else:
                dataX = self._dataSegmentX[title]
                data = self._dataSegment[title]
            
            if len(data)>5 and (("FILTER" in self._modes[title] and len(self._dataSegment[title]) % self._windowSize == 0) or not "FILTER" in self._modes[title]):
                currentIndex = dataX[-1]-3
                
                self._changeRateDataX[title].append(len(self._changeRateData[title]))
                self._changeRateData[title].append((-1*data[currentIndex+2]+
                                            8*data[currentIndex+1]-
                                            8*data[currentIndex-1]+
                                            data[currentIndex-2])/(12*PERIOD))
                self._changeRateDataTime[title].append(str(time.localtime().tm_hour)+":"+
                                                 str(time.localtime().tm_min)+":"+
                                                 str(time.localtime().tm_sec))
        
        if "INTERPOLATE" in self._modes[title] and len(self._dataSegment[title]) > 5:
            tck = interpolate.splrep(self._dataSegmentX[title], self._dataSegment[title], s=0)
            self._interpolatedDataX[title] = np.arange(0,len(self._dataSegment[title]),len(self._dataSegment[title])/(len(self._dataSegment[title])*12.5))
            self._interpolatedData[title] = interpolate.splev(self._interpolatedDataX[title], tck, der=0)
          
        self._plotGraph(title)
        
    def _clearData(self):
        self._dataSegment = {"SCR":[],"RR":[], "HR":[], "SST":[]}          #raw data
        self._filteredData = {"SCR":[],"RR":[], "HR":[], "SST":[]}         #filtered data
        self._changeRateData = {"SCR":[],"RR":[], "HR":[], "SST":[]}       #change rate data
        self._interpolatedData = {"SCR":[],"RR":[], "HR":[], "SST":[]}     #interpolated data
    
        self._dataSegmentX = {"SCR":[],"RR":[], "HR":[], "SST":[]}         #raw data X axis
        self._filteredDataX = {"SCR":[],"RR":[], "HR":[], "SST":[]}        #filtered data X axis
        self._changeRateDataX = {"SCR":[],"RR":[], "HR":[], "SST":[]}      #change rate data X axis
        self._interpolatedDataX = {"SCR":[],"RR":[], "HR":[], "SST":[]}    #interpolated data X axis
    
        self._usedData = {"SCR":[],"RR":[], "HR":[], "SST":[]}
        self._usedDataX = {"SCR":[],"RR":[], "HR":[], "SST":[]}

    def _plotGraph(self,title):
        #choose what data to use
        if self._modes[title] == [] or "INTERPOLATE" in self._modes[title]:
            self._usedDataX[title] = self._dataSegmentX[title]
            self._usedData[title] = self._dataSegment[title]
        elif "CHANGERATE" in self._modes[title]:
            self._usedDataX[title] = self._changeRateDataX[title]
            self._usedData[title] = self._changeRateData[title]
        elif "FILTER" in self._modes[title]:
            self._usedDataX[title] = self._filteredDataX[title]
            self._usedData[title] = self._filteredData[title]
        
        #update graph width
        
        if len(self._usedData[title])>0 and self._usedDataX[title][-1] >= self._currentWidth:
            widthBefore = self._currentWidth
            self._currentWidth += GRAPHWIDTH
            self._axSCR.axis([widthBefore, self._currentWidth, -4096, 4096])
        
        
        #plotting

        points = self._axSCR.plot(self._usedDataX[title], self._usedData[title], Colour[title])[0]
        
        # restore background
        self._SCR.canvas.restore_region(self._background)
        # redraw just the points
        self._axSCR.draw_artist(points)
        # fill in the axes rectangle
        self._SCR.canvas.blit(self._axSCR.bbox)

        self._background = self._SCR.canvas

'''
#test
p = Plotter({"SCR":["FILTER","CHANGERATE"],"RR":["FILTER"], "HR":["INTERPOLATE"], "SST":["FILTER"]})
print "Initialised"
for i in range(100):
    tstart = time.time()
    p.addData(10*i+100*random.random(), "SCR")
    p.addData(i+100*random.random(), "RR")
    p.addData(40*i+100*random.random(), "HR")
    p.addData(1000-50*i+100*random.random(), "SST")
    #plt.pause(PERIOD)
    print time.time()-tstart
    
p.stopPlotting()
'''
