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
        
    