'''
Created on 10/08/2016

@author: sunsuper
'''

import Angle
import Sightings
import re
import xml.dom.minidom
import math
import time


class Fix():
    '''
    Read navigational sightings and to adjust those sightings based on atmospheric conditions.
    '''

    def __init__(self, myLogFile = None):
        functionName = "Fix.__init__:  "
        if(myLogFile == None):
            myLogFile = "log.txt"
        elif(not(isinstance(myLogFile, basestring))):
            raise ValueError(functionName + "The name should be a string.")
        elif(myLogFile == ""):
            raise ValueError(functionName + "The name should be a string having a length .GE. 1.")
        
        try:
            f = open(myLogFile, 'a')
            myStr = "LOG: " + self.getDateTime() + " Start of log\n"
            f.write(myStr)
        except:
            raise ValueError(functionName + "File error.")
        
        self.logFile = f
        self.logFileName = myLogFile
        self.sightingFileName = None

    def getDateTime(self):
        myTime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime(time.time())) + ('-' if time.timezone > 0 else '+') + time.strftime('%H:%M', time.gmtime(abs(time.timezone)))
        return myTime
    
    def setSightingFile(self, mySightingFile = None):
        functionName = "Fix.setSightingFile:  "
        if (mySightingFile == None):
            raise ValueError(functionName + "There is no input.")
        elif (mySightingFile == ""):
            raise ValueError(functionName + "File name is empty.")
        else:
            pattern = re.compile(r'.\.xml\Z')
            match = pattern.search(mySightingFile)
            if not(match):
                raise ValueError(functionName + "File name is invalid.")
        
        try:
            f = open(mySightingFile, 'r')
            f.close()
        except:
            raise ValueError(functionName + "File cannot be opened.")
             
        self.sightingFileName = mySightingFile
        
        myStr = "LOG: " + self.getDateTime() + " Start of sighting file:  " + self.sightingFileName + "\n"
        self.logFile.write(myStr)
        return mySightingFile
    
    def getSightings(self):
        functionName = "Fix.getSightings:  "
        if (self.sightingFileName == None):
            raise ValueError(functionName + "No sighting file has been set.")

        anSightings = Sightings.Sightings(self.sightingFileName)
        if(anSightings.setSightings() == False):
            raise ValueError(functionName + "Errors are encountered in the sighting file.")

        self.sightings = anSightings.getSightings()
        self.adjustedAltitudes = self.adjustAltitudes(anSightings.getSightings())
        
        self.writeAltitude()
        approximateLatitude = "0d0.0"
        approximateLongitude = "0d0.0"
        return (approximateLatitude, approximateLongitude) 
    
    def adjustAltitudes(self, sightings):
        adjustedAltitudes = []
        for i in sightings:
            adjustedAltitudes.append(self.adjustAltitude(i))
        return adjustedAltitudes
    
    def adjustAltitude(self, sighting):
        height = float(sighting.getHeight())
        pressure = float(sighting.getPressure())
        temperature = float(sighting.getTemperature())
        observedAltitude = sighting.getObservation()
        horizon = sighting.getHorizon()
        
        if horizon == 'Natural':
            dip = (-0.97 * math.sqrt(height)) / 60
        else:
            dip = 0
        c_temp = (temperature - 32)/1.8
        anAngle = Angle.Angle()
        anAngle.setDegreesAndMinutes(observedAltitude)
        refrection = (-0.00452 * pressure)/(273 + c_temp)/(math.tan(anAngle.getDegrees()*math.pi/180))
        adjustedAltitude = anAngle.getDegrees() + dip + refrection
#         adjustedAltitude = round(adjustedAltitude, 1)
        anAngle.setDegrees(adjustedAltitude)
        return anAngle.getString()

    def writeAltitude(self):
        sightings = self.sightings
        numSighting = len(sightings)
        adjustedAltitudeArr = []
        orderArr = []
        for i in range(0, numSighting):
            sighting = sightings[i]
            adjustedAltitude = self.adjustAltitude(sighting)
            adjustedAltitudeArr.append(adjustedAltitude)
            elements = []
            elements.append(sighting.getDate())
            elements.append(sighting.getTime())
            elements.append(sighting.getBody())
            elements.append(self.adjustedAltitudes[i])
            orderArr.append(elements)
    
        sortedOrder = self.sort(orderArr)
        self.writeLogFile(sortedOrder)

    def sort(self, arr):
        for i in range(0, len(arr) - 1):
            for j in range(0, len(arr) - 1 - i):
                if (arr[j][0] > arr[j + 1][0]):
                    tmp = arr[j]
                    arr[j] = arr[j + 1]
                    arr[j + 1] = tmp
                elif (arr[j][0] == arr[j + 1][0]):
                    if (arr[j][1] > arr[j + 1][1]):
                        tmp = arr[j]
                        arr[j] = arr[j + 1]
                        arr[j + 1] = tmp
                    elif (arr[j][1] == arr[j + 1][1]):
                        if (arr[j][2] > arr[j + 1][2]):
                            tmp = arr[j]
                            arr[j] = arr[j + 1]
                            arr[j + 1] = tmp
        return arr
    
    def getAdjustedAltitudes(self):
        return self.adjustedAltitudes
    
    def writeLogFile(self, arr):
#         f = open(self.logFileName, "w")
        for i in arr:
            myStr = "LOG: " + self.getDateTime() + " " + i[2] + "\t " + i[0] + " \t " + i[1] + " \t " + i[3] + " \n"
            self.logFile.write(myStr)
        myStr = "LOG: " + self.getDateTime() + " Ending of sighiting file:  " + self.sightingFileName + "\n"
        self.logFile.write(myStr)
        self.logFile.close()
        
        
        