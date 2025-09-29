from _calendar.google_cal_connector import googleCalCon
from _database.sqliteConnector import plutus

class calendarHandler:
    
    classes=None
    
    calendar = None
    
    def __init__(self, weeks):
        self.calendar = googleCalCon(weeks=weeks)
    
    def getData(self):
        database = plutus()
        database.connect()
        
        batchID = database.getNewBatchID("classes") - 1
        
        self.classes = database.getClasses(batchID=batchID)
        
        database.closeConnection()
        
        return 0
    
    def sendData(self, colorscheme, showCancelled, showChanged):
        for entry in self.classes:
            color = None
            if entry["state"] == 'CANCELLED':
                if not showCancelled:
                    continue
                color = colorscheme['cancelled']
            elif entry["state"] == 'CHANGED':
                if not showChanged:
                    continue
                color = colorscheme['changed']
            elif entry["state"] == 'ADDITIONAL':
                color = colorscheme['changed']
            if entry['type'] == 'EXAM':
                color = colorscheme['exam']
            event = self.calendar.buildEvent(
                    name=entry["name"],
                    location=entry["room"],
                    description=entry["state"],
                    namePrefix=f"{entry["state"]} ",
                    background=color,
                    start=entry["startTime"],
                    end=entry["endTime"]
                    )
            
            self.calendar.createEntry(event=event)
    
    def deleteEvents(self):
        
        database = plutus()
        database.connect()
        
        prevBatchID = database.getNewBatchID("classes") - 2
        
        if prevBatchID < 0:
            return 0
        
        
        oldClasses = database.getClasses(batchID=prevBatchID)
        
        database.closeConnection()
        
        if len(self.classes) > len(oldClasses):
            self.calendar.removeEvents()
            return 1
            
        return 0