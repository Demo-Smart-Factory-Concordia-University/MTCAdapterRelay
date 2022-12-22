from mtcadapterrelay import MTCAdapterRelay, MTCAdapterRelayHandler
import sys


class DS18B20_MTCAdapterRelayHandler(MTCAdapterRelayHandler):
    """
    Serial port connection paramters
    """
    
    serial_port = '/dev/ttyUSB1'


class DS18B20_MTCAdapterRelay(MTCAdapterRelay):
    """
    MTConnect adapter serving as a relay to a device connected
    on the serial port handeld by DS18B20_MTCAdapterRelayHandler
    """
    
    adapter_port = 8881
    deviceHandler_class = DS18B20_MTCAdapterRelayHandler


myAdapter = DS18B20_MTCAdapterRelay()
try:
    myAdapter.serve_forever()
except KeyboardInterrupt:
    sys.exit(0)
