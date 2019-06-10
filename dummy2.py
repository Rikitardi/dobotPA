#--------Library Bawaan--------#
from time import sleep
from glob import glob
from threading import Thread
import socket
import select, errno,sys

#--------Library Buatan--------#
from Lib.riset import setport,setsocket
from Lib.manual_move import manualmove
from pydobot import Dobot
from pydobot.dobot import Dobot
from pydobot.JOG import JOG
from pydobot.PTP import PTP
#from test import stick

#----------Variable Global---------#

global conn
global mmove

#---------Variable Teach-----------#

temp_j1 = []
temp_j2 = []
temp_j3 = []
temp_j4 = []
temp_x = []
temp_y = []
temp_z = []
temp_r = []
urutan = []

global temp_j1
global temp_j2
global temp_j3
global temp_j4
global temp_x
global temp_y
global temp_z
global temp_r
global urutan

#----------Set Koneksi---------#
def koneksi(setsocket):
    ip = ''
    port = 5051
    setsocket1 = setsocket(ip , port)
    close = setsocket1.close()
    global close
    sock = setsocket1.socked()
    global sock

#-----------Set Port-----------#
setport = setport()
mainset = setport.mainset()
jog = setport.jog()
mport = setport.m_port()
mmove = manualmove(mport)
PTP = PTP(mport)
#------------fungsi------------#
fpause1 = 0
fstop1 = 0
fvacum = 0
fvacum1 = 0
def sendpose():
    getpose = mainset.run()
    # getpose1 = str(getpose)
    getpose1 = format('K:%s:%s:%s:%s:%s:%s:%s:%s' % (getpose[1],getpose[2],getpose[3],getpose[4],getpose[5],getpose[6],getpose[7],getpose[8]))
    getpose2 = getpose1.encode()
    conn.sendall(getpose2)
    return getpose
def main():
    stop = False
    flag = False
    teach = False
    sisa = 0
    jejak = 0
    global fpause1
    global fstop1
    global fvacum1
    while not stop:
        if conn:
            try:
                rdy_read, rdy_write, sock_err = select.select([conn,], [conn], [])
            except select.error:
                print('Select() failed on socket with {}'.format(client_address))
                return 1
            if len(rdy_read) > 0:
                data_recv = conn.recv(8)
                data2 = data_recv.decode()
                print(data2)
                data3 = data2
                mmove.move(data3, 1)
                if len(data3)>=4:
                    data4 = data3[3]
                    if data4 == "1":
                        data5 = data3
                        global data5
                        flag = True
                    if data4 == "0":
                        flag = False
                if data3 == "Von" or data3 == "Vof":
                        data5 = data3
                        global data5
                if data2 == "TEACH":
                    data5 = "home"
                    global data5
                    if teach == False:
                        teach = True
                    elif teach == True:
                        teach = False
                    print(teach)
                if teach == True:
                    print(fpause1)
                    fungsi = mmove.fungsi(data2)
                    print('ini : {}'.format(fungsi))
                    if fungsi == "START":
                        if fpause1 == 1:
                            mainset.start()
                            fhenti = runauto(sisa)
                            fpause1 = fhenti[0]
                            sisa =  fhenti[1]
                            fstop1 = fhenti[2]
                            fvacum1 = fhenti[3]                            
                        elif fpause1 == 0:
                            fhenti = runauto(sisa)
                            fpause1 = fhenti[0]
                            sisa = fhenti[1]
                            fstop1 = fhenti[2]
                            fvacum1 = fhenti[3]
                        elif fstop1 == 1:
                            if fvacum1 == 0:
                                mainset.start()
                                PTP.SPEED(10,10)
                                PTP.MOVJ_XYZ(temp_x[0], temp_y[0], temp_z[0], temp_r[0])
                                fstop1 = 0
                            elif fvacum1 == 1:
                                pass
                    if fungsi == "RECORD": 
                        teaching()
            if flag == True or teach == True:
                pose = sendpose()
                global pose
        else:
            stop = True
def teaching():
    joint1 = float(pose[1])
    joint2 = float(pose[2])
    joint3 = float(pose[3])
    joint4 = float(pose[4])
    x = float(pose[5])
    y = float(pose[6])
    z = float(pose[7])
    r = float(pose[8])

    temp_j1.append(joint1)
    temp_j2.append(joint2)
    temp_j3.append(joint3)
    temp_j4.append(joint4)
    temp_x.append(x)
    temp_y.append(y)
    temp_z.append(z)
    temp_r.append(r)
    urutan.append(data5)
                
    print(str(temp_j1))
    print(str(temp_j2))
    print(str(temp_j3))
    print(str(temp_j4))
    print(str(temp_x))
    print(str(temp_y))
    print(str(temp_z))
    print(str(temp_r))
    print(str(urutan))
def runauto(sisa):
    for i in range(sisa, len(urutan)):
        urutanp = i
        global urutanp
        global fvacum
        if urutan[i] == "Vof":
            fvacum = 0
            mmove.move(urutan[i], 1)
        if urutan[i] == "Von":
            fvacum = 1
            mmove.move(urutan[i], 1)
        else:
            PTP.SPEED(10,10)
            PTP.MOVJ_XYZ(temp_x[i], temp_y[i], temp_z[i], temp_r[i])
        fpause = 0
        fstop = 0
        while True:
            try:
                rdy_read, rdy_write, sock_err = select.select([conn,], [conn], [])
            except select.error:
                return 1
            if len(rdy_read) > 0:
                pause = conn.recv(8)
                pause_d = pause.decode()
                fungsi = mmove.fungsi(pause_d)
                if fungsi == "PAUSE":
                    fpause = 1
                    mainset.force()           
                    break
                if fungsi == "STOP":
                    fstop = 1
                    mainset.force
                    break
            pose1 = sendpose()
            if pose1[5] == str(temp_x[i]) and pose1[6] == str(temp_y[i]) and pose1[7] == str(temp_z[i]) and pose1[8] == str(temp_r[i]): 
                break
        if fpause == 1:
            listhenti = [fpause, i, fstop, fvacum]
            return listhenti
            break
        if fstop == 1:
            listhenti = [fpause, i, fstop, fvacum]
            return listhenti
            break 
    listhenti = [fpause, 0, fstop, fvacum]
    return listhenti

#------------main------------#

koneksi(setsocket)

while True:
    print ("menunggu")
    conn, client_address = sock.accept()
    global conn
    print('alamat : {}'.format(client_address))
    tersambung = False
    main()

    # jumlah = 0
    # while True:
    #     tersambung = True
    #     jumlah = 1 + jumlah
    #     print(jumlah)
    #     sleep(1)
    #     if jumlah == 20:
    #         close
    #         break
# print("nunggu 10 detik")
# sleep(10)
# close
# print("terputus")
# main()


