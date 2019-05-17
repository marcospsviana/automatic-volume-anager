import RPi.GPIO as GPIO
import time
import _thread

class Io(object):
    def __init__(self):
        fechado = False
        
    
        def set_io(self):
            ''' definindo os pinos de entrada e saída para comandos
             e leitura de estados '''
            GPIO.setmode(GPIO.BOARD)
            
            
            GPIO.setup( 29, GPIO.OUT)
            GPIO.setup( 33, GPIO.OUT)
            GPIO.setup( 35, GPIO.IN)
            
            GPIO.output(29, 0)
            GPIO.output(33, 0)
        def ativo():
            if GPIO.input(35) == 1:
                while fechado == False:
                
                    GPIO.output(29, 1)
                    time.sleep(0.5)
                    GPIO.output(29,0)
                    time.sleep(0.5)
                    if fechado == True:
                        break
                    
        def ocupado():
            ''' leitura do pino 35 '''
            if GPIO.input(35) == 0:
                GPIO.output(33, 1)
                fechado = True
            else:
                GPIO.output(33, 0)
                fechado = False
                
        
                
            
        set_io(self)
        ativo()
        #time.sleep(1)
        ocupado()
        #time.sleep(1)
        #desocupado()
        #GPIO.cleanup()
            
if __name__ == '__main__':
    while True:
        Io()