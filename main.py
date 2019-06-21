#--------Library Bawaan--------#
from time import sleep
from glob import glob
from threading import Thread
import socket
import select, errno,sys
import requests
#--------Library Buatan--------#
from Lib.riset import setport,setsocket
print("before")
from Lib.manual_move import manualmove
print("after")
from pydobot import Dobot
from pydobot.dobot import Dobot
from pydobot.JOG import JOG
from pydobot.PTP import PTP
from pin import pinPanel
#from test import stick


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

#----------Set Koneksi---------#
def koneksi(setsocket):
    ip = ''
    port = 5051
    setsocket1 = setsocket(ip , port)
    close = setsocket1.close()
    global close
    sock = setsocket1.socked()
    global sock


#-----------Set pinPanel-----------#

gpio = pinPanel()

#-----------Set Port-----------#



#------------fungsi------------#
fpause1 = 0
fpause2 = 0
fstop1 = 0
fvacum = 0
fvacum1 = 0
ftohome = 0
floop = 0
speeda = ""

def indicator(lampu, init):
    if lampu == "merah":
        gpio.lampu(lampu,1)
        if init == 0:
            feedback("lampuMerah")
    elif lampu == "kuning":
        gpio.lampu(lampu,1)
        feedback("lampuKuning")
    elif lampu == "hijau":
        gpio.lampu(lampu,1)
        feedback("lampuHijau")
def waitdata(panjangData):
    # print("wait data")
    try:
        rdy_read, rdy_write, sock_err = select.select([conn,], [conn], [])
    except select.error:
        print('Select() failed on socket with {}'.format(client_address))
        return 1
    if len(rdy_read) > 0:
        data_recv = conn.recv(panjangData)
        data2 = data_recv.decode()
        tombolEmg  = gpio.tombolEmg()
        if data2 == "EMG" or tombolEmg == 0:                          #EMGERGENCY#
            print("EMG HERE")
            mainset.force()
            return "EMG"
        return [True, data2]    
    return [False]
        

def sendpose(pvacum,syarat):
    # print("ini sendpose")
    getpose = dobotkk.run()
    if getpose == 'ERROR 101' :
        pesan = 'ERROR 101'
        return pesan
    requests.get('http://192.168.43.82/webPA/API_pa.php?x='+str(getpose[6])+'&y='+str(getpose[5])+'&z='+str(getpose[7])+'&r='+str(getpose[8])+'&f=1')
    if syarat == 1:
        getpose1 = format('K:%s:%s:%s:%s:%s:%s:%s:%s::vc#%s::#' % (getpose[5],getpose[6],getpose[7],getpose[8],getpose[1],getpose[2],getpose[3],getpose[4],pvacum))
        getpose2 = getpose1.encode()
    else:
        getpose1 = format('K:%s:%s:%s:%s:%s:%s:%s:%s::::#' % (getpose[5],getpose[6],getpose[7],getpose[8],getpose[1],getpose[2],getpose[3],getpose[4]))
        getpose2 = getpose1.encode()
        datapose = format('DATA POSISI TERAKHIR : J1:%s, J2:%s, J3:%s, J4:%s, X1:%s, X2:%s, X3:%s, X4:%s::::#' % (getpose[1],getpose[2],getpose[3],getpose[4],getpose[5],getpose[6],getpose[7],getpose[8]))
        print(getpose2)
    conn.sendall(getpose2)
    return getpose  
def henti(i,j,fvacum,fstop,fpause):
    # indicator("merah",0) #--------------------------> ind Merah
#---------------------recv data henti------------------------# 
    while True:    
        wdata = waitdata(10)
        if wdata == "EMG":
            return "EMG"
        if wdata[0] == True:
            pause_d = wdata[1]
            fungsi = mmove.fungsi(pause_d)
            # print("terus aja sampai modar")
            if fungsi == "PAUSE":
                fpause = 1
                mainset.force()    
                # print("ini pause")       
                break
            if fungsi == "STOP":
                # print("keadaan : stop di tekan")
                fstop = 1
                mainset.force()
                break
        pose1 = sendpose(fvacum,0)
        if pose1 =='ERROR 101':
            error = 'ERROR 101'
            return error
        if pose1[5] == str(temp_x[i]) and pose1[6] == str(temp_y[i]) and pose1[7] == str(temp_z[i]) and pose1[8] == str(temp_r[i]): 
            break    
#---------------------syarat henti------------------------#
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
        # print("keadaan : fstop aktive")
        listhenti = [fpause, i, fstop, fvacum, j, 1]
        return listhenti 
    listbangsat = [0,0,0,0,0,0]
    return listbangsat
def feedback(kondisi):
    # print("feeeeeeeeeeeeeeeeeeeeeedddddddddddddbbbbbbbbbbbbbacccccccccckkkkkkkkkk")
    if kondisi == False:
        # print("play false")
        fbstr = 'play:false:'
        conn.sendall(fbstr.encode())
    elif kondisi == True:
        # print("play true")
        fbstr = 'play:true:'
        conn.sendall(fbstr.encode())
    elif kondisi == "emg-fcum":
        # print("emg-fcum")
        fbstr = 'emg-fcm:true:'
        conn.sendall(fbstr.encode())
    elif kondisi == "terhubung":
        # print("koneksi-true")
        fbstr = 'koneksi:true:'
        conn.sendall(fbstr.encode())
    elif kondisi == "lampuMerah":
        fbstr = 'indi:merah:'
        conn.sendall(fbstr.encode())
    elif kondisi == "lampuHijau":
        fbstr = 'indi:hijau:'
        conn.sendall(fbstr.encode())
    elif kondisi == "lampuKuning":
        fbstr = 'indi:kuning:'
        conn.sendall(fbstr.encode())
    elif kondisi == "serial":
        fbstr = 'serial:terhubung:'
        conn.sendall(fbstr.encode())
def main():
    # print("ini fungsi main")
    emg_fcum = 0
    stop = False
    # print(stop)
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
    # print("pasti di siniiiii")
    # print("kok gk masuk")
    keluarmain = 0
    indicator("hijau",0)
    while not stop:
        if conn:
            wdata = waitdata(10)
            if wdata == "EMG":
                # print("emg di main")
                keluarmain = 1
                break
            if wdata[0] == True:
                data2 = wdata[1]
                # print(data2)
                data3 = data2
#--------------------------MANUAL FUNC-------------------------#
                mmove.move(data3, 1)
                if data3.find("J") != -1:   #------------------------> indicator
                    if data3[3] == "1":
                        indicator("kuning",0)
                    if data3[3] == "0":
                        indicator("hijau",0)
#---------------------------HOME FUNC--------------------------#                
                if data3 == "HOME":
                    mainset.home(True)
                    while True:
                        pooose1 = sendpose(1,0)
                        try :
                            x = round(float(pooose1[5]))
                            y = round(float(pooose1[6]))
                            z = round(float(pooose1[7]))
                            r = round(float(pooose1[8]))
                            print(x)
                            print(y)
                            print(z)
                            print(r)
                        except ValueError:
                            continue
                        if x == 250 and y == 0 and z == 50 and r == 0: 
                            sleep(5)
                            break
#--------------------------EXIT FUNC---------------------------#
                if data3 == "EXIT":
                    print("close")
                    close
                    stop = True
#-------------------------VACUUM FUNC--------------------------#
                if len(data3)>=4:
                    data4 = data3[3]
                    if data4 == "1":
                        data5 = data3
                        global data5
                        flag = True
                        # print(flag)
                    elif data4 == "0":
                        flag = False
                        # print(flag)
                if data3 == "Von" or data3 == "Vof":
                    data5 = data3
                    global data5
#------------------------TEACHING FUNC-------------------------#
                if data2 == "TEACH":
                    data5 = "home"
                    global data5
                    teach = True
                    print(teach)
                if teach == True:
                    fungsi = mmove.fungsi(data2)
                    if data2.find("REMOVE") != -1:
                        arrayD = fungsi[1]
                        remove(int(arrayD))
                    if data2.find("STR") != -1:
                        indicator("merah",0)
                        pengulangan = fungsi[1]
                        speeda = fungsi[2]
                        fungsi = fungsi[0]
                        global speeda
                    if fungsi == "BATAL":
                        # print("sebelum di hapus")
                        deletedata()
                        teach = False
                    if fungsi == "STR":
                        indicator("kuning",0)
                        feedback(False)
                        if fpause2 == 0:
                            if fpause1 == 1:
                                mainset.start()
                                fhenti = runauto(sisa, floop, int(pengulangan))
                                if fhenti == "EMG":
                                    keluarmain = 1
                                    break
                                if fhenti == 'ERROR 101':
                                    return 1
                                fpause1 = fhenti[0]
                                sisa =  fhenti[1]
                                fstop1 = fhenti[2]
                                fvacum1 = fhenti[3]
                                floop = fhenti[4]                            
                                if fstop1 == 0:
                                    fpause2 = 0
                                elif fstop1 == 1:
                                    fpause2 = 1
                            elif fpause1 == 0:
                                fhenti = runauto(sisa, floop, int(pengulangan))
                                if fhenti == "EMG":
                                    keluarmain = 1
                                    break
                                if fhenti == 'ERROR 101':
                                    return 1                                
                                # print(fhenti)
                                fpause1 = fhenti[0]
                                sisa = fhenti[1]
                                fstop1 = fhenti[2]
                                fvacum1 = fhenti[3]
                                floop = fhenti[4]
                                if fstop1 == 0:
                                    fpause2 = 0
                                elif fstop1 == 1:
                                    fpause2 = 1
                                # print("keadaan : fstop1 = {}".format(fstop1))
                                # print("keadaan : fvacum1 = {}".format(fvacum1))
                        if fstop1 == 1 and fpause2 == 1:
                            # print("masuk stop")
                            if fvacum1 == 0:
                                # print("vaccumm menyala")
                                emg0 = 0
                                while True:
                                    wdata = waitdata(10)
                                    if wdata == "EMG":
                                        emg0 = 1
                                        break
                                    if wdata[0] == True:
                                        data2 = wdata[1]
                                        if data2 == "A_RESET":
                                            mainset.start()
                                            # print("keadaan : menuju home")
                                            PTPm.SPEED(float(speeda),10)
                                            PTPm.MOVJ_XYZ(temp_x[0], temp_y[0], temp_z[0], temp_r[0])
                                            fbreak = 0
                                            while True:
                                                wdata = waitdata(10)
                                                if wdata == "EMG":
                                                    emg0 = 1
                                                    fbreak = 1
                                                    break
                                                spose1 = sendpose(1,0)
                                                # print(spose1)
                                                if spose1 == 'ERROR 101':
                                                    # print(spose1)
                                                    return 1
                                                if spose1[5] == str(temp_x[0]) and spose1[6] == str(temp_y[0]) and spose1[7] == str(temp_z[0]) and spose1[8] == str(temp_r[0]): 
                                                    indicator("hijau",0)
                                                    # print("harusnya break")
                                                    fbreak = 1
                                                    feedback(True)
                                                    break
                                            if fbreak == 1:
                                                break
                                if emg0 == 1:
                                    keluarmain = 1
                                    break
                                fstop1 = 0
                                fpause2 = 0
                                sisa = 0
                                # print("berhasil 0")
                            elif fvacum1 == 1:
                                # print("vaccumm mati")
                                while True:
                                    emg1 = 0
                                    wdata = waitdata(10)
                                    if wdata == "EMG":
                                        emg1 =1
                                        break
                                    if wdata[0] == True:
                                        data2 = wdata[1]
                                        # print('ini di stop: {}'.format(data2))
                                        if data2 == "Vof":
                                            # print("di tekan")
                                            mainset.start()
                                            fungsi = mmove.move(data2,1)
                                            # print("harusnya mati")
                                            fbreak = 0
                                        elif data2 == "A_RESET":
                                            PTPm.SPEED(float(speeda),10)
                                            PTPm.MOVJ_XYZ(temp_x[0], temp_y[0], temp_z[0], temp_r[0])
                                            while True:
                                                wdata = waitdata(10)
                                                if wdata == "EMG":
                                                    emg1 = 1
                                                    fbreak = 1
                                                    break
                                                spose1 = sendpose(1,0)
                                                # print(spose1)
                                                if spose1 == 'ERROR 101':
                                                    # print(spose1)
                                                    return 1
                                                if spose1[5] == str(temp_x[0]) and spose1[6] == str(temp_y[0]) and spose1[7] == str(temp_z[0]) and spose1[8] == str(temp_r[0]): 
                                                    # print("harus break")
                                                    indicator("hijau",0)
                                                    feedback(True)
                                                    fbreak = 1
                                                    break
                                            if fbreak == 1:
                                                break                                                                                
                                if emg1 == 1:
                                    keluarmain = 1
                                    break
                                fstop1 = 0
                                fpause2 = 0
                                sisa = 0
                                # print("berhasil 1")
                    if fungsi == "RECORD": 
                        teach1 = teaching()
                        # print("TEACHING LOHHH")
                        if teach1 == 1:
                            return 1
                    if data2 == "LStart":
                        # print("siap di save")
                        while True:
                            flag_u = 0
                            v = ""
                            keluarMain = 0
                            wdata = waitdata(1000)
                            if wdata == "EMG":
                                # print("emg di main")
                                keluarMain = 1
                                break
                            if wdata[0] == True:
                                # print("ini delete load")
                                deletedata()
                                load = wdata[1]
                                array1 = load.split("#")
                                p_array1 = len(array1)
                                for i in range(p_array1):
                                    if i != p_array1 - 1:
                                        array2 = array1[i].split(",")
                                        p_array2 = len(array2)
                                        x = array2[1]
                                        y = array2[2]
                                        z = array2[3]
                                        r = array2[4]
                                        j1 = array2[5]
                                        j2 = array2[6]
                                        j3 = array2[7]
                                        j4 = array2[8]
                                        u = array2[9]

                                        if u != "ON":
                                            v = ""

                                        elif u == "ON" and flag_u == 0:
                                            flag_u = 1
                                            v = "Von"

                                        elif flag_u == 1 and u == "ON" :
                                            v = ""

                                        elif u == "OFF" and flag_u == 1:
                                            v = "Vof"
                                            flag_u = 0

                                        elif u == "OFF" and flag_u == 0:
                                            v = ""
                                        load_koordinat(float(j1),float(j2),float(j3),float(j4),float(x),float(y),float(z),float(r),v)
                                        init = 0
                                if load.find("LDone")!= -1:
                                    break
                        if keluarMain == 1:
                            break
            if flag == True:
                pose = sendpose(1,0)
                if pose == 'ERROR 101':
                    # print(pose)
                    return 1
#--------------------PEMBERTHENIAN EMERGENCY -------------------#
    if keluarmain == 1: #pemberhentian emergency
        while True:
            wdata = waitdata(10)
            if wdata[0] == True:
                data2 = wdata[1]
                print(data2)
                print("Emergency ditekan")
                if data2 == "ERESET": #pemberhentian reset
                    mainset.start()
                    if emg_fcum == 1:
                        while True:
                            wdata = waitdata(10)
                            if wdata == "EMG":
                                break                            
                            if wdata[0] == True:
                                data2 = wdata[1]
                                if data2 == "Vof":                                    
                                    mainset.start()
                                    mmove.move(data2,1)
                                    feedback("emg-fcum")
                                    backHome = 1    
                                if data2 == "HOME" and backHome == 1:
                                    backHome = 1
                                    mainset.home(True)
                                    while True:
                                        pooose1 = sendpose(1,0)
                                        wdata = waitdata(10)
                                        if wdata == "EMG":
                                            break
                                        try :
                                            x = round(float(pooose1[5]))
                                            y = round(float(pooose1[6]))
                                            z = round(float(pooose1[7]))
                                            r = round(float(pooose1[8]))
                                        except ValueError:
                                            continue
                                        if x == 250 and y == 0 and z == 50 and r == 0: 
                                            sleep(5)
                                            return "EMG"
                                    if emgInternal == 1:
                                        emgInternal = 0
                                        break
                    elif emg_fcum == 0:
                        print("emg_fcum")
                        while True:
                            wdata = waitdata(10)
                            if wdata == "EMG":
                                break
                            print("menunggu home")
                            if wdata[0] == True:
                                data2 = wdata[1]
                                if data2 == "HOME":
                                    mainset.start()
                                    mainset.home(True)
                                    while True:
                                        wdata = waitdata(10)
                                        if wdata == "EMG":
                                            emgInternal = 1
                                            break
                                        print("proses home")
                                        pooose1 = sendpose(1,0)
                                        print(type(pooose1[5]))
                                        try :
                                            x = round(float(pooose1[5]))
                                            y = round(float(pooose1[6]))
                                            z = round(float(pooose1[7]))
                                            r = round(float(pooose1[8]))
                                        except ValueError:
                                            continue
                                        if x == 250 and y == 0 and z == 50 and r == 0: 
                                            print("sleep")
                                            sleep(5)
                                            return "EMG"
                            if emgInternal == 1:
                                emgInternal = 0
                                break

    fpause1 = 0
    fpause2 = 0
    fstop1 = 0
    fvacum = 0
    fvacum1 = 0
    ftohome = 0
    floop = 0
    return 0
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
    print("data di delete")
def remove(i):
    del temp_j1[i]
    del temp_j2[i]
    del temp_j3[i]
    del temp_j4[i]
    del temp_x[i]
    del temp_y[i]
    del temp_z[i]
    del temp_r[i]
    del urutan[i]
def load_koordinat(j1,j2,j3,j4,x,y,z,r,u):
    temp_j1.append(j1)
    temp_j2.append(j2)
    temp_j3.append(j3)
    temp_j4.append(j4)
    temp_x.append(x)
    temp_y.append(y)
    temp_z.append(z)
    temp_r.append(r)
    urutan.append(u)
                
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
    pose = sendpose(1,0)
    if pose =='ERROR 101':
        error = 'ERROR 101'
        return error

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
                
    print('J1 :{}'.format(str(temp_j1)))
    print('J2 :{}'.format(str(temp_j2)))
    print('J3 :{}'.format(str(temp_j3)))
    print('J4 :{}'.format(str(temp_j4)))
    print('X :{}'.format(str(temp_x)))
    print('Y :{}'.format(str(temp_y)))
    print('Z :{}'.format(str(temp_z)))
    print('R :{}'.format(str(temp_r)))
    print('urutan :{}'.format(str(urutan)))
def runauto(sisa,sisaloop,pengulangan):
    for j in range(sisaloop, pengulangan):
        print('pengulangan : {}'.format(j))
        for i in range(sisa, len(urutan)):
            print('step : {}'.format(i))
            global urutanp
            global fvacum
            p = len(urutan)-1
            print('syarat akhir: {}'.format(p))
            if i == p:
                global ftohome
                ftohome = 1
            urutanp = i
            if urutan[i] == "Vof":
                fvacum = 0
                emg_fcum = 0
                global emg_fcum
                jala = sendpose(fvacum,1)
                if jala =='ERROR 101':
                    error = 'EEROR 101'
                    return error
                mmove.move(urutan[i], 1)
            elif urutan[i] == "Von":
                fvacum = 1
                jala = sendpose(fvacum,1)
                emg_fcum = 1
                global emg_fcum
                if jala =='ERROR 101':
                    error = 'ERROR 101'
                    return error
                mmove.move(urutan[i], 1)
            else:
                PTPm.SPEED(float(speeda),50)
                PTPm.MOVJ_XYZ(temp_x[i], temp_y[i], temp_z[i], temp_r[i])
                fpause = 0
                fstop = 0
                nilaihenti = henti(i,j,fvacum,fstop,fpause)
                if nilaihenti == "EMG":
                    return nilaihenti
                if nilaihenti == 'ERROR 101':
                    return nilaihenti
                print("berhasil")
                if nilaihenti[5] == 1:
                    return nilaihenti
            if ftohome == 1:
                PTPm.SPEED(float(speeda),50)
                PTPm.MOVJ_XYZ(temp_x[0], temp_y[0], temp_z[0], temp_r[0])
                nilaihenti1 = henti(0,j,fvacum,fstop,fpause)
                if nilaihenti1 == "EMG":
                    return nilaihenti1
                if nilaihenti1 == 'ERROR 101':
                    return nilaihenti1
                if nilaihenti1[0] == 1:
                    while True:
                        dongo = 0
                        wdata = waitdata(10)
                        if wdata == "EMG":
                            return "EMG"
                        if wdata[0] == True:
                            phome = wdata[1] 
                            # print(phome)
                            if phome.find("STR") != -1:
                                feedback(False)
                                mainset.start()
                                PTPm.SPEED(float(speeda),50)
                                PTPm.MOVJ_XYZ(temp_x[0], temp_y[0], temp_z[0], temp_r[0])
                                dongo = 1
                        if dongo == 1:
                            nilaihenti1 = henti(0,j,fvacum,fstop,0)
                            if nilaihenti1 == "EMG":
                                return nilaihenti1
                            if nilaihenti1 == 'ERROR 101':
                                return nilaihenti1
                            if nilaihenti1[0] == 0:
                                break
                ftohome = 0
                # print('nilai ftohom:{}'.format(ftohome))
    listhenti = [nilaihenti1[0], 0, nilaihenti1[2], nilaihenti1[3], 0]
    feedback(True)
    return listhenti
def setportlokal():
    print("menunggu port")
    while True:
        available_ports = glob('/dev/ttyUSB0')
        if len(available_ports) == 0:
            available_ports = glob('/dev/ttyUSB1')
            if len(available_ports) == 0:
                available_ports = glob('/dev/ttyUSB2')
                if len(available_ports) == 0:
                    available_ports = glob('/dev/ttyUSB3')
        if len(available_ports) != 0:
            return available_ports    
        wdata = waitdata(10)
        if wdata == "EMG":
            print("masuk emg")
            return "EMG"
        if wdata[0] == True:
            Input = wdata[1]
            print(Input)
            if Input == "EXIT":
                conn.close()
                return False
def dobotPort(port,fungsi):
    if fungsi == 1:
        main = Dobot(port = port )
        return main
    if fungsi == 2:
        jog = JOG(port = port)
        return jog
#---------------------main looping------------------------#

koneksi(setsocket)
error = 0
a = 0
error = ""

while True:
    if error == "":
        indicator("merah",1)
        print ("menunggu koneksi")
        conn, client_address = sock.accept()

        global conn
        print('alamat : {}'.format(client_address))
        tersambung = False
        feedback("terhubung") #---------->> TCP-IP

    if error == 0 or error == "EMG" or  error == "":
        print("set port")
        try:
            avail_ports =setportlokal()
            print(avail_ports)
            if avail_ports != False:
                feedback("serial") #------------>>Serial
                dobotkk = Dobot(avail_ports[0])
                global dobotkk
                sendpose(1,0)
                mainset = dobotPort(avail_ports[0],1)
                global mainset
                jog = dobotPort(avail_ports[0],2)
                global jog
                mmove = manualmove(avail_ports[0])
                global move
                PTPm = PTP(avail_ports[0])
                global PTPm
                error = main()
        except ConnectionResetError:
            print("keluar2")
            error = ""
            pass
#------------------------- pelabuhan error -----------------------------#
        if error == 1:
            a = 0
            print("yg ini kah")
            deletedata()
            fpause1 = 0
            fpause2 = 0
            fstop1 = 0
            fvacum = 0
            fvacum1 = 0
            ftohome = 0
            floop = 0
            speeda = ""
            mainset.close()
        print('ini error bukan di main: {}'.format(error))
        print("force close")
        error = ""   
#---------------------- pelabuhan error selesai ------------------------#


    elif error == 1:
        print("menunggu port")
        avail_ports =setport()
        dobotkk = Dobot(avail_ports[0])
        global dobotkk
        error = main()
        if error == 1:
            a = 0
            print("atau yg ini kah")
            deletedata()
            fpause1 = 0
            fpause2 = 0
            fstop1 = 0
            fvacum = 0
            fvacum1 = 0
            ftohome = 0
            floop = 0
            speeda = ""
            mainset.close()
        print('ini error bukan di main'.format(error))
        print("force close") 
    
    # jumlah = 0
    # while True:
    #     tersambung = True
    #     jumlah = 1 + jumlah
    #     print(jumlah)
    #     sleep(1)
    #     if jumlah == 20:
    #         close
    #         break

#1.48 6/14/2019
#10:10 6/20/19
#2:20 6/21/19