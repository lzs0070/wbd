import math

class Angle():
    def __init__(self):
        #self.angle = ...       set to 0 degrees 0 minutes
        self.degrees = 0
    
    def printDegrees(self):
        #output degrees
        print("The degrees is" + self.degrees)
        
    def verifyDegrees(self, myStr):
        if myStr[0] == '-' or myStr[0] == '+':
            newStr = myStr[1:len(myStr)]
        else:
            newStr = myStr

        if not(newStr.isdigit()):   #remove the influence of sign when judging whether myStr is digit
            return False
        elif(type(eval(myStr)) == float):
            return False
        return True    
            
    def verifyMinutes(self, myStr):
        #remove the influence of sign when judging whether myStr is digit                 
        if myStr[0] == '-' or myStr[0] == '+':
            newStr = myStr[1:len(myStr)]
        else:
            newStr = myStr

        #if there is non-digit in newStr, except the first '.' at non-first position
        count = 0
        for i in range(0, len(newStr)):
            if newStr[i] == '.' and count == 0 and i != 0:
                count = count + 1
            elif(not(newStr[i].isdigit())):
                return 1

        '''
        if not(newStr.isdigit()):   
            print 'newstr=', newStr
            return 1    #should be digit
        else:
        '''

        myNum = eval(myStr)
        if myNum < 0:
            return 2    #should be positive
        elif(math.floor(myNum*10) < myNum*10):
            return 3    #one decimal place
        return 0
    
    
    def setDegrees(self, myDegrees = 0):
        if(not(isinstance(myDegrees, int) or isinstance(myDegrees, float))):
            #if myDegrees is not a number
            raise ValueError("Angle.setDegrees(): The input is not integer or float number!")
        else:
            self.degrees = myDegrees % 360
        return self.degrees
    
    def setDegreesAndMinutes(self, myDegrees):
        position = myDegrees.index('d');
        #look for 'd' in myDegrees
        if(position < 0):
            #if there is no 'd' in myDegrees
            raise ValueError('Angle.setDegreesAndMinutes(): The input is not invalid (missing separator).')
        elif(position == 0):
            #if the first character in myDegrees is 'd'
            raise ValueError('Angle.setDegreesAndMinutes(): The input is not invalid (missing degrees).')
        elif(position == len(myDegrees) - 1):
            #if the last character in myDegrees is 'd'
            raise ValueError('Angle.setDegreesAndMinutes(): The input is not invalid (missing minutes).')
        else:
            firstStr = myDegrees[0:position]
            secondStr = myDegrees[position+1:len(myDegrees)]
            
            #check Degrees
            if not(self.verifyDegrees(firstStr)):
                raise ValueError('Angle.setDegreesAndMinutes(): The input is not invalid (degrees should be an integer).')
            
            #check minutes
            if self.verifyMinutes(secondStr) == 1:
                print 'secondstr=', secondStr
                raise ValueError('Angle.setDegreesAndMinutes(): The input is not invalid (minutes should be digit).')
            elif self.verifyMinutes(secondStr) == 2:
                raise ValueError('Angle.setDegreesAndMinutes(): The input is not invalid (minutes should be positive).')
            elif self.verifyMinutes(secondStr) == 3:
                raise ValueError('Angle.setDegreesAndMinutes(): The input is not invalid (minutes must have one decimal place).')
            
            #if degrees and minutes are both valid
            self.degrees = int(firstStr)
            self.portion = float(secondStr)
            if self.degrees < 0:
                self.degrees = (self.degrees - self.portion/60) % 360
            else:
                self.degrees = (self.degrees + self.portion/60) % 360
            
            '''
            try:
                firstPart = int(firstStr)
                secondPart = float(secondStr)
            except Exception as e:
                print'Angle.setDegreesAndMinutes(): The input is not invalid (', e, ').'
            '''
        
        return self.degrees 
    
            
    def add(self, newAngle):
        if(not(isinstance(newAngle, Angle))):
            raise ValueError('Angle.add(): The input is not a valid instance of Angle.')
        
        self.degrees = (self.degrees + newAngle.degrees) % 360
        return self.degrees
    
    def subtract(self, newAngle):
        if(not(isinstance(newAngle, Angle))):
            raise ValueError('Angle.subtract(): The input is not a valid instance of Angle.')
        
        self.degrees = (self.degrees - newAngle.degrees) % 360
        return self.degrees
    
    def compare(self, newAngle):
        if(not(isinstance(newAngle, Angle))):
            raise ValueError('Angle.compare(): The input is not a valid instance of Angle.')
        
        if(self.degrees < newAngle.getDegrees()):
            return -1
        elif(self.degrees == newAngle.getDegrees()):
            return 0
        else:
            return 1
        
    
    def getString(self):
        wholeDegree = self.degrees
        degreePart = int(wholeDegree)
        minutePart = wholeDegree - degreePart
        minutePart = round(minutePart*60, 1)
        degreeStr = str(degreePart) + 'd' + str(minutePart)
        return degreeStr
    
    def getDegrees(self):
        return self.degrees