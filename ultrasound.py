from flask import Flask, request
import json
import requests
import base64
import re
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import xmltodict


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


app = Flask(__name__)


SERVER_URL = "http://VM_IP_ADDRESS:8081/ultrasound" # Fill in IP address of local VM


with open('edr_devices.json') as devicesFile:
    devices = json.load(devicesFile)

def maxVolume(deviceType):
    switcher = {
        "SX20": 90,
        "SX80": 90,
        "MX700": 90,
        "MX800": 90,
        "MX800D": 90,
        "CodecPlus": 90,
        "CodecPro": 90,
        "SX10": 70,
        "MX200G2": 70,
        "MX300G2": 70,
        "RoomKit": 70,
        "RoomKitMini": 60,
        "Board55S": 90,
        "Board70S": 90,
        "Board85S": 90,
        "Board55": 58,
        "Board70": 70,
        "Room70": 80,
        "Room55D": 80,
        "Room70G2": 80,
        "DX80": 90,
        "DX70": 60,
        "Room55": 84
    }

    return switcher.get(deviceType, 60)

def ultrasoundOn(device):
    url = "https://" + device["ipAddress"] + "/putxml"
    payload = "<XmlDoc><Configuration><Audio><Ultrasound><MaxVolume>" + str(maxVolume(device["type"])) + "</MaxVolume></Ultrasound></Audio></Configuration></XmlDoc>"
    #payload = json.dumps(payload)
    header = {'Content-Type': "text/xml"}

    try:
        getResponse = requests.request("POST", url, data=payload, headers=header, verify=False, auth=(device["username"], device["password"]))
        getResponse = xmltodict.parse(getResponse.content)
        return(getResponse)
    except:
        return("Down")


def ultrasoundOff(device):
    url = "https://" + device["ipAddress"] + "/putxml"
    payload = "<XmlDoc><Configuration><Audio><Ultrasound><MaxVolume>0</MaxVolume></Ultrasound></Audio></Configuration></XmlDoc>"
    #payload = json.dumps(payload)
    header = {'Content-Type': "text/xml"}

    try:
        getResponse = requests.request("POST", url, data=payload, headers=header, verify=False, auth=(device["username"], device["password"]))
        getResponse = xmltodict.parse(getResponse.content)
        return(getResponse)
    except:
        return("Down")


def registerFeedback(device):
    url = "https://" + device["ipAddress"] + "/putxml"
    payload = "<XmlDoc><Command><HttpFeedback><Register><Expression item=\"1\">/Event/UserInterface/Extensions/Widget/Action</Expression><FeedbackSlot>" + str(2) + "</FeedbackSlot><Format>JSON</Format><ServerUrl>" + SERVER_URL + "</ServerUrl></Register></HttpFeedback></Command></XmlDoc>"
    #payload = json.dumps(payload)
    header = {'Content-Type': "text/xml"}

    try:
        getResponse = requests.request("POST", url, data=payload, headers=header, verify=False, auth=(device["username"], device["password"]))
        getResponse = xmltodict.parse(getResponse.content)
        return(getResponse)
    except:
        return("Down")


# Route to register feedback from the first device in devices.json
@app.route('/')
def hello():

    returnAnswer = registerFeedback(devices[0])

    return str(returnAnswer)

# Receive feedback from in-room control
@app.route('/ultrasound', methods=['POST'])
def ultrasound():

    if request.method == 'POST':

        jsonAnswer = json.loads(request.data)

        if jsonAnswer["Event"]["UserInterface"]["Extensions"]["Widget"]["Action"]["WidgetId"]["Value"] == "ultrasound":
            if jsonAnswer["Event"]["UserInterface"]["Extensions"]["Widget"]["Action"]["Type"]["Value"] == "released":

                onDevice = int(jsonAnswer["Event"]["UserInterface"]["Extensions"]["Widget"]["Action"]["Value"]["Value"]) - 1 #id string

                c = 0

                for i in devices:
                    if c == onDevice:
                        returnAnswer = ultrasoundOn(i)
                        print(returnAnswer)
                    else:
                        print("in else")
                        returnAnswer = ultrasoundOff(i)
                        print(returnAnswer)
                    c += 1
                    print(str(c))

    return 'All set'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081)
