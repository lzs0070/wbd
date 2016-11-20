# import Navigation.prod.Fix as Fix
import Navigation.prod.Angle as Angle
import uuid
import math
import os
import sys
import re
import time
import datetime
import numpy as np
# from scipy import stats
# import matplotlib.pyplot as plt

# 
# anAngle = Angle.Angle()
# anAngle.setDegreesAndMinutes('0d0')
# print anAngle.getString()




# # DEFAULT_LOG_FILE = 'log.txt'
# # theLogFile = open(DEFAULT_LOG_FILE, 'r')
# # entry = theLogFile.readline()
# # print entry
# # print entry.find("Start of log")
# # del theLogFile
# logStartString = "Start of log"
# logSightingString = "Start of sighting file"
# # RANDOM_LOG_FILE = "log" + str(uuid.uuid4())[-12:] + ".txt"
# RANDOM_LOG_FILE = "log" + "d59f818abe7e" + ".txt"
# # theFix = Fix.Fix(logFile=RANDOM_LOG_FILE)
# print RANDOM_LOG_FILE
# 
# theFix = Fix.Fix(RANDOM_LOG_FILE)
# theLogFile = open(RANDOM_LOG_FILE, 'r')
# entry = theLogFile.readline()
# del theLogFile
# print RANDOM_LOG_FILE
# print entry
# print entry.find(logStartString)
# 
# testFile = "CA02_300_ValidOneStarArtificialHorizon.xml"
# targetStringList = ["Hadar", "2016-03-01", "23:40:01", "29d55.7"]
# theFix = Fix.Fix(RANDOM_LOG_FILE)
# theFix.setSightingFile(testFile)
# theFix.getSightings()

# DEFAULT_LOG_FILE = 'log.txt'
# ABSPATH=os.path.abspath(sys.argv[0])
# ABSPATH1=os.path.dirname(ABSPATH)
# print ABSPATH
# print ABSPATH1
# 
# 
# theFix = Fix.Fix()
# theLogFile = open(DEFAULT_LOG_FILE, 'r')
# entry = theLogFile.readline()
# print entry
# print entry.find('yida')

f = open("stars.txt", 'r')
line = f.readline()
print line
p = line.find('\t')
print p
print line[0:p]

body = line[0 : p]
print body + " ", len(body)
line = line[p + 1 : len(line)]
p = line.find('\t')
date = line[0 : p]
print date + " ", len(date)
line = line[p + 1 : len(line)]
p = line.find('\t')
longitude = line[0 : p]
print longitude + " ", len(longitude)
line = line[p + 1 : len(line)]
p = line.find('\t')
latitude = line[0 : p]
print latitude + " ", len(latitude)
f.close()

rs_date = r'(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)'
rs_date = r'^(?:(?:(?:0?[1-9]|1[0-9]|2[0-8])([-/.]?)(?:0?[1-9]|1[0-2])|(?:29|30)([-/.]?)(?:0?[13-9]|1[0-2])|31([-/.]?)(?:0?[13578]|1[02]))([-/.]?)(?!0000)[0-9]{4}|29([-/.]?)0?2([-/.]?)(?:[0-9]{2}(?:0[48]|[2468][048]|[13579][26])|(?:0[48]|[2468][048]|[13579][26])00))$'
rs_date = r'(((0[1-9]|[12][0-9]|3[01])/((0[13578]|1[02]))|((0[1-9]|[12][0-9]|30)/(0[469]|11))|(0[1-9]|[1][0-9]|2[0-8])/(02))/([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3}))|(29/02/(([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00)))'
pattern = re.compile(rs_date)
match = pattern.search('04-01-16')
print match
match = pattern.search('2004-01-16')
print match

strDate = '2/8/21'
try:
    time.strptime(strDate, '%m/%d/%y')
    print 'date true'
except:
    print 'date False'

myStr = '-.0100000'
v = eval(myStr)
print v
print type(v) == float
print type(v) == int

# strDate = '01-10-10'
# time.strftime(strDate, '%m-%d-%y')
# print strDate

d1 = datetime.datetime(05, 2, 16)
d2 = datetime.datetime(04, 12, 31)
print (d2 - d1).days

print int('09')