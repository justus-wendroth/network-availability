import urllib
import time
import json
import os
from datetime import datetime


def connectedToInternet(url="http://google.com", timeout=5) -> bool:
    try:
        urllib.request.urlopen(url, timeout=timeout)
        return True
    except urllib.request.URLError:
        return False
    
    
    # try:
    #     # _ = requests.head(url, timeout=timeout)
    #     print("trying")
    #     urllib.request.urlopen(url, timeout=timeout)
    #     return True
    # except:
    #     print(urllib.error)
    #     return False


def getCurrentTime() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def writeOutageToFile(startOfOutage: str, endOfOutage: str):
    with open("out/outages.json", "w") as outageFile:
        outages = json.load(outageFile)
        outages.append({"START": startOfOutage, "END": endOfOutage})
        json.dump(outages, outageFile, indent=4)


def createOutageFile():
    with open("out/outages.json", "w+") as outageFile:
        json.dump([], outageFile, indent=4)


def testConnectionContiously():
    previouslyConnected = connectedToInternet()
    startOfOutage = None

    if not previouslyConnected:
        startOfOutage = getCurrentTime()

    while True:
        time.sleep(3)
        connected = connectedToInternet()
        print(connected)

        if not connected and previouslyConnected:
            previouslyConnected = False
            startOfOutage = getCurrentTime()
            print("Outage started: " + startOfOutage)
        elif connected and not previouslyConnected:
            previouslyConnected = True
            endOfOutage = getCurrentTime()
            writeOutageToFile(startOfOutage, endOfOutage)
            print("Outage ended: " + startOfOutage + " until " + endOfOutage)


if not os.path.exists("out/outages.json"):
    createOutageFile()

testConnectionContiously()
