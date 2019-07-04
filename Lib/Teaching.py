#--------Library Bawaan--------#
import socket
from time import sleep
import socket
import select, errno,sys

#--------Library Buatan--------#
from riset import setport,setsocket
from manual_move import manualmove
sys.path.append('../')
from pydobot import Dobot
from pydobot.PTP import PTP
from pydobot.JOG import JOG

def setsock():
    ip_server = '192.168.43.190'
    port = 5039
    global setsocket
    setsocket = setsocket(ip_server,port)
    conn = setsocket.koneksi()
    return conn

# setsock()
# port = setport.m_port()
setport = setport()
jog = setport.jog()
main = setport.main()

getpose = main.run()

joint1 = float(getpose[1])
joint2 = float(getpose[2])
joint3 = float(getpose[3])
joint4 = float(getpose[4])

temp_j1 = []
temp_j2 = []
temp_j3 = []
temp_j4 = []
urutan = []

home1 = 0.0
home2 = 0.0
home3 = 0.0
home4 = 0.0

flag = 0
flag1 = 0
henti1 = 0
henti2 = 0
henti3 = 0
henti4 = 0

v = 100
a = 100
v1 = 10
a1 = 5
tapak = 0
x = 1

while True:
    getpose = main.run()
    joint1 = float(getpose[1])
    joint2 = float(getpose[2])
    joint3 = float(getpose[3])
    joint4 = float(getpose[4])
    sleep(1)
    flag=1

    Masuk = input("Perintah :")
    if Masuk == "bof":
        main.suck(False)
        if flag1 == 1:
            urutan.append("bof")
            temp_j1.append('')
            temp_j2.append('')
            temp_j3.append('')
            temp_j4.append('')
    if Masuk == "bon":
        main.suck(True)
        if flag1 == 1:
            urutan.append("bon")
            temp_j1.append('')
            temp_j2.append('')
            temp_j3.append('')
            temp_j4.append('')
    if Masuk == "d":
        temp_j1.clear()
        temp_j2.clear()
        temp_j3.clear()
        temp_j4.clear()
        urutan.clear()

        home1 = 0.0
        home2 = 0.0
        home3 = 0.0
        home4 = 0.0
    if Masuk == "u":
        print(joint1)
        print(joint2)
        print(joint3)
        print(joint4)
    if Masuk == "c":
        print(temp_j1)
        print(temp_j2)
        print(temp_j3)
        print(temp_j4)
        print(urutan)
    if Masuk == "j2-":
        jog.jspeed(20, 10)
        jog.joint2min()
        if flag1 == 1:
            urutan.append("j2-")
    if Masuk == "j2+":
        jog.jspeed(20, 10)
        jog.joint2pos()
        if flag1 == 1:
            urutan.append("j2+")
    if Masuk == "j+":
        jog.jspeed(v, a)
        jog.joint1pos()
        if flag1 == 1:
            urutan.append("j+")
    if Masuk == "j-":
        jog.jspeed(v, a)
        jog.joint1min()
        if flag1 == 1:
            urutan.append("j-")
    if Masuk == "s":
        jog.idle()
        if flag1 == 1:
            getpose = main.run()
            joint1 = float(getpose[1])
            joint2 = float(getpose[2])
            joint3 = float(getpose[3])
            joint4 = float(getpose[4])
            temp_j1.append(joint1)
            temp_j2.append(joint2)
            temp_j3.append(joint3)
            temp_j4.append(joint4)
    if Masuk == "h":
        home1 = joint1
        home2 = joint2
        home3 = joint3
        home4 = joint4
        flag = 1
        flag1 = 1
    if Masuk == "ch":
        print(home1)
        print(home2)
        print(home3)
        print(home4)
    if Masuk == "g" and flag == 1:
        pengulangan = input("pengulangan :")
        print("percobaan")
        print('home:{}'.format(home1))
        p = len(urutan)
        i=0
        # print('flag henti1: {}'.format(henti1))
        # print('flag henti2: {}'.format(henti2))

#------------------joint 1--------------------#
        while True: 
            if joint1 > home1 and henti1 == 0:
                jog.jspeed(v, a)
                jog.joint1min()
                while True:
                    getpose = main.run()
                    joint1 = float(getpose[1])
                    print('{}'.format(joint1))
                    if joint1 <= home1:
                        # print("j1>home joint1 == home1")
                        jog.jspeed(0.001, 10)
                        jog.idle()
                        v = v/5
                        a = a/5
                        ketelitian1 = home1 - 0.1
                        ketelitian1 = '{:03.2f}'.format(ketelitian1)
                        print('ketelitian1:{}'.format(ketelitian1))
                        if joint1 > float(ketelitian1) :
                            print("henti1")
                            henti1 = 1
                        print('henti1 : {}'.format(henti1))
                        break
            if joint1 < home1 and henti2 == 0:
                jog.jspeed(v,a)
                jog.joint1pos()
                while True:
                    getpose = main.run()
                    joint1 = float(getpose[1])
                    print('{}'.format(joint1))
                    if joint1 > home1 :
                        # print("j1<home joint1 == home1")
                        jog.jspeed(0.001, 10)
                        jog.idle()
                        v = v/5
                        a = v/5
                        ketelitian2 = home1 + 0.1
                        ketelitian2 = '{:03.2f}'.format(ketelitian2)
                        print('ketelitian2:{}'.format(ketelitian2))
                        if joint1 < float(ketelitian2):
                            print("henti2")
                            henti2 = 1
                        print('henti2:{}'.format(henti2))
                        break
            if joint1 == home1:
                    jog.jspeed(0.001, 10)
                    jog.idle()
                    henti1 = 1
                    henti2 = 1
            if henti1 == 1 and henti2 ==1:
                tapak = 1
                break
#------------------joint 2--------------------#

        while True: 
            sleep(1)
            if joint2 > home2 and henti3 == 0:
                jog.jspeed(v1, a1)
                jog.joint2min()
                while True:
                    getpose = main.run()
                    joint2 = float(getpose[2])
                    print('{}'.format(joint2))
                    if joint2 <= home2:
                        # print("j1>home joint1 == home1")
                        jog.jspeed(0.001, 10)
                        jog.idle()
                        v1 = v1/5
                        a1 = a1/5
                        ketelitian1 = home2 - 0.1
                        ketelitian1 = '{:03.2f}'.format(ketelitian1)
                        print('ketelitian1:{}'.format(ketelitian1))
                        if joint2 > float(ketelitian1) :
                            print("henti3")
                            henti3 = 1
                        print('henti3 : {}'.format(henti3))
                        break
            if joint2 < home2 and henti4 == 0:
                jog.jspeed(v1,a1)
                jog.joint2pos()
                while True:
                    getpose = main.run()
                    joint2 = float(getpose[2])
                    print('{}'.format(joint2))
                    if joint2 > home2 :
                        # print("j1<home joint1 == home1")
                        jog.jspeed(0.001, 10)
                        jog.idle()
                        v1 = v1/5
                        a1 = v1/5
                        ketelitian2 = home2 + 0.1
                        ketelitian2 = '{:03.2f}'.format(ketelitian2)
                        print('ketelitian2:{}'.format(ketelitian2))
                        if joint2 < float(ketelitian2):
                            print("hent4i")
                            henti4 = 1
                        print('henti4:{}'.format(henti4))
                        break
                    sleep(1)    
            if joint2 == home2:
                    jog.jspeed(0.001, 10)
                    jog.idle()
                    henti3 = 1
                    henti4 = 1
            if henti3 == 1 and henti4 ==1:
                tapak = 1
                break
#------------------set--------------------#
        main.suck(False)
        v1 =10
        a1 =1
        v = 10
        a = 1
        henti1 = 0
        henti2 = 0
        henti3 = 0
        henti4 = 0
        print('selesai')   
        sleep(1)
#------------------auto---------------------#
        for x in range(int(pengulangan)):
            for i in range(len(urutan)):
                if urutan[i] == "bof":
                    main.suck(False)
                    print("bof")
                if urutan[i] == "bon":
                    main.suck(True)
                    print("bon")
                if urutan[i] == "j-" and temp_j1[i] != '' :
                    jog.jspeed(20, 20)
                    jog.joint1min()
                    print("j-")
                    while True:
                        getpose = main.run()
                        joint1 = float(getpose[1])
                        joint2 = float(getpose[2])
                        joint3 = float(getpose[3])
                        joint4 = float(getpose[4])
                        print(joint1)
                        if joint1 <= temp_j1[i]:
                            jog.jspeed(0.1, 1)
                            jog.idle()
                            break
                if urutan[i] == "j+" and temp_j1[i] != '' :
                    jog.jspeed(20, 20)
                    jog.joint1pos()
                    print("j+")
                    while True:
                        getpose = main.run()
                        joint1 = float(getpose[1])
                        joint2 = float(getpose[2])
                        joint3 = float(getpose[3])
                        joint4 = float(getpose[4])
                        print(joint1)
                        if joint1 >= temp_j1[i]:
                            jog.jspeed(0.1, 1)
                            jog.idle()
                            break
                if urutan[i] == "j2+" and temp_j2[i] != '' :
                    jog.jspeed(20, 10)
                    jog.joint2pos()
                    print("j2+")
                    while True:
                        getpose = main.run()
                        joint1 = float(getpose[1])
                        joint2 = float(getpose[2])
                        joint3 = float(getpose[3])
                        joint4 = float(getpose[4])
                        print(joint2)
                        if joint2 >= temp_j2[i]:
                            jog.jspeed(0.1, 1)
                            jog.idle()
                            break
                if urutan[i] == "j2-" and temp_j2[i] != '' :
                    jog.jspeed(20, 10)
                    jog.joint2min()
                    print("j2-")
                    while True:
                        getpose = main.run()
                        joint1 = float(getpose[1])
                        joint2 = float(getpose[2])
                        joint3 = float(getpose[3])
                        joint4 = float(getpose[4])
                        print(joint2)
                        if joint2 <= temp_j2[i]:
                            jog.jspeed(0.1, 1)
                            jog.idle()
                            break

        flag = 0
        flag1= 0