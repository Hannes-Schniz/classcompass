from _schedule.untisDataHandler import apiHandler
from _calendar.calendarDataHandler import calendarHandler
import _maintenance.databaseMaint 
from configReader import configExtract
from datetime import datetime, timedelta, timezone
from _maintenance.dbmaint import maintenance
import os

conf = configExtract("config.json").conf
dataHandler = apiHandler() 
calendar = calendarHandler(int(conf['weeksAhead']))
database = plutus()

for i in range(int(conf['weeksAhead'])):
    currDate = (datetime.now(timezone.utc) + timedelta(days=i*7) ).strftime('%Y-%m-%d')
    dt = datetime.strptime(currDate, '%Y-%m-%d')
    start = dt - timedelta(days=dt.weekday())
    end = (start + timedelta(days=5)).strftime('%Y-%m-%d')
    start = start.strftime('%Y-%m-%d')
    dataHandler.getData(start=start, end=end, classID=conf['classID'])
    
dataHandler.sendData()

calendar.getData()

calendar.deleteEvents()

calendar.sendData(conf['color-scheme'], conf['showCancelled'], conf['showChanged'])
calendar.sendData(conf['color-scheme'])

if int(conf['history']) <= 0:
    print ("[ERR] : History parameter too low")
    return 0
databaseMaint.delete(int(conf['history']))

maintenance(conf['maxBatch'])