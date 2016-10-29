'''
Created on 10/10/2016

@author: sunsuper
'''

import xml.dom.minidom
import re
import Navigation.prod.Angle as Angle

class Sighting():

    def __init__(self, myNode):
        self.node = myNode
        
    def parseSighting(self):
        try:
            tmpBody = self.node.getElementsByTagName('body')
            if len(tmpBody) == 0:
                return False
            else:
                myBody = tmpBody[0].firstChild.data
            
            tmpTime = self.node.getElementsByTagName('time')
            if len(tmpTime) == 0:
                return False
            else:
                myTime = tmpTime[0].firstChild.data
                
            tmpDate = self.node.getElementsByTagName('date')
            if len(tmpDate) == 0:
                return False
            else:
                myDate = tmpDate[0].firstChild.data
                
            tmpObservation = self.node.getElementsByTagName('observation')
            if len(tmpObservation) == 0:
                return False
            else:
                myObservation = tmpObservation[0].firstChild.data
            
            tmpTemperature = self.node.getElementsByTagName('temperature')
            if len(tmpTemperature) == 0:
                myTemperature = 72
            else:
                myTemperature = tmpTemperature[0].firstChild.data
            
            tmpHeight = self.node.getElementsByTagName('height')
            if len(tmpHeight) == 0:
                myHeight = 0
            else:
                myHeight = tmpHeight[0].firstChild.data
            
            tmpPressure = self.node.getElementsByTagName('pressure')
            if len(tmpPressure) == 0:
                myPressure = 1010
            else:
                myPressure = tmpPressure[0].firstChild.data
           
            tmpHorizon = self.node.getElementsByTagName('horizon')
            if len(tmpHorizon) == 0:
                myHorizon = 'Natural'
            else:
                myHorizon = tmpHorizon[0].firstChild.data
        except:
            return False
        
        if not(self.checkDate(str(myDate))):
            return False
           
        if not(self.checkTime(str(myTime))):
            return False
        
        if not(self.checkAltitude(str(myObservation))):
            return False
        
        if not(self.checkHeight(str(myHeight))):
            return False
        
        if not(self.checkTemperature(myTemperature)):
            return False
        
        if not(self.checkPressure(myPressure)):
            return False
        
        if not(self.checkHorizon(myHorizon)):
            return False
        
        self.body = str(myBody)
        self.time = str(myTime)
        self.date = str(myDate)
        self.observation = str(myObservation)
        self.height = str(myHeight)
        self.temperature = str(myTemperature)
        self.pressure = str(myPressure)
        self.horizon = str(myHorizon)
        
        return True
    
    def checkDate(self, myDate):
        rs_date = r'(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)'
        pattern = re.compile(rs_date)
        match = pattern.match(myDate)
        if not(match):
            return False
        return True
    
    def checkTime(self, myTime):
        rs_time = r'^(0\d{1}|1\d{1}|2[0-3]):[0-5]\d{1}:([0-5]\d{1})$'
        pattern = re.compile(rs_time)
        match = pattern.match(myTime)
        if not(match):
            return False
        return True
    
    def checkAltitude(self, myAltitude):
        anAngle = Angle.Angle()
        try:
            anAngle.setDegreesAndMinutes(str(myAltitude))
        except:
            return False
        if (anAngle.getDegrees() < 0.1/60):
            return False
        return True
        
    def checkHeight(self, myHeight):
        if not(self.isDecimal(str(myHeight))):
            return False
        elif float(str(myHeight)) < 0:
            return False
        return True

    def checkTemperature(self, myTemperature):
        if not(self.isInteger(str(myTemperature))):
            return False
        elif int(myTemperature) < -20 or int(myTemperature) > 120:
            return False
        return True
    
    def checkPressure(self, myPressure):
        if not(self.isInteger(str(myPressure))):
            return False
        elif int(myPressure) < 100 or int(myPressure) > 1100:
            return False
        return True
    
    def checkHorizon(self, myHorizon):
        if str(myHorizon) != 'Artificial' and str(myHorizon) != 'Natural' and str(myHorizon) != 'artificial' and str(myHorizon) != 'natural':
#         if str(myHorizon) != 'Artificial' and str(myHorizon) != 'Natural':
            return False
        return True
    
    def getBody(self):
        return self.body
    
    def getTime(self):
        return self.time
    
    def getDate(self):
        return self.date
    
    def getObservation(self):
        return self.observation
    
    def getHeight(self):
        return self.height
    
    def getTemperature(self):
        return self.temperature
    
    def getPressure(self):
        return self.pressure
    
    def getHorizon(self):
        return self.horizon
    
    def isDecimal(self, param):
        try:
            float(param)
        except:
            return False
        return True
    
    def isInteger(self, param):
        try:
            int(param)
        except:
            return False
        return True
            