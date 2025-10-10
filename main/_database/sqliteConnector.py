import sqlite3
import os
import hashlib


class plutus:
    
    conn = None
    cur = None
    
    def __init__(self):
        pass
    
    def addClass(self,date, startTime, endTime, type, state, stateDetail, room, subject, substituteText, batchID):
        insert = f"INSERT INTO classes (batchID, date, startTime, endTime, type, state, stateDetail, room, subject, substituteText) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.cur.execute(insert, (batchID, date, startTime, endTime, type, state, stateDetail, room, subject, substituteText))
    
    def addDiff(self, batchID, oldDate, newDate, oldStart, newStart, oldEnd, newEnd, oldState, newState, oldStateDetail, newStateDetail, oldRoom, newRoom, oldSubject, newSubject, oldText, newText):
        insert = f"INSERT INTO diff (batchID, oldDate, newDate, oldStart, newStart, oldEnd, newEnd, oldState, newState, oldStateDetail, newStateDetail, oldRoom, newRoom, oldSubject, newSubject, oldText, newText) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        self.cur.execute(insert, (batchID, oldDate, newDate, oldStart, newStart, oldEnd, newEnd, oldState, newState, oldStateDetail, newStateDetail, oldRoom, newRoom, oldSubject, newSubject, oldText, newText))
    
    def connect(self):
        self.conn = sqlite3.connect(os.environ['DB_PATH'])
        self.cur = self.conn.cursor()
    
    def closeConnection(self):
        self.conn.commit()
        self.conn.close()
        
    def getNewBatchID(self, table):
        close = False
        if self.conn is None:
            self.connect()
            close = True
        currentBatchID = self.cur.execute(f"select max(batchID) from {table}").fetchone()[0]
        if  currentBatchID == None:
            currentBatchID = 0
        if close:
            self.closeConnection()
        return currentBatchID+1
    
    
    def getClasses(self, batchID: int):
        select = f"select * from classes where batchID = {batchID} order by date, startTime"
        res = self.cur.execute(select)
        
        result = res.fetchall()
        
        resultList = []
        
        for row in result:
            resultList.append({
                'date': row[1],
                'startTime': row[2],
                'endTime': row[3],
                'type': row[4],
                'state': row[5],
                'stateDetail' : row[6],
                'room': row[7],
                'name': row[8],
                'substituteText': row[9]
            })
        
        return resultList
    
    def getDiffs(self, batchID: int):
        """Return all diffs for a batch as a list of dicts.

        Uses the actual diff schema (old/new fields) and a parameterized query.
        """
        columns = [
            "batchID",
            "oldDate", "newDate",
            "oldStart", "newStart",
            "oldEnd", "newEnd",
            "oldState", "newState",
            "oldStateDetail", "newStateDetail",
            "oldRoom", "newRoom",
            "oldSubject", "newSubject",
            "oldText", "newText",
        ]

        select = (
            "SELECT "
            + ", ".join(columns)
            + " FROM diff WHERE batchID = ?"
        )
        res = self.cur.execute(select, (batchID,))
        rows = res.fetchall()

        return [dict(zip(columns, row)) for row in rows]
    
    def addNotification(self, message, plattform, destination):
        
        h = hashlib.new('md5')
        string = f"{message}:{plattform}:{destination}"
        h.update(string.encode('utf-8'))
        
        select = f"Select count(*) from notifications where hash = ?"
        
        exists = self.cur.execute(select, (h.hexdigest(),)).fetchone()[0]
        
        if exists > 0:
            return -1
        
        insert = f"INSERT INTO notifications (message, plattform, destination, hash) VALUES (?,?,?,?)"
        
        self.cur.execute(insert, (f"{message}", f"{plattform}", f"{destination}", f"{h.hexdigest()}",))
        self.conn.commit()
        return 0
        
    
    def removeFirstBatch(self):
        removeClasses = "delete from classes where batchID = (select min(batchID) from classes)"
        #removediffs = "delete from diff where batchID = (select min(batchID) from diff)"
        
        self.cur.execute(removeClasses)
        #self.cur.execute(removediffs)
        
        return 0
    
    def batchAmount(self):
        batchCount = "select count(*) from (select * from classes group by batchID)"
        return self.cur.execute(batchCount).fetchone()[0]