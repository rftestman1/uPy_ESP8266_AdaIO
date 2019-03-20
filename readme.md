# Seedgistics Tower Monitor
MicroPython file used to control the Seedgistics Tower Monitor control unit
  
## Requirements
In order to run this you will need to set up some sort of IDE with a connection to a ESP8266 board. I suggest using this manual [here](https://blog.jetbrains.com/pycharm/2018/01/micropython-plugin-for-pycharm/ "PyCharm + ESP8266")
  

## How to build
```bash
pip install -r requirements.txt
```  

## How to configure
In order to set up this project you will need to open the config.py file at the root of the project and make the appropriate changes:
```python
NETWORK_SSID = "stringnetwork name"
NETWORK_PASSWORD = "network password"
MAX_CONNECTION_RETRY_ATTEMPTS = number of connection retry attempts

PUBLISH_TIME_SEC = seconds between pubish attempts
SUBSCRIBE_CHECK_PERIOD_SEC = second between subscription checks
DEVICE_ID = "guid to identify the device"

ADAFRUIT_IO_URL = b'io.adafruit.com'
ADAFRUIT_USERNAME = b'adafruit username'
ADAFRUIT_IO_KEY = b'adafruit io key'
ADAIO_PubFD_1 = b'GC_FreeMemory'
ADAIO_PubFD_2 = b'Water Temp Deg C'
ADAIO_PubFD_3 = b'Outdoor Temp Deg C'
ADAIO_PubFD_4 = b'Outdoor Relative Humidity'
ADAIO_SubFD_1 = b'blue-led-control'
```

## How to run
```bash
python main.py
```