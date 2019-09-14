#!/usr/bin/python3
# -*- coding: utf-8 -*-


import mysql.connector as mdb
import datetime
from datetime import date, timedelta, time
import time
import random
import string
from random import choice, sample
#from .portas import Portas


class Banco(object):
    def __init__(self):
        self.data = ''

        self.__conn = mdb.connect(
            user='root', password='m1cr0@t805i', database='coolbag')
        self.__c = self.__conn.cursor(buffered=True)

        self.__c.execute('''CREATE TABLE IF NOT EXISTS`tb_armario` (
	       `id_armario` INT(30) NOT NULL AUTO_INCREMENT,
	       `classe` TINYTEXT NOT NULL DEFAULT '' COLLATE 'utf8mb4_unicode_ci',
	       `local` TINYTEXT NOT NULL DEFAULT '' COLLATE 'utf8mb4_unicode_ci',
	       `terminal` VARCHAR(50) NOT NULL DEFAULT '' COLLATE 'utf8mb4_unicode_ci',
	       `estado` TINYTEXT NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	       `nivel` TINYTEXT NULL DEFAULT '' COLLATE 'utf8mb4_unicode_ci',
	       `numeracao` TINYTEXT NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	       `porta` TINYTEXT NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	       PRIMARY KEY (`id_armario`)
           )
           COLLATE='utf8mb4_unicode_ci'
           ENGINE=InnoDB
           AUTO_INCREMENT=11
           '''
                       )
        self.__c.execute(''' CREATE TABLE IF NOT EXISTS `tb_usuario` (
	`id_usuario` INT(10)  AUTO_INCREMENT,
	`nome` VARCHAR(50) NULL DEFAULT NULL,
	`email` VARCHAR(80) NOT NULL,
	`telefone` TEXT NOT NULL,
	PRIMARY KEY (`id_usuario`)
)
ENGINE=InnoDB;''')
        self.__c.execute('''CREATE TABLE IF NOT EXISTS `tb_locacao` (
	`id_locacao` INT(10)  AUTO_INCREMENT,
	`data_locacao` DATETIME NOT NULL,
	`tempo_locado` DATETIME NOT NULL,
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
        """ verifica se existe um usuario já cadastrado atraves de busa pelo email
        ou telefone, caso haja , compara o email obtido do banco com o fornecido e o telefone
        obtido com o fornecido , havendo discrepancia ele atualiza o registro. Caso não haver 
        registro algum é feito um novo registro.
        Dados: str: nome
        str: telefone
        str: email
        return: id_usuario  """

        self.nome = str(nome)
        self.email = str(email)
        self.telefone = str(telefone)
        self.__c.execute("SELECT * from tb_usuario where email= '%s' OR telefone= '%s'" % (self.email, self.telefone))
        self.select = self.__c.fetchall()

        if self.select == [] or self.select == None:
            consulta = ''

            self.__c.execute("INSERT INTO tb_usuario (id_usuario, nome, email, telefone) values (null,'%s','%s','%s')" % (self.nome, self.email,  self.telefone))
            self.__conn.commit()
            self.__c.execute("SELECT id_usuario from tb_usuario where email='%s' AND telefone='%s'" % (self.email, self.telefone,))
            consulta = self.__c.fetchall()
            print("-----CONSULTA ID USUARIO-----")
            print(consulta)
            return consulta

        elif self.select[0][2] != self.email and self.select[0][3] == self.telefone:
                self.__c.execute("UPDATE tb_usuario SET email = '%s' WHERE id_usuario = %s"%(self.email, self.select[0][0]))
                self.__conn.commit()
                
                return self.select[0][0]# id_usuario
        elif self.select[0][2] == self.email and self.select[0][3] != self.telefone:
                self.__c.execute("UPDATE tb_usuario SET telefone = '%s' WHERE id_usuario = %s"%(self.telefone, self.select[0][0]))
                self.__conn.commit()
                return self.select[0][0]
        else:
            return self.select[0][0]
            

        self.__conn.close()

    def locar_armario(self, nome, email, telefone, dia, hora, minuto, armario):
        #self.port = Portas()
        dia = dia
        dia = dia.replace(".0","")
        self.__dia = int(dia)
        self.__hora = int(hora.replace(".0",""))
        minuto = minuto
        print("minuto---*",minuto)
        minuto = int(minuto.replace(".0",""))
        
        self.__minuto = minuto
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
            datetime.timedelta(days=self.__dia)  # adiciona dias
        # adiciona horas ao tempo atual
        self.__futuro = self.__futuro + datetime.timedelta(hours=self.__hora)
        self.__futuro = self.__futuro + \
            datetime.timedelta(minutes=self.__minuto)  # adiciona minutos
        # registra a data limite para a não cobrança de taxa extra
        self.__data_limite = self.__futuro

        self.__data_limite = self.__data_limite + \
            datetime.timedelta(minutes=10)  # adiciona 10 minutos de tolerancia
        print("data limite para salvar no banco", self.__data_limite)

        self.__senha = ''

        self.dados_locatario = self.create_user(
            self.__nome, self.__email, self.__telefone)
        print("dados locatario data.py locacao===>", self.dados_locatario)
        # seleciona um armario com a classe indicada e recebe seu id
        loca_armario = self.localisa_armario(self.__armario)
        print('======= loca ramario =====')
        print(loca_armario)
        #self.__c.execute("SET FOREIGN_KEY_CHECKS = 0;")
        # se houver armário livre segue com cadastro de locação
        if (loca_armario != []) or (loca_armario != None):
            self.__senha = self.__get_passwd()
            print("==== id_armario, id_usuario ======")
            #print(loca_armario[0], self.dados_locatario[0])
            self.__c.execute("INSERT INTO tb_locacao(id_locacao, data_locacao,tempo_locado,tempo_corrido,senha,id_armario,id_usuario) VALUES(null, '%s','%s',null,'%s',%s,%s)"% (self.__data_locacao, self.__data_limite, self.__senha, loca_armario[0], self.dados_locatario))
            
            self.__c.execute("UPDATE tb_armario SET estado = 'OCUPADO' where id_armario = %s" % (loca_armario[0]))
            
            self.__conn.commit()
            self.__conn.close()
            return "locacao concluida com sucesso"
            
            ##port = self.select_port(loca_armario[0])
            #self.port.exec_port(str(port[0][0]), "abre")
        else:
            return loca_armario
    def select_port(self, armario):
        __armario = armario
        self.__c.execute("SELECT porta FROM coolbag.tb_armario where id_armario = %s"%(__armario))
        self.retorno_porta = self.__c.fetchall()
        return self.retorno_porta


    def localisa_armario(self, classe):

        result = ()
        self.__classe = str(classe)
        # verifica se há armario livre na classe selecionada
        self.__c.execute(
            "SELECT id_armario  from tb_armario where classe = '%s' and ESTADO = 'LIVRE' ORDER BY id_armario" % (self.__classe,))
        result = self.__c.fetchall()
        print('-----------localisa-------')
        print(result)
        print('-----fimlocalisa----')
        if (result == []) or (result == None) or (result == 0):
            return "nao ha armario disponivel"

        else:
            return(result[0])

        

    @staticmethod
    def select_user(password):
        __conn = mdb.connect(
            user='root', password='m1cr0@t805i', database='coolbag')
        __c = __conn.cursor(buffered=True)
        __password = password
        
        print("nome ou mail select user",__password)
        query = ''
        __c.execute("SELECT id_usuario FROM tb_locacao where senha = '"+ __password +"'")
        query = __c.fetchall()
        print("##### id usuario ###")
        print(query)
        if query == []:
            return 'senha incorreta, tente novamente'
        else:
            return query
        __conn.close()

    def __get_passwd(self):
        """ gera a senha automaticamente com combinação aleatória de 2 letras e 2 numeros
        sem ordem predefinida , a ordem dos dígitos também serão aleatórios """
        __password = []
        self.__pass2 = ''
        __alfabet = list(string.ascii_letters)
        print('---alfabet-----')
        print(__alfabet)
        
        while len(__password) < 4:
            result  = random.randrange(0, 9)
            if result not in __password:
                __password.append(result)
            
            add_alfa = choice(__alfabet)
            if add_alfa not in __password:
                __password.append(add_alfa)
            print(__password)

        __passwd = sample(__password, len(__password))
        print('===========senha=======')
        print(__passwd)
        print('======fimsenha=========')
        for i in __passwd:
            self.__pass2 += str(i)
        return self.__pass2

    def __send_passwd(self, passwd):
        pass  # self.passwd = passwd
    
    
    @staticmethod
    def get_locacao(senha, id_usuario):
        __conn = mdb.connect(
            user='root', password='m1cr0@t805i', database='coolbag')
        __c = __conn.cursor(buffered=True)
        result = ''
        __senha = senha
        print('---senha---',__senha)
        __id_user = id_usuario
        print('*** id usuario *** ', __id_user)
        print(__senha)
        __c.execute("SELECT id_armario, id_locacao, tempo_locado from tb_locacao where senha = '%s' AND id_usuario = %s" %(__senha,__id_user[0]))
        #for reg in __c.next_proc_resultset():
        __result = __c.fetchall()
        print("888888 ---- result")
        print(__result)
        return __result
        __conn.close()


    def liberar_armario(self, senha):
        
        result = ''
        id_armario = ''
        taxa = 0.15
        hj = datetime.datetime.now()
        #hj = datetime.timedelta( hj.hour, hj.minute, hj.second)
        #hj = hj + datetime.timedelta(minutes=+10)
        print("hj", hj)
        self.__senha = senha
        print('nome e senha de data', self.__senha, self.__nome)
        self.__id_user = self.select_user(self.__senha)
        if self.__id_user == 'senha incorreta, tente novamente':
            return 'senha incorreta, tente novamente'
        
        else:
            self.__locacao = self.get_locacao(self.__senha, self.__id_user[0])
            print('********** dados locacao **************')
            print("self.locacao", self.__locacao)
            print("self.locacao[0][2]",self.__locacao[0][2])
            print("self.locacao[0 0]", self.__locacao[0][0])
            if (self.__locacao[0][2]) > hj:
                
                tempo_total = hj - self.__locacao[0][2]
                dias_passados = tempo_total.days
                minutos_passados = tempo_total.seconds / 60
                valor_total = ((dias_passados * 24 * 60) + minutos_passados) * taxa
                result = self.cobranca(valor_total,hj)
                
                self.__c.execute("DELETE FROM tb_locacao WHERE senha = '%s'" % (self.__senha,))
                self.__c.execute("UPDATE tb_armario set estado = 'LIVRE' WHERE id_armario = %s" % (self.__locacao[0][0]))
                self.__conn.commit()
                self.__conn.close()
                return "armario liberado"
                port = self.select_port(self.__locacao[0][0])
                self.port.exec_port(port[0], "abre")
            else:
                
                tempo = hj - self.__locacao[0][2] 
                tempo = (tempo.days * 24 * 60) + ( tempo.seconds / 60 )
                print('-------> %s'%tempo)
                result = self.cobranca_excedente(int(tempo))
                return result


    def remover_armario(self, id_armario):

        self.__id = id_armario
        self.__c.execute(
            "SELECT estado  from tb_armario where id_armario = '%s'" % (self.__id))
        result = self.__c.fetchall()
        if result == 'LIVRE':
            self.__c.execute(
                "DELETE FROM tb_armario where id_armario = %s " % (self.__id))
        else:
            return "não é possível remover armario, verifique se o mesmo não está em uso"

    def cadastrar_armario(self, classe, terminal, coluna, nivel):

        self.__c = self.__conn.cursor(buffered=True)
        self.__classe = classe
        self.__local = 'home'
        self.__terminal = terminal
        self.__coluna = coluna
        self.__nivel = nivel
        self.__c.execute("INSERT INTO tb_armario ( id_armario, classe, terminal, local, estado, nivel )" +
                       "VALUES (0,%s,%s,%s, 'LIVRE', %s)", (self.__classe, self.__terminal, self.__coluna, self.__nivel))
        result = self.__c.fetchone()
        self.__conn.commit()
        self.__conn.close()
        return (self.__classe, self.__coluna, self.__nivel, self.__terminal, "cadastrado com sucesso")

    def resgatar_bagagem(self, senha):
        ''' seleciona a locacao conforme a senha fornecida retornando todos os dados:
        id_locacao , id_usuario, id_armario: type int
        data_limite : type datetime
        libera armario após ser confirmado e verificar que não haja saldo devedor
        saldo devedor calculo: data atual datetime - tempo_locado datetime 
        
        if finalizar == True:
            pass'''

        #self.__email = email
        #self.__telefone = telefone
        self.__senha = senha

        self.__c.execute(
            "SELECT * FROM tb_locacao where senha = '%s'" % (self.__senha))
        self.__result = self.__c.fetchall()
        print('resgatar_bagagem result---->', self.__result)
        print(self.__result[0])
        return self.__result[0]
        # envia a data limite para calculo de tempo excedente
        self.__cobranca = self.__cobranca(self.result[0][2])
        if self.__cobranca == None:
            self.liberar_armario(self.__senha)
        else:
            return ('tempo excedente',self.__cobranca)

    @classmethod
    def cobranca(self, total, data_futura):
        """ compara duas datas retornando a diferença de tempo entre as duas
            parametros: data_atual tipo datetime, tempo_locado tipo datetime
            retorno: diferença tipo datetime.timedelta convertido em minutos e calculado o preço conforme 
            taxa por minuto cobrado"""
        
        self.__TAXA = 0.15 
        self.__data_atual = data_futura
        #self.__data_futura = data_futura
        self.__tempo_locado = total
        #self.__tempo_corrido = self.__data_futura - self.__data_atual
        '''if (self.__tempo_corrido.days and self.__tempo_corrido) <= 0:
            return None
        else:'''
        
        __total_preco = self.__tempo_locado * self.__TAXA  # preço total do excedente
        __total_preco = "%.2f"%(__total_preco) # formatando para duas casas decimais apos virgula
        __total_preco = str(__total_preco.replace('.',',')) #troca ponto por virgula pra formatar em moeda BR
        print('modulo data')
        return __total_preco

    @staticmethod
    def cobranca_excedente(tempo):

        message = "tempo excedido cobrança de R$ : %s"
        taxa = 0.15
        print('22222222222 tempo 222222222222')
        print(tempo)
        
        __excedente = float(tempo)
        total = __excedente * taxa
        total = "%.2f"%total
        print ('$$$$$$$ total $$$$ %s' % total)
        return (total )
    
    def finalizar(self,senha):
        
        result = ''
        id_armario = ''
        taxa = 0.15
        hj = datetime.datetime.now()
        hj = datetime.datetime(hj.year, hj.month, hj.day, hj.hour, hj.minute, hj.second)
        hj = hj + datetime.timedelta(minutes=+10)
        
        self.__senha = senha
        
        print('senha e nome finalizar', self.__senha)
        self.__id_user = self.select_user(self.__senha)
        if self.__id_user == 'senha, email ou telefone incorretos, tente novamente':
            return 'senha, email ou telefone incorretos, tente novamente'
        
        else:
            self.__locacao = self.get_locacao(self.__senha, self.__id_user[0])
            if (self.__locacao[0][2]) >= hj:
                
                tempo_total = hj - self.__locacao[0][2]
                dias_passados = tempo_total.days
                minutos_passados = tempo_total.seconds / 60
                valor_total = ((dias_passados * 24 * 60) + minutos_passados) * taxa
                result = self.cobranca(valor_total,hj)
                
                self.__c.execute("DELETE FROM tb_locacao WHERE senha = '%s'" % (self.__senha,))
                self.__c.execute("UPDATE tb_armario set estado = 'LIVRE' WHERE id_armario = '%s'" % (self.__locacao[0][0],))
                self.__conn.commit()
                self.__conn.close()
                return "armario liberado"
                port = self.select_port(self.__locacao[0][0])
                self.port.exec_port(port[0], "abre")
            else:
                
                tempo = hj - self.__locacao[0][2] 
                tempo = (tempo.days * 24 * 60) + ( tempo.seconds / 60 )
                print('-------> %s'%tempo)
                result = self.cobranca_excedente(int(tempo))
                return result
        

    
    @staticmethod
    def listar_classes_armarios():
        __conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        __c = __conn.cursor(buffered=True)
        __classes = []
        result = ''
        __c.execute("SELECT classe FROM tb_armario WHERE estado = 'LIVRE'")
        result = __c.fetchall()
        print('result listar classes data', result)
        return result
        __conn.close()
    
    def seleciona_classe(self, classe):
        self.classe = classe
        print('classe recebida data', self.classe)
        __conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        __c = __conn.cursor(buffered=True)
        __classes = []
        result = ''
        __c.execute("select classe from tb_armario where estado = 'LIVRE' and classe = '%s'"%self.classe)
        result = __c.fetchall()
        print('result data classe', result)
        return result
        __conn.close()
    
    @classmethod
    def abrir_armario(self,senha):
        print('senha data', senha)
        result = ''
        id_armario = ''
        taxa = 0.15
        hj = datetime.datetime.now()
        hj = datetime.datetime(hj.year, hj.month, hj.day, hj.hour, hj.minute, hj.second)
        hj = hj + datetime.timedelta(minutes=+10)
        
        self.__senha = senha
        self.__id_user = self.select_user(self.__senha)
        if self.__id_user == 'senha incorreta, tente novamente':
            return 'senha incorreta, tente novamente'
        
        else:
            self.__locacao = self.get_locacao(self.__senha, self.__id_user[0])
            
            print('********** dados locacao **************')
            print(self.__locacao[0][2])
            if (self.__locacao[0][2]) >= hj:
                
                tempo_total = hj - self.__locacao[0][2]
                dias_passados = tempo_total.days
                minutos_passados = tempo_total.seconds / 60
                valor_total = ((dias_passados * 24 * 60) + minutos_passados) * taxa
                result = self.cobranca(valor_total,hj)
                
                self.__c.execute("SELECT id_armario FROM tb_locacao WHERE senha = '%s'" % (self.__senha,))
                self.__conn.commit()
                self.__conn.close()
                return "armario liberado"
                port = self.select_port(loca_armario[0][0])
                self.port.exec_port(port, "abre")
            else:
                
                tempo = hj - self.__locacao[0][2] 
                tempo = (tempo.days * 24 * 60) + ( tempo.seconds / 60 )
                print('-------> %s'%tempo)
                result = self.cobranca_excedente(int(tempo))
                return result
    def finalizar_pagamento(self, senha):
        __conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        __c = __conn.cursor(buffered=True)
        __senha = senha
        #__nome = nome
        #__id_user = self.select_user(__nome)
        #__locacao = self.get_locacao(__senha, __id_user[0])
        __c.execute("DELETE FROM tb_locacao WHERE senha = '%s'"%(__senha))
        id_armario = __c.execute("SELECT id_armario FROM tb_locacao WHERE senha = '%s'" % (__senha,))
        print("finaliza_pagamento id armario", id_armario)
        self.__c.execute("UPDATE tb_armario set estado = 'LIVRE' WHERE id_armario = '%s'" % (id_armario,))
        __conn.commit()
        return "locacao finalizada com sucesso"
        __conn.close()





if __name__ == "__main__":
    Banco()
