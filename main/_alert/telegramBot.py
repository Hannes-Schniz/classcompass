import time

import requests
from configReader import configExtract

from constants import envFile, files

env = configExtract(files.ENVIRONMENT).conf
maint = configExtract(files.CONFIG).conf["maintenance"] == 1
TOKEN = env[envFile.BOTTOKEN]
chat_id = env[envFile.CHAT]


def sendMessage(message):
    params = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    if maint:
        return
    requests.post(url=url, params=params)


def createText(summary, location, description, date, start, end):
    date = f"{date.split('-')[2]}.{date.split('-')[1]}.{date.split('-')[0]}"
    return f"<b>{summary}</b>\n<b>Raum:</b> {location}\n<b>Stunde</b>: {date} {start}-{end}\n<b>Beschreibung:</b> {description}"


def shareCalendar():
    params = {}
    while True:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        print(requests.get(url=url, params=params).json())
        time.sleep(1)
import requests

class TelegramBot():

    def sendMessage(self, chat, token, message):
        params = {"chat_id":chat,"text": message, "parse_mode": "HTML"}
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url=url, params=params)

    #def shareCalendar(self):
    #    params = {}
    #    while True:
    #        url = f"https://api.telegram.org/bot{self.TOKEN}/getUpdates"
    #        print(requests.get(url=url, params=params).json())
    #        time.sleep(1)
