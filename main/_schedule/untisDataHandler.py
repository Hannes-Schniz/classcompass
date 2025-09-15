from _schedule.untis_connector import exporter
from _database.sqliteConnector import plutus

class apiHandler:

    diffs=None
    classes=None
    

    def getData(self,start, end,classID):
        untis_exporter = exporter()

        untisData = untis_exporter.getData(start=start, end=end, classID=classID, verbose=True)
        self.diffs += untisData[1]
        self.classes += untisData[0]
        
    def sendData(self):
        database = plutus()
        database.connect()
        
        try:
            batchID = database.getNewBatchID("classes")
            # Process and insert classes data
            if self.classes is not None:
                for item in self.classes:
                    database.addClass(
                        batchID=batchID,
                        date=item['date'],
                        startTime=item['startTime'],
                        endTime=item['endTime'],
                        type=item['type'],
                        state=item['state'],
                        stateDetail=item['stateDetail'],
                        room=item['room'],
                        subject=item['subject'],
                        substituteText=item['substituteText']
                    )
                print(f"Successfully inserted {len(self.classes)} classes with batchID {batchID}")
            
            # Process and insert diffs data
            if self.diffs is not None:
                for item in self.diffs:
                    database.addDiff(
                        batchID=batchID,
                        oldDate=item['oldDate'],
                        newDate=item['newDate'],
                        oldStart=item['oldStart'],
                        newStart=item['newStart'],
                        oldEnd=item['oldEnd'],
                        newEnd=item['newEnd'],
                        oldState=item['oldState'],
                        newState=item['newState'],
                        oldStateDetail=item['oldStateDetail'],
                        newStateDetail=item['newStateDetail'],
                        oldRoom=item['oldRoom'],
                        newRoom=item['newRoom'],
                        oldSubject=item['oldSubject'],
                        newSubject=item['newSubject'],
                        oldText=item['oldText'],
                        newText=item['newText']
                    )
                print(f"Successfully inserted {len(self.diffs)} diffs with batchID {batchID}")
        
        except Exception as e:
            print(f"Error inserting data: {e}")
            raise e
        finally:
            # Always close the database connection
            database.closeConnection()
        