'''
Created on 10/11/2016

@author: sunsuper
'''

import xml.dom.minidom

class Sightings():

    def __init__(self, fileName):
        self.sightingFile = fileName
        try:
            dom = xml.dom.minidom.parse(self.sightingFile)
            root = dom.documentElement
            sightingArray = root.getElementsByTagName('sighting')
            self.sightings = sightingArray
            return True
        except:
            return False

    def getSightings(self):
        return self.sightings
    
    def getSighting(self, ID):
        return self.sightings[ID]
    

        