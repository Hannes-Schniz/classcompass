from _database.sqliteConnector import plutus


def maintenance(count):
    db = plutus()
    db.connect()
    
    batchCount = db.batchAmount()
    
    for i in range(batchCount - count-1):
        db.removeFirstBatch()
    
    db.closeConnection()
        
    
    