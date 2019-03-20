import utime
import machine
import dht


# Function will blink the blue led on ESP8266
def blink_led(n_times, t):
    pin = machine.Pin
    led = pin(2, pin.OUT)
    enabled = False
    for k in range(1, n_times):
        if enabled:
            led.off()
            print('LED On!')
        else:
            led.on()
            print('LED Off!')
        utime.sleep_ms(t)
        enabled = not enabled


def read_tmp36(adc):
    v = .00322 * adc
    tempc = 100 * (v - 0.5)
    tempf = (tempc * 1.8) + 32
    return str(round(tempc, 1)), str(round(tempf, 1))


def deep_sleep(t_sleep):
    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after 10 seconds, t_sleep = 10000, (waking the device)
    rtc.alarm(rtc.ALARM0, t_sleep * 1000)

    # put the device to sleep
    machine.deepsleep()


def set_red_led(enabled):
    pin = machine.Pin
    led = pin(0, pin.OUT)
    if enabled:
        led.off()  # pin goes low LED on
        utime.sleep_ms(3000)
    else:
        led.on()  # pin goes high LED off


def read_am2320(io_pin):
    machine.Pin(io_pin, machine.Pin.OUT, value=0)
    # Read one wire temp and humidity sensor AM2320
    d = dht.DHT22(machine.Pin(io_pin, machine.Pin.IN, machine.Pin.PULL_UP))
    d.measure()
    utime.sleep_ms(2000)
    return str(d.temperature()), str(d.humidity())
