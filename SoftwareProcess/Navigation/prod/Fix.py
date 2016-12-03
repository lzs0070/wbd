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
from math import degrees

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
    
    def getSightings(self, assumedLatitude = None, assumedLongitude = None):
        functionName = "Fix.getSightings:  "
        if (self.sightingFileName == None):
            raise ValueError(functionName + "No sighting file has been set.")
        if (self.ariesFileName == None):
            raise ValueError(functionName + "No aries file has been set.")
        if (self.starFileName == None):
            raise ValueError(functionName + "No star file has been set.")

        if (assumedLatitude == None):
            assumedLatitude = "0d0.0"
        if (assumedLongitude == None):
            assumedLongitude = "0d0.0"
        
        if self.checkAssumedLatitude(assumedLatitude) == False:
            raise ValueError(functionName + "Invalid Latitude.")
        if self.checkAssumedLongitude(assumedLongitude) == False:
            raise ValueError(functionName + "Invalid Longitude.")
        
        assumedLatitude.replace(' ', '')
        assumedLongitude.replace(' ', '')
        
        if assumedLatitude[0] == 'N' or assumedLatitude[0] == 'n':
            myPrefix = 'N'
            realAssumedLatitude = assumedLatitude[1 : len(assumedLatitude)]
        elif assumedLatitude[0] == 'S' or assumedLatitude[0] == 's':
            myPrefix = 'S'
            realAssumedLatitude = '-' + assumedLatitude[1 : len(assumedLatitude)]
        else:
            myPrefix = ''
            realAssumedLatitude = assumedLatitude
        
        self.assumedLatitude = assumedLatitude
        self.assumedLongitude = assumedLongitude
        self.prefix = myPrefix

        anSightings = Sightings.Sightings(self.sightingFileName)
        if(anSightings.setSightings() == False):
            raise ValueError(functionName + "Errors are encountered in the sighting file.")

        self.sightings = anSightings
        self.sightings.setReferenceStatus(self.starFileName, self.ariesFileName)
        self.sightings.setAdjustedAltitudes()
        self.sightings.calculate(self.starFileName, self.ariesFileName, realAssumedLatitude, assumedLongitude)
        self.writeAltitude()
        
        number = self.sightings.countErrors()
        myStr = "LOG:\t" + self.getDateTime() + "\tSighting errors:\t" + str(number) + "\n"
        self.LogFile.log(myStr)
        
        approAltitude = self.sightings.getApproximateLatitude()
        if approAltitude[0] == '-':
            approAltitude = 'S' + approAltitude[1:len(approAltitude)]
            
        else:
            approAltitude = 'N' + approAltitude
        myStr = "LOG:\t" + self.getDateTime() + "\tApproximate latitude:\t" + approAltitude + "\tApproximate longitude:\t" + self.sightings.getApproximateLongitude() + "\n"
        self.LogFile.log(myStr)
#         approximateLatitude = "0d0.0"
#         approximateLongitude = "0d0.0"
        return (myPrefix + self.sightings.getApproximateLatitude(), self.sightings.getApproximateLongitude()) 
    
#     def adjustAltitudes(self, sightings):
#         adjustedAltitudes = []
#         for i in range(0, len(sightings)):
#             if sightings[i].getValid() == True and sightings[i].getReference() == True:
#                 adjustedAltitudes.append(self.adjustAltitude(sightings[i]))
#             else:
#                 adjustedAltitudes.append([])
#         return adjustedAltitudes
#     
#     def adjustAltitude(self, sighting):
#         height = float(sighting.getHeight())
#         pressure = float(sighting.getPressure())
#         temperature = float(sighting.getTemperature())
#         observedAltitude = sighting.getObservation()
#         horizon = sighting.getHorizon()
#         
#         if horizon == 'Natural' or horizon == 'natural':
#             dip = (-0.97 * math.sqrt(height)) / 60
#         else:
#             dip = 0
#         c_temp = (temperature - 32)/1.8
#         anAngle = Angle.Angle()
#         anAngle.setDegreesAndMinutes(observedAltitude)
#         refrection = (-0.00452 * pressure)/(273 + c_temp)/(math.tan(anAngle.getDegrees()*math.pi/180))
#         adjustedAltitude = anAngle.getDegrees() + dip + refrection
# #         adjustedAltitude = round(adjustedAltitude, 1)
#         anAngle.setDegrees(adjustedAltitude)
#         return anAngle.getString()

    def writeAltitude(self):
        sightings = self.sightings.getSightings()
        numSighting = len(sightings)
        orderArr = []
        for i in range(0, numSighting):
            sighting = sightings[i]
            if sighting.getValid() == True and sighting.getReference() == True:
                elements = []
                elements.append(sighting.getDate())
                elements.append(sighting.getTime())
                elements.append(sighting.getBody())
                elements.append(sighting.getAdjustedAltitude())
                elements.append(sighting.getGeographicLatitude())
                elements.append(sighting.getGeographicLongitude())
                elements.append(self.assumedLatitude)
                elements.append(self.assumedLongitude)
                elements.append(sighting.getAzimuthAdjustment())
                elements.append(sighting.getDistanceAdjustmentArcMin())
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
            myStr = "LOG:\t" + self.getDateTime() + "\t" + i[2] + "\t " + i[0] + " \t " + i[1] + " \t " + i[3] + " \t " + i[4] + " \t " + i[5] + " \t " + i[6] + " \t " + i[7] + " \t " + i[8] +" \t " + str(i[9]) + " \n"
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
    
    def checkAssumedLatitude(self, assumedLatitude):
        if assumedLatitude == '':
            return False
         
        try:
            assumedLatitude.strip()
        except:
            return False
        
        if assumedLatitude == '0d0.0':
            return True;
        
        hPart = assumedLatitude[0]
        anglePart = assumedLatitude[1:len(assumedLatitude)].strip()
        if hPart == 'N' or hPart == 'n' or hPart == 'S' or hPart == 's':
            if anglePart == '0d0.0':
                return False
            else:
                if self.verifyLatitude(anglePart) == False:
                    return False;
        elif anglePart != '0d0.0':
            return False
            
        return True
    
    def checkAssumedLongitude(self, assumedLongitude):
        if assumedLongitude == '':
            return False
        
        try:
            assumedLongitude.strip()
        except:
            return False
        
        if self.verifyLongitute(assumedLongitude) == False:
            return False;
        
        return True

    
    def verifyLatitude(self, latitude):
        if latitude == '':
            return False
        
        try:
            # locate 'd' in latitude
            position = latitude.index('d')
        except:
            # if 'd' is missing
            return False
        
        if position == 0:
            # if Degree is missing
            return False
        elif position == len(latitude) - 1:
            # if Minute is missing
            return False
        else:
            firstStr = latitude[0:position]
            secondStr = latitude[position + 1:len(latitude)]
            
            #check Degrees
            if not(self.verifyAltitudeDegree(firstStr)):
                return False
            
            #check minutes
            if not(self.verifyAltitudeMinute(secondStr)):
                return False

        return True
    
    def verifyAltitudeDegree(self, degree):
        if degree[0] == '-':
            return False

        if not(degree.isdigit()):
            # if degree is no integer
            return False

        try:
            if int(degree) < 0 or int(degree) >= 90:
                return False
        except:
            return False
        
        return True
    
    def verifyAltitudeMinute(self, minute):
        #remove the influence of sign when judging whether myStr is digit                 
        if minute[0] == '-':
            return False

        if minute.isdigit():
            # if minute is integer
            return False
        
        try:
            position = minute.index('.')
        except:
            return False
        
        if position != len(minute) - 2:
            # if there is more than one digit at the right of decimal point
            return False
        
        try:
            if float(minute) < 0 or float(minute) >= 60:
                return False
        except:
            return False

        return True
    
    
    def verifyLongitute(self, longitude):
        if longitude == '':
            return False
        
        try:
            # locate 'd' in latitude
            position = longitude.index('d')
        except:
            # if 'd' is missing
            return False
        
        if position == 0:
            # if Degree is missing
            return False
        elif position == len(longitude) - 1:
            # if Minute is missing
            return False
        else:
            firstStr = longitude[0:position]
            secondStr = longitude[position + 1:len(longitude)]
            
            #check Degrees
            if not(self.verifyLongitudeDegree(firstStr)):
                return False
            
            #check minutes
            if not(self.verifyLongitudeMinute(secondStr)):
                return False

        return True
    
    
    def verifyLongitudeDegree(self, degree):
        if degree[0] == '-':
            return False

        if not(degree.isdigit()):
            # if degree is no integer
            return False

        try:
            if int(degree) < 0 or int(degree) >= 360:
                return False
        except:
            return False
        
        return True
    
    def verifyLongitudeMinute(self, minute):
        return self.verifyAltitudeMinute(minute)
    
    
    