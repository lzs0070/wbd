'''
Created on 10/11/2016

@author: sunsuper
'''

import xml.dom.minidom
import Sighting
import Navigation.prod.Angle as Angle
import math

class Sightings():

    def __init__(self, fileName):
        self.sightingFile = fileName

    def setSightings(self):
        try:
            dom = xml.dom.minidom.parse(self.sightingFile)
            root = dom.documentElement
            sightingArray = root.getElementsByTagName('sighting')
            anSightings = []
            
            # travel all sightings
            for i in range(0, len(sightingArray)):
                anSightings.append(Sighting.Sighting(sightingArray[i]))
                if (anSightings[i].parseSighting() == False):
    #                     return False
                    continue
        except:
            return False

        self.sightings = anSightings
        return True
    
    def setReferenceStatus(self, starFileName, ariesFileName):
        for sighting in self.sightings:
            if sighting.getValid() == True:
                sighting.setReference(starFileName, ariesFileName)
            
    def getSightings(self):
        return self.sightings
    
    def getSighting(self, ID):
        return self.sightings[ID]
    
    def setAdjustedAltitudes(self):
        for i in range(0, len(self.sightings)):
            if self.sightings[i].getValid() == True and self.sightings[i].getReference() == True:
                self.sightings[i].setAdjustedAltitude()
    
    def getAdjustedAltitudes(self):
        adjustedAltitudes = []
        for i in range(0, len(self.sightings)):
            if self.sightings[i].getValid() == True and self.sightings[i].getReference() == True:
                adjustedAltitudes.append(self.sightings[i].getAdjustedAltitude())
            else:
                adjustedAltitudes.append([])
        return adjustedAltitudes
    
    def countErrors(self):
        count = 0
        for sighting in self.sightings:
            if sighting.getValid() != True or sighting.getReference() != True:
                count = count + 1
                 
        return count
    
    def calculate(self, starFileName, ariesFileName, assumedLatitude, assumedLongitude):
        sumDistanceCos = 0
        sumDistanceSin = 0
        for sighting in self.sightings:
            if sighting.getValid() == True and sighting.getReference() == True:
                sighting.calculateGeographicalPosition(starFileName, ariesFileName)
                sighting.calculateLHA(assumedLongitude)
                sighting.calculateCorrectedAltitude(assumedLatitude)
                sighting.calculateDistanceAdjustment()
                sighting.calculateAzimuthAdjustment(assumedLatitude)
                sumDistanceCos = sumDistanceCos + sighting.getDistanceAdjustmentArcMin() * sighting.getCosAzimuth()
                sumDistanceSin = sumDistanceSin + sighting.getDistanceAdjustmentArcMin() * sighting.getSinAzimuth()
        sumDistanceCos = sumDistanceCos/60
        sumDistanceSin = sumDistanceSin/60
        
        anAngle = Angle.Angle()
        anAngle.setDegreesAndMinutes(assumedLatitude)
        radianApproximateLatitude = anAngle.getDegrees() + sumDistanceCos
        if radianApproximateLatitude < 0:
            radianApproximateLatitude = -1 * radianApproximateLatitude
            prefix = '-'
        elif radianApproximateLatitude > 270:
            radianApproximateLatitude = 360 - radianApproximateLatitude
            prefix = '-'
        else:
            prefix = ''
        anAngle.setDegreesAndMinutes(assumedLongitude)
        radianApproximateLongitude = anAngle.getDegrees() + sumDistanceSin
        anAngle.setDegrees(radianApproximateLatitude)
        self.approximateLatitude = prefix + anAngle.getString()
        anAngle.setDegrees(radianApproximateLongitude)
        self.approximateLongitude = anAngle.getString()
        

        
        
#         anAngle = Angle.Angle()
#         anAngle.setDegreesAndMinutes(assumedLatitude)
#         totalMinutes = anAngle.getMinutes() + sumDistanceCos
#         anAngle.setMinutes(totalMinutes)
#         self.approximateLatitude = anAngle.getString()
#         anAngle.setDegreesAndMinutes(assumedLongitude)
#         totalMinutes = anAngle.getMinutes() + sumDistanceSin
#         anAngle.setMinutes(totalMinutes)
#         self.approximateLongitude = anAngle.getString()
        
    
    def getApproximateLatitude(self):
        return self.approximateLatitude
    
    def getApproximateLongitude(self):
        return self.approximateLongitude
        
                
                
                
                
                
                