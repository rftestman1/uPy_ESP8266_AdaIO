import peripherals as prph
import wifi_connect as wifi
import mqtt_connect as mqtt

# Enter Wifi SSID and PW
SSID = 'NETGEAR25'
PW = 'slowwater161'

# Enter time interval in seconds for publishing data to broker
publish_time = 30

# Test sensors before connecting to WIFI and Broker
prph.led_blink(10, 500)                     # 10 x 0.5s Blink on startup
tc, tf = prph.tmp36()
print('Temp Celsius = {}c'.format(tc))
print('Temp Fahrenheit = {}f'.format(tf))
prph.redled(True)
t2320, h2320 = prph.am2320(14)
print('AM2320 Temp = {}c'.format(t2320))
print('AM2320 Humidity = {}%'.format(h2320))

# test sleep mode ** code below this will not be executed
# prph.deepsleep(5)

while wifi.do_connect(SSID, PW):          # Pass in the SSID and PW
    try:
        mqtt.broker_connect(publish_time)
    except OSError:
        print('Broker connection lost going to Deep Sleep mode')
        prph.deepsleep(60)
prph.led_blink(20, 250)                     # 20 x 0.25s fast Blink if no connection
print('Going to Deep Sleep mode')
prph.deepsleep(60)
