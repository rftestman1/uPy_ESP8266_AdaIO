


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
ADAFRUIT_IO_KEY = b'4a8287af16f346d6be64bb6be020d3e3'
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
            print('Publish:  GC FreeMem = {}'.format(free_heap_in_bytes))
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
