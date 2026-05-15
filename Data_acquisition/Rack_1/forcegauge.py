# Import libraries
import time
import numpy as np
import serial
import pymodbus.client as ModbusClient
from pymodbus import (
    ExceptionResponse,
    Framer,
    ModbusException,
    pymodbus_apply_logging_config,
)

class Torbal:
    MAX_FORCE = 9

    def __init__(self, port):
        self.comport = serial.Serial(port, baudrate=9600, timeout=10) # Doesn't work at 115200 baud.
        print("Opened Torbal com port: ", port)

    def force(self):
        resp = self.read_force()
        self.f = float(resp[2:10])
        self.units = chr(resp[12])
        return self.f
    
    def read_force(self):
        self.comport.reset_input_buffer() # clear input buffer
        #written = self.comport.write(b"SI\r\n") # command string to query Torbal FB10
        written = self.comport.write(b"Sx1\r\n") # command string to query Torbal FB10 WITHOUT STABILITY SETTING!
        #print("Bytes out: written {:}, waiting {:}".format(written, self.comport.out_waiting))
        self.comport.flush() # wait until all of the command string is written
        #print("Bytes post flush waiting {:}".format(self.comport.out_waiting))
        #i = 0
        #bytes = 0
        #timein = time.time_ns()
        str = self.comport.readline(16)

        # while bytes < 16: 
        #     time.sleep(0.05)
        #     bytes = self.comport.in_waiting
        #     print("Bytes Rcv: ", bytes)
        #     #print("Loop index is: %i", i)
        #     #i = i+1
        #timeout = time.time_ns()
        #print("Read time: {:.0f} ms".format((timeout-timein)/1e6))
        #return  self.comport.read_all()
        return str
    
    def check_bounds(self, f):
        if np.abs(f) > self.MAX_FORCE:
            return True
        else:
            return False

    def close_port(self):
        self.comport.close()
        #print("Closed")
        #time.sleep(2)
        print("Closed Torbal com port: ", self.comport.port)
    
    
class MXmoonfree:

    def __init__(self, port):
        framer = Framer.RTU
        self.slave = 1
        self.client = ModbusClient.ModbusSerialClient(
                    port,
                    framer=framer,
                    # timeout=10,
                    # retries=3,
                    # retry_on_empty=False,
                    # strict=True,
                    baudrate=9600,
                    bytesize=8,
                    parity="N",
                    stopbits=1,
                    # handle_local_echo=False,
                )
        self.client.connect()
    
    def force(self):
        devresp = self.readHoldingRegisters(0, 2)
        time.sleep(0.2)
        return self.IEEE754_to_float(devresp)
    
    def upperLimit(self):
        devresp = self.readHoldingRegisters(2, 2)
        self.upperLimit = self.IEEE754_to_float(devresp)
        return self.upperLimit
    
    def lowerLimit(self):
        devresp = self.readHoldingRegisters(4, 2)
        self.lowerLimit = self.IEEE754_to_float(devresp)
        return self.lowerLimit
    
    def comparisonValue(self):
        devresp = self.readHoldingRegisters(6, 2)
        self.comparisonValue = self.IEEE754_to_float(devresp)
        return self.comparisonValue
    
    def G(self):
        devresp = self.readHoldingRegisters(8, 2)
        self.gravity = self.IEEE754_to_float(devresp)
        return self.gravity
    
    def range(self):
        devresp = self.readHoldingRegisters(10, 1)
        self.range = devresp.registers[0]
        return self.range
    
    def printHoldingRegisters(self):
        devresp = self.readHoldingRegisters(0, 13)
        #print("Holding registers (0-12) = ", devresp.registers)
        print("Holding registers (0-12) = ",[hex(x) for x in devresp.registers]) # In hex
        
    def readHoldingRegisters(self, address, count):
        devresp = self.client.read_holding_registers(address=address, count=count, slave=self.slave)
        return devresp
    
    def IEEE754_to_float(self, devresp):
        msw = devresp.registers[0]
        lsw = devresp.registers[1]
        x = (msw << 16) + lsw
        # print(hex(msw), hex(lsw), hex(x))
        return IEEE754_to_f32(x)
        
    def connect(self):
        self.client.connect()
        
    def close(self):
        self.client.close()

# IEEE754 to float32 conversion using numpy.    
IEEE754_to_f32 = lambda i:np.uint32(i).view("f4")