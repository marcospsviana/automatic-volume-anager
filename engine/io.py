import RPi.GPIO as GPIO
import time

class Io(object):
    def __init__(self):
        def set_io(self):
            ''' definindo os pinos de entrada e saída para comandos
             e leitura de estados '''
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup( 7, GPIO.OUT)
            #gP.SETUP( 11, GPIO.OUT)
            GPIO.setup( 29, GPIO.OUT)
            GPIO.setup( 31, GPIO.OUT)
            GPIO.output(7, 0)
            GPIO.output(29, 0)
            GPIO.output(31, 0)
        def ativo():
            for i in range(10):
                GPIO.output(7, 1)
                time.sleep(1)
                GPIO.output(7,0)
                time.sleep(1)
        def ocupado():
            for i in range(10):
                GPIO.output(29,1)
                time.sleep(1)
                GPIO.output(29,0)
        def desocupado():
            for i in range(5):
                GPIO.output(31,1)
                time.sleep(1)
                GPIO.output(31,0)
                
            
        set_io(self)
        ativo()
        time.sleep(1)
        ocupado()
        time.sleep(1)
        desocupado()
            
if __name__ == '__main__':
    Io()