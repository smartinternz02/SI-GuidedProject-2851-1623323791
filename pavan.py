
import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import json
from gtts import gTTS
import os


#Provide your IBM Watson Device Credentials
organization = "1zqjlv"
deviceType = "iotdevice"
deviceId = "1001"
authMethod = "token"
authToken = "1234567890"


# Initialize the device client.
T=0
H=0

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])


        if cmd.data['command']=='feed':
                print("FEED")
        if cmd.data['command']=='feedon':
                

                text="feeding device is activated"
                language='en'

                output=gTTS(text=text, lang=language,slow=False)


                output.save("feedon.mp3")


                os.system("start feedon.mp3")
        if cmd.data['command']=='feedoff':
                

                text="feeding device is diactivated"
                language='en'

                output=gTTS(text=text, lang=language,slow=False)


                output.save("feedoff.mp3")


                os.system("start feedoff.mp3")
                
        
        if cmd.command == "setInterval":
                if 'interval' not in cmd.data:
                        print("Error - command is missing required information: 'interval'")
                else:
                        interval = cmd.data['interval']
        elif cmd.command == "print":
                if 'message' not in cmd.data:
                        print("Error - command is missing required information: 'message'")
                else:
                        print(cmd.data['message'])

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        s=random.randint(0,100)
        w=random.randint(0,100)
        #Send Temperature & Humidity to IBM Watson
        data = {"d":{ 'foodlevel' : s, 'waterlevel': w, }}
        #print data
        def myOnPublishCallback():
            print ("foodlevel = %s C" % s, "waterlevel = %s %%" % w,"to IBM Watson")

        success = deviceCli.publishEvent("Data", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
