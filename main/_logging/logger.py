import os
from datetime import datetime


def __init__(self, logpath):
    self.logpath = logpath
    self.loglevels = ["INF", "ERR", "WRN"]
    self.baseLogName = "classCompassDiag"
    self.openFile()

def logMessage(self, state, text):
    if state not in self.loglevels:
        self.logfile.write("[ERR] Logstate not found") 
        self.closeFile()
        raise StateNotFound("Logstate not found")

    self.logfile.write(f"[{state}] {text}") 
    
def openFile(self):
    date = datetime.today().strftime('%Y-%m-%d')
    logfile = f"{date}_{self.baseLogName}"
    self.logfile = open(f"{self.logpath}/{logfile}")

def closeFile(self):
    self.logfile.close()
