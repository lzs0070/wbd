import Navigation.prod.Fix as Fix
import Navigation.prod.Angle as Angle
import math

anFix = Fix.Fix()
anFix.setSightingFile("abc.xml")
anFix.getSightings()
# 
# anAngle = Angle.Angle()
# anAngle.setDegreesAndMinutes('0d0')
# print anAngle.getString()

anFix = Fix.Fix()
anFix.setSightingFile("abc.xml")
anFix.getSightings()
Angle1 = Angle.Angle()
Angle1.setDegreesAndMinutes('15d01.5')
Angle2 = Angle.Angle()
Angle2.setDegreesAndMinutes('45d11.9')
adjustedAltitudes = anFix.getAdjustedAltitudes()
Angle3 = Angle.Angle()
Angle3.setDegreesAndMinutes(adjustedAltitudes[0])
Angle4 = Angle.Angle()
Angle4.setDegreesAndMinutes(adjustedAltitudes[1])
print adjustedAltitudes[0]
print adjustedAltitudes[1]

print math.tan(15.08167*math.pi/180)
print math.tan(45*180/math.pi)

U = 1, 2
V = 3, 4
X = 1, 2
print cmp(U, V)
print cmp(U, X)
