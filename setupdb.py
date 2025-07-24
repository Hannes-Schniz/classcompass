import sqlite3
con = sqlite3.connect("maps.db")
cur = con.cursor()


with open('sql/createClasses.sql', 'r') as createClasses:
    createClasses = createClasses.read()
with open('sql/createDiff.sql', 'r') as createDiff:
    createDiff = createDiff.read()
    
cur.executescript(createClasses)
cur.executescript(createDiff)
con.commit()
con.close()