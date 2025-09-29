from _database.sqliteConnector import plutus


def maintenance(count):
    db = plutus()
    db.connect()
    
    batchCount = db.batchAmount()
    
    if batchCount - count < 2:
        return 0
    
    for i in range(batchCount - count):
        print(f"[INF] Removing Batch")
        db.removeFirstBatch()
    
    db.closeConnection()
        
    
    