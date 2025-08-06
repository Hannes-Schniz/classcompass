from schedule.untis_connector import exporter
from configReader import configExtract

ex = exporter()

conf = configExtract("config.json").conf

print(ex.getData(start="2025-07-21", end="2025-07-25", classID=conf['classID'], verbose=True))