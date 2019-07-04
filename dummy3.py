import RPi.GPIO as GPIO
from time import sleep
#pin 23,5,13,19,26 as output
#pin 4 as Emg

#-----------------Deklarasi PIN---------------#
merah = 23
kuning = 5
hijau = 13
power = 19
jstick = 26
emg = 4
Out = "Out"
In = "In"
H = "H"
L = "L"

def setupPin(pin,status):
    if status == "Out":
        # print(pin)
        GPIO.setup(pin, GPIO.OUT)
    if status == "In":
        # print(pin)
        GPIO.setup(pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
def pinOut(pin, status):
    if status == "H":
        GPIO.output(pin, GPIO.HIGH)
    if status == "L":
        GPIO.output(pin, GPIO.LOW)


class pinPanel():
    lampuMerah = 23
    lampuKuning = 5
    lampuHijau = 13
    lampuPower = 19
    lampuJstick = 26
    emg = 4
    Out = "Out"
    In = "In"
    H = "H"
    L = "L"

    def __init__(self):
        print(merah)
        self.lampuMerah = 23
        self.lampuKuning = 5
        self.lampuHijau = 13
        self.lampuPower = 19
        self.lampuJstick = 26
        self.emg = 4
        self.Out = "Out"
        self.In = "In"
        self.H = "H"
        self.L = "L"

        GPIO.setmode(GPIO.BCM)
        setupPin(self.lampuMerah, Out)
        setupPin(self.lampuKuning, Out)
        setupPin(self.lampuHijau, Out)
        setupPin(self.lampuPower, Out)
        setupPin(self.lampuJstick, Out)
        setupPin(self.emg, In)
        pinOut(self.lampuMerah, self.L)
        pinOut(self.lampuKuning, self.L)
        pinOut(self.lampuPower, self.L)
        pinOut(self.lampuJstick, self.L)
        pinOut(self.lampuJstick, self.L)
    
    def lampu(self, cmd, on):
        if cmd == "merah":
            if on == 1:
                pinOut(self.lampuMerah, self.H)
            if on == 0:
                pinOut(self.lampuMerah, self.L)

        elif cmd == "kuning":
            if on == 1:
                pinOut(self.lampuKuning, self.H)
            if on == 0:
                pinOut(self.lampuKuning, self.L)

        elif cmd == "hijau":
            if on == 1:
                pinOut(self.lampuHijau, self.H)
            if on == 0:
                pinOut(self.lampuHijau, self.L)

        elif cmd == "power":
            if on == 1:
                pinOut(self.lampuPower, self.H)
            if on == 0:
                pinOut(self.lampuPower, self.L)

        elif cmd == "jstick":
            if on == 1:
                pinOut(self.lampuJstick, self.H)
            if on == 0:
                pinOut(self.lampuJstick, self.L)
    def tombolEmg(self):
        return GPIO.input(emg)
    def clean(self):
        GPIO.cleanup()
if __name__ == "__main__":
    merah = "merah"
    kuning = "kuning"
    hijau = "hijau"
    power = "power"
    jstick = "jstick"
    panel = pinPanel()
while True:
    if panel.tombolEmg() == 1:
        panel.lampu(merah,1)
        sleep(5)
        panel.clean()
        break
#-----------------Setup PIN---------------#

