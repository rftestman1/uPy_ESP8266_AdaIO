import utime
from machine import Pin


def blink_led():
    led = Pin(2, Pin.OUT)
    enabled = False
    while True:
        if enabled:
            led.off()
            print('Blue LED off')
        else:
            led.on()
            print('Blue LED on')
        utime.sleep_ms(2000)
        enabled = not enabled
