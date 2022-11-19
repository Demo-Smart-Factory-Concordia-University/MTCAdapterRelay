# MTCAdapterRelay
MTConnect Adapter acting as a relay for a physical device (e.g. a sensor) sending SHDR data on the serial port.

The MTCAdapterReay allows to hock up a device capable of sending SHDR data on the serial port but
not capable of sending TCP/IP data to an MTConnect Agent.

The MTCAdapterRelay is a small Python library desinged to work together with the [MTConnect cpp agent](https://github.com/mtconnect/cppagent).

## Usage
Two classes need to be define: an MTCAdapterRelayHandler class and a MTCAdapterRelay.

### MTCAdapterRelayHandler
The MTCAdapterRelayHandler is responsible to define the proper parameters for communicating with the
device over the serial port.

At minimum the 'serial_port' attribute must be defined. It is the name of the Linux device file
to access the serial port (e.g. `/dev/ttyUSB1`).

Further the following attributes may have to be redfined to match the configuration of the used serial port:
```
baudrate = 115200
parity = serial.PARITY_NONE
bytesize = serial.EIGHTBITS
stopbits = serial.STOPBITS_ONE
```

### MTCAdapterRelay
The MTCAdapterRelay is a specialized TCP/IP server which implements the PING/PONG hearthbeat convention of 
the [MTConnect cpp agent](https://github.com/mtconnect/cppagent).

The attribute `adapter_port` (default value 7878) holds the port number on which the adapter relay will run.

The attribute `deviceHandler_class` must contain the MTCAdapterRelayHandler class defining the correct
serial port paramters to communicate with the device.

### Example
A typical example looks like this 
(this is an example for a temperature sensor connected via an Arduino type device.
The Arduino sketch is availble [here](/arduino)):
```
from mtcadapterrelay import MTCAdapterRelay, MTCAdapterRelayHandler
import sys


class DS18B20_MTCAdapterRelayHandler(MTCAdapterRelayHandler):
    
    serial_port = '/dev/ttyUSB1'
    baudrate = 115200
    parity = serial.PARITY_NONE
    bytesize = serial.EIGHTBITS
    stopbits = serial.STOPBITS_ONE


class DS18B20_MTCAdapterRelay(MTCAdapterRelay):
    
    adapter_port = 8881
    deviceHandler_class = DS18B20_MTCAdapterRelayHandler

    
myServer = DS18B20_MTCAdapterRelay()
try:
    myServer.serve_forever()
except KeyboardInterrupt:
    sys.exit(0)
```
