from _database.sqliteConnector import plutus

def delete(history:int):
    database = plutus()

    batches = database.getBatches()

    if batches <= history:
        return 0

    for i in range(batches - history):
        database.deleteLastBatch()


