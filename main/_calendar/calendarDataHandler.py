from _calendar.google_cal_connector import googleCalCon
from _database.sqliteConnector import plutus
from datetime import datetime

class calendarHandler:
    
    classes=None

    old_classes = None
    
    calendar = None
    
    def __init__(self, weeks):
        self.calendar = googleCalCon(weeks=weeks)
    
    def getData(self):
        database = plutus()
        database.connect()
        
        batchID = database.getNewBatchID("classes") - 1

        old_batchID = database.getNewBatchID("classes") - 2
        
        self.classes = database.getClasses(batchID=batchID)

        self.classes = database.getClasses(batchID=old_batchID)
        
        database.closeConnection()
        
        return 0
    
    def sendData(self, colorscheme, showCancelled, showChanged):
        insertQueue = []
        deleteCal = False
        for entry in self.classes:
            color = None
            if entry["state"] == 'CANCELLED':
                if entry not in self.old_classes:
                    deleteCal = True
                if not showCancelled:
                    continue
                color = colorscheme['cancelled']
            elif entry["state"] == 'CHANGED':
                if entry not in self.old_classes:
                    deleteCal = True
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
                    description=f"Comment: {entry['substituteText']}",
                    namePrefix=f"{entry["state"]} ",
                    background=color,
                    start=entry["startTime"],
                    end=entry["endTime"]
                    )
            if (datetime.fromisoformat(event['start'].get('dateTime')) < datetime.now()):
                continue
            insert = self.calendar.checkInsertEvent(event=event)
            if (insert):
                deleteCal = True
            insertQueue.append(event)

        if not deleteCal:
            return 0

        self.calendar.removeEvents()

        for event in insertQueue:
            self.calendar.sendEvent(event)

    
    def deleteEvents(self):
        
        database = plutus()
        database.connect()
        
        prevBatchID = database.getNewBatchID("classes") - 2
        currBatchID = database.getNewBatchID("classes") - 1
        
        if prevBatchID < 0:
            return 0
        
        
        oldClasses = database.getClasses(batchID=prevBatchID)
        
        currClasses = database.getClasses(batchID=currBatchID)
        
        database.closeConnection()
        
        if len(currClasses) > len(oldClasses):
            self.calendar.removeEvents()
            return 1
            
        return 0
