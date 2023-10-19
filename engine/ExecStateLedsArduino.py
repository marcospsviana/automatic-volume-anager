import mysql.connector as mdb
import pandas as pd
import serial
from DataAccessObjects import DataAccessObjectsManager
from portas import Portas
import time


class StatusLedsArduino:
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyUSB0', 9600)
        self.porta = Portas()
        __conn = mdb.connect(user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        # __c = __conn.cursor(buffered=True)
        # db_conn = sqlite3.Connection("db_portas.db")
        # cursor = db_conn.cursor()
        # cursor.execute("create table if not exists portas( porta text, estado text)")
        query_select = 'select porta, estado from tb_armario'
        result = pd.read_sql(query_select, __conn)
        for i in range(0, len(result)):
            estado = str(result['estado'][i]) + ':'
            porta = str(result['porta'][i])
            print(type(estado))
            print(type(porta))
            estado_porta = porta.encode('utf-8') + (estado.lower()).encode('utf-8')
            resultado = self.serial.write(b'%s' % (estado_porta))
            print(resultado)
            time.sleep(0.5)


if __name__ == '__main__':
    StatusLedsArduino()
