# -*- encoding: utf-8 -*-
import mysql.connector as mdb
import datetime
from datetime import date, timedelta, time
import time
import random
import string
from random import choice, sample


class Banco(object):
    def __init__(self):
        self.data = ''
        self.loca_armario = 0
        self.conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        self.c = self.conn.cursor(buffered=True)

        self.c.execute('''CREATE TABLE IF NOT EXISTS `tb_armario` (
	                    `id_armario` INT(30) AUTO_INCREMENT,
	                    `classe` TINYTEXT NOT NULL DEFAULT '',
	                    `local` TINYTEXT NOT NULL DEFAULT '',
	                    `terminal` VARCHAR(50) NOT NULL DEFAULT '',
                        `estado` TEXT(7),
	                    PRIMARY KEY (`id_armario`))ENGINE=InnoDB;'''
                       )
        self.c.execute(''' CREATE TABLE IF NOT EXISTS `tb_usuario` (
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
	`senha` TEXT NULL DEFAULT '',
	`id_armario` INT(10)  DEFAULT 0,
	`id_usuario` INT(10)  DEFAULT 0,
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
        self.conn = mdb.connect(
            user='root', password='m1cr0@t805i', database='coolbag')
        self.c = self.conn.cursor(buffered=True)
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.loca_armario = 1
        print('-----dados------')
        print(self.nome)
        print(self.email)
        print(self.telefone)
        print('----fim dados-----')
        self.c.execute("SELECT * from tb_usuario where email='%s' AND telefone='%s'" %
                       (self.email, self.telefone,))
        self.select = self.c.fetchone()
        print('----------- select --------')
        print(self.select)
        if self.select == None:

            self.c.execute("INSERT INTO tb_usuario (id_usuario, nome, email, telefone) values (0,'%s','%s','%s')" % (
                self.nome, self.email, self.telefone,))
            self.conn.commit()
            self.c.execute(
                "SELECT * from tb_usuario where email='%s' AND telefone='%s'" % (self.email, self.telefone))
            consulta = self.c.fetchone()
            return consulta[0]

        else:
            return self.select[0]

        self.con.close()

    def locar_armario(self, nome, email, telefone, dia, hora, minuto , armario):
        self.conn = mdb.connect(user='root', password='m1cr0@t805i', database='coolbag')
        self.c = self.conn.cursor(buffered=True)
        self.__dia = int(dia)
        self.__hora = int(hora)
        self.__minuto = int(minuto)
        self.__armario = str(armario)
        self.__nome = str(nome)
        self.__email = str(email)
        self.__telefone = str(telefone)
        self.__data_locacao = datetime.datetime.now()
        self.__futuro = self.__data_locacao#datetime.datetime(self.adiciona.year, self.adiciona.month, self.adiciona.day, self.__data_locacao.hour, self.__data_locacao.minute)
        self.__futuro = self.__futuro + timedelta(days=self.__dia)# adiciona dias
        self.__futuro = self.__futuro + timedelta(hours=self.__hora) # adiciona horas ao tempo atual
        self.__futuro = self.__futuro + timedelta(minutes=self.__minuto) # adiciona minutos
        self.__data_limite = self.__futuro # registra a data limite para a não cobrança de taxa extra
        self.__data_limite = self.__data_limite + timedelta(minutes=10)# adiciona 10 minutos de tolerancia
       
        self.__senha = ''
        
        self.dados_locatario = self.create_user(
            self.nome, self.email, self.telefone)
        
        self.__senha = self.__get_passwd()
        
        # INSERT INTO tb_locacao (id_locacao, tempo_corrido, data_locacao, tempo_locado,senha,id_armario,id_usuario ) VALUES (null, null,'2019-05-26','5400','e34r',1,1);
        self.c.execute("INSERT INTO tb_locacao (id_locacao, tempo_corrido, data_locacao, tempo_locado,senha,id_armario,id_usuario ) VALUES (NULL, NULL, '%s', '%s',  '%s', %s,%s)" % (self.data, self.__data_limite, self.__senha, self.loca_armario, self.dados_locatario))
        self.conn.commit()
        self.c.execute("UPDATE tb_armario SET estado = 'OCUPADO' where id_armario = %s" % (
            self.loca_armario,))

        self.conn.close()

    def localisa_armario(self, classe):
        self.conn = mdb.connect(
            user='root', password='m1cr0@t805i', database='coolbag')
        self.c = self.conn.cursor(buffered=True)
        result = ()
        self.classe = str(classe)

        self.c.execute(
            "SELECT *  from tb_armario where classe = '%s' and ESTADO = 'LIVRE'" % (self.classe,))
        result = self.c.fetchone()
        print('-----------localisa-------')
        print(result[0])
        print('-----fimlocalisa----')
        if result != None:
            return(result[0])
        else:
            return "nao ha armario disponivel"

        self.conn.close()

    def select_user(self, email, telefone):
        __email = email
        __telefone = telefone
        self.c.execute("SELECT id_usuario from tb_usuario where email='%s' and telefone='%s'" % (
            __email, __telefone))
        query = self.c.fetchall()
        return query

    def __get_passwd(self):
        """ gera a senha automaticamente com combinação aleatória de 2 letras e 2 numeros
        sem ordem predefinida , a ordem dos dígitos também serão aleatórios """
        __password = []
        self.__pass2 = ''
        __alfabet = list(string.ascii_lowercase)
        print('---alfabet-----')
        print(__alfabet)
        for i in range(2):
            __password.append(random.randrange(0, 9))
            __password.append(choice(__alfabet))

        __passwd = sample(__password, len(__password))
        print('===========senha=======')
        print(__passwd)
        print('======fimsenha=========')
        for i in __passwd:
            self.__pass2 += str(i)
        return self.__pass2

    def __send_passwd(self, passwd):
        pass #self.passwd = passwd

    def liberar_armario(self, armario):
        self.con = self.conn
        self.armario = armario
        self.c.execute("ALTER TABLE tb_armario")
        # return(result[0])

    def cadastrar_armario(self, classe, local, terminal):
        self.conn = mdb.connect(
            user='root', password='m1cr0@t805i', database='coolbag')
        self.c = self.conn.cursor(buffered=True)
        self.classe = classe
        self.local = local
        self.terminal = terminal
        self.c.execute("INSERT INTO tb_armario ( id_armario, classe, local, terminal, estado )" +
                       "VALUES (0,%s,%s,%s, 'LIVRE')", (self.classe, self.local, self.terminal))
        self.conn.commit()
        self.conn.close()
    def resgatar_bagagem(self, senha):
        ''' seleciona a locacao conforme a senha fornecida retornando todos os dados:
        id_locacao , id_usuario, id_armario: type int
        data_limite : type datetime
        '''
        
        #self.__email = email
        #self.__telefone = telefone
        self.__senha = senha
        
        self.c.execute("SELECT * FROM tb_locacao where senha = '%s'"% (self.__senha) )
        self.__result = self.c.fetchall()
        print(self.__result)
        return self.__result
        self.__cobranca = self.cobranca(self.result[0][2])# envia a data limite para calculo de tempo excedente
        if self.__cobranca == None:
            self.liberar_armario
        else:
            self.pagamento
        
        
    def cobranca(tempo_locado):
        self.__taxa = 0.15
        """ compara duas datas retornando a diferença de tempo entre as duas
            parametros: data_atual tipo datetime, tempo_locado tipo datetime
            retorno: diferença tipo datetime.timedelta convertido em minutos e calculado o preço conforme 
            taxa por minuto cobrado"""
        self.__data_atual = datetime.datetime.now()
        #self.__data_atual = (int(self.__data_atual.month)*24*3600, int(self.__data_atual.day), int(self.__data_atual.hour), int(self.__data_atual.minute))
        
        self.__tempo_locado = tempo_locado
        self.__tempo_corrido = self.__data_atual -  self.__tempo_locado
        if (self.__tempo_corrido.days and self.__tempo_corrido) == 0:
            return None
        else:
            __total_minutos = (self.__tempo_corrido.days * 24 * 60) + (self.__tempo_corrido.seconds / 60) #calculo do total de tempo excedente em minutos
            __total_minutos = float('{:.2f}'.format(__total_minutos))# formatando o valor para duas casas apos a virgura e convertendo em float
            __total_minutos = __total_minutos * taxa # preço total do excedente
            return __total_minutos

    def pagamento(self, valor):
        pass



        

if __name__ == "__main__":
    Banco()
