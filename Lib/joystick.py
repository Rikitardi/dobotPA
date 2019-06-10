#import evdev
from select import select
from glob import glob
from evdev import InputDevice, categorize, ecodes
from Lib.riset import setport,setsocket

#-----------Set Port-----------#
setport = setport()
mainset = setport.mainset()

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
    #cree un objet gamepad | creates object gamepad
    #affiche la liste des device connectes | prints out device info at start
    # print(gamepad)
    print("init")
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
        print("aneh")
        #Boutons | buttons 
        if event.type == ecodes.EV_KEY:
            #print(event)
            if event.value == 1:
                if event.code == Btn1:
                    perintah = '1'
                    print(perintah)
                    return perintah
                elif event.code == Btn2:
                    perintah = '2'
                    print(perintah)
                    return perintah
                elif event.code == Btn3:
                    perintah = '3'
                    print(perintah)
                    return perintah
                elif event.code == Btn4:
                    perintah = '4'
                    print(perintah)
                    return perintah
                elif event.code == Btn5:
                    perintah = '5'
                    print(perintah)
                    return perintah
                elif event.code == Btn6:
                    perintah = '6'
                    print(perintah)
                    return perintah
                elif event.code == BtnL1:
                    perintah = 'L1'
                    print(perintah)
                    return perintah
                elif event.code == BtnR1:
                    perintah = 'R1'
                    print(perintah)
                    return perintah
                elif event.code == BtnL2:
                    perintah = 'L2'
                    print(perintah)
                    return perintah
                elif event.code == BtnR2:
                    perintah = 'R2'
                    print(perintah)
                    return perintah
                elif event.code == BtnL3:
                    perintah = 'L3'
                    print(perintah)
                    return perintah
                elif event.code == BtnR3:
                    perintah = 'R3'
                    print(perintah)
                    return perintah
            elif event.value == 0:
                perintah = '0'
                print(perintah)
                return perintah
        #Gamepad analogique | Analog gamepad
        if event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            print("langkah 1")
            #print ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value
            if ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_X":
                print("langkah 2")
                if absevent.event.value == 0:
                    perintah = 'LXu'
                    print("si goblog")
                    print(perintah)
                    return perintah
                elif absevent.event.value == 255:
                    perintah = 'LXd'
                    print("si kehed")
                    print(perintah)
                    return perintah
                elif absevent.event.value == 128:
                    perintah = 'LXc'
                    print(perintah)
                    return perintah
            elif ecodes.bytype[absevent.event.type][absevent.event.code] == "ABS_Y":
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
        print("akhir aneh")
        print(event)
        print(gamepad.read_loop())
    print("paling akhir")
# test()
# while True:
#     joystick()    