### Meraki Location Scanning Python Receiver

### A basic web service to accept Location Scanning data from a Cisco Meraki network
- Accept a GET request from Meraki and respond with a validator
- Meraki will POST to the server, if validated.
- POST will contain a validator and a secret, which can be verified by the server.
- JSON data will be in the data object POST

## Prerequisites
* Flask must be installed
http://flask.pocoo.org/docs/0.12/
* Cisco Meraki Network with Location Scanning API enabled and configured to point to this server
* Expose your server publicly using a tool like ngrok: https://ngrok.com/


## locationscanningreceiver.py
-- The basic app will show the "blue-dot" location of the clients on a map
-- To launch from python directly: `python3 locationscanningreceiver.py -v <validator> -s <secret>`
-- To launch via flask:
```
export FLASK_APP=locationscanningreceiver.py -v <validator> -s <secret>
flask run -h 0.0.0.0
 * Running on http://0.0.0.0:5000/
```

## locationscanningreceiver-mongodb.py
-- Extends the basic app by placing data into a local MongoDB database to save historical data.
-- Requires https://www.mongodb.com/
-- Requires pymongo (`pip install pymongo`)
-- To launch from python directly:
    -- `mkdir mongodata`
    -- `mongod --dbpath=./mongodata --nojournal`
    -- from another terminal or command line window: `python3 locationscanningreceiver-mongodb.py -v <validator> -s <secret>`
-- To launch via flask:
    -- `mkdir mongodata`
    -- `mongod --dbpath=./mongodata --nojournal`
    -- from another terminal or command line window:
    ```
    export FLASK_APP=locationscanningreceiver-mongodb.py -v <validator> -s <secret>
    flask run -h 0.0.0.0
     * Running on http://0.0.0.0:5000/
    ```  

## Defaults
* Location Scanning Receiver Port: 5000
* Location Post URL: http://yourserver:5000/

* use ngrok to expose port 5000
```
ngrok http 5000
```
Then use the new url it creates as your base URL: https://<uniqueurl>.ngrok.io/

# Cisco Meraki Location Scanning API Documentation
https://documentation.meraki.com/MR/Monitoring_and_Reporting/CMX_Analytics#CMX_Location_API

### Initial code written by Cory Guynn
2016

http://www.InternetOfLEGO.com

### Extended by Matt DeNapoli
2017

https://developer.cisco.com
