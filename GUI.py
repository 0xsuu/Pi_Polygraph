
from Tkinter import *
from threading import Thread

#Custom libs
from ADC import *
from PlotGraph import *

#Global Variables
i2cAddress = 0x21

redButtonPin = 17
yellowButtonPin = 23
heartRatePin = 18

ledPins = [5,6,12,13,16,19,20,26]
thereHold = 204.8

calibrateWindowWidth = 300
calibrateWindowHeight = 150

interviewWindowWidth = 300
interviewWindowHeight = 180

class GUI(Frame):
    def __init__(self, master):
        #General initialization
        GPIO.setwarnings(False) 	#disable runtime warnings
        GPIO.setmode(GPIO.BCM)		#use Broadcom GPIO names
        
        #initialize 4 ports
        self._jp4 = ADC(i2cAddress, "JP4")
        self._jp5 = ADC(i2cAddress, "JP5")
        self._jp6 = ADC(i2cAddress, "JP6")
        self._jp7 = ADC(i2cAddress, "JP7")
        
        #GUI initialization
        Frame.__init__(self, master)
        self._master = master
        
        self._interviewing = False
        self._redButtonPressed = False
        
        self.pack()
        self._createWidgetsForCalibrateMode()
            
    #############################
    #
    # Calibrate Mode
    #
    #############################
    #Create Calibrate Widgets
    def _createWidgetsForCalibrateMode(self):
        #clean up
        for widget in self.winfo_children():
            widget.destroy()

        #Set resolution
        self._master.geometry(str(calibrateWindowWidth)+"x"+str(calibrateWindowHeight))
        
        #draw common widgets
        self._createCommonWidgets(0)
        self._modeMenu.place(x=self.winfo_width()/2-self._modeMenu.winfo_reqwidth()/2, y=10)
        
        #draw calibrate widgets
        #2 labels for SCR and RR
        JP5Label = Label(self)
        JP5Label["text"] = "SCR"
        JP5Label.place(x=calibrateWindowWidth/3.0-JP5Label.winfo_reqwidth()/2.0, 
                       y=self.winfo_height()/2.0 - 20)
        
        JP4Label = Label(self)
        JP4Label["text"] = "RR"
        JP4Label.place(x=2*calibrateWindowWidth/3.0-JP4Label.winfo_reqwidth()/2.0, 
                       y=self.winfo_height()/2.0 - 20)

        #2 labels for showing data
        self._JP5CaliLabel = Label(self)
        self._JP5CaliLabel["text"] = "No Data"
        self._JP5CaliLabel.place(x=calibrateWindowWidth/3.0-self._JP5CaliLabel.winfo_reqwidth()/2.0-10, 
                           y=self.winfo_height()/2.0)

        self._JP4CaliLabel = Label(self)
        self._JP4CaliLabel["text"] = "No Data"
        self._JP4CaliLabel.place(x=2*calibrateWindowWidth/3.0-self._JP4CaliLabel.winfo_reqwidth()/2.0+10, 
                           y=self.winfo_height()/2.0)
        
        #Thread for SCR and RR                   
        self._threadCaliRun = True
        self._threadUpdateJP5CaliData = Thread(target = self._updateJP5CaliLabel, args=())
        self._threadUpdateJP5CaliData.start()  
        self._threadUpdateJP4CaliData = Thread(target = self._updateJP4CaliLabel, args=())
        self._threadUpdateJP4CaliData.start()
         
        #GPIO.setup(heartRatePin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        #GPIO.add_event_detect(heartRatePin, GPIO.RISING, callback=self._updateHeartRateCaliData)
        
        #Thread for HR
        for i in ledPins:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, False)
        self._currentLED = 0
        self._threadUpdateHeartRateCaliData = Thread(target = self._updateHeartRateCaliData, args=())
        self._threadUpdateHeartRateCaliData.start() 

    #RR
    def _updateJP5CaliLabel(self):
        #Loop start
        if self._threadCaliRun:
            data = self._jp5.readData()
            if data < 2048 - thereHold:
                self._JP5CaliLabel["fg"] = "red"
                self._JP5CaliLabel["text"] = "Decrease "+str(data-2048)
            elif data > 2048 + thereHold:
                self._JP5CaliLabel["fg"] = "red"
                self._JP5CaliLabel["text"] = "Increase "+str(data-2048)
            else:
                self._JP5CaliLabel["fg"] = "green"
                self._JP5CaliLabel["text"] = "Calibreated "+str(data-2048)
            
            self._JP5CaliLabel.place(x=calibrateWindowWidth/3.0-self._JP5CaliLabel.winfo_reqwidth()/2.0-10, 
                           y=self.winfo_height()/2.0)
            #Loop end
            self._JP5CaliLabel.after(1000, self._updateJP5CaliLabel)
    
    #SCR        
    def _updateJP4CaliLabel(self):
        #Loop start
        if self._threadCaliRun:
            data = self._jp4.readData()
            if data < 2048 - thereHold:
                self._JP4CaliLabel["fg"] = "red"
                self._JP4CaliLabel["text"] = "Decrease "+str(data-2048)
            elif data > 2048 + thereHold:
                self._JP4CaliLabel["fg"] = "red"
                self._JP4CaliLabel["text"] = "Increase "+str(data-2048)
            else:
                self._JP4CaliLabel["fg"] = "green"
                self._JP4CaliLabel["text"] = "Calibreated "+str(data-2048)
            
            self._JP4CaliLabel.place(x=2*calibrateWindowWidth/3.0-self._JP4CaliLabel.winfo_reqwidth()/2.0+10, 
                           y=self.winfo_height()/2.0)
            
            #Loop end
            self._JP4CaliLabel.after(1000, self._updateJP4CaliLabel)
            
    #HR
    def _updateHeartRateCaliData(self):
        #Loop start
        if self._threadCaliRun:
            data = self._jp7.readData()
            self._lightUp(int(round(data/4096.0 *8)))
            
            #Loop end
            self.after(125, self._updateHeartRateCaliData)
            
    #Set Pi LED to ledLength
    def _lightUp(self, ledLength):
        #Error detecting
        if ledLength > 8:
            print "ledLength too large"
            return
            
        #Turn on or off the LED
        if ledLength > self._currentLED:
            for i in range(self._currentLED, ledLength):
                LED = ledPins[i]
                GPIO.output(LED, True)
        elif ledLength < self._currentLED:
            for i in range(ledLength, self._currentLED):
                LED = ledPins[ledLength + self._currentLED - 1 - i]
                GPIO.output(LED, False)
                
        self._currentLED = ledLength
        
        
    #############################
    #
    # Interview Mode
    #
    #############################
    #Create Interview Widgets
    def _createWidgetsForInterviewMode(self):
        #clean up
        for widget in self.winfo_children():
            widget.destroy()

        #Set resolution
        self._master.geometry(str(interviewWindowWidth)+"x"+str(interviewWindowHeight))
        
        #draw common widgets
        self._createCommonWidgets(1)
        self._modeMenu.place(x=self.winfo_width()/2-self._modeMenu.winfo_reqwidth()/2, y=10)

        #Set up GPIO Event
        GPIO.setup(redButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(redButtonPin, GPIO.RISING, callback=self._questionAsked, bouncetime=500)

        GPIO.setup(yellowButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(yellowButtonPin, GPIO.RISING, callback=self._responseGiven, bouncetime=500)

        self._SCRDataLabel = Label(self)
        self._SCRDataLabel["text"] = "SCR Data"
        self._SCRDataLabel.place(x=20, y=50)
        
        self._RRDataLabel = Label(self)
        self._RRDataLabel["text"] = "RR Data"
        self._RRDataLabel.place(x=20, y=75)
        
        self._HRDataLabel = Label(self)
        self._HRDataLabel["text"] = "HR Data"
        self._HRDataLabel.place(x=20, y=100)
        
        self._SSTDataLabel = Label(self)
        self._SSTDataLabel["text"] = "SST Data"
        self._SSTDataLabel.place(x=20, y=125)
        
        self._SCRFilter = IntVar()
        SCRFilterChk = Checkbutton(self, text="Filter", variable=self._SCRFilter)
        SCRFilterChk.place(x=90, y=50)
        
        self._SCRChangeRate = IntVar()
        SCRChangeRateChk = Checkbutton(self, text="Change Rate", variable=self._SCRChangeRate)
        SCRChangeRateChk.place(x=145, y=50)
        
        self._RRFilter = IntVar()
        RRFilterChk = Checkbutton(self, text="Filter", variable=self._RRFilter)
        RRFilterChk.place(x=90, y=75)
        
        self._HRInterpolate = IntVar()
        HRInterpolateChk = Checkbutton(self, text="Interpolate", variable=self._HRInterpolate)
        HRInterpolateChk.place(x=90, y=100)
        
        self._SSTFilter = IntVar()
        SSTFilterChk = Checkbutton(self, text="Filter", variable=self._SSTFilter)
        SSTFilterChk.place(x=90, y=125)
        
        #Start Button
        self._startInterview = Button(self)
        self._startInterview["text"] = "Start"
        self._startInterview["command"] = self._startTheInterview
        self._startInterview.place(x=self.winfo_width()/2-self._startInterview.winfo_reqwidth()/2, y=self.winfo_height()-35)
        
    def _startTheInterview(self):
        tmpSCR = []
        tmpRR = []
        tmpHR = []
        tmpSST = []
        
        if self._SCRFilter.get()==1:
            tmpSCR.append("FILTER")
        if self._SCRChangeRate.get()==1:
            tmpSCR.append("CHANGERATE")
        if self._RRFilter.get()==1:
            tmpRR.append("FILTER")
        if self._HRInterpolate.get()==1:
            tmpHR.append("INTERPOLATE")
        if self._SSTFilter.get()==1:
            tmpSST.append("FILTER")
            
        self._p = Plotter({"SCR":tmpSCR,
                          "RR":tmpRR,
                          "HR":tmpHR,
                          "SST":tmpSST})
        self._interviewing = True
        self._readData()
         
    def _readData(self):
        if self._interviewing:
            if self._redButtonPressed:
                self._p.addData(self._jp5.readData(), "SCR")
                self._p.addData(self._jp4.readData(), "RR")
                self._p.addData(self._jp7.readData(), "HR")
                self._p.addData(self._jp6.readData(), "SST")
            
            self.after(125, self._readData)
        else:
            self._p.stopPlotting()
        
    def _questionAsked(self, pin):
        self._redButtonPressed = True

    def _responseGiven(self, pin):
        self._redButtonPressed = False
        self._interviewing = False
        
        
    #############################
    #
    # Common stuff
    #
    #############################
    def _createCommonWidgets(self, mode):
        self.pack(fill=BOTH, expand=1)
        
        #Quit button
        self._QUIT = Button(self)
        self._QUIT["text"] = "Quit"
        self._QUIT["command"] =  self._quit

        self.update() #update frame to get current resolution
        self._QUIT.place(x=self.winfo_width() - 60, y=self.winfo_height() - 35) #set at bottom right
        
        #Switch mode option menu
        items = ["Calibreate Mode", "Interview Mode"]

        self._choice = StringVar()
        self._choice.set(items[mode])
        self._choice.trace("w", self._switchMode)
        self._modeMenu = OptionMenu(self, self._choice, *items)
        self._modeMenu.command = self._switchMode
        
    #Quit function override
    def _quit(self):
        self._threadCaliRun = False
        self._master.destroy()
        
    #Switch mode
    def _switchMode(self, *args):
        if self._choice.get() == "Interview Mode":
            self._threadCaliRun = False
            self._createWidgetsForInterviewMode()
        elif self._choice.get() == "Calibreate Mode":
            self._createWidgetsForCalibrateMode()

        
        

