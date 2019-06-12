from Lib.riset import setport,setsocket
# import importlib 
from Lib.manual_move import manualmove
# from time import sleep
from pydobot import Dobot
from pydobot.dobot import Dobot
from pydobot.JOG import JOG
from pydobot.PTP import PTP
# sleep(2)
print("ajig")

setport = setport()
mainset = setport.mainset()
# jog = setport.jog()
# mport = setport.m_port()
# mmove = manualmove(mport)
# PTP = PTP(mport)

# importlib.reload(Lib.manual_move)

print("pisah")

mainset = setport.mainset()
# setport
# mainset