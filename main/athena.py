from schedule.untisDataHandler import apiHandler
from calendar.calendarDataHandler import calendarHandler
from configReader import configExtract
from datetime import datetime, timedelta, timezone
import os

conf = configExtract("config.json").conf
dataHandler = apiHandler() 
calendarHandler = calendarHandler()

for i in range(int(conf['weeksAhead'])):
    currDate = (datetime.now(timezone.utc) + timedelta(days=i*7) ).strftime('%Y-%m-%d')
    dt = datetime.strptime(currDate, '%Y-%m-%d')
    start = dt - timedelta(days=dt.weekday())
    end = (start + timedelta(days=5)).strftime('%Y-%m-%d')
    start = start.strftime('%Y-%m-%d')
    dataHandler.getData(start=start, end=end, classID=conf['classID'])
    
dataHandler.sendData()

calendarHandler.getData()
