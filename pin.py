import RPi.GPIO as GPIO
from time import sleep
#pin 23,5,13,19,26 as output
#pin 4 as Emg

#-----------------Deklarasi PIN---------------#
merah = 37
kuning = 35
hijau = 33
power = 31
jstick = 29
emg = 11
Out = "Out"
In = "In"
H = "H"
L = "L"

def setupPin(pin,status):
    if status == "Out":
        GPIO.setup(pin, GPIO.OUT)
    if status == "In":
        GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
def pinOut(pin, status):
    if status == "H":
        GPIO.output(pin, GPIO.HIGH)
    if status == "L":
        GPIO.output(pin, GPIO.LOW)


class pinPanel():
    # lampuMerah = 19
    # lampuKuning = 26
    # lampuHijau = 13
    lampuPower = 20
    lampuJstick = 21
    # emg = 4
    # Out = "Out"
    # In = "In"
    # H = "H"
    # L = "L"

    def __init__(self):
        print(merah)
        self.lampuMerah = 5
        self.lampuKuning = 6
        self.lampuHijau = 13
        self.lampuPowerOn = 19
        self.lampuPowerOff = 26 
        # self.lampuJstickOn = 26
        # self.lampuJstickOff = 21 #----->
        self.emg = 11
        self.Out = "Out"
        self.In = "In"
        self.H = "H"
        self.L = "L"

        GPIO.setmode(GPIO.BCM)
        setupPin(self.lampuMerah, Out)
        setupPin(self.lampuKuning, Out)
        setupPin(self.lampuHijau, Out)
        setupPin(self.lampuPowerOn, Out)
        setupPin(self.lampuPowerOff, Out)
        setupPin(self.emg, In)
        # setupPin(self.lampuJstick, Out)
        pinOut(self.lampuMerah, self.L)
        pinOut(self.lampuKuning, self.L)
        pinOut(self.lampuPowerOn, self.L)
        pinOut(self.lampuPowerOff, self.L)

    
    def lampu(self, cmd, on):
        if cmd == "merah":
                pinOut(self.lampuKuning, self.L)
                pinOut(self.lampuHijau, self.L)
                pinOut(self.lampuMerah, self.H)

        elif cmd == "kuning":
                pinOut(self.lampuHijau, self.L)
                pinOut(self.lampuMerah, self.L)
                pinOut(self.lampuKuning, self.H)

        elif cmd == "hijau":
                pinOut(self.lampuMerah, self.L)
                pinOut(self.lampuKuning, self.L)
                pinOut(self.lampuHijau, self.H)

        elif cmd == "power":
            if on == 0:
                pinOut(self.lampuPowerOn, self.L)
                pinOut(self.lampuPowerOff, self.H)
            if on == 1:
                pinOut(self.lampuPowerOff, self.L)
                pinOut(self.lampuPowerOn, self.H)

        # elif cmd == "jstick":
        #     if on == 1:
        #         pinOut(self.lampuJstickOff, self.L)
        #         pinOut(self.lampuJstickOn, self.H)                
        #     if on == 0:
        #         pinOut(self.lampuJstickOn, self.L)
        #         pinOut(self.lampuJstickOff, self.H)
    def tombolEmg(self):
        return GPIO.input(self.emg)
    def clean(self):
        GPIO.cleanup()
if __name__ == "__main__":
    try:
        merah = "merah"
        kuning = "kuning"
        hijau = "hijau"
        power = "power"
        jstick = "jstick"
        panel = pinPanel()
        while True:
            if panel.tombolEmg() == 1:
                panel.lampu(power,1)
                print("yes")
            elif panel.tombolEmg() == 0:
                panel.lampu(power,0)
                print("no")  
            panel.clean
    except KeyboardInterrupt:
        panel.clean    
        print("byeee")
        # cmd1 = input("cmd :")
        # if cmd1 == "1":
        #     panel.lampu(merah,1)
    	# if cmd1 == "2":
        # 	panel.lampu(kuning,1)
    	# if cmd1 == "3":
        # 	panel.lampu(hijau,1)
    	# if cmd1 == "4":
        # 	panel.lampu(power,1)
    finally:
        GPIO.cleanup()
#-----------------Setup PIN---------------#


#11/54 21.6.2019
