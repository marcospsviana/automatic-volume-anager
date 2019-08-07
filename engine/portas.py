import RPi.GPIO as GPIO
import time
import serial


class Portas(object):
    def __init__(self):
        PORT_A0 = "servo_A0"
        PORT_A1 = "servo_A1"
        PORT_A2 = "servo_A2"
        PORT_A3 = "servo_A3"
        PORT_A4 = "servo_A4"
        PORT_0 = "servo_0"
        PORT_1 = "servo_1"
        PORT_2 = "servo_2"
        PORT_3 = "servo_3"
        PORT_4 = "servo_4"
        PORT_5 = "servo_5"
        PORT_6 = "servo_6"
        PORT_7 = "servo_7"
        PORT_8 = "servo_8"
        PORT_9 = "servo_9"
        PORT_10 = "servo_10"
        PORT_11 = "servo_11"
        PORT_12 = "servo_12"
        PORT_13 = "servo_13"
        PORT_14 = "servo_14"
        PORT_15 = "servo_15"
        PORT_16 = "servo_16"
        PORT_17 = "servo_17"
        PORT_18 = "servo_18"
        PORT_19 = "servo_19"
        PORT_20 = "servo_20"
        PORT_21 = "servo_21"
        PORT_22 = "servo_22"
        PORT_23 = "servo_23"
        PORT_24 = "servo_24"
        PORT_25 = "servo_25"
        PORT_26 = "servo_26"
        PORT_27 = "servo_27"
        PORT_28 = "servo_28"
        PORT_29 = "servo_29"
        PORT_30 = "servo_30"
        PORT_31 = "servo_31"
        PORT_32 = "servo_32"
        PORT_33 = "servo_33"
        PORT_34 = "servo_34"
        PORT_35 = "servo_35"
        PORT_36 = "servo_36"
        PORT_37 = "servo_37"
        PORT_38 = "servo_38"
        PORT_39 = "servo_39"
        PORT_40 = "servo_40"
        PORT_41 = "servo_41"
        PORT_42 = "servo_42"
        PORT_43 = "servo_43"
        PORT_44 = "servo_44"
        PORT_45 = "servo_45"
        PORT_46 = "servo_46"
        PORT_47 = "servo_47"
        PORT_48 = "servo_48"
        PORT_49 = "servo_49"
        PORT_50 = "servo_50"
        PORT_51 = "servo_51"

        self.serial = serial.Serial("/dev/ttyS0", 9600)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(12, GPIO.IN)

        
    def exec_port(self, port, command):
        self.port = str(port)
        print(self.port)
        self.command =str(command)
        print(self.command)
        __exec = self.port + ":" + self.command+ "\n"
        print(__exec)
        __exec = b'%b'%(__exec.encode('utf-8'))
        self.serial.write(__exec)
        time.sleep(30)
        self.port = b'%b'%(self.port.encode('utf-8'))
        comando = self.port + b":fecha\n" 
        self.serial.write(comando)


if __name__ == "__main__":
    Ports()


'''class Io(object):
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
            
            
        GPIO.setup( 29, GPIO.OUT)
        GPIO.setup( 33, GPIO.OUT)
        GPIO.setup( 35, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup( 37, GPIO.IN)
            
        GPIO.output(29, 0)
        GPIO.output(33, 0)
        
        fechado = False
        while True:
            if GPIO.input(35) == 1:
                while fechado == False:
                    GPIO.output(33,0)
                    GPIO.output(29, 1)
                    time.sleep(0.5)
                    GPIO.output(29,0)
                    time.sleep(0.5)
                    if GPIO.input(35) == 0:
                        fechado = True
                        GPIO.output(33,1)
            time.sleep(0.5)
            fechado= False
            if GPIO.input(37) == 1:
                print("cadastrar armario?")
                


            
    
        
            
if __name__ == '__main__':
    while True:
        Io()
'''