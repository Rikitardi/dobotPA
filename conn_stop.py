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
fpause2 = 0
fstop1 = 0
fvacum = 0
fvacum1 = 0
ftohome = 0
loop = 1
speeda = ""

def sendpose(x):
    getpose = mainset.run()
    if x == 0:
        getpose1 = format('K:%s:%s:%s:%s:%s:%s:%s:%s::' % (getpose[5],getpose[6],getpose[7],getpose[8],getpose[1],getpose[2],getpose[3],getpose[4]))
        getpose2 = getpose1.encode()
        conn.sendall(getpose2)
        print("oh di sini")
        sleep(.2)
        return getpose
    elif str(x).find("VC") == 0:
        getpose1 = format('K:%s:%s:%s:%s:%s:%s:%s:%s:%s::' % (getpose[5],getpose[6],getpose[7],getpose[8],getpose[1],getpose[2],getpose[3],getpose[4],x))
        getpose2 = getpose1.encode()
        conn.sendall(getpose2)
        print("oh di sini")
        sleep(.2)
        return getpose
    elif x == 2:
        getpose = mainset.run()
        return getpose



def main():
    stop = False
    flag = False
    teach = False
    sisa = 0
    lsisa = 0
    jejak = 0
    global fpause1
    global fpause2
    global fstop1
    global fvacum1
    global loop
    global speeda
    while not stop:
        if conn:
            try:
                rdy_read, rdy_write, sock_err = select.select([conn,], [conn], [])
            except select.error:
                print('Select() failed on socket with {}'.format(client_address))
                return 1
            if len(rdy_read) > 0:
                data_recv = conn.recv(10)
                data2 = data_recv.decode()
                print(data2)
                print(len(data2))
                data3 = data2
                mmove.move(data3, 1)
                if data2.find("SPEEDA") != -1:
                    fspeeda = data2.split()
                    speeda = fspeeda[1] 
                    print(speeda)
                if data3 == "EXIT":
                    print("close")
                    close
                    stop = True
                if data3.find("J") != -1:
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
                    teach = True
                    print(teach)
                if teach == True:
                    print(fpause1)
                    if data2.find("REMOVE") != -1:
                        fungsil = mmove.fungsi(data2)
                        removedata(int(fungsil[1]))
                    if data2.find("START") != -1:
                        print("START")
                        fungsil = mmove.fungsi(data2)
                        print(fungsil)
                        if fungsil[0] == "START":
                            loop = fungsil[1] 
                            if fpause2 == 0:
                                if fpause1 == 1:
                                    mainset.start()
                                    fhenti = runauto(sisa, lsisa)
                                    fpause1 = fhenti[0]
                                    sisa =  fhenti[1]
                                    fstop1 = fhenti[2]
                                    fvacum1 = fhenti[3]                            
                                    lsisa = fhenti[4]
                                    if fstop1 == 0:
                                        fpause2 = 0
                                    elif fstop == 1:
                                        fpause2 = 1
                                elif fpause1 == 0:
                                    fhenti = runauto(sisa,lsisa)
                                    fpause1 = fhenti[0]
                                    sisa = fhenti[1]
                                    fstop1 = fhenti[2]
                                    fvacum1 = fhenti[3]
                                    lsisa  = fhenti[4]
                                    if fstop1 == 0:
                                        fpause2 = 0
                                    elif fstop1 == 1:
                                        fpause2 = 1
                                    print("keadaan : fstop1 = {}".format(fstop1))
                                    print("keadaan : fvacum1 = {}".format(fvacum1))
                            elif fstop1 == 1 and fpause2 == 1:
                                if fvacum1 == 0:
                                    mainset.start()
                                    print("keadaan : menuju home")
                                    PTP.SPEED(float(speeda),10)
                                    PTP.MOVJ_XYZ(temp_x[0], temp_y[0], temp_z[0], temp_r[0])
                                    fstop1 = 0
                                    fpause2 = 0
                                    sisa = 0
                                elif fvacum1 == 1:
                                    pass
                    else:
                        fungsi = mmove.fungsi(data2)
                        if fungsi == "BATAL":
                            deletedata()
                            teach = False
                            print("data di delete")
                        if fungsi == "RECORD": 
                            teaching()
                    print(flag)
            if flag == True and teach == True:
                print("ini yg aneh")
                sendpose(0)
        # else:
        #     print("stop = true")
        #     stop = True
def removedata(a):
    del temp_j1[a]
    del temp_j2[a]
    del temp_j3[a]
    del temp_j4[a]
    del temp_x[a]
    del temp_y[a]
    del temp_z[a]
    del temp_r[a]
    del urutan[a]
    infodata()
def deletedata():
    temp_j1.clear()
    temp_j2.clear()
    temp_j3.clear()
    temp_j4.clear()
    temp_x.clear()
    temp_y.clear()
    temp_z.clear()
    temp_r.clear()
    urutan.clear()

    print(temp_j1)
    print(temp_j2)
    print(temp_j3)
    print(temp_j4)
    print(temp_x)
    print(temp_y)
    print(temp_z)
    print(temp_r)
    print(urutan)
def infodata():
    print(str(temp_j1))
    print(str(temp_j2))
    print(str(temp_j3))
    print(str(temp_j4))
    print(str(temp_x))
    print(str(temp_y))
    print(str(temp_z))
    print(str(temp_r))
    print(str(urutan))
def teaching():
    spose = sendpose(0)
    joint1 = float(spose[1])
    joint2 = float(spose[2])
    joint3 = float(spose[3])
    joint4 = float(spose[4])
    x = float(spose[5])
    y = float(spose[6])
    z = float(spose[7])
    r = float(spose[8])

    temp_j1.append(joint1)
    temp_j2.append(joint2)
    temp_j3.append(joint3)
    temp_j4.append(joint4)
    temp_x.append(x)
    temp_y.append(y)
    temp_z.append(z)
    temp_r.append(r)
    urutan.append(data5)
    infodata()
def runauto(sisa, lsisa):
    for k in range(lsisa, int(loop)):
        print('pengulangan : {}'.format(k))
        for i in range(sisa, len(urutan)):
            print('langkah : {}'.format(i))
            global urutanp
            global fvacum
            p = len(urutan) - 1
            if i == p:
                global ftohome
                ftohome = 1
            urutanp = i
            if urutan[i] == "Vof":
                fvacum = 0
                mmove.move(urutan[i], 1)
                sendpose("VC#of")
            if urutan[i] == "Von":
                fvacum = 1
                mmove.move(urutan[i], 1)
                sendpose("VC#on")
            else:
                PTP.SPEED(float(speeda),10)
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
                        print("keadaan : stop di tekan")
                        fstop = 1
                        mainset.force()
                        break
                pose1 = sendpose(0)
                if pose1[5] == str(temp_x[i]) and pose1[6] == str(temp_y[i]) and pose1[7] == str(temp_z[i]) and pose1[8] == str(temp_r[i]): 
                    break
            if fpause == 1:
                listhenti = [fpause, i, fstop, fvacum, k]
                return listhenti
                break
            if fstop == 1:
                print("keadaan : fstop aktive")
                listhenti = [fpause, i, fstop, fvacum, k]
                return listhenti
                break 
    if ftohome == 1:
        PTP.SPEED(float(speeda),10)
        PTP.MOVJ_XYZ(temp_x[0], temp_y[0], temp_z[0], temp_r[0])
        ftohome = 0
    listhenti = [fpause, 0, fstop, fvacum, 0]
    return listhenti

#------------main------------#

koneksi(setsocket)

while True:
    print ("menunggu")
    conn, client_address = sock.accept()
    global conn
    print('alamat : {}'.format(client_address))
    tersambung = False
    sendpose(0)
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


