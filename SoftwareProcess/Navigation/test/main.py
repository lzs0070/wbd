import Navigation.prod.Fix as Fix
import Navigation.prod.Angle as Angle

# anFix = Fix.Fix()
# anFix.setSightingFile("abc(tiny altitude).xml")
# anFix.getSightings()
# 
# anAngle = Angle.Angle()
# anAngle.setDegreesAndMinutes('0d0')
# print anAngle.getString()

anFix = Fix.Fix()
anFix.setSightingFile("abc.xml")
Angle1 = Angle.Angle()
Angle1.setDegreesAndMinutes('15d01.5')
Angle2 = Angle.Angle()
Angle2.setDegreesAndMinutes('45d11.9')
adjustedAltitudes = anFix.getAdjustedAltitudes()