import unittest
import Navigation.prod.Fix as Fix
import os
import uuid
import sys

class MyFixTest2(unittest.TestCase):

    def setUp(self):
        self.className = "Fix."
        self.logStartString = "Start of log"
        self.logSightingString = "Start of sighting file"
        
        # set default log file name
        self.DEFAULT_LOG_FILE = "log.txt"
        if(os.path.isfile(self.DEFAULT_LOG_FILE)):
            os.remove(self.DEFAULT_LOG_FILE)
            
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

    def tearDown(self):
        pass

# Acceptance Test: 100
#     Analysis - Constructor
#         inputs
#             none / a string having a length .GE. 1. default: "log.txt"
#         outputs
#             instance of Fix
#         state change
#             writes absolute path to the log file
#      
#         Happy path
#             nominal case: Fix()
#             nominal case: Fix("abc.txt")
#         Sad path
#             input type: digital
#             input length: 0
#             input case: unavalible name
#
# Sad path
    def test100_910_ShouldRaiseExceptionOnNonString(self):
        expectedDiag = self.className + "__init__:"
        with self.assertRaises(ValueError) as context:
            Fix.Fix(123)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test100_920_ShouldRaiseExceptionOnEmptyString(self):
        expectedDiag = self.className + "__init__:"
        with self.assertRaises(ValueError) as context:
            Fix.Fix("")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test100_930_ShouldRaiseExceptionOnFileFail(self):
        expectedDiag = self.className + "__init__:"
        with self.assertRaises(ValueError) as context:
            Fix.Fix("Z:\\abc")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

# Happy path
    def test100_010_ShouldCreateInstanceOfFixWithoutInput(self):
        theFix = Fix.Fix()
        try:
            theLogFile = open(self.DEFAULT_LOG_FILE, 'r')
            entry = theLogFile.readline()
            del theLogFile
            self.assertNotEquals(-1, entry.find(self.DEFAULT_LOG_FILEPATH), 
                                 "Minor:  first line of log is incorrect")
        except IOError:
            self.fail()
        self.assertIsInstance(theFix, Fix.Fix, "major:  log file failed to create")
        self.cleanup()  
    
    def test100_020_ShouldCreateInstanceOfFixWithInput(self):
#         self.assertIsInstance(Fix.Fix("abc.txt"), Fix.Fix)
        theFix = Fix.Fix(self.RANDOM_LOG_FILE)
        try:
            theLogFile = open(self.RANDOM_LOG_FILE, 'r')
            entry = theLogFile.readline()
            del theLogFile
            a = entry.find(self.RANDOM_LOG_FILEPATH)
            
            self.assertNotEquals(-1, entry.find(self.RANDOM_LOG_FILEPATH), 
                                 "Minor:  first line of log is incorrect")
        except IOError:
            self.fail()
        self.assertIsInstance(theFix, Fix.Fix, "major:  log file failed to create")
        self.cleanup()


# Acceptance Test: 200
#     Analysis - setSightingFile
#         inputs
#             none / a string having a length .GE. 1. default: "log.txt"
#         outputs
#             instance of Fix
#         state change
#             writes "absolute path" to the log file
#      
#         Happy path
#             nominal case: Fix()
#             nominal case: Fix("abc.txt")
#         Sad path
#             input type: digital
#             input length: 0
#             input case: unavalible name
#
# Sad path

#    Sad path
    def test200_910_ShouldRaiseExceptionOnEmptyInput(self):
        expectedDiag = self.className + "setSightingFile:"
        anFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            anFix.setSightingFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test200_920_ShouldRaiseExceptionOnEmptyString(self):
        expectedDiag = self.className + "setSightingFile:"
        anFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            anFix.setSightingFile("")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test200_930_ShouldRaiseExceptionOnInvalidFileName(self):
        expectedDiag = self.className + "setSightingFile:"
        anFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            anFix.setSightingFile(".xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test200_940_ShouldRaiseExceptionOnInvalidFileName(self):
        expectedDiag = self.className + "setSightingFile:"
        anFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            anFix.setSightingFile("abc")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test200_950_ShouldRaiseExceptionOnInvalidFileName(self):
        expectedDiag = self.className + "setSightingFile:"
        anFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            anFix.setSightingFile("abc.txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test200_960_ShouldRaiseExceptionOnUnvaliableFile(self):
        expectedDiag = self.className + "setSightingFile:"
        anFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            anFix.setSightingFile("Z:\\.xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test200_970_ShouldRaiseExceptionOnUnexistedFile(self):
        expectedDiag = self.className + "setSightingFile:"
        anFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            anFix.setSightingFile("sun.xml")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])


# Happy path
    def test200_010_ShouldReturnInputValue(self):     
        'Minor:  '
        theFix = Fix.Fix(logFile = self.RANDOM_LOG_FILE)
        try:
            result = theFix.setSightingFile("CA02_200_ValidStarSightingFile.xml")
            self.assertEquals(result, self.DEFAULT_SIGHT_FILEPATH)
        except:
            self.fail("Minor: incorrect keyword specified in setSighting parm")
        self.cleanup()
        


# 300 setAriesFile
#    Analysis
#        inputs:
#            ariesFile: string, mandatory, unvalidated, format = f.txt (len(f) >= 1)
#        outputs:
#            returns:  absolute filepath
#            also:    writes "Aries file:\t" + filepath to log file
#
#    Happy tests:
#        ariesFile:  
#            legal file name  -> setAriesFile("ariesFile.txt")  
#    Sad tests:
#        ariesFile:
#            missing -> setAriesFile()
#            nonstring -> setAriesFile(42)
#            length error -> setAriesFile(".txt")
#            nonTXT -> setAriesFile("ariesFile.xml")
#            nonexistent file -> setAriesFile("missing.txt")

    def test300_010_ShouldConstructWithKeywordParm(self):
        'Minor:  '
        theFix = Fix.Fix(logFile = self.RANDOM_LOG_FILE)
        try:
            result = theFix.setAriesFile("aries.txt")
            self.assertEquals(result, self.DEFAULT_ARIES_FILEPATH)
        except:
            self.fail("Minor: incorrect keyword specified in setSighting parm")
        self.cleanup()   
    
    def test300_020_ShouldSetValidAriesFile(self):
        theFix = Fix.Fix()
        result = theFix.setAriesFile("aries.txt")
        self.assertNotEquals(-1, result.find(self.DEFAULT_ARIES_FILEPATH), 
                             "Minor:  first setAries logged entry is incorrect")
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        self.assertNotEquals(-1, logFileContents[-1].find(self.DEFAULT_ARIES_FILEPATH), 
                             "Minor:  first setAries logged entry is incorrect")
        theLogFile.close()
        
    def test300_910_SholdRaiseExceptionOnMissingFileName(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to check for missing aries file")  

    def test300_920_ShouldRaiseExceptionOnFileLengthError(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile(".txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for .GE. 1 aries file name") 

    def test300_930_ShouldRaiseExceptionOnNonStringFileName(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile(42)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non-string aries file name")  
        
    def test300_940_ShouldRaiseExceptionOnNonTxtFile1(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile("aries.")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non.xml aries file extension")
         
    def test300_950_ShouldRaiseExceptionOnNonTxtFile2(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile("txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to delineate between aries file name and extension") 
  
    def test300_960_SholdRaiseExceptionOnMissingFile(self):
        expectedDiag = self.className + "setAriesFile:"
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setAriesFile(self.RANDOM_LOG_FILE+".txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to check for missing aries file") 



# 400 setStarFile
#    Analysis
#        inputs:
#            starFile: string, mandatory, unvalidated, format = f.txt (len(f) >= 1)
#        outputs:
#            returns:  absolute filepath
#            also:    writes "Star file:\t" + filepath to log file
#
#    Happy tests:
#        starFile:  
#            legal file name  -> setStarFile("starFile.txt")  
#    Sad tests:
#        starFile:
#            missing -> setStarFile()
#            nonstring -> setStarFile(42)
#            length error -> setStarFile(".txt")
#            nonTXT -> setStarFile("starFile.xml")
#            nonexistent file -> setStarFile("missing.txt")

    def test400_010_ShouldConstructWithKeywordParm(self):
        'Minor:  '
        theFix = Fix.Fix(logFile = self.RANDOM_LOG_FILE)
        try:
            result = theFix.setStarFile("stars.txt")
            self.assertEquals(result, self.DEFAULT_STAR_FILEPATH)
        except:
            self.fail("Minor: incorrect keyword specified in setStar parm")
        self.cleanup()   
    
    def test400_020_ShouldSetValidStarFile(self):
        theFix = Fix.Fix()
        result = theFix.setStarFile("stars.txt")
        self.assertNotEquals(-1, result.find(self.DEFAULT_STAR_FILEPATH), 
                             "Minor:  first setStar logged entry is incorrect")
        theLogFile = open(self.DEFAULT_LOG_FILE, "r")
        logFileContents = theLogFile.readlines()
        self.assertNotEquals(-1, logFileContents[-1].find(self.DEFAULT_STAR_FILEPATH), 
                             "Minor:  first setStar logged entry is incorrect")
        theLogFile.close()
         
    def test400_910_SholdRaiseExceptionOnMissingFileName(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to check for missing star file")  
 
    def test400_920_ShouldRaiseExceptionOnFileLengthError(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile(".txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for .GE. 1 star file name") 
 
    def test400_930_ShouldRaiseExceptionOnNonStringFileName(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile(42)
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non-string star file name")  
         
    def test400_940_ShouldRaiseExceptionOnNonTxtFile1(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile("star.")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to check for non.xml star file extension")
          
    def test400_950_ShouldRaiseExceptionOnNonTxtFile2(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile("txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Minor:  failure to delineate between star file name and extension") 
   
    def test400_960_SholdRaiseExceptionOnMissingFile(self):
        expectedDiag = self.className + "setStarFile:"
        theFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            theFix.setStarFile(self.RANDOM_STAR_FILE+".txt")
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to check for missing star file") 

#     def test500_010_ShouldConstructWithTolerantofWrongSightings(self):
        

# 500 getStarFile
#    Analysis
#        outputs:
#            returns:  a tuple consisting of the latitude and longitude of the approximate location
#    Happy tests:
#         sightingFile: 
#             create an instance even there are errors in sightingFile
#    Sad tests:
#        starFile:
#            without aries file
#            without star file

    def test500_010_ShouldConstructWithValidFile(self):
        theFix = Fix.Fix()
        theFix.setSightingFile("sightings.xml")
        theFix.setStarFile("stars.txt")
        theFix.setAriesFile("aries.txt")
        theFix.getSightings()
        

    def test500_910_ShouldRaiseExceptionOnMissingAriesFile(self):
        expectedDiag = self.className + "getSightings:"
        theFix = Fix.Fix()
        theFix.setSightingFile("abc.xml")
        theFix.setStarFile("stars.txt")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to set sighting file before getSightings()")   
    
    def test500_920_ShouldRaiseExceptionOnMissingAriesFile(self):
        expectedDiag = self.className + "getSightings:"
        theFix = Fix.Fix()
        theFix.setSightingFile("abc.xml")
        theFix.setAriesFile("aries.txt")
        with self.assertRaises(ValueError) as context:
            theFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)],
                          "Major:  failure to set sighting file before getSightings()") 


    def cleanup(self):
        try:
            if(os.path.isfile(self.RANDOM_LOG_FILE)):
                os.remove(self.RANDOM_LOG_FILE) 
        except:
            pass 