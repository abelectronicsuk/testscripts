import cayenne.client
import ow
import time
import sys

# Cayenne authentication info.
# This should be obtained from the Cayenne Dashboard.
MQTT_USERNAME = "USERNAME"
MQTT_PASSWORD = "PASSWORD"
MQTT_CLIENT_ID = "CLIENT_ID"


# The callback for when a message is received from Cayenne.
def on_message(message):
    print("message received: " + str(message))
    # If there is an error processing the message return an error string,
    # otherwise return nothing.

client = cayenne.client.CayenneMQTTClient()
client.on_message = on_message
client.begin(MQTT_USERNAME, MQTT_PASSWORD, MQTT_CLIENT_ID)

# Initialise the 1-Wire bus
ow.init('localhost:4304')

# get a list of 1-Wire sensors and print it to the screen
sensorlist = ow.Sensor('/').sensorList()

for sensor in sensorlist:
    print('Device Found')
    print('Address: ' + sensor.address)
    print('Family: ' + sensor.family)
    print('ID: ' + sensor.id)
    print('Type: ' + sensor.type)
    print(' ')

timestamp = 0

if len(sensorlist) > 0:
    # get the temperature from each sensor every 10 seconds
    while True:
        client.loop()

        if (time.time() > timestamp + 10):
            i = 1
            for sensor in sensorlist:
                # Check if the device is a temperature sensor
                if sensor.type == 'DS18S20' or sensor.type == 'DS18B20':
                    client.celsiusWrite(i, sensor.temperature)
                    i = i+1
            timestamp = time.time()
