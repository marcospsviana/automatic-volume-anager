import RPi.GPIO as GPIO
import time
#from cadastrar_armario import Janela

class Io(object):
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
