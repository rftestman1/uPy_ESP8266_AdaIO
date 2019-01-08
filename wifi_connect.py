# The MIT License (MIT)
# Copyright (c) 2018 Mike Teachman
# https://opensource.org/licenses/MIT

import network
import time
import sys


def do_connect(ssid, pw):
    # WiFi connection information
    WIFI_SSID = ssid
    WIFI_PASSWORD = pw

    # turn off the WiFi Access Point
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    # Activate WiFi network connection
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)

    # wait until the device is connected to the WiFi network
    MAX_ATTEMPTS = 20
    attempt_count = 0
    while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)
        print('Trying to connect!')
        attempt_count += 1
        time.sleep(1)

    if wifi.isconnected():
        print('wifi connected!')
        print('Network Config: ', wifi.ifconfig())
        return True

    if attempt_count == MAX_ATTEMPTS:
        print('could not connect to the WiFi network')
        return False
        sys.exit()
