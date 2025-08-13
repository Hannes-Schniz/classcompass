from schedule.untis_connector import exporter
from configReader import configExtract
import os

untis_exporter = exporter()

conf = configExtract("config.json").conf

MINUTECOUNTERVAR = "athena_counter"

minute = os.environ[MINUTECOUNTERVAR]

if minute > 0: 
    os.environ[MINUTECOUNTERVAR] = minute - 1
    quit(0)

os.environ[MINUTECOUNTERVAR] = conf['weeksAhead']

untisData = untis_exporter.getData(start="2025-07-21", end="2025-07-25", classID=conf['classID'], verbose=True)