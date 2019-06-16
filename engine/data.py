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

        self.nome = str(nome)
        self.email = str(email)
        self.telefone = str(telefone)
        selecao = "SELECT id_usuario from tb_usuario where email= %s AND telefone= %s"

        self.c.execute(selecao, (self.email, self.telefone))
        self.select = self.c.fetchall()

        if self.select == [] or self.select == None:

            self.c.execute("INSERT INTO tb_usuario (id_usuario, nome, email, telefone) values (NULL,'%s','%s','%s')" % (
                self.nome, self.email,  self.telefone))
            self.conn.commit()
            self.c.execute(
                "SELECT id_usuario from tb_usuario where email=%s AND telefone=%s", (self.email, self.telefone,))
            consulta = self.c.fetchall()
            return consulta

        else:
            return self.select

        self.con.close()

    def locar_armario(self, nome, email, telefone, dia, hora, minuto, armario):

        self.__dia = int(dia)
        self.__hora = int(hora)
        self.__minuto = int(minuto)
        self.__armario = str(armario)
        self.__nome = str(nome)
        self.__email = str(email)
        self.__telefone = str(telefone)
        self.__data_locacao = datetime.datetime.now()
        print('=== data locacao ====')
        print(self.__data_locacao)
        # datetime.datetime(self.adiciona.year, self.adiciona.month, self.adiciona.day, self.__data_locacao.hour, self.__data_locacao.minute)
        self.__futuro = self.__data_locacao
        self.__futuro = self.__futuro + \
            timedelta(days=self.__dia)  # adiciona dias
        # adiciona horas ao tempo atual
        self.__futuro = self.__futuro + timedelta(hours=self.__hora)
        self.__futuro = self.__futuro + \
            timedelta(minutes=self.__minuto)  # adiciona minutos
        # registra a data limite para a não cobrança de taxa extra
        self.__data_limite = self.__futuro
        self.__data_limite = self.__data_limite + \
            timedelta(minutes=10)  # adiciona 10 minutos de tolerancia

        self.__senha = ''

        self.dados_locatario = self.create_user(
            self.__nome, self.__email, self.__telefone)
        # seleciona um armario com a classe indicada e recebe seu id
        loca_armario = self.localisa_armario(self.__armario)
        print('======= loca ramario =====')
        print(loca_armario)
        self.c.execute("SET FOREIGN_KEY_CHECKS = 0;")
        # se houver armário livre segue com cadastro de locação
        if (loca_armario != []) or (loca_armario != None):
            self.__senha = self.__get_passwd()
            stmt = ("INSERT INTO `coolbag`.`tb_locacao`(`id_locacao`,`data_locacao`,`tempo_locado`,`tempo_corrido`,`senha`,`id_armario`,`id_usuario`)"
                    "VALUES('%s','%s','%s','%s','%s','%s','%s')")

            self.c.execute(stmt % (0, self.__data_locacao, self.__data_limite,
                                   0, self.__senha, loca_armario[0], self.dados_locatario))
            self.c.execute(
                "UPDATE tb_armario SET estado = 'OCUPADO' where id_armario = %s" % (loca_armario[0]))
            self.conn.commit()
            self.conn.close()
            return "locacao concluida com sucesso"
        else:
            return loca_armario

    def localisa_armario(self, classe):

        result = ()
        self.classe = str(classe)
        # verifica se há armario livre na classe selecionada
        self.c.execute(
            "SELECT id_armario  from tb_armario where classe = '%s' and ESTADO = 'LIVRE'" % (self.classe,))
        result = self.c.fetchall()
        print('-----------localisa-------')
        print(result)
        print('-----fimlocalisa----')
        if (result == []) or (result == None) or (result == 0):
            return "nao ha armario disponivel"

        else:
            return(result)

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
        pass  # self.passwd = passwd

    def liberar_armario(self, armario):
        self.con = self.conn
        self.armario = armario
        self.c.execute("ALTER TABLE tb_armario ")
        # return(result[0])

    def remover_armario(self, id_armario):

        self.__id = id_armario
        self.c.execute(
            "SELECT estado  from tb_armario where id_armario = '%s'" % (self.__id))
        result = self.c.fetchall()
        if result == 'LIVRE':
            self.c.execute(
                "DELETE FROM tb_armario where id_armario = %s " % (self.__id))
        else:
            return "não é possível remover armario, verifique se o mesmo não esta"

    def cadastrar_armario(self, classe, terminal, coluna, nivel):

        self.c = self.conn.cursor(buffered=True)
        self.__classe = classe
        self.__local = 'home'
        self.__terminal = terminal
        self.__coluna = coluna
        self.__nivel = nivel
        self.c.execute("INSERT INTO tb_armario ( id_armario, classe, local, terminal, estado, coluna, nivel )" +
                       "VALUES (0,%s,%s,%s, 'LIVRE', %s, %s)", (self.__classe, self.__local, self.__terminal, self.__coluna, self.__nivel))
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

        self.c.execute(
            "SELECT * FROM tb_locacao where senha = '%s'" % (self.__senha))
        self.__result = self.c.fetchall()
        print(self.__result[0])
        return self.__result[0]
        # envia a data limite para calculo de tempo excedente
        self.__cobranca = self.cobranca(self.result[0][2])
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
        self.__tempo_corrido = self.__data_atual - self.__tempo_locado
        if (self.__tempo_corrido.days and self.__tempo_corrido) == 0:
            return None
        else:
            # calculo do total de tempo excedente em minutos
            __total_minutos = (self.__tempo_corrido.days *
                               24 * 60) + (self.__tempo_corrido.seconds / 60)
            # formatando o valor para duas casas apos a virgura e convertendo em float
            __total_minutos = float('{:.2f}'.format(__total_minutos))
            __total_minutos = __total_minutos * taxa  # preço total do excedente
            return __total_minutos

    def pagamento(self, valor):
        pass


if __name__ == "__main__":
    Banco()
