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
    
    def sendData(self, colorscheme):
        for entry in self.classes:
            color = None
            if entry["state"] == 'CANCELLED':
                color = colorscheme['cancelled']
            elif entry["state"] == 'CHANGED':
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
        
        batchID = database.getNewBatchID("classes") - 1
        
        oldClasses = database.getClasses(batchID=batchID)
        
        database.closeConnection()
        
        if len(self.classes) > len(oldClasses):
            self.calendar.removeEvents()
            return 1
            
        return 0