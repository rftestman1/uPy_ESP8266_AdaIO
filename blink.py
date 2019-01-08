import utime
from machine import Pin


# Function will blink the blue led on ESP8266
def led_blink(n_times, t):
    led = Pin(2, Pin.OUT)
    enabled = False
    x = 0
    while x < n_times:
        if enabled:
            led.off()
            print('LED On!')
        else:
            led.on()
            print('LED Off!')
        utime.sleep_ms(t)
        enabled = not enabled
        x += 1

