import blink as b
import wifi_connect as wifi
import mqtt_connect as mqtt

# Enter Wifi SSID and PW
SSID = 'NETGEAR25'
PW = 'slowwater161'

# Enter time interval for publishing data to broker
publish_time = 30

b.led_blink(10, 500)
while wifi.do_connect(SSID, PW):
    mqtt.broker_connect(publish_time)
    b.led_blink(4, 1000)
b.led_blink(20, 250)
