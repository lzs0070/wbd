'''
Created on 10/10/2016

@author: sunsuper
'''

import xml.dom.minidom

class Sighting():

    def __init__(self, myNode):
        self.node = myNode
        try:
            tmpBody = myNode.getElementsByTagName('body')
            tmpTime = myNode.getElementsByTagName('time')
            tmpDate = myNode.getElementsByTagName('date')
            tmpObservation = myNode.getElementsByTagName('observation')
            self.body = tmpBody[0].firstChild.data
            self.time = tmpTime[0].firstChild.data
            self.date = tmpDate[0].firstChild.data
            self.observation = tmpObservation[0].firstChild.data
            return True
        except:
            return False
        
    def getBody(self):
        return self.body
    
    def getTime(self):
        return self.time
    
    def getDate(self):
        return self.date
    
    def getObservation(self):
        return self.observation
        