'''
Created on 10/11/2016

@author: sunsuper
'''

import xml.dom.minidom
import Sighting

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
    
    def countErrors(self):
        count = 0
        for sighting in self.sightings:
            if sighting.getValid() != True or sighting.getReference() != True:
                count = count + 1
                 
        return count
    
    def calculation(self, starFileName, ariesFileName):
        for sighting in self.sightings:
            if sighting.getValid() == True and sighting.getReference() == True:
                sighting.calculationGeographicalPosition(starFileName, ariesFileName)