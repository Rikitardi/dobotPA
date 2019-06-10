#--------Library Bawaan--------#
from time import sleep
from glob import glob
from threading import Thread
from multiprocessing import Process
import socket
import select, errno,sys

#--------Library Buatan--------#
sys.path.append('../')
from pydobot.dobot import Dobot
from pydobot.PTP import PTP
from pydobot.JOG import JOG

#--------Config Port--------#
class setport():
    port1 = True
    def __init__(self, debug = False):
        self.debug = debug
        self.available_ports = glob('/dev/ttyUSB0')  # mask for OSX Dobot port
        if len(self.available_ports) == 0:
            self.available_ports = glob('/dev/ttyUSB1')
            if len(self.available_ports) == 0:
                self.available_ports = glob('/dev/ttyUSB2')
                if len(self.available_ports) == 0:
                    self.available_ports = glob('/dev/ttyUSB3')
                    if len(self.available_ports) == 0:
                        print('no port found for Dobot Magician')
                        exit(1)
    def mainset(self):
        self.main = Dobot(port = self.available_ports[0] )
        return self.main
    def jog(self):
        self.jog = JOG(port = self.available_ports[0])
        return self.jog
    def m_port(self):
        self.m_port = self.available_ports[0]
        return self.m_port

class setsocket():
    def __init__(self,ip_server,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ip_server = ip_server
        self.port = port
        self.server_address=(self.ip_server,self.port)
        self.sock.bind(self.server_address)
        self.sock.listen(1)
    def socked(self):
        self.sock1 = self.sock
        return(self.sock1)

    # def koneksi(self):
    #     print('starting server (host: {},port: {})'.format(self.ip_server, self.port))
    #     print("Waiting Connection")
    #     self.conn, self.client_address = self.sock.accept()
    #     print('Connected with : {}'.format(self.client_address))
    #     return self.conn

    def close(self):
        self.sock.close

if __name__ == "__main__":
    #ip_server = '192.168.43.190'
    #port = 5035
    #setsocket = setsocket(ip_server,port)
    #koneksi = setsocket.koneksi()

    setport = setport()
    main = setport.main()
    print(main.run())
