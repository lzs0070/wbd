import os
import sys
from __builtin__ import str

class LogFile(object):

    def __init__(self, logFileName):
        self.filename = logFileName
        ABSPATH = os.path.abspath(self.filename)
        self.filepath = ABSPATH
    
    def log(self, logString):
        try:
            f = open(self.filename, 'a')
            f.write(logString)
            f.close()
        except:
            return False
        
        return True

    def getFileName(self):
        return self.filename
    
    def getFilePath(self):
        return self.filepath