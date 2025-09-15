from google_cal_connector import googleCalCon
from database.sqliteConnector import plutus

class calendarHandler:
    
    classes=None
    diffs=None
    
    def getData(self):
        database = plutus()
        database.connect()
        
        batchID = database.getNewBatchID() - 1
        
        self.classes = database.getClasses(batchID=batchID)
        
        print(self.classes)
        return 0