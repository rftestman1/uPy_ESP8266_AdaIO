import network
import time
import sys
from config import NETWORK_SSID
from config import NETWORK_PASSWORD
from config import MAX_CONNECTION_RETRY_ATTEMPTS


def turn_off_wifi():
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)


def turn_on_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    return wifi


def do_connect():
    turn_off_wifi()
    wifi = turn_on_wifi()

    # wait until the device is connected to the WiFi network
    attempt_count = 0
    while not wifi.isconnected():
        wifi.connect(NETWORK_SSID, NETWORK_PASSWORD)
        print('Trying to connect!')
        attempt_count += 1
        time.sleep(1)

    if wifi.isconnected():
        print('wifi connected!')
        print('Network Config: ', wifi.ifconfig())
        return True

    if attempt_count == MAX_CONNECTION_RETRY_ATTEMPTS:
        print('could not connect to the WiFi network')
        return False
        sys.exit()
