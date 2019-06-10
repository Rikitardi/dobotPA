#--------Library Bawaan--------#
from time import sleep
from glob import glob
from threading import Thread
import socket
import select, errno,sys

#--------Library Buatan--------#
sys.path.append('../')
from Lib.riset import setport
from pydobot.dobot import Dobot
from pydobot.JOG import JOG

setport = setport()
mainset = setport.mainset()

class manualmove():
    def __init__(self, available_ports):
        self.available_ports = available_ports
        print(self.available_ports)
        self.JogFunc=JOG(self.available_ports)
        self.Vac = Dobot(self.available_ports)

    def fungsi(self, fungsi1, aktive = 1):        
        self.fungsi1 = fungsi1
        self.aktive = aktive
        if self.fungsi1.find("REMOVE") != -1:
            self.remove = self.fungsi1.split()
            return self.remove
            print(self.fungsi1)
        if self.fungsi1 == "TEACH" :
            return "TEACH"
            print(self.fungsi1)
        if self.fungsi1 == "T_RECORD " :
            return "RECORD"
            print(self.fungsi1)
        if self.fungsi1 == "T_BATAL" :
            return "BATAL"
            print(self.fungsi1)
        if self.fungsi1 == "T_DELETE" :
            return "DELETE"
            print(self.fungsi1)
        if self.fungsi1 == "A_PAUSE" :
            return "PAUSE"
            self.JogFunc.idle()            
            print(self.fungsi1)
        if self.fungsi1.find("STR") != -1:
            self.start = self.fungsi1.split()
            return self.start
            print(self.fungsi1)
        if self.fungsi1 == "A_STOP" :
            return "STOP"
            print(self.fungsi1)
        if self.fungsi1 == "A_RESET" :
            return "RESET"
            print(self.fungsi1)
        if self.fungsi1 == "A_CANCEL" :
            return "CANCEL"
            print(self.fungsi1)
        if self.fungsi1 == "B_SPEED" :
            return "SPEED"
            print(self.fungsi1)
        if self.fungsi1 == "S_EMG" :
            return "EMG"
            print(self.fungsi1)
        if self.fungsi1 == "S_RESET" :
            return "RESET"
            print(self.fungsi1)
        if self.fungsi1 == "S_Homepos" :
            return "Homepos"
            print(self.fungsi1)
        if self.fungsi1 == "EXIT" :
            return "EXIT"
            print(self.fungsi1)
        if self.fungsi1 == "T_BATAL" :
            return "BATAL"
            print(self.fungsi1)
    def move(self, data2, aktive):
        self.data2 = data2
        self.aktive = aktive
        if self.data2.find("SPEEDM") != -1:
            self.speed = self.data2.split()
            self.velo = self.speed[1]
            self.JogFunc.jspeed(float(self.velo),50)
        if self.data2 == "J1P1" :
            if self.aktive == 1:
                print(data2)
            self.JogFunc.joint1pos()
        elif self.data2 == "J1M1":
            if self.aktive == 1:
                print(data2)
            self.JogFunc.joint1min()
        elif self.data2 == "J2P1":
            if self.aktive == 1:
                print(data2)
            self.JogFunc.joint2pos()            
        elif self.data2 == "J2M1":
            if self.aktive == 1:
                print(data2)
            self.JogFunc.joint2min()
        elif self.data2 == "J3P1":
            if self.aktive == 1:
                print(data2)
            self.JogFunc.joint3pos()
        elif self.data2 == "J3M1":
            if self.aktive == 1:
                print(data2)
            self.JogFunc.joint3min()
        elif self.data2 == "J4P1":
            if self.aktive == 1:
                print(data2)
            self.JogFunc.joint4pos()
        elif self.data2 == "J4M1":
            if self.aktive == 1:
                print(data2)
            self.JogFunc.joint4min()
        elif self.data2 == "J1P0" or self.data2 == "J1M0" or self.data2 == "J2P0" or self.data2 == "J2M0" or self.data2 == "J3P0" or self.data2 == "J3M0" or self.data2 == "J4P0" or self.data2 == "J4M0":
            if self.aktive == 1:
                print(data2)
            self.JogFunc.jspeed(2,1)
            self.JogFunc.idle()
            self.JogFunc.jspeed(float(self.velo),50)
        elif self.data2 == "Von":
            if self.aktive == 1:
                print(data2)
            self.Vac.suck(True)
        elif self.data2 == "Vof":
            if self.aktive == 1:
                print(data2)
            self.Vac.suck(False)

if __name__ == "__main__":
    setport = setport()
    port_available = setport.m_port()
    manualmove = manualmove(port_available)
    manualmove.move("J1P1")