import time
from umqtt.robust import MQTTClient
import os
import gc
import sys
from machine import Pin

from hardware import peripherals as prph
from hardware.mcp3008 import MCP3008
from config import DEVICE_ID
from config import ADAFRUIT_IO_URL
from config import ADAFRUIT_USERNAME
from config import ADAFRUIT_IO_KEY
from config import ADAIO_PubFD_1
from config import ADAIO_PubFD_2
from config import ADAIO_PubFD_3
from config import ADAIO_PubFD_4
from config import ADAIO_SubFD_1
from config import SUBSCRIBE_CHECK_PERIOD_SEC


def subscription_call_back(topic, msg):
    led = Pin(2, Pin.OUT)
    print('Subscribe:  Received Data:  Topic = {}, Msg = {}\n'.format(topic, msg))
    if msg == b'ON':
        led.off()
        print('Blue led on')
    else:
        led.on()
        print('Blue led off')


def broker_connect():
    mqtt_client_id = bytes('client_' + str(DEVICE_ID), 'utf-8')

    '''connect to Adafruit IO MQTT broker using unsecure TCP (port 1883)
        To use a secure connection (encrypted) with TLS:
        set MQTTClient initializer parameter to "ssl=True"
        Caveat: a secure connection uses about 9k bytes of the heap
        (about 1/4 of the micropython heap on the ESP8266 platform)'''

    client = MQTTClient(client_id=mqtt_client_id,
                        server=ADAFRUIT_IO_URL,
                        user=ADAFRUIT_USERNAME,
                        password=ADAFRUIT_IO_KEY,
                        ssl=False)

    try:
        client.connect()
    except Exception as e:
        print('Could not connect to MQTT server {}{}'.format(type(e).__name__, e))
        print('Going to Deep Sleep mode')
        prph.deep_sleep(60)
        sys.exit()

    '''publish free heap statistics to Adafruit IO using MQTT
        subscribe to the same feed
        
        format of feed name:
        "ADAFRUIT_USERNAME/feeds/ADAFRUIT_IO_FEEDNAME"'''

    mqtt_PubFD1 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAIO_PubFD_1), 'utf-8')
    mqtt_PubFD2 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAIO_PubFD_2), 'utf-8')
    mqtt_PubFD3 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAIO_PubFD_3), 'utf-8')
    mqtt_PubFD4 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAIO_PubFD_4), 'utf-8')
    mqtt_SubFD1 = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, ADAIO_SubFD_1), 'utf-8')

    client.set_callback(subscription_call_back)
    client.subscribe(mqtt_SubFD1)
    mcp = MCP3008()

    while True:
        try:
            # Publish free heap memory from GC (Garbage Collection)
            free_heap_in_bytes = gc.mem_free() / 1000
            print('Publish:  GC FreeMem = {} k'.format(free_heap_in_bytes))
            client.publish(mqtt_PubFD1,
                           bytes(str(free_heap_in_bytes), 'utf-8'),
                           qos=0)
            tc_water, tf_water = prph.read_tmp36(mcp.read_channels(0))
            print('Publish:  Water Temp = {} c'.format(tc_water))
            client.publish(mqtt_PubFD2,
                           bytes(str(tc_water), 'utf-8'),
                           qos=0)
            # Publish outdoor temperature in C
            t2320, h2320 = prph.read_am2320(4)
            print('Publish:  Outdoor Temp = {} c'.format(t2320))
            client.publish(mqtt_PubFD3,
                           bytes(str(t2320), 'utf-8'),
                           qos=0)
            # Publish outdoor humidity in %
            print('Publish:  Outdoor Humidity = {} %'.format(h2320))
            client.publish(mqtt_PubFD4,
                           bytes(str(h2320), 'utf-8'),
                           qos=0)

            # Subscribe.  Non-blocking check for a new message.
            client.check_msg()
            time.sleep(SUBSCRIBE_CHECK_PERIOD_SEC)
        except KeyboardInterrupt:
            print('Ctrl-C pressed...exiting')
            client.disconnect()
            sys.exit()
