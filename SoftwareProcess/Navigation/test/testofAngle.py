'''
Created on 09/04/2016

@author: Li Sun
'''

import Navigation.prod.Angle as Angle

#test of construction of Angle
try:
    myAngle = Angle.Angle()
    print(myAngle.degrees)
except ValueError as e:
    print(e)
        
#test of setDegrees
try:
    print(myAngle.setDegrees('abc'))
except ValueError as e:
    print(e)

#test of setDegreesAndMunites
try:
    print(myAngle.setDegreesAndMinutes('0100d01.'))
except ValueError as e:
    print(e)
    

#test of add
try:
    newAngle = Angle.Angle()
    print(newAngle.setDegrees(245))
    #print('myAngle=', myAngle.degrees, 'newAngle=', newAngle.degrees)
    myAngle.add(newAngle)
    print(myAngle.degrees)
except ValueError as e:
    print(e)    
    
#test of subtract
try:
    myAngle.subtract(newAngle)
    print(myAngle.degrees)
except ValueError as e:
    print(e)  

#test of compare
try:
    print(myAngle.compare(22))
except ValueError as e:
    print(e)

#test of getString
print(myAngle.getString())
    


#instantiate angles
angle1 = Angle.Angle()
angle2 = Angle.Angle()
angle3 = Angle.Angle()
angle4 = Angle.Angle()


#set
print 'set:-------------------------'
angle1Degrees = angle1.setDegreesAndMinutes("45d0.0")
print 'angle1Degrees =', angle1Degrees
angle2Degrees = angle2.setDegrees(myDegrees = -19.5)
print 'angle2Degrees =', angle2Degrees
angle3Degrees = angle3.setDegreesAndMinutes("0d30.0")
print 'angle3Degrees =', angle3Degrees

#Attempts to set an invalid value should result
try:
    invalidAngle = angle2.setDegrees("")
except ValueError as rasedException:
    print(rasedException)

#add
print 'add:-------------------------'
addedDegrees1 = angle1.add(angle2)
print 'addedDegrees1 =', addedDegrees1
addedDegrees3 = angle2.add(angle3)
print 'addedDegrees3 =', addedDegrees3

#Attempts to pass a parm that is not an instance of Angle
try:
    angle1.add("42d0")
except ValueError as raisedException:
    print(raisedException)



#subtract
print 'subtract:-------------------------'
subtractedDegrees = angle4.subtract(angle1)
print 'subtractedDegrees =', subtractedDegrees

#Attempt to pass a parm that is not an instance of Angle
try:
    angle1.subtract(0)
except ValueError as raisedException:
    print(raisedException)
    

#compare
print 'compare:-------------------------'
angle1.setDegrees(45.0)
angle2.setDegrees(45.1)
result = angle1.compare(angle2)
print 'result =', result

#Attempts to pass a parm that is not an instance of Angle
try:
    angle1.compare(42.0)
except ValueError as raisedException:
    print(raisedException)


#getString
print 'getString:-------------------------'
angle1String = angle1.getString()
print 'angle1String =', angle1String
angle2String = angle2.getString()
print 'angle2String =', angle2String
angle3.setDegrees(45.123)
angle3String = angle3.getString()
print 'angle3String =', angle3String


#getDegrees
print 'getDegrees:-------------------------'
angle1Degrees = angle1.getDegrees()
print 'angle1Degrees =', angle1Degrees
angle2Degrees = angle2.getDegrees()
print 'angle2Degrees =', angle2Degrees
angle3Degrees = angle3.getDegrees()   
print 'angle3Degrees =', angle3Degrees 




