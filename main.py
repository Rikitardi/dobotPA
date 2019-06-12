#--------Library Bawaan--------#
from time import sleep
from glob import glob
from threading import Thread
import socket
import select, errno,sys
import requests
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
floop = 0
speeda = ""
def sendpose(pvacum,syarat):
    getpose = mainset.run()
    r = requests.get('http://192.168.43.82/webPA/API_pa.php?x='+str(getpose[6])+'&y='+str(getpose[5])+'&z='+str(getpose[7])+'&r='+str(getpose[8])+'&f=1')
    if syarat == 1:
        getpose1 = format('K:%s:%s:%s:%s:%s:%s:%s:%s::vc#%s::' % (getpose[5],getpose[6],getpose[7],getpose[8],getpose[1],getpose[2],getpose[3],getpose[4],pvacum))
        getpose2 = getpose1.encode()
    else:
        getpose1 = format('K:%s:%s:%s:%s:%s:%s:%s:%s::::' % (getpose[5],getpose[6],getpose[7],getpose[8],getpose[1],getpose[2],getpose[3],getpose[4]))
        getpose2 = getpose1.encode()
    conn.sendall(getpose2)
    return getpose
def henti(i,j,fvacum,fstop,fpause):
    while True:

        try:
            rdy_read, rdy_write, sock_err = select.select([conn,], [conn], [])
        except select.error:
            return 1
        if len(rdy_read) > 0:
            pause = conn.recv(8)
            pause_d = pause.decode()
            fungsi = mmove.fungsi(pause_d)
            print("terus aja sampai modar")
            if fungsi == "PAUSE":
                feedback(True)
                fpause = 1
                mainset.force()    
                print("ini pause")       
                break
            if fungsi == "STOP":
                feedback(True)
                print("keadaan : stop di tekan")
                fstop = 1
                mainset.force()
                break
        pose1 = sendpose(fvacum,0)
        if pose1[5] == str(temp_x[i]) and pose1[6] == str(temp_y[i]) and pose1[7] == str(temp_z[i]) and pose1[8] == str(temp_r[i]): 
            break    
    if fpause == 1:
        listhenti = [fpause, i, fstop, fvacum, j, 1]
        print(listhenti[0])
        print(listhenti[1])
        print(listhenti[2])
        print(listhenti[3])
        print(listhenti[4])
        print(listhenti[5])
        print("keadaan : fpause aktive")
        return listhenti
    if fstop == 1:
        print("keadaan : fstop aktive")
        listhenti = [fpause, i, fstop, fvacum, j, 1]
        return listhenti 
    listbangsat = [0,0,0,0,0,0]
    # print("diujung henti")
    return listbangsat
def feedback(kondisi):
    if kondisi == False:
        print("play false")
        fbstr = 'play:false'
        # conn.sendall(fbstr.encode())
    elif kondisi == True:
        print("play true")
        fbstr = 'play:true'
        # conn.sendall(fbstr.encode())
def main():
    print("ini fungsi main")
    stop = False
    flag = False
    teach = False
    sisa = 0
    jejak = 0
    floop = 0
    global fpause1
    global fpause2
    global fstop1
    global fvacum1
    global floop
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
                data3 = data2
                mmove.move(data3, 1)
                if data3 == "EXIT":
                    print("close")
                    close
                    stop = True
                if len(data3)>=4:
                    data4 = data3[3]
                    if data4 == "1":
                        data5 = data3
                        global data5
                        flag = True
                        print(flag)
                    elif data4 == "0":
                        flag = False
                        print(flag)
                if data3 == "Von" or data3 == "Vof":
                    data5 = data3
                    global data5
                if data2 == "TEACH":
                    data5 = "home"
                    global data5
                    teach = True
                    print(teach)
                elif teach == True:
                    print(fpause1)
                    fungsi = mmove.fungsi(data2)
                    if data2.find("STR") != -1:
                        pengulangan = fungsi[1]
                        speeda = fungsi[2]
                        fungsi = fungsi[0]
                        global speeda
                    if fungsi == "BATAL":
                        deletedata()
                        teach = False
                        print("data di delete")
                    if fungsi == "STR":
                        feedback(False)
                        if fpause2 == 0:
                            if fpause1 == 1:
                                mainset.start()
                                fhenti = runauto(sisa, floop, int(pengulangan))
                                fpause1 = fhenti[0]
                                sisa =  fhenti[1]
                                fstop1 = fhenti[2]
                                fvacum1 = fhenti[3]
                                floop = fhenti[4]                            
                                if fstop1 == 0:
                                    fpause2 = 0
                                elif fstop == 1:
                                    fpause2 = 1
                            elif fpause1 == 0:
                                fhenti = runauto(sisa, floop, int(pengulangan))
                                print(fhenti)
                                fpause1 = fhenti[0]
                                sisa = fhenti[1]
                                fstop1 = fhenti[2]
                                fvacum1 = fhenti[3]
                                floop = fhenti[4]
                                if fstop1 == 0:
                                    fpause2 = 0
                                elif fstop1 == 1:
                                    fpause2 = 1
                                print("keadaan : fstop1 = {}".format(fstop1))
                                print("keadaan : fvacum1 = {}".format(fvacum1))
                        if fstop1 == 1 and fpause2 == 1:
                            print("masuk stop")
                            if fvacum1 == 0:
                                mainset.start()
                                print("keadaan : menuju home")
                                PTP.SPEED(float(speeda),10)
                                PTP.MOVJ_XYZ(temp_x[0], temp_y[0], temp_z[0], temp_r[0])
                                fstop1 = 0
                                fpause2 = 0
                                sisa = 0
                            elif fvacum1 == 1:
                                print("vaccumm menyala")
                                while True:
                                    try:
                                        rdy_read, rdy_write, sock_err = select.select([conn,], [conn], [])
                                    except select.error:
                                        print('Select() failed on socket with {}'.format(client_address))
                                        return 1
                                    if len(rdy_read) > 0:
                                        print("data masuk")
                                        data_recv = conn.recv(10)
                                        data2 = data_recv.decode()
                                        print('ini di stop: {}'.format(data2))
                                        if data2 == "Vof":
                                            print("di tekan")
                                            mainset.start()
                                            fungsi = mmove.fungsi(data2,1)
                                            fstop1 = 0
                                            fpause2 = 0
                                            sisa = 0
                                            break
                    if fungsi == "RECORD": 
                        teaching()
            if flag == True:
                pose = sendpose(1,0)
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
def teaching():
    pose = sendpose(1,0)
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
def runauto(sisa,sisaloop,pengulangan):
    for j in range(sisaloop, pengulangan):
        print('pengulangan : {}'.format(j))
        for i in range(sisa, len(urutan)):
            print('step : {}'.format(i))
            global urutanp
            global fvacum
            # print('panjang record: {}'.format(len(urutan)))
            p = len(urutan)-1
            # print('syarat akhir: {}'.format(p))
            if i == p:
                global ftohome
                ftohome = 1
            urutanp = i
            if urutan[i] == "Vof":
                fvacum = 0
                sendpose(fvacum,1)
                mmove.move(urutan[i], 1)
            elif urutan[i] == "Von":
                fvacum = 1
                sendpose(fvacum,1)
                mmove.move(urutan[i], 1)
            else:
                # print("ada pergerakan")
                PTP.SPEED(float(speeda),50)
                PTP.MOVJ_XYZ(temp_x[i], temp_y[i], temp_z[i], temp_r[i])
                fpause = 0
                fstop = 0
                # print("disini bukan")
                nilaihenti = henti(i,j,fvacum,fstop,fpause)
                # print("berhasil")
                if nilaihenti[5] == 1:
                    # print("oke")
                    return nilaihenti

            if ftohome == 1:
                # print ("going to home")
                PTP.SPEED(float(speeda),50)
                PTP.MOVJ_XYZ(temp_x[0], temp_y[0], temp_z[0], temp_r[0])
                nilaihenti1 = henti(0,j,fvacum,fstop,fpause)
                # print('keadaan pause ftohome:{} '.format(nilaihenti1[0]))
                if nilaihenti1[0] == 1:
                    while True:
                        dongo = 0
                        try:
                            rdy_read, rdy_write, sock_err = select.select([conn,], [conn], [])
                        except select.error:
                            return 1
                        if len(rdy_read) > 0:
                            pausehome = conn.recv(8)
                            phome = pausehome.decode()
                            print(phome)
                            if phome.find("STR") != -1:
                                feedback(False)
                                mainset.start()
                                PTP.SPEED(float(speeda),50)
                                PTP.MOVJ_XYZ(temp_x[0], temp_y[0], temp_z[0], temp_r[0])
                                dongo = 1
                        if dongo == 1:
                            nilaihenti1 = henti(0,j,fvacum,fstop,0)
                            if nilaihenti1[0] == 0:
                                break
                ftohome = 0
                # print('nilai ftohom:{}'.format(ftohome))
    listhenti = [nilaihenti1[0], 0, nilaihenti1[2], nilaihenti1[3], 0]
    return listhenti

#------------main------------#

koneksi(setsocket)
while True:
    print ("menunggu")
    conn, client_address = sock.accept()
    global conn
    print('alamat : {}'.format(client_address))
    tersambung = False
    sendpose(1,0)
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



