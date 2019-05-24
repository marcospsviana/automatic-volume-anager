import sqlite3
import datetime


class Banco(object):
	def __init__(self):
		self.conn = sqlite3.connect('coolbag.db')
		self.c = self.conn.cursor()




		
		self.c.execute( '''CREATE TABLE IF NOT EXISTS tb_armario( ID_ARMARIO INTEGER PRIMARY KEY AUTOINCREMENT,
		                                                      CLASSE TEXT,
															  LOCAL TEXT,
															  ESTADO TEXT,
															  TERMINAL TEXT,
															  PORTA_NUMERO INT)'''
		         )
		self.c.execute( ''' CREATE TABLE IF NOT EXISTS tb_usuario( ID_USUARIO INTEGER PRIMARY KEY AUTOINCREMENT,
		                                                      NOME TEXT,
															  EMAIL TEXT,
															  TEMPO_LOCACAO TIME,
															  SENHA TEXT,
															  ID_ARMARIO INTEGER,
															  FOREIGN KEY(ID_ARMARIO) REFERENCES tb_armario(ID_ARMARIO ) )''')
		self.c.execute('''CREATE TABLE IF NOT EXISTS tb_locacao (ID_LOCACAO INTEGER PRIMARY KEY AUTOINCREMENT,
		                                                    VALOR MONETARY,
															VALOR_EXCEDENTE MONETARY,
															DATA_CONTRATACAO DATETIME,
															TEMPO_CONTRATADO TIME,
															TEMPO_CORRIDO TIME,
															ID_USUARIO INTEGER,
															FOREIGN KEY (ID_USUARIO) REFERENCES tb_usuario( ID_USUARIO)) ''')
		               
	def locar_armario(self, armario, senha, id_usuario):
		self.hora_locacao = datetime.now()
		self.armario = armario
		self.id_usuario = id_usuario
		self.senha = senha
		
	
	def localisa_armario(self, armario):
		self.armario = armario
		result = self.busca_armario(self.armario)
		if result:
			return(result[0])
		else:
			return "nao ha armario disponivel"

		

	def liberar_armario(self):
		pass
		return(result[0])

	def cadastrar_armario(self):
		print("cadastrado")

	def busca_armario(self, classe):
		result = ''
		classe = classe
		self.c.execute("SELECT *  from tb_armario where classe = '" +
		                classe + "' and ESTADO = 'livre'")
		return self.c.fetchall()
		
		
if __name__ == "__main__":
	Banco()
