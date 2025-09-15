import sqlite3
import os


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
    