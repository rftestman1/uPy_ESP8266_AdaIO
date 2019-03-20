import peripherals as prph
import wifi_connect as wifi
import mqtt_connect as mqtt
from mcp3008 import MCP3008

# Enter Wifi SSID and PW
SSID = 'CPGVentures'
PW = 'Soulshine2019'

# Enter time interval in seconds for publishing data to broker
publish_time = 30

# Test sensors before connecting to WIFI and Broker
prph.led_blink(10, 500)                     # 10 x 0.5s Blink on startup
mcp = MCP3008()
tc_water, tf_water = prph.tmp36(mcp.read(0))
print('Temp Celsius = {}c'.format(tc_water))
print('Temp Fahrenheit = {}f'.format(tf_water))
prph.redled(True)
t2320, h2320 = prph.am2320(4)
print('AM2320 Temp = {}c'.format(t2320))
print('AM2320 Humidity = {}%'.format(h2320))

while wifi.do_connect(SSID, PW):          # Pass in the SSID and PW
    try:
        mqtt.broker_connect(publish_time, tc_water)
    except OSError:
        print('Broker connection lost going to Deep Sleep mode')
        prph.deepsleep(60)
prph.led_blink(20, 250)                     # 20 x 0.25s fast Blink if no connection
print('Going to Deep Sleep mode')
prph.deepsleep(60)
