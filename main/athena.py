from _schedule.untisDataHandler import apiHandler
from _calendar.calendarDataHandler import calendarHandler
from configReader import configExtract
from datetime import datetime, timedelta, timezone
from _maintenance.dbmaint import maintenance
from constants import cfgParams, files

conf = configExtract(files.CONFIG.value).conf
dataHandler = apiHandler() 
calendar = calendarHandler(int(conf[cfgParams.WEEKSAHEAD.value]))

for i in range(int(conf[cfgParams.WEEKSAHEAD.value])):
    currDate = (datetime.now(timezone.utc) + timedelta(days=i*7) ).strftime('%Y-%m-%d')
    dt = datetime.strptime(currDate, '%Y-%m-%d')
    start = dt - timedelta(days=dt.weekday())
    end = (start + timedelta(days=5)).strftime('%Y-%m-%d')
    start = start.strftime('%Y-%m-%d')
    dataHandler.getData(start=start, end=end, classID=conf[cfgParams.CLASSID.value])
    
dataHandler.sendData()

calendar.getData()

calendar.deleteEvents()

calendar.sendData(conf[cfgParams.COLORSCHEME.value], conf[cfgParams.SHOWCANCELLED.value], conf[cfgParams.SHOWCHANGED.value])

maintenance(conf[cfgParams.MAXBATCH.value])