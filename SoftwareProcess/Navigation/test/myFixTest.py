'''
Created on 10/08/2016

@author: sunsuper
'''
import unittest
import Navigation.prod.Fix as Fix
import xml
from _elementtree import XML
from __builtin__ import file

class FixTest(unittest.TestCase):

    def setUp(self):
        self.className = "Fix."

    def tearDown(self):
        pass

# Acceptance Test: 100
#     Analysis - Constructor
#         inputs
#             none / a string having a length .GE. 1. default: "log.txt"
#         outputs
#             instance of Fix
#         state change
#             writes "Start of log" to the log file
#      
#         Happy path
#             nominal case: Fix()
#         Sad path
#             length of string inputed is 0
#
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
        self.assertIsInstance(Fix.Fix(), Fix.Fix)
        
    def test100_020_ShouldCreateInstanceOfFixWithInput(self):
        self.assertIsInstance(Fix.Fix("abc.txt"), Fix.Fix)
        
        

# Acceptance Test: 200
#     Analysis - setSightingFile
#         inputs
#             a string name "f.xml" of a file contains XML descriptions of navigational sightings
#                 length of f is .GE. 1
#                 have file extension of ".xml"
#         outputs
#             A string having the value passed as the "sightingFile".
#         state change
#             writes "Start of sighting file f.xml" to the log file
#      
#         Sad path
#             empty input
#             invalid string: empty name, missing ".xml"
#             the file can not be opened (for whatever reason)
#         Happy path
#             nominal case: writes "Start of singting file f.xml" to the log file

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
        anFix = Fix.Fix()
        self.assertEquals("abc.xml", anFix.setSightingFile("abc.xml"))
    


# Acceptance Test: 300
#     Analysis - getSightings
#         inputs
#             none
#         outputs
#             a tuple consisting of the latitude and longitude of the approximate location
#         state change
#             navigation calculations are written to the log file
#      
#         Sad path
#             no sighting file has been set
#             errors are encountered in the sighting file
#             the observed altitude is .LT. 0.1 arc-minutes
#         Happy path
#             nominal case: 

#    Sad path

    def test300_010_ShouldRaiseExceptionOnNoSettingSightingfile(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        with self.assertRaises(ValueError) as context:
            anFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
        
    def test300_020_ShouldRaiseExceptionOnMissingDateTag(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("abc(no date).xml")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])
 
    def test300_030_ShouldRaiseExceptionOnMissingBodyTag(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("abc(no body).xml")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test300_040_ShouldRaiseExceptionOnMissingTimeTag(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("abc(no time).xml")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test300_050_ShouldRaiseExceptionOnMissingObservationTag(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("abc(no observation).xml")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test300_060_ShouldRaiseExceptionOnInvalidDate(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("abc(invalid date).xml")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])

    def test300_070_ShouldRaiseExceptionOnInvalidTime(self):
        expectedDiag = self.className + "getSightings:"
        anFix = Fix.Fix()
        anFix.setSightingFile("abc(invalid time).xml")
        with self.assertRaises(ValueError) as context:
            anFix.getSightings()
        self.assertEquals(expectedDiag, context.exception.args[0][0:len(expectedDiag)])








   

