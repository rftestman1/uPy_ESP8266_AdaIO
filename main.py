from hardware import peripherals as prph
from network_connections import mqtt_connect as mqtt, wifi_connect as wifi
from hardware.mcp3008 import MCP3008

from config import NETWORK_SSID


def start_up_check():
    print("Blinking led 10 times for half a second")
    prph.blink_led(10, 500)

    mcp = MCP3008()
    tc_water, tf_water = prph.read_tmp36(mcp.read_channels(0))
    print('Temp Celsius = {}c'.format(tc_water))
    print('Temp Fahrenheit = {}f'.format(tf_water))

    prph.set_red_led(True)
    t2320, h2320 = prph.read_am2320(4)
    print('AM2320 Temp = {}c'.format(t2320))
    print('AM2320 Humidity = {}%'.format(h2320))


def main():
    while wifi.do_connect():
        try:
            mqtt.broker_connect()
        except OSError:
            print('OSError Exception: Broker connection lost going to Deep Sleep mode')
            prph.deep_sleep(60)

    print('Could not connect to network ' + NETWORK_SSID + " shutting down.")
    prph.blink_led(20, 250)  # 20 x 0.25s fast Blink if no connection
    prph.deep_sleep(60)


if __name__ == "__main__":
    main()
