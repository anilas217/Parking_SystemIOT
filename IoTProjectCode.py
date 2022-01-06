#!/usr/bin/python3
import RPi.GPIO as GPIO

from urllib.request import urlopen
from urllib.request import Request
import time
import paho.mqtt.publish as publish
import psutil
import string
channel_ID = "1626247"

GPIO.setmode(GPIO.BCM)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
TRIG = 23
ECHO = 24
myAPI = 'YK3G3RXTPI94F8DA' 
print ("Distance Measurement In Progress")
baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI 
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
mqtt_host = "mqtt3.thingspeak.com"

# Your MQTT credentials for the device
mqtt_client_ID = "OQMOCgUhOy8bNAsyAQcmGic"

mqtt_username  = "OQMOCgUhOy8bNAsyAQcmGic"

mqtt_password  = "f5b7qEpV5TL0inMH/P0IRNeY"
t_transport = "websockets"
t_port = 80
# Create the topic string.
topic = "channels/" + channel_ID + "/publish"


try:
    while True:
        
        GPIO.output(TRIG, False)
        print ("Waiting For Sensor To Settle")
        time.sleep(5)
        
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        
        while GPIO.input(ECHO)==0:
            pulse_start = time.time()
        
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start
        
        distance = pulse_duration * 17150
        
        distance = round(distance, 2)
        
        print ("Distance: ",distance,"cm")
        payload = "field1=" + str(distance)
        publish.single(topic, payload, hostname=mqtt_host, transport=t_transport, port=t_port, client_id=mqtt_client_ID, auth={'username':mqtt_username,'password':mqtt_password})
        if(distance >10 and distance <60):
            GPIO.output(7,True)
            time.sleep(3)
        else:
            GPIO.output(12,True)
            GPIO.output(11,False)
            time.sleep(3)
            
except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program
    print("Cleaning up!")
    gpio.cleanup()