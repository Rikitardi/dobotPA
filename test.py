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
vacum = False

def sendpose():
    getpose = mainset.run()
    # getpose1 = str(getpose)
    getpose1 = format('K:%s:%s:%s:%s:%s:%s:%s:%s' % (getpose[1],getpose[2],getpose[3],getpose[4],getpose[5],getpose[6],getpose[7],getpose[8]))
    getpose2 = getpose1.encode()
    # conn.sendall(getpose2)
    return getpose

pose = False

def stick():
    vacum = False
    while True:
        print("---")
        print("awal")
        flag = True
        control = joystick()
        print("jalan")
        if control == 'LXu':
            mmove.move("J1P1",1)
            pose = True
            global pose
            print("ini nih")
        elif control == 'LXd':
            mmove.move("J1M1",1)
            pose = True
            global pose
        elif control == 'LYu':
            mmove.move("J2P1",1)
            pose = True
            global pose
        elif control == 'LYd':
            mmove.move("J2M1",1)
            pose = True
            global pose
        elif control == 'RYd':
            mmove.move("J3P1",1)
            pose = True
            global pose
        elif control == 'RYu':
            mmove.move("J3M1",1)
            pose = True
            global pose
        elif control == 'RXu':
            mmove.move("J4P1",1)
            pose = True
            global pose
        elif control == 'RXd':
            mmove.move("J4M1",1)
            pose = True
            global pose
        elif control == 'LYc' or control == 'LXc' or control == 'RYc' or control == 'RXc':
            mmove.move("J1P0",1)
            pose = True
            global pose
        elif control == '3':
            if vacum == False:
                mmove.move("Von",1)
                vacum = True
            elif vacum == True:
                mmove.move("Vof",1)
                vacum = False
        print("ujung")

stick()