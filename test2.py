#--------Library Bawaan--------#
from time import sleep
from glob import glob
from threading import Thread
import socket
import select, errno,sys

#--------Library Buatan--------#
from Lib.riset import setport,setsocket
from Lib.manual_move import manualmove
from Lib.joystick import joystick
from pydobot import Dobot
from pydobot.dobot import Dobot
from pydobot.JOG import JOG
from pydobot.PTP import PTP


#-----------Set Port-----------#
setport = setport()
mainset = setport.mainset()
jog = setport.jog()
mport = setport.m_port()
mmove = manualmove(mport)
PTP = PTP(mport)
# control = joystick()
vacum = False

print("aaaaaa")

while True:
    print("sebelum")
    control = joystick()
    print("jalan")
    if control == 'LXu':
        mmove.move("J1P1",1)
    elif control == 'LXd':
        mmove.move("J1M1",1)
    elif control == 'LYu':
        mmove.move("J2P1",1)
    elif control == 'LYd':
        mmove.move("J2M1",1)
    elif control == 'RYd':
        mmove.move("J3P1",1)
    elif control == 'RYu':
        mmove.move("J3M1",1)
    elif control == 'RXu':
        mmove.move("J4P1",1)
    elif control == 'RXd':
        mmove.move("J4M1",1)
    elif control == 'LYc' or control == 'LXc' or control == 'RYc' or control == 'RXc':
        mmove.move("J1P0",1)
    elif control == '3':
        if vacum == False:
            mmove.move("Von",1)
            vacum = True
        elif vacum == True:
            mmove.move("Vof",1)
            vacum = False
