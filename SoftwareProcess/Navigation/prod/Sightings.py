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
            for i in range(0, len(sightingArray)):
                anSightings.append(Sighting.Sighting(sightingArray[i]))
                if (anSightings[i].parseSighting() == False):
                    return False
        except:
            return False

        self.sightings = anSightings
        return True
    
    def getSightings(self):
        return self.sightings
    
    def getSighting(self, ID):
        return self.sightings[ID]
    

        