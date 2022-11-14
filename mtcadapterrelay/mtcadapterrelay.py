# Prerequisites:
# python3 -m pip install pyserial

import serial
import socket
import socketserver
import getpass


class ImproperlyConfigured(Exception):
    """ Something is improperly configured """
    pass


class MTCAdapterRelayHandler(socketserver.BaseRequestHandler):
    """
    Reads SHDR data from a device via the serial port and forwards them to the MTConnect Agent
    """
   
    serial_port = None
    baudrate = 115200
    parity = serial.PARITY_NONE
    bytesize = serial.EIGHTBITS
    stopbits = serial.STOPBITS_ONE
    ser_timeout = 100
    
    
    def __init__(self, request, client_address, server):
        """ Constructor """
        socketserver.BaseRequestHandler.__init__(self, request, client_address, server)
        # Configuration validations
        if self.serial_port == None:
            raise ImproperlyConfigured("MTCAdapterRelay requires the attribute 'serial_port' to be defined")
        self.ser = self.openSerialCom()
        
        
    def handle(self):
        """ Handles connection from MTConnect Agent """
        print("Connection from {}".format(self.client_address[0]))
        # sends logged user to agent 
        self.request.sendall(("|operator|" + getpass.getuser() + "\n").encode())
        self.request.settimeout(0.01)
        if self.serial_port == None:
            raise ImproperlyConfigured("MTCAdapterRelay requires the attribute 'serial_port' to be defined")
        ser = self.openSerialCom()
        while 1:
            try:
                data = self.request.recv(1024)
            except socket.timeout:
                if ser.inWaiting() > 0:
                    # strip possible "\n"
                    shdr = ser.readline().decode('utf-8').strip()
                    self.sendSHDR(shdr)
                    self.request.sendall((shdr+"\n").encode())
                continue
                
            if not data:
                print("Connection from Agent closed")
                break
            
            if data == "* PING\r\n".encode():
                self.request.sendall("* PONG 60000\n".encode())
            
            
    def openSerialCom(self):
        """ Opens communication with device """
        ser = serial.Serial(self.serial_port)
        ser.baudrate = self.baudrate
        ser.parity = self.parity
        ser.bytesize = self.bytesize
        ser.stopbits = self.stopbits
        ser.timeout = self.ser_timeout
        return ser
    
    
    def sendSHDR(self, shdr):
        """ Sends SHDR to MTConnect agent """
        print(shdr)
        

class MTCAdapterRelay(socketserver.TCPServer):
    """
    Implements a MTConnect Adapter server
    Reads SHDR data from serial port defined in deviceHandler_class
    """
    
    adapter_port = 7880
    deviceHandler_class = None
   
    
    def __init__(self):
        """ Constructor """
        # Configuration validations
        if self.deviceHandler_class == None:
            raise ImproperlyConfigured("MTCAdapterRelay requires the attribute 'deviceHandler_class' to be defined")
        
        socketserver.TCPServer.__init__(self, ('', self.adapter_port), self.deviceHandler_class)