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
import LogFile
import os

class Fix():
    '''
    Read navigational sightings and to adjust those sightings based on atmospheric conditions.
    '''

    def __init__(self, logFile = None):
        functionName = "Fix.__init__:  "
        if(logFile == None):
            logFile = "log.txt"
        elif(not(isinstance(logFile, basestring))):
            raise ValueError(functionName + "The name should be a string.")
        elif(logFile == ""):
            raise ValueError(functionName + "The name should be a string having a length .GE. 1.")
        
        self.LogFile = LogFile.LogFile(logFile)
        myStr = "LOG:\t" + self.getDateTime() + "\tLog file:\t" + self.LogFile.getFilePath() + '\n'
        if self.LogFile.log(myStr) == False:
            raise ValueError(functionName + "File error.")

        self.logFileName = logFile
        self.sightingFileName = None
        self.ariesFileName = None
        self.starFileName = None

    def getDateTime(self):
        myTime = time.strftime('%y-%m-%d %H:%M:%S', time.localtime(time.time())) + ('-' if time.timezone > 0 else '+') + time.strftime('%H:%M', time.gmtime(abs(time.timezone)))
        return myTime
    
    def setSightingFile(self, sightingFile = None):
        functionName = "Fix.setSightingFile:  "
        if (sightingFile == None):
            raise ValueError(functionName + "There is no input.")
        elif (sightingFile == ""):
            raise ValueError(functionName + "File name is empty.")
        try:
            pattern = re.compile(r'.\.xml\Z')
            match = pattern.search(sightingFile)
            if not(match):
                raise ValueError(functionName + "File name is invalid.")
        except:
            raise ValueError(functionName + "File name is invalid.")
        
        try:
            f = open(sightingFile, 'r')
            f.close()
        except:
            raise ValueError(functionName + "File cannot be opened.")

        ABSPATH = os.path.abspath(sightingFile)
        myStr = "LOG:\t" + self.getDateTime() + "\tSighting file:\t" + ABSPATH + "\n"
        self.LogFile.log(myStr)
        
        self.sightingFileName = sightingFile
        
        return ABSPATH
    
    def getSightings(self):
        functionName = "Fix.getSightings:  "
        if (self.sightingFileName == None):
            raise ValueError(functionName + "No sighting file has been set.")
        if (self.ariesFileName == None):
            raise ValueError(functionName + "No aries file has been set.")
        if (self.starFileName == None):
            raise ValueError(functionName + "No star file has been set.")

        anSightings = Sightings.Sightings(self.sightingFileName)
        if(anSightings.setSightings() == False):
            raise ValueError(functionName + "Errors are encountered in the sighting file.")

        self.sightings = anSightings
        self.sightings.setReferenceStatus(self.starFileName, self.ariesFileName)
        self.adjustedAltitudes = self.adjustAltitudes(anSightings.getSightings())
        self.sightings.calculation(self.starFileName, self.ariesFileName)
        
        self.writeAltitude()
        number = self.sightings.countErrors()
        myStr = "LOG:\t" + self.getDateTime() + "\tSighting errors:\t" + str(number) + "\n"
        self.LogFile.log(myStr)
        approximateLatitude = "0d0.0"
        approximateLongitude = "0d0.0"
        return (approximateLatitude, approximateLongitude) 
    
    def adjustAltitudes(self, sightings):
        adjustedAltitudes = []
        for i in range(0, len(sightings)):
            if sightings[i].getValid() == True and sightings[i].getReference() == True:
                adjustedAltitudes.append(self.adjustAltitude(sightings[i]))
            else:
                adjustedAltitudes.append([])
        return adjustedAltitudes
    
    def adjustAltitude(self, sighting):
        height = float(sighting.getHeight())
        pressure = float(sighting.getPressure())
        temperature = float(sighting.getTemperature())
        observedAltitude = sighting.getObservation()
        horizon = sighting.getHorizon()
        
        if horizon == 'Natural' or horizon == 'natural':
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
        sightings = self.sightings.getSightings()
        numSighting = len(sightings)
        adjustedAltitudeArr = []
        orderArr = []
        for i in range(0, numSighting):
            sighting = sightings[i]
            if sighting.getValid() == True and sighting.getReference() == True:
                adjustedAltitude = self.adjustAltitude(sighting)
                adjustedAltitudeArr.append(adjustedAltitude)
                elements = []
                elements.append(sighting.getDate())
                elements.append(sighting.getTime())
                elements.append(sighting.getBody())
                elements.append(self.adjustedAltitudes[i])
                elements.append(sighting.getLatitude())
                elements.append(sighting.getLongitude())
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
        f = open(self.logFileName, 'a')
        for i in arr:
            myStr = "LOG:\t" + self.getDateTime() + "\t" + i[2] + "\t" + i[0] + " \t " + i[1] + " \t " + i[3] + " \t " + i[4] + " \t " + i[5] + " \n"
            f.write(myStr)
#         myStr = "LOG: " + self.getDateTime() + " End of sighting file:  " + self.sightingFileName + "\n"
#         f.write(myStr)
        f.close()
    
    def setAriesFile(self, ariesFile = None):
        functionName = "Fix.setAriesFile:"
        if (ariesFile == None):
            raise ValueError(functionName + "There is no input.")
        elif (ariesFile == ".txt"):
            raise ValueError(functionName + "File name is empty.")
        try:
            pattern = re.compile(r'.\.txt\Z')
            match = pattern.search(ariesFile)
            if not(match):
                raise ValueError(functionName + "File name is invalid.")
        except:
            raise ValueError(functionName + "File name is invalid.")
        
        try:
            f = open(ariesFile, 'r')
            f.close()
        except:
            raise ValueError(functionName + "File cannot be opened.")
        
        ABSPATH = os.path.abspath(ariesFile)
        myStr = "LOG:\t" + self.getDateTime() + "\tAries file:\t" + ABSPATH + "\n"
        self.LogFile.log(myStr)
        
        self.ariesFileName = ariesFile
        
        return ABSPATH
    
    def setStarFile(self, starFile = None):
        functionName = "Fix.setStarFile:"
        if (starFile == None):
            raise ValueError(functionName + "There is no input.")
        elif (starFile == ".txt"):
            raise ValueError(functionName + "File name is empty.")
        try:
            pattern = re.compile(r'.\.txt\Z')
            match = pattern.search(starFile)
            if not(match):
                raise ValueError(functionName + "File name is invalid.")
        except:
            raise ValueError(functionName + "File name is invalid.")
        
        try:
            f = open(starFile, 'r')
            f.close()
        except:
            raise ValueError(functionName + "File cannot be opened.")
        
        ABSPATH = os.path.abspath(starFile)
        myStr = "LOG:\t" + self.getDateTime() + "\tStar file:\t" + ABSPATH + "\n"
        self.LogFile.log(myStr)
        
        self.starFileName = starFile
        
        return ABSPATH