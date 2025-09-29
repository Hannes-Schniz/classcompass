from _database.sqliteConnector import plutus


def maintenance(count):
    db = plutus()
    db.connect()
    
    for i in range(count-1):
        db.removeFirstBatch()
    
    db.closeConnection()
        
    
    