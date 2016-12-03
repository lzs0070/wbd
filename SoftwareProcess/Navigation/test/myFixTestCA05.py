import unittest
import Navigation.prod.Fix as Fix
import os
import uuid


class Test(unittest.TestCase):


    def setUp(self):
        self.className = "Fix."
        self.logStartString = "Start of log"
        self.logSightingString = "Start of sighting file"
        
        # set default log file name
        self.DEFAULT_LOG_FILE = "log.txt"
#         if(os.path.isfile(self.DEFAULT_LOG_FILE)):
#             os.remove(self.DEFAULT_LOG_FILE)
            
        # generate random log file name
        self.RANDOM_LOG_FILE = "log" + str(uuid.uuid4())[-12:] + ".txt"
        
        # get default log filepath
        ABSPATH = os.path.abspath(self.DEFAULT_LOG_FILE)
#         ABSPATH = os.path.dirname(ABSPATH)
        self.DEFAULT_LOG_FILEPATH = ABSPATH
        
        # get random log filepath
        ABSPATH = os.path.abspath(self.RANDOM_LOG_FILE)
        self.RANDOM_LOG_FILEPATH = ABSPATH
        
        # generate random aries file name
        self.RANDOM_ARIES_FILE = "aries" + str(uuid.uuid4())[-12:] + ".txt"
        # get random log filepath
        ABSPATH = os.path.abspath(self.RANDOM_LOG_FILE)
        self.RANDOM_ARIES_FILEPATH = ABSPATH
        
        # generate default aries file name
        self.DEFAULT_ARIES_FILE = "aries.txt"
        # get default aries filepath
        ABSPATH = os.path.abspath(self.DEFAULT_ARIES_FILE)
        self.DEFAULT_ARIES_FILEPATH = ABSPATH
        
        # generate random sighting file name
        self.RANDOM_SIGHT_FILE = "sighting" + str(uuid.uuid4())[-12:] + ".xml"
        # get random sighting filepath
        ABSPATH = os.path.abspath(self.RANDOM_SIGHT_FILE)
        self.RANDOM_SIGHT_FILEPATH = ABSPATH
        
        # generate default sighting file name
        self.DEFAULT_SIGHT_FILE = "CA02_200_ValidStarSightingFile.xml"
        # get default sighting filepath
        ABSPATH = os.path.abspath(self.DEFAULT_SIGHT_FILE)
        self.DEFAULT_SIGHT_FILEPATH = ABSPATH
        
        # generate random star file name
        self.RANDOM_STAR_FILE = "stars" + str(uuid.uuid4())[-12:] + ".txt"
        # get random star filepath
        ABSPATH = os.path.abspath(self.RANDOM_STAR_FILE)
        self.RANDOM_STAR_FILEPATH = ABSPATH
        
        # generate default star file name
        self.DEFAULT_STAR_FILE = "stars.txt"
        # get default sighting filepath
        ABSPATH = os.path.abspath(self.DEFAULT_STAR_FILE)
        self.DEFAULT_STAR_FILEPATH = ABSPATH


# Acceptance Test: 300
#     Analysis - getSightings
#         inputs
#             assumedAltitude, assumedLongitude
#         outputs
#             a tuple consisting of the latitude and longitude of the approximate location
#         state change
#             navigation calculations are written to the log file
#      
#         Sad path
#             assumedLatitude missing "N" or "S" but with non-zero angle ("1d1.0")
#             assumedLatitude with "N" or "S" but with zero angle ("N0d0.0")
#             assumedLatitude without angle ("N")
#             assumedLatitude missing degree ("Nd30.0")
#             assumedLatitude missing minute ("N30d")
#             assumedLatitude with float degree ("N3.1d30.0")
#             assumedLatitude with integer minute ("S31d30")
#             assumedLatitude with float minute with more than one digit to the right of the decimal point ("S31d30.01")
#             assumedLatitude with negative degree ("N-0.1d30.0")
#             assumedLatitude with degree >= 90 ("N90d30.0")
#             assumedLatitude with negative minute("N30d-0.0")
#             assumedLatitude with minute >= 60 ("S90d60.0")
#             assumedLongitude with degree >= 360 ("360d30.0")
#
#         Happy path
#             assumedLatitude without parameters ("")
#             assumedLongitude without parameters ("")

#   Sad path----------------------------------------------------------------------

    def test300_900_ShouldRaiseExceptionOnAltitudeMissingHButWithNonZeroAngle(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude="1d1.0")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
   
    def test300_901_ShouldRaiseExceptionOnAltitudeWithHandZeroAngle(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude="N0d0.0")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
        
    def test300_902_ShouldRaiseExceptionOnAltitudeWithoutAngle(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude="N")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    
    def test300_903_ShouldRaiseExceptionOnDigitalParameters(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude=123)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    
    def test300_904_ShouldRaiseExceptionOnMissingD(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude='s1024')
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        

    def test300_905_ShouldRaiseExceptionOnEmptyString(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude="")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
        
    def test300_910_ShouldRaiseExceptionOnAltitudeMissingDegree(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude="Nd30.0")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
        
    def test300_911_ShouldRaiseExceptionOnAltitudeMissingMinute(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude="N30d")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
        
    def test300_920_ShouldRaiseExceptionOnAltitudeFloatDegree(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude="N3.1d30.0")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    
    def test300_921_ShouldRaiseExceptionOnAltitudeFloatDegree(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude="N3.0d30.0")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    
    def test300_922_ShouldRaiseExceptionOnAltitudeIntegerMinute(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude="N31d30")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        

    def test300_923_ShouldRaiseExceptionOnAltitudeTwoDigitals(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude="N31d30.00")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
    
    
    def test300_930_ShouldRaiseExceptionOnAltitudeNegativeDegree(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude="N-31d30.00")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
        
    def test300_931_ShouldRaiseExceptionOnAltitudeOutboundDegree(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude="N90d30.00")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    
    def test300_932_ShouldRaiseExceptionOnAltitudeNegativeMinute(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude="N89d-0.00")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    
    def test300_933_ShouldRaiseExceptionOnAltitudeOutboundMinute(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLatitude="S09d60.0")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
    
    
    def test300_934_ShouldRaiseExceptionOnLongitudeOutboundMinute(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLongitude="360d30.0")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
        
    def test300_935_ShouldRaiseExceptionOnEmptyString(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings(assumedLongitude="")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        

#   Happy path----------------------------------------------------------------------

    def test300_000_ShouldCreateInstanceWithoutParameters(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings2.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
#         anFix.getSightings('N27d59.5', '85d33.4')
        anFix.getSightings()
#         anFix.getSightings()

    def test300_010_ShouldCreateInstanceWithParameters(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings2.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
#         anFix.getSightings('N27d59.5', '85d33.4')
        anFix.getSightings('S53d38.4', '74d35.3')
#         anFix.getSightings()

    def test300_020_ShouldCreateInstanceWithPartialParameters(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("sightings2.xml")
        anFix.setAriesFile("aries.txt")
        anFix.setStarFile("stars.txt")
#         anFix.getSightings('N27d59.5', '85d33.4')
        anFix.getSightings('S53d38.4')
#         anFix.getSightings()




    def tearDown(self):
        pass


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
