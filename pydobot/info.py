import struct
import time
import serial

from pydobot.dobot import Dobot
from pydobot.message import Message

class info(Dobot):
    def __init__(self, port, verbose=True):
        Dobot.__init__(self, port, verbose=True)
        
    def devicesn(self):
        msg = Message()
        msg.id = 0
        msg.ctrl = 0x00
        response = self._send_command(msg)
        self.ret = struct.unpack_from('char', response.params)
        if self.verbose:
            print("pydobot: " % self.ret)
        return response
    
    def devicename(self):
        msg = Message()
        msg.id = 1
        msg.ctrl = 0x00
        return self._send_command(msg)
    
    def devicever(self):
        msg = Message()
        msg.id = 2
        msg.ctrl = 0x00
        return self._send_command(msg)
    
    def devicewithl(self):
        msg = Message()
        msg.id = 3
        msg.ctrl = 0x00
        return self._send_command(msg)

    def deviceid(self):
        msg = Message()
        msg.id = 4
        msg.ctrl = 0x00
        return self._send_command(msg)
    
    def alarm_status(self):
        msg = Message()
        msg.id = 3
        msg.ctrl = 0x00
        return self._send_command(msg)
    
    def GetAngleSensorStaticError(self):
        msg = Message()
        msg.id = 140
        msg.ctrl = 0x00
        return self._send_command(msg)
    
    
