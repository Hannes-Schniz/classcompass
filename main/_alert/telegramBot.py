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