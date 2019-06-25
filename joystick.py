#import evdev
from select import select
from glob import glob
from evdev import InputDevice, categorize, ecodes
from Lib.riset import setport,setsocket
from multiprocessing import Value
import multiprocessing as mp
import threading
import queue
from time import sleep
from ctypes import c_char

jsvalue = mp.Value('i', 0)


#-----------Set Port-----------#
# setport = setport()
# mainset = setport.mainset()

#---------gamepad Port---------#
global gamepad
joys = glob('/dev/input/event0')
if len(joys) == 0:
    print("joystick not found")
    exit(1)

gamepad = InputDevice('/dev/input/event0')

#-----------Fungsi -----------#
def test():
    nilai = 0
    while nilai == 0 :
        r,w,x = select([gamepad], [], [])
        for event in gamepad.read():
            if event.type == ecodes.EV_ABS:
                absevent = categorize(event)
                if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_X":
                    print('nilai :%i'%(event.type))
                    if event.value == 1:
                        print("break")
                        nilai = 1
    print("finish")
def sendpose():
    getpose = mainset.run()
    # getpose1 = str(getpose)
    getpose1 = format('K:%s:%s:%s:%s:%s:%s:%s:%s' % (getpose[1],getpose[2],getpose[3],getpose[4],getpose[5],getpose[6],getpose[7],getpose[8]))
    getpose2 = getpose1.encode()
    # conn.sendall(getpose2)
    return getpose1
def joystick():
    while True:
        print("hublad")
        #cree un objet gamepad | creates object gamepad
        #affiche la liste des device connectes | prints out device info at start
        # print(gamepad)
        # print("init")
        Btn1 = 288
        Btn2 = 289
        Btn3 = 290
        Btn4 = 291
        Btn5 = 292
        Btn6 = 293
        BtnL1 = 294
        BtnR1 = 295
        BtnL2 = 296
        BtnR2 = 297
        BtnL3 = 298
        BtnR3 = 299

        for event in gamepad.read_loop():
            # print("aneh")
            #Boutons | buttons 
            if event.type == ecodes.EV_KEY:
                #print(event)
                if event.value == 1:
                    if event.code == Btn1:
                        perintah = 1
                        jsvalue.value =  perintah
                        break
                    elif event.code == Btn2:
                        perintah = 2
                        jsvalue.value =  perintah
                    elif event.code == Btn3:
                        perintah = 3
                        jsvalue.value =  perintah
                    elif event.code == Btn4:
                        perintah = 4
                        jsvalue.value =  perintah
                elif event.value == 0:
                    perintah = 0
                    jsvalue.value =  perintah

            #Gamepad analogique | Analog gamepad
            if event.type == ecodes.EV_ABS:
                absevent = categorize(event)
                # print("langkah 1")
                # print(ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value)
                if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_HAT0X":
                    # print("langkah 2")
                    if absevent.event.value == -1:
                        perintah = 'kiri'
                        print(perintah)
                        return perintah
                    elif absevent.event.value == 0:
                        perintah = 'henti'
                        print(perintah)
                        return perintah
                    elif absevent.event.value == 1:
                        perintah = 'kanan'
                        print(perintah)
                        return perintah
                elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_HAT0Y":
                    if absevent.event.value == 0:
                        perintah = 'LYu'
                        print(perintah)
                        return perintah
                    elif absevent.event.value == 255:
                        perintah = 'LYd'
                        print(perintah)
                        return perintah
                    elif absevent.event.value == 128:
                        perintah = 'LYc'
                        print(perintah)
                        return perintah
                elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_RX":
                    if absevent.event.value == 0:
                        perintah = 'RXu'
                        print(perintah)
                        return perintah
                    elif absevent.event.value == 255:
                        perintah = 'RXd'
                        print(perintah)
                        return perintah
                    elif absevent.event.value == 128:
                        perintah = 'RXc'
                        print(perintah)
                        return perintah
                elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_RZ":
                    if absevent.event.value == 0:
                        perintah = 'RYu'
                        print(perintah)
                        return perintah
                    elif absevent.event.value == 255:
                        perintah = 'RYd'
                        print(perintah)
                        return perintah
                    elif absevent.event.value == 128:
                        perintah = 'RYc'
                        print(perintah)
                        return perintah
            # print("akhir aneh")
            # print(event)
            # print(gamepad.read_loop())
        # print("paling akhir")


js = mp.Process(target = joystick)
js.start()

def counter():
    for i in(range(5)):
        print(i)
        sleep(2)
while True:
    counter()
    if jsvalue.value == 1:
        print(jsvalue.value)
        print("ini satu")
    if jsvalue.value == 0:
        print(jsvalue.value)
        print("hello world")
