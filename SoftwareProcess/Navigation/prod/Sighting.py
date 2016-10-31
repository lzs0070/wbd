'''
Created on 10/10/2016

@author: sunsuper
'''

import xml.dom.minidom
import re
import Navigation.prod.Angle as Angle
import time
import datetime
import math
from Navigation.test.main import latitude, longitude

class Sighting():

    def __init__(self, myNode):
        self.node = myNode
        self.valid = False
        self.referenced = False
        self.starReference = None
        self.starDate = None
        self.ariesReference = None
        self.latitude = None
        self.longitude = None
        
    def parseSighting(self):
        try:
            tmpBody = self.node.getElementsByTagName('body')
            if len(tmpBody) == 0:
                return False
            else:
                myBody = tmpBody[0].firstChild.data
#                 if self.chechStar(strStarFile, myBody) == False:
#                     return False
            
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
        
        if not(self.checkLatitude(str(myObservation))):
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
        self.valid = True
        
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
    
    def checkLatitude(self, myLatitude):
        anAngle = Angle.Angle()
        try:
            anAngle.setDegreesAndMinutes(str(myLatitude))
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
    
    def checkStar(self, strStarFile):
        f = open(strStarFile, 'r')
        result = True
        beforeIndex = -1
        afterIndex = -1
        lines = f.readlines()
        for i in range(0, len(lines)):
            if self.checkStarInfo(lines[i]) == True:
                targetDate = self.getDateFromLine(lines[i])
                deltaDate = self.calculateDeltaDate(targetDate, self.getDate())
                if deltaDate >= 0:
                    if beforeIndex == -1:
                        beforeIndex = i
                        bestBeforeDate = targetDate
                        bestBeforeDateDiffence = deltaDate
                    elif bestBeforeDateDiffence > deltaDate:
                        beforeIndex = i
                        bestBeforeDate = targetDate
                        bestBeforeDateDiffence = deltaDate
                else:
                    if afterIndex == -1:
                        afterIndex = i
                        bestAfterDate = targetDate
                        bestAfterDateDiffence = -1 * deltaDate
                    elif bestAfterDateDiffence > (-1 * deltaDate):
                        afterIndex = i
                        bestAfterDate = targetDate
                        bestAfterDateDiffence = -1 * deltaDate
        f.close()
        if beforeIndex == -1 and afterIndex == -1:
            result = False
        else:
            if beforeIndex != -1:
                self.starReference = beforeIndex
                self.starDate = bestBeforeDate
            else:
                self.starReference = afterIndex
                self.starDate = bestAfterDate
        
        return result
    
    def checkStarInfo(self, line):
        p = line.find('\t')
        if p == -1:
            return False
        else:
            newbody = line[0 : p]
            if newbody != self.body:
                return False
            
            line = line[p + 1 : len(line)]
            p = line.find('\t')
            newdate = line[0 : p]
            if self.checkDateFormat(newdate) == False:
                return False
            
            line = line[p + 1 : len(line)]
            p = line.find('\t')
            longitude = line[0 : p]
            if self.checkLongitudeFormat(longitude) == False:
                return False
            
            line = line[p + 1 : len(line)]
            p = line.find('\t')
            latitude = line[0 : p]
            if self.checkLatitudeFormat(latitude) == False:
                return False

        return True
        
    def checkDateFormat(self, strDate):
        try:
            time.strptime(strDate, '%m/%d/%y')
            p = strDate.find('/')
            month = strDate[0 : p]
            if len(month) != 2:
                return False
            
            strDate = strDate[p + 1 : len(strDate)]
            p = strDate.find('/')
            day = strDate[0 : p]
            if len(day) != 2:
                return False
            
            year = strDate[p + 1 : len(strDate)]
            if len(year) != 2:
                return False
            
            return True
        except:
            return False
    
    def checkLongitudeFormat(self, strLongitude):
        if(strLongitude == ""):
            return False
        
        try:
            position = strLongitude.index('d')
        except ValueError:
            return False

        if(position <= 0):
            return False
        elif(position == len(strLongitude) - 1):
            return False
        else:
            firstStr = strLongitude[0 : position]
            secondStr = strLongitude[position + 1 : len(strLongitude)]
            #check Degrees
            if not(self.verifyDegreeInLongitude(firstStr)):
                return False
            #check minutes
            if not(self.verifyMinuteInLongitude(secondStr)):
                return False
        
        return True
    
    def verifyDegreeInLongitude(self, strDegree):
        try:
            v = eval(strDegree)
        except:
            return False
        
        if type(v) == float:
            return False

        if v < 0 or v >= 360:
            return False

        return True
    
    def verifyMinuteInLongitude(self, strMinute):
        try:
            v = eval(strMinute)
        except:
            return False
        
        if type(v) == int:
            return False
        
        p = strMinute.find('.')
        if p == -1 or p == 0:
            return False
        
        firstStr = strMinute[0 : p]
        secondStr = strMinute[p + 1 : len(strMinute)]
        
        # exclude '0.100000'
        if len(secondStr) > 1:
            return False
        
        try:
            intPart = eval(firstStr)
        except:
            return False
        
        if type(intPart) != int:
            return False
        
        if intPart < 0 or intPart >= 60:
            return False
        
        return True
    
    
    def checkLatitudeFormat(self, strLatitude):
        if(strLatitude == ""):
            return False
        
        try:
            position = strLatitude.index('d')
        except ValueError:
            return False

        if(position <= 0):
            return False
        elif(position == len(strLatitude) - 1):
            return False
        else:
            firstStr = strLatitude[0 : position]
            secondStr = strLatitude[position + 1 : len(strLatitude)]
            #check Degrees
            if not(self.verifyDegreeInLatitude(firstStr)):
                return False
            #check minutes
            if not(self.verifyMinuteInLatitude(secondStr)):
                return False
        
        return True
    
    def verifyDegreeInLatitude(self, strDegree):
        try:
            v = eval(strDegree)
        except:
            return False
        
        if type(v) == float:
            return False

        if v <= -90 or v >= 90:
            return False

        return True
    
    def verifyMinuteInLatitude(self, strMinute):
        return self.verifyMinuteInLongitude(strMinute)
    
    def getValid(self):
        return self.valid
    
    def getReference(self):
        return self.referenced
    
    def checkAries(self, ariesFileName):
        targetDate = self.getDate()
        targetDate = self.convertDateFormat(targetDate)
        targetHour = self.getHour(self.getTime())
        result = False
        f = open(ariesFileName)
        lines = f.readlines()
        for i in range(0, len(lines)):
            if self.checkAriesInfo(lines[i], targetDate, targetHour) == True:
                self.ariesReference = i
                result = True
                break
        
        f.close()
        return result
    
    def checkAriesInfo(self, line, targetDate, targetHour):
        p = line.find('\t')
        if p == -1:
            return False
        else:
            date = line[0 : p]
            if date != targetDate:
                return False
            
            line = line[p + 1 : len(line)]
            p = line.find('\t')
            hours = line[0 : p]
            if self.checkHoursFormat(hours) == False:
                return False
            elif hours != targetHour:
                return False

            line = line[p + 1 : len(line)]
            p = line.find('\t')
            longitude = line[0 : p]
            if self.checkLongitudeFormat(longitude) == False:
                return False

        return True
    
    def convertDateFormat(self, date):  # date: yyyy-mm-dd -> mm/dd/yy
        p = date.find('-')
        year = date[0 : p]
        year = year[2 : len(year)]
        date = date[p + 1 : len(date)]
        p = date.find('-')
        month = date[0 : p]
        date = date[p + 1 : len(date)]
        day = date
        
        newdate = month + '/' + day + '/' + year
        return newdate
    
    def checkHoursFormat(self, hours):
        if len(hours) > 2:
            return False
        try:
            v = eval(hours)
            if type(v) == float:
                return False
            if v < 0 or v > 23:
                return False
            if len(hours) == 2:
                if hours[0] == '0':
                    return False
        except:
            return False
        return True
    
    def getHour(self, strTime):
        p = strTime.find(':')
        hour = strTime[0 : p]
        if len(hour) > 1 and hour[0] == '0':
            hour = hour[1:len(hour)]
        return hour
    
    def setReference(self, starFileName, ariesFileName):
        if self.checkStar(starFileName) == False:
            return False
        
        if self.checkAries(ariesFileName) == False:
            return False
    
        self.referenced = True
        return True
    
    def getDateFromLine(self, line):
        p = line.find('\t')
        line = line[p + 1 : len(line)]
        p = line.find('\t')
        date = line[0 : p]
        return date
    
    def calculateDeltaDate(self, date1, date2):     # date2: yyyy-mm-dd; date1: mm/dd/yy; return date2 - date1
        try:
            # extract date2
            p = date2.find('-')
            year2 = date2[0 : p]
            year2 = year2[2 : len(year2)]
            year2 = int(year2)
            
            date2 = date2[p + 1 : len(date2)]
            p = date2.find('-')
            month2 = date2[0 : p]
            month2 = int(month2)
            
            day2 = date2[p + 1 : len(date2)]
            day2 = int(day2)
            
            # extract date1
            p = date1.find('/')
            month1 = date1[0 : p]
            month1 = int(month1)
            
            date1 = date1[p + 1 : len(date1)]
            p = date1.find('/')
            day1 = date1[0 : p]
            day1 = int(day1)
            
            year1 = date1[p + 1 : len(date1)]
            year1 = int(year1)
            
            d1 = datetime.datetime(year1, month1, day1)
            d2 = datetime.datetime(year2, month2, day2)
        except:
            pass
        
        return (d2 - d1).days
    
    def getLongitudeFromAries(self, line):
        p = line.find('\t')
        line = line[p + 1 : len(line)]
        p = line.find('\t')
        line = line[p + 1 : len(line)]
        p = line.find('\t')
        longitude = line[0 : p]
        return longitude
    
    def getLatitudeFromStar(self, line):
        p = line.find('\t')
        line = line[p + 1 : len(line)]
        p = line.find('\t')
        line = line[p + 1 : len(line)]
        p = line.find('\t')
        line = line[p + 1 : len(line)]
        p = line.find('\t')
        latitude = line[0 : p]
        return latitude
    
    def getLongitudeFromStar(self, line):
        p = line.find('\t')
        line = line[p + 1 : len(line)]
        p = line.find('\t')
        line = line[p + 1 : len(line)]
        p = line.find('\t')
        longitude = line[0 : p]
        return longitude
    
    def getLongitudeFromAires(self, line):
        p = line.find('\t')
        line = line[p + 1 : len(line)]
        p = line.find('\t')
        line = line[p + 1 : len(line)]
        p = line.find('\t')
        longitude = line[0 : p]
        return longitude
    
    def getHourFromAries(self, myStr):
        p = myStr.find('\t')
        myStr = myStr[p + 1 : len(myStr)]
        p = myStr.find('\t')
        hour = myStr[0 : p]
        return hour
    
    def getTimeFromStar(self, line):
        p = line.find('\t')
        line = line[p + 1 : len(line)]
        p = line.find('\t')
        line = line[p + 1 : len(line)]
        p = line.find('\t')
        longitude = line[0 : p]
        return longitude
    
    def getDegree(self, myStr):
        p = myStr.find('d')
        degree = myStr[0 : p]
        return degree
    
    def getMinute(self, myStr):
        p = myStr.find('d')
        minute = myStr[p + 1 : len(myStr)]
        return minute
    
    def getLatitude(self):
        return self.latitude
    
    def getLongitude(self):
        return self.longitude
    
    def getMin(self, strTime):
        p = strTime.find(':')
        strTime = strTime[p + 1 : len(strTime)]
        p = strTime.find(':')
        minute = strTime[0 : p]
        if len(minute) > 1 and minute[0] == '0':
            minute = minute[1:len(minute)]
        return minute
    
    def getSecond(self, strTime):
        p = strTime.find(':')
        strTime = strTime[p + 1 : len(strTime)]
        p = strTime.find(':')
        strTime = strTime[p + 1 : len(strTime)]
        second = strTime
        if len(second) > 1 and second[0] == '0':
            second = second[1:len(second)]
        return second
    
    def calculationGeographicalPosition(self, starFileName, ariesFileName):
        f1 = open(starFileName, 'r')
        lines = f1.readlines()
        lineStar = lines[self.starReference]
        f1.close()
        
        f2 = open(ariesFileName, 'r')
        lines = f2.readlines()
        lineAries = lines[self.ariesReference]
        nextLineAries = lines[self.ariesReference + 1]
        f2.close()
        
        latitude = self.getLatitudeFromStar(lineStar)
        latitude_degree = self.getDegree(latitude)
        latitude_minute = self.getMinute(latitude)
        
        longitude = self.getLongitudeFromStar(lineStar)
        SHASTART_degree = self.getDegree(longitude)
        SHASTART_minute = self.getMinute(longitude)
        
        
        
        GHAAries1 = self.getLongitudeFromAires(lineAries)
        GHAAries1_degree = self.getDegree(GHAAries1)
        GHAAries1_minute = self.getMinute(GHAAries1)
        
        GHAAries2 = self.getLongitudeFromAries(nextLineAries)
        GHAAries2_degree = self.getDegree(GHAAries2)
        GHAAries2_minute = self.getMinute(GHAAries2)
        
        time = self.getTime()
        m = self.getMin(time)
        s = self.getSecond(time)
        m = eval(m)
        s = eval(s)
        s = m*60 + s
        
        Angle1 = Angle.Angle()
        Angle2 = Angle.Angle()
        
        Angle1.setDegreesAndMinutes(GHAAries1)
        Angle2.setDegreesAndMinutes(GHAAries2)
        
        GHAAries1 = Angle1.getDegrees()
        GHAAries2 = Angle2.getDegrees()
        
        GHAAries = abs(GHAAries1 - GHAAries2) * s / 3600
        
        Angle3 = Angle.Angle()
        Angle3.setDegrees(GHAAries)
        GHAAries = GHAAries1 + GHAAries
        
        Angle4 = Angle.Angle()
        Angle4.setDegreesAndMinutes(longitude)
        SHASTAR = Angle4.getDegrees()
        GHAObservation = GHAAries + SHASTAR
        Angle5 = Angle.Angle()
        Angle5.setDegrees(GHAObservation)
#
#         GHAAries1_degree = eval(GHAAries1_degree)
#         GHAAries2_degree = eval(GHAAries2_degree)
#         GHAAries1_minute = eval(GHAAries1_minute)
#         GHAAries2_minute = eval(GHAAries2_minute)
#         abs_degree = abs(GHAAries1_degree - GHAAries2_degree)
#         abs_minute = abs(GHAAries1_minute - GHAAries2_minute)
#         GHAAries_degree = abs_degree * s / 3600
#         GHAAries_minute = abs_minute * s / 3600
#         remender = GHAAries_degree - math.floor(GHAAries_degree)
#         GHAAries_minute += remender * 60
        
        # C
#         SHASTART_degree = eval(SHASTART_degree)
#         SHASTART_minute = eval(SHASTART_minute)
#         GHAObservation_degree = GHAAries_degree + SHASTART_degree
#         GHAObservation_minute = GHAAries_minute + SHASTART_minute
#         hi = GHAObservation_minute/60
#         GHAObservation_minute = GHAObservation_minute%60
#         GHAObservation_minute = round(GHAObservation_minute, 1)
#         GHAObservation_degree += hi
#         GHAObservation_degree = GHAObservation_degree%360
#     
#         
#         longitude = str(GHAObservation_degree) + 'd' + str(GHAObservation_minute)
        
        self.latitude = latitude
        self.longitude = Angle5.getString()
        
        a = 1
        
        
        
        