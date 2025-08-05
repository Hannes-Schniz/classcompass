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
        self.conn = sqlite3.connect(os.environ['DBPATHDEF'])
        self.cur = self.conn.cursor()
    
    def closeConnection(self):
        self.conn.commit()
        self.conn.close()
        
    def getNewBatchID(self):
        close = False
        if None == self.conn:
            self.connect()
            close = True
        currentBatchID = self.cur.execute("select max(batchID) from classes").fetchone()
        if close:
            self.closeConnection()
        return currentBatchID+1
        
    