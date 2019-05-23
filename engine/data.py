import sqlite3


class Banco(object):
	def __init__(self):
		conn = sqlite3.connect('coolbag.db')
		c = conn.cursor()TABELA ARMARIOS
ID_ARMARIO  TYPE INT (PRIMARY_KEY)
CLASSE TYPE TEXT ( A, B, C, D)
LOCAL TYPE TEXT ( SUPERIOR, INFERIOR )
LIVRE TYPE BOOLEAN 
TERMINAL TYPE TEXT
PORTA_NUMERO TYPE INT

TABELA USUARIOS


TABELA LOCACAO




		
		c.execute( '''CREATE TABLE IF NOT EXISTS tb_armario( ID_ARMARIO INTEGER PRIMARY KEY AUTOINCREMENT,
		                                                      CLASSE TEXT,
															  LOCAL TEXT.
															  ESTADO TEXT,
															  TERMINAL TEXT,
															  PORTA_NUMERO INT)'''
		         )
		c.execute( ''' CREATE TABLE IF NOT EXISTS tb_usuario( ID_USUARIO INTEGER PRIMARY KEY AUTOINCREMENT,
		                                                      NOME TEXT,
															  EMAIL TEXT,
															  TEMPO_LOCACAO TIME,
															  SENHA TEXT,
															  FOREIGN KEY(ID_ARMARIO) REFERENCES tb_armario(ID_ARMARIO ) )''')
		c.execute('''CREATE TABLE IF NOT EXISTS tb_locacao (ID_LOCACAO INT PRIMARY_KEY AUTOINCREMENT,
		                                                    VALOR MONETARY,
															VALOR_EXCEDENTE MONETARY,
															TEMPO_CONTRATADO TIME,
															TEMPO_CORRIDO TIME,
															FOREIGN KEY (ID_USUARIO) REFERENCES tb_usuario( ID_USUARIO) ''')
		               
	def locar_armario(self):
		pass
		
	def liberar_armario(self, armario):
		pass

	def cadastrar_armario(self):
		print("cadastrado")
	
	def busca_armario(self, classe):
		classe = classe
		c.execute('''SELECT CLASSE  from tb_armario where classe = ?  and ESTADO = LIVRE''')
		
if __name__ == "__main__":
	Banco()