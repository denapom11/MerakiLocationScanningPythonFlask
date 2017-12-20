#!flask/bin/python

"""
Cisco Meraki Location Scanning Receiver

A simple example demonstrating how to interact with the CMX API.

How it works:
- Meraki access points will listen for WiFi clients that are searching for a network to join and log the events.
- The "observations" are then collected temporarily in the cloud where additional information can be added to
the event, such as GPS, X Y coordinates and additional client details.
- Meraki will first send a GET request to this CMX receiver, which expects to receieve a "validator" key that matches
the Meraki network's validator.
- Meraki will then send a JSON message to this application's POST URL (i.e. http://yourserver/ method=[POST])
- The JSON is checked to ensure it matches the expected secret, version and observation device type.
- The resulting data is sent to the "save_data(data)" function where it can be sent to a databse or other service
    - This example will simply print the CMX data to the console.

Default port: 5000

Cisco Meraki CMX Documentation
https://documentation.meraki.com/MR/Monitoring_and_Reporting/CMX_Analytics#CMX_Location_API

Written by Cory Guynn
2016

www.InternetOfLEGO.com
Developers.Meraki.com
"""

# Libraries
from pprint import pprint
from flask import Flask
from flask import json
from flask import request
from flask import render_template
import sys, getopt
import json
from pymongo import MongoClient

############## USER DEFINED SETTINGS ###############
# MERAKI SETTINGS
validator = "EnterYourValidator"
secret = "EnterYourSecret"
version = "2.0" # This code was written to support the CMX JSON version specified
locationdata = 'Location Data Holder'

client = MongoClient("mongodb://localhost:27017")
db = client.locationdata


# Save Location Data
def save_data(data):
    print("---- SAVING Location DATA ----")

    pprint(data, indent=1)

    ## Adjust data before DB insert ##
    # Add GeoJSON structure for MongoDB Compass (or similar) mapping
    '''for i in data["data"]["observations"]:
        print("i",i)
        data["data"]["secret"] = "hidden"
        lat = i["location"]["lat"]
        lng = i["location"]["lng"]
        clientMac = i["clientMac"]
        data["data"]["geoJSON"] = {
          "type": "Feature",
          "geometry": {
            "type": "Point",
            "coordinates": [lat,lng]
          },
          "properties": {
            "name": clientMac
          }
        }

        #data["data"]["locationGeoJSON"] = json.dumps(locationGeoJSON)
        #data["data"].append({"geoJSON":{"type": "Feature","geometry": {"type": "Point","coordinates": [i["location"]["lat"], i[["location"]["lng"], i["location"]["unc"]]},"properties": {"name": i["clientMac"]}}})
    '''

    # Commit to database
    result = db.locationdata.insert_one(data)
    print("MongoDB insert result: ",result)

####################################################
app = Flask(__name__)


# Respond to Meraki with validator
@app.route('/', methods=['GET'])
def get_validator():
    print("validator sent to: ",request.environ['REMOTE_ADDR'])
    return validator

# Accept CMX JSON POST
@app.route('/', methods=['POST'])
def get_locationJSON():
    global locationdata
    if not request.json or not 'data' in request.json:
        return("invalid data",400)
    locationdata = request.json
    pprint(locationdata, indent=1)
    print("Received POST from ",request.environ['REMOTE_ADDR'])

    # Verify secret
    if locationdata['secret'] != secret:
        print("secret invalid:", locationdata['secret'])
        return("invalid secret",403)
    else:
        print("secret verified: ", locationdata['secret'])

    # Verify version
    if locationdata['version'] != version:
        print("invalid version")
        return("invalid version",400)
    else:
        print("version verified: ", locationdata['version'])

    # Determine device type
    if locationdata['type'] == "DevicesSeen":
        print("WiFi Devices Seen")
    elif locationdata['type'] == "BluetoothDevicesSeen":
        print("Bluetooth Devices Seen")
    else:
        print("Unknown Device 'type'")
        return("invalid device type",403)

    # Return success message
    return "Location POST Received"

@app.route('/go', methods=['GET'])
def get_go():
    return render_template('index.html',**locals())


@app.route('/clients/', methods=['GET'])
def get_clients():
    global locationdata
    pprint(locationdata["data"]["observations"], indent=1)
    return json.dumps(locationdata["data"]["observations"])

@app.route('/clients/<clientMac>', methods=['GET'])
def get_individualclients(clientMac):
    global locationdata
    for client in locationdata["data"]["observations"]:
        if client["clientMac"] == clientMac:
            return json.dumps(client)
    return ''

# Launch application with supplied arguments

def main(argv):
    global validator
    global secret


    try:
       opts, args = getopt.getopt(argv,"hv:s:",["validator=","secret="])
    except getopt.GetoptError:
       print ('locationscanningreceiver-mongodb.py -v <validator> -s <secret>')
       sys.exit(2)
    for opt, arg in opts:
       if opt == '-h':
           print ('locationscanningreceiver-mongodb.py -v <validator> -s <secret>')
           sys.exit()
       elif opt in ("-v", "--validator"):
           validator = arg
       elif opt in ("-s", "--secret"):
           secret = arg

    print ('validator: '+ validator)
    print ('secret: '+ secret)


if __name__ == '__main__':
    main(sys.argv[1:])
    app.run(port=5000,debug=False)
