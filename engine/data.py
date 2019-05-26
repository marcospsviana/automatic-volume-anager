import mysql.connector as mdb
import datetime
import random
import string
from random import choice

class Banco(object):
	def __init__(self):
		self.conn = mdb.connect(user='root', password='microat8051',database='coolbag')
		self.c = self.conn.cursor()




		
		self.c.execute( '''CREATE TABLE IF NOT EXISTS `tb_armario` (
	                    `id_armario` INT(30) AUTO_INCREMENT,
	                    `classe` TINYTEXT NOT NULL DEFAULT '0',
	                    `local` TINYTEXT NOT NULL DEFAULT '0',
	                    `terminal` VARCHAR(50) NOT NULL DEFAULT '0',
						`estado` TEXT(7),
	                    PRIMARY KEY (`id_armario`))ENGINE=InnoDB;'''
		             )
		self.c.execute( ''' CREATE TABLE IF NOT EXISTS `tb_usuario` (
	`id_usuario` INT(10)  AUTO_INCREMENT,
	`nome` VARCHAR(50) NULL DEFAULT NULL,
	`email` VARCHAR(80) NOT NULL,
	`telefone` TEXT NOT NULL,
	PRIMARY KEY (`id_usuario`)
)
ENGINE=InnoDB;''')
		self.c.execute('''CREATE TABLE IF NOT EXISTS `tb_locacao` (
	`id_locacao` INT(10)  AUTO_INCREMENT,
	`data_locacao` DATETIME NOT NULL,
	`tempo_locado` TIME NOT NULL DEFAULT '00:00:00',
	`tempo_corrido` TIME NULL DEFAULT '00:00:00',
	`senha` TEXT NULL DEFAULT '0',
	`id_armario` INT(10)  DEFAULT '0',
	`id_usuario` INT(10)  DEFAULT '0',
	INDEX `id_locacao` (`id_locacao`),
	INDEX `FK__tb_armario` (`id_armario`),
	INDEX `FK__tb_usuario` (`id_usuario`),
	CONSTRAINT `FK__tb_armario` FOREIGN KEY (`id_armario`) REFERENCES `tb_armario` (`id_armario`) ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT `FK__tb_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `tb_usuario` (`id_usuario`) ON UPDATE CASCADE ON DELETE CASCADE
)
ENGINE=InnoDB
;
''')
		               
	def create_user(self, nome, email, telefone):
		self.nome = nome
		self.email = email
		self.telefone = telefone
		consulta = self.c.execute("SELECT id_usuario from tb_usuario where email=%s AND telefone=%s", (self.email, self.telefone))
		if consulta == none:
			self.c.execute("INSERT INTO tb_usuario (id_usuario, nome, email, telefone) values (0,%s,%s,%s)",(self.nome, self.email, self.telefone))
			self.conn.commit()
			consulta = self.c.execute("SELECT id_usuario from tb_usuario where email=%s AND telefone=%s", (self.email, self.telefone))
			return consulta.fetchall()
		else:
			return consulta
		
		return consulta.fetchall()
		
	
	def locar_armario(self, armario, nome, email, telefone):
		self.armario = armario
		self.email = email
		self.hora_locacao = datetime.datetime.now()
		self.loca_armario = self.localisa_armario(self.armario)
		if self.loca_armario == "nao ha armario disponivel":
			print(self.loca_armario)
		else:
			print(self.armario)
		
		self.senha = ''
		self.senha = self.get_passwd()
		
		
	
	def localisa_armario(self, armario):
		self.armario = armario
		result = self.busca_armario(self.armario)
		if result == self.armario:
			return(result[0])
		else:
			return "nao ha armario disponivel"
		

		

	def liberar_armario(self, armario):
		self.con = self.conn
		self.armario = armario
		self.c.execute("ALTER TABLE tb_armario")
		return(result[0])
		

	def cadastrar_armario(self, classe, local, terminal):
		self.classe = classe
		self.local = local
		self.terminal = terminal
		self.c.execute("INSERT INTO tb_armario ( id_armario, classe, local, terminal, estado )"+ 
		                "VALUES (0,%s,%s,%s, 'LIVRE')", (self.classe, self.local, self.terminal))
		self.conn.commit()
		self.conn.close()

	
	def busca_armario(self, classe):
		result = ''
		self.classe = classe
		
		self.c.execute("SELECT *  from tb_armario where classe = '" +
		                self.classe + "' and ESTADO = 'LIVRE'")
		result =  self.c.fetchall()
		return result
		
	
	def get_passwd(self):
		password = []
		alfabet = list(string.ascii_lowercase)
		for i in range(2):
			password.append( random.randrange(0,9))
			password.append(choice(alfabet))
		passwd = random.shuffle(password)
		return password


		
		
if __name__ == "__main__":
	Banco()
