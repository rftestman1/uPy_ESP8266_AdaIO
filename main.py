# The MIT License (MIT)
# Copyright (c) 2018 Mike Teachman
# https://opensource.org/licenses/MIT
#
# Example MicroPython and CircuitPython code showing how to use the MQTT protocol with Adafruit IO, to  
# publish and subscribe on the same device
#
# Tested using the releases:
#   ESP8266
#       MicroPython 1.9.3
#       MicroPython 1.9.4
#       CircuitPython 2.3.1     (needs addition of CircuitPython specific umqtt module)
#       CircuitPython 3.0.0     (needs addition of CircuitPython specific umqtt module)
#   ESP32
#       MicroPython 1.9.4       (needs addition of MicroPython umqtt module)
#
# Tested using the following boards:
#   Adafruit Feather HUZZAH ESP8266
#   Adafruit Feather HUZZAH ESP32
#   WeMos D1 Mini
#
# User configuration parameters are indicated with "ENTER_".  

import network
import time
from umqtt.robust import MQTTClient
import os
import gc
import sys
# ESP8266 Control
from machine import Pin

led = Pin(2, Pin.OUT)
# led.off()

# the following function is the callback which is 
# called when subscribed data is received
def cb(topic, msg):
    # led = Pin(2, Pin.OUT)
    print('Subscribe:  Received Data:  Topic = {}, Msg = {}\n'.format(topic, msg))
    if msg == b'ON':
        led.off()
        print('led on')
    else:
        led.on()
        print('led off')
    # free_heap = int(str(msg,'utf-8'))

# WiFi connection information
WIFI_SSID = 'NETGEA***'
WIFI_PASSWORD = 'slowwater***'

# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# wait until the device is connected to the WiFi network
MAX_ATTEMPTS = 20
attempt_count = 0
while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    time.sleep(1)

if attempt_count == MAX_ATTEMPTS:
    print('could not connect to the WiFi network')
    sys.exit()

# create a random MQTT clientID 
random_num = int.from_bytes(os.urandom(3), 'little')
mqtt_client_id = bytes('client_'+str(random_num), 'utf-8')

# connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
# 
# To use a secure connection (encrypted) with TLS: 
#   set MQTTClient initializer parameter to "ssl=True"
#   Caveat: a secure connection uses about 9k bytes of the heap
#         (about 1/4 of the micropython heap on the ESP8266 platform)
ADAFRUIT_IO_URL = b'io.adafruit.com' 
ADAFRUIT_USERNAME = b'stormin'
ADAFRUIT_IO_KEY = b'add IO Key here'
ADAIO_PubFD_1 = b'GC_FreeMemory'
ADAIO_SubFD_1 = b'blue-led-control'

client = MQTTClient(client_id=mqtt_client_id, 
                    server=ADAFRUIT_IO_URL, 
                    user=ADAFRUIT_USERNAME, 
                    password=ADAFRUIT_IO_KEY,
                    ssl=False)
                    
try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

# publish free heap statistics to Adafruit IO using MQTT
# subscribe to the same feed
#
# format of feed name:  
#   "ADAFRUIT_USERNAME/feeds/ADAFRUIT_IO_FEEDNAME"
mqtt_PubFD1 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAIO_PubFD_1), 'utf-8')
mqtt_SubFD1 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAIO_SubFD_1), 'utf-8')
client.set_callback(cb)      
client.subscribe(mqtt_SubFD1)
PUBLISH_PERIOD_IN_SEC = 120
SUBSCRIBE_CHECK_PERIOD_IN_SEC = 0.5 
accum_time = 0
while True:
    try:
        # Publish
        if accum_time >= PUBLISH_PERIOD_IN_SEC:
            free_heap_in_bytes = gc.mem_free()
            print('Publish:  freeHeap = {}'.format(free_heap_in_bytes))
            client.publish(mqtt_PubFD1,
                           bytes(str(free_heap_in_bytes), 'utf-8'), 
                           qos=0) 
            accum_time = 0                
        
        # Subscribe.  Non-blocking check for a new message.  
        client.check_msg()

        time.sleep(SUBSCRIBE_CHECK_PERIOD_IN_SEC)
        accum_time += SUBSCRIBE_CHECK_PERIOD_IN_SEC
        # print('Accumulated Time = {}'.format(accum_time))
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()
