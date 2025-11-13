import requests
from configReader import configExtract


class exporter:
    urlRest = "https://erato.webuntis.com/WebUntis/api/rest/view/v1/timetable/entries"

    conf = configExtract("environment.json").conf

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "de-DE,de;q=0.9,en-DE;q=0.8,en;q=0.7,en-US;q=0.6",
        "anonymous-school": conf["anonymous-school"],
        "cookie": conf["cookie"],
    }

    def getElementMap(self, elements):
        elementMap = {}
        for element in elements:
            elementMap[element["id"]] = element

        return elementMap

    def getData(self, start, end, classID, verbose=False):
        optionsRest = (
            "?start="
            + start
            + "&end="
            + end
            + "&format=2&resourceType=CLASS&resources="
            + classID
            + "&periodTypes=&timetableType=STANDARD"
        )

        try:
            response = requests.get(self.urlRest + optionsRest, headers=self.headers)
            if response.status_code != 200:
                print(
                    f"Error fetching Data from API {response.status_code} Reason: {response.reason}"
                )
                quit(1)
            raw_data = response.json()
        except:
            raise Exception("Failed to retrieve Untis data correctly")

        periods = []
        diffs = []
        for day in raw_data["days"]:
            date = day["date"]
            for entry in day["gridEntries"]:
                status = entry["status"]
                stateDetail = entry["statusDetail"]
                classType = entry["type"]
                oldStart = None
                oldEnd = None
                changes = None
                changedClass = None
                changedRoom = None
                subText = entry["substitutionText"]
                if subText == None:
                    subText = ""
                start = entry["duration"]["start"]
                end = entry["duration"]["end"]
                if entry["position1"]:
                    shortName = entry["position1"][0]["current"]["shortName"]
                if entry["position2"]:
                    if entry["position2"][0]["current"]:
                        room = entry["position2"][0]["current"]["displayName"]
                if entry["statusDetail"] == "MOVED" and entry["status"] == "CANCELLED":
                    oldStart = start
                    oldEnd = end
                    start = entry["moved"]["start"]
                    end = entry["moved"]["end"]
                if entry["statusDetail"] == "MOVED" and entry["status"] != "CANCELLED":
                    oldStart = entry["moved"]["start"]
                    oldEnd = entry["moved"]["end"]
                if entry["status"] == "CHANGED":
                    if entry["position1"][0]["removed"] != None:
                        changedClass = entry["position1"][0]["removed"]["displayName"]
                    if entry["position2"][0]["removed"] != None:
                        changedRoom = entry["position2"][0]["removed"]["shortName"]

                periods.append(
                    {
                        "date": date,
                        "startTime": start,
                        "endTime": end,
                        "type": classType,
                        "state": status,
                        "stateDetail": stateDetail,
                        "room": room,
                        "subject": shortName,
                        "substituteText": subText,
                    }
                )
                if status != "REGULAR":
                    diffs.append(
                        {
                            "oldDate": "",
                            "newDate": date,
                            "oldStart": oldStart,
                            "newStart": start,
                            "oldEnd": oldEnd,
                            "newEnd": end,
                            "newState": status,
                            "oldState": "",
                            "newStateDetail": stateDetail,
                            "oldStateDetail": "",
                            "oldRoom": changedRoom,
                            "newRoom": room,
                            "oldSubject": changedClass,
                            "newSubject": shortName,
                            "newText": subText,
                            "oldText": "",
                        }
                    )

        if verbose:
            print(f"[VERBOSE] {len(periods)} fetched.")
        return [periods, diffs]
