import sqlite3

Class Banco(object):
	def __init__(self):
		conn = sqlite3.connect('coolbag.db')
		c = conn.cursor()
		
		c.execute( '''CREATE TABLE IF NOT EXISTS tb_armario( id_armario INTEGER PRIMARY KEY AUTOINCREMENT,
		                                                    classe TEXT,
		                                                    local  TEXT,
		                                                    livre BOOLEAN,
		                                                    terminal TEXT)'''
		         )
		c.execute( ''' CREATE TABLE IF NOT EXISTS tb_usuario( id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
		               nome TEXT, senha TEXT, id_armario INT FOREIGN KEY ) ''')
		               
		def locar_armario(self):
			pass
		
		def liberar_armario(self, armario):
			pass
