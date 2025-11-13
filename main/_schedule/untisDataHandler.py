from _schedule.untis_connector import exporter
from _database.sqliteConnector import plutus
from constants import api, logLevel, dbParams

class apiHandler:

    diffs=[]
    classes=[]
    

    def getData(self,start, end,classID):
        untis_exporter = exporter()

        untisData = untis_exporter.getData(start=start, end=end, classID=classID, verbose=True)
        self.diffs += untisData[1]
        self.classes += untisData[0]
        
    def sendData(self):
        database = plutus()
        database.connect()
        
        try:
            batchID = database.getNewBatchID(dbParams.CLASSESTABLE.value)
            # Process and insert classes data
            if self.classes is not []:
                for item in self.classes:
                    database.addClass(
                        batchID=batchID,
                        date=item[api.DATE.value],
                        startTime=item[api.STARTTIME.value],
                        endTime=item[api.ENDTIME.value],
                        type=item[api.TYPE.value],
                        state=item[api.STATE.value],
                        stateDetail=item[api.STATEDETAIL.value],
                        room=item[api.ROOM.value],
                        subject=item[api.SUBJECT.value],
                        substituteText=item[api.SUBSTITUTETEXT.value]
                    )
                print(f"[{logLevel.INFO.value}] Successfully inserted {len(self.classes)} classes with batchID {batchID}")
            
            # Process and insert diffs data
            if self.diffs is not []:
                for item in self.diffs:
                    database.addDiff(
                        batchID=batchID,
                        oldDate=item[api.OLDDATE.value],
                        newDate=item[api.NEWDATE.value],
                        oldStart=item[api.OLDSTART.value],
                        newStart=item[api.NEWSTART.value],
                        oldEnd=item[api.OLDEND.value],
                        newEnd=item[api.NEWEND.value],
                        oldState=item[api.OLDSTATE.value],
                        newState=item[api.NEWSTATE.value],
                        oldStateDetail=item[api.OLDSTATEDETAIL.value],
                        newStateDetail=item[api.NEWSTATEDETAIL.value],
                        oldRoom=item[api.OLDROOM.value],
                        newRoom=item[api.NEWROOM.value],
                        oldSubject=item[api.OLDSUBJECT.value],
                        newSubject=item[api.NEWSUBJECT.value],
                        oldText=item[api.OLDTEXT.value],
                        newText=item[api.NEWTEXT.value]
                    )
                print(f"[{logLevel.INFO.value}] Successfully inserted {len(self.diffs)} diffs with batchID {batchID}")
        
        except Exception as e:
            print(f"[{logLevel.ERROR.value}] Error inserting data: {e}")
            raise e
        finally:
            # Always close the database connection
            database.closeConnection()
        