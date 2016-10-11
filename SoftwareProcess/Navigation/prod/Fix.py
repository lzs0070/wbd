'''
Created on 10/08/2016

@author: sunsuper
'''

import Angle
import re
import xml.dom.minidom

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
            f = open(myLogFile, 'w')
            f.write("Start of log")
            f.close()
        except:
            raise ValueError(functionName + "File error.")
        
        self.logFile = myLogFile
        self.sightingFile = None
    
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
             
        self.sightingFile = mySightingFile
        return mySightingFile
    
    def getSightings(self):
        functionName = "Fix.getSightings:  "
        if (self.sightingFile == None):
            raise ValueError(functionName + "No sighting file has been set.")
#         try:
#             f = open(self.sightingFile, 'r')
#             f.close()
#         except:
#             raise ValueError(functionName + "File cannot be opened.")
        
        try:
            dom = xml.dom.minidom.parse(self.sightingFile)
            root = dom.documentElement
        except:
            print("emp")
        sightingArray = root.getElementsByTagName('sighting')
        numSighting = len(sightingArray)
        order = [numSighting]
        bodyArray = root.getElementsByTagName('body')
        numBody = len(bodyArray)
        timeArray = root.getElementsByTagName('time')
        numTime = len(timeArray)
        observationArray = root.getElementsByTagName('observation')
        numObservation = len(observationArray)
        dateArray = root.getElementsByTagName('date')
        numDate = len(dateArray)
        
        if (numSighting != numBody or numSighting != numTime
             or numSighting != numDate or numSighting != numObservation):
            raise ValueError(functionName + "A mandatory tag is missing.")
        
        # test of invalid date
        rs_date = r'(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)'
        pattern = re.compile(rs_date)
        for i in range(0, numDate):
            myDate = dateArray[i].firstChild.data
            match = pattern.match(str(myDate))
            if not(match):
                raise ValueError(functionName + "Invalid date.")

        # test of invalid time
        rs_time = r'^(0\d{1}|1\d{1}|2[0-3]):[0-5]\d{1}:([0-5]\d{1})$'
        pattern = re.compile(rs_time)
        for i in range(0, numTime):
            myTime = timeArray[i].firstChild.data
            match = pattern.match(str(myTime))
            if not(match):
                raise ValueError(functionName + "Invalid time.")





        
        