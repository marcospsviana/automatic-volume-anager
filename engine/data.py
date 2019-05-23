import sqlite3

class Banco(object):
	def __init__(self):
		conn = sqlite3.connect('coolbag.db')
		c = conn.cursor()
		
		c.execute( '''CREATE TABLE IF NOT EXISTS tb_armario( id_armario INTEGER PRIMARY KEY AUTOINCREMENT,
		                                                    classe TEXT,
		                                                    local  TEXT,
		                                                    livre BOOLEAN,
															porta TEXT,
		                                                    terminal TEXT)'''
		         )
		c.execute( ''' CREATE TABLE IF NOT EXISTS tb_usuario( id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
		               email TEXT, senha TEXT, id_armario INT,
					   FOREIGN KEY(id_armario) REFERENCES tb_armario(id_armario ) )''')
		               
	def locar_armario(self):
		pass
		
	def liberar_armario(self):
		pass

	def cadastrar_armario(self):
		print("cadastrado")
		
if __name__ == "__main__":
	Banco()