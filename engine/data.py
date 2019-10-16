#!/usr/bin/python3
# -*- coding: utf-8 -*-


import mysql.connector as mdb
import datetime
from datetime import date, timedelta, time
import time
import random
import string
from random import choice, sample
import pandas as pd
import smtplib
import json
#from .portas import Portas


class Banco(object):
    def __init__(self):
        self.data = ''
        global TAXA_HORA_A, TAXA_HORA_B, TAXA_HORA_C, TAXA_HORA_D
        global TAXA_DIARIA_A, TAXA_DIARIA_B, TAXA_DIARIA_C, TAXA_DIARIA_D
        TAXA_DIARIA_A = 37.5
        TAXA_DIARIA_B = 24.5
        TAXA_DIARIA_C = 14.5
        TAXA_DIARIA_D = 9.0
        TAXA_HORA_A = 2.10
        TAXA_HORA_B = 1.56
        TAXA_HORA_C = 1.05
        TAXA_HORA_D = 0.6

        self.__conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
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
           `compartimento` TINYTEXT NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
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
  `id_locacao` int(10) NOT NULL AUTO_INCREMENT,
  `data_locacao` datetime NOT NULL,
  `tempo_locado` datetime NOT NULL,
  `tempo_corrido` time DEFAULT '00:00:00',
  `senha` tinytext COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_armario` int(10) NOT NULL DEFAULT 0,
  `id_usuario` int(10) NOT NULL DEFAULT 0,
  KEY `id_locacao` (`id_locacao`),
  KEY `FK__tb_armario` (`id_armario`),
  KEY `FK__tb_usuario` (`id_usuario`),
  CONSTRAINT `FK__tb_armario` FOREIGN KEY (`id_armario`) REFERENCES `tb_armario` (`id_armario`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK__tb_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `tb_usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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

        self.nome = str(nome).lower()
        self.email = str(email).lower()
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

    def locar_armario(self, nome, email, telefone, dia, hora, minuto, armario, language, total):
        #self.port = Portas()
        dia = dia
        dia = dia.replace(".0","")
        self.__dia = int(dia)
        self.__hora = int(hora.replace(".0",""))
        minuto = minuto
        print("minuto---*",minuto)
        minuto = int(minuto.replace(".0",""))
        self.__total = total
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
        
        #print('======= loca ramario =====')
        #print(loca_armario)
        #self.__c.execute("SET FOREIGN_KEY_CHECKS = 0;")
        # se houver armário livre segue com cadastro de locação
        retorno = self.pagamento_locacao(self.__total)
        if retorno == "lk4thHG34=GKss0xndhe":
            self.__senha = self.__get_passwd()
            #self.__hash_senha = hashlib.sha3_512(b"%s"%self.__senha).hexdigest()
            print("==== id_armario, id_usuario ======")
            #print(loca_armario[0], self.dados_locatario[0])
            self.__c.execute("INSERT INTO tb_locacao(id_locacao, data_locacao,tempo_locado,tempo_corrido,senha,id_armario,id_usuario) VALUES(null, '%s','%s',null,'%s',%s,%s)"% (self.__data_locacao, self.__data_limite, self.__senha, loca_armario[0], self.dados_locatario))
            
            self.__c.execute("UPDATE tb_armario SET estado = 'OCUPADO' where id_armario = %s" % (loca_armario[0]))
            
            self.__conn.commit()

            #self.__c.execute("select data_locacao, tempo_locado, senha from tb_locacao where id_armario= %s" %(loca_armario[0]))
            query_select = "select senha from tb_locacao where id_armario= %s" %(loca_armario[0])
            data_and_passwd = pd.read_sql(query_select, self.__conn)
            compartimento = "select compartimento from tb_armario where id_armario = %s" %(loca_armario[0])
            compartimento_select = pd.read_sql(compartimento, self.__conn)
            self.__data_locacao = str(self.__data_locacao)
            self.__data_limite = str(self.__data_limite)
            mes_locacao = str(self.__data_locacao[5:7])
            dia_locacao = str(self.__data_locacao[8:10])
            mes_locado = str(self.__data_limite[5:7])
            dia_locado = str(self.__data_limite[8:10])
            senha = data_and_passwd.head().values[0]
            compartimento = compartimento_select.head().values[0]
            hora_locacao = str(self.__data_locacao[11:16])
            hora_locada = str(self.__data_limite[11:16])
            data_locacao = dia_locacao + "/" + mes_locacao
            tempo_locado = dia_locado + "/" + mes_locado
            #self.send_email(self.__nome, self.__email, senha[0], compartimento[0], data_locacao, hora_locacao, tempo_locado,  hora_locada, language)

            #query_select = self.__c.fetchall()
            
            print("result locacao" , query_select)
            
            
            port = self.select_port(loca_armario[0])
            print("porta selecionada", port[0][0])
            # HABILILAR NO RASPBERRY PI self.port.exec_port(str(port[0][0]), "abre")
            return ("locacao concluida com sucesso", data_locacao, hora_locacao, tempo_locado, hora_locada, senha, compartimento)
        elif retorno == "houve um problema com o pagamento":
            return loca_armario
        self.__conn.close()
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
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        __c = __conn.cursor(buffered=True)
        __password = password
        
        print("nome ou mail select user",__password)
        query = ''
        __c.execute("SELECT id_usuario FROM tb_locacao where senha = '"+ __password +"'")
        query = __c.fetchall()
        print("##### id usuario ----")
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
        __alfabet = list(string.ascii_uppercase)
        __num = list(range(10))
        for n in __num:
            __alfabet.append(n)
        
        while len(__password) < 4:
            """result  = random.randrange(0, 9)
            if result not in __password:
                __password.append(result)"""
            
            add_alfa = choice(__alfabet)
            if add_alfa not in __password:
                __password.append(add_alfa)
            if len(__password) == 4:
                self.__c.execute("select senha from tb_locacao")
                comparativo = self.__c.fetchall()
                if __password in comparativo:
                    __password = ""
                else:
                    __passwd = sample(__password, len(__password))
                    print('===========senha=======')
                    print(__passwd)
                    print('======fimsenha=========')
                    for i in __passwd:
                        self.__pass2 += str(i)

            print(__password)

       
        return self.__pass2

    def __send_passwd(self, passwd):
        pass  # self.passwd = passwd
    
    
    @staticmethod
    def get_locacao(senha):
        __conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        __c = __conn.cursor(buffered=True)
        result = ''
        __senha = senha
        print('---senha---',__senha)
        #__id_user = id_usuario
        #print('*** id usuario *** ', __id_user[0])
        #print(__senha)
        #__c.execute("SELECT id_armario, id_locacao, tempo_locado, data_locacao from tb_locacao where senha = '%s' AND id_usuario = %s" %(__senha,__id_user[0]))
        dados = pd.read_sql("SELECT id_armario, id_locacao, tempo_locado, data_locacao from tb_locacao where senha = '%s'" %(__senha), __conn)
        #for reg in __c.next_proc_resultset():
        #__result = __c.fetchall()
        #print("888888 ---- result")
        #print(__result)
        print("dados get_locacao", dados)
        return (dados )
        __conn.close()


    def liberar_armario(self, senha):
        
        result = ''
        id_armario = ''
        hj = datetime.datetime.now()
        hj = pd.to_datetime(hj, unit='ns')
        #hj = datetime.timedelta( hj.hour, hj.minute, hj.second)
        #hj = hj + datetime.timedelta(minutes=+10)
        print("hj", hj)
        self.__senha = senha
        print('nome e senha de data', self.__senha)
        self.__id_user = self.select_user(self.__senha)
        if self.__id_user == 'senha incorreta, tente novamente':
            return 'senha incorreta, tente novamente'
        
        else:
            self.__locacao = self.get_locacao(self.__senha)
            print('********** dados locacao **************')
            print("self.locacao", self.__locacao.head())
            print("self.locacao[0][2]",self.__locacao[0][2])
            print("self.locacao[0 0]", self.__locacao[0][0])
            if (self.__locacao[0][2]) > hj:
                
                tempo_total = hj - self.__locacao['tempo_locado'][0]
                dias_passados = tempo_total.components.days
                #minutos_passados = tempo_total.seconds / 60
                minuto = tempo_total.components.minutes
                horas_passadas = tempo_total.components.hours
                #valor_total = ((dias_passados * 24 * 60) + minutos_passados) * taxa
                calculo_minuto = 0
                
                if minuto <= 15 and minuto > 5:
                    calculo_minuto = (1/4) 
                elif minuto > 15 and minuto <= 30:
                    calculo_minuto = (2/4) 
                elif minuto > 15 and minuto <= 30:
                    calculo_minuto = (3/4) 
                valor_total = ((dias * taxa) + (hora * TAXA) + calculo_minuto * TAXA)


                #valor_total = ((dias_passados * 24) + horas_passadas ) * taxa_hora + valor_taxa_15
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
                dias = tempo.days 
                horas = tempo.seconds // 3600
                minutos = tempo.seconds % 3600
                tempo = (tempo.days * 24 * 60) + ( tempo.seconds // 3600 ) + tempo.seconds % 60
                print('-------> %s'%tempo)
                result = self.cobranca_excedente(dias, horas, minutos)
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

    def cadastrar_armario(self, classe, terminal, coluna, nivel, porta, compartimento):

        self.__c = self.__conn.cursor(buffered=True)
        self.__classe = classe
        self.__local = 'home'
        self.__terminal = terminal
        self.__coluna = coluna
        self.__nivel = nivel
        self.__porta = porta
        self.__compartimento = compartimento
        self.__c.execute("INSERT INTO tb_armario ( id_armario, classe, terminal, local, estado, nivel, porta, compartimento )" +
                       "VALUES (0,%s,%s,%s, 'LIVRE', %s, %s, %s)", (self.__classe, self.__terminal, self.__coluna, self.__nivel, self.__porta, self.__compartimento))
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
        
        
        self.__data_atual = data_futura
        #self.__data_futura = data_futura
        self.__tempo_locado = total
        #self.__tempo_corrido = self.__data_futura - self.__data_atual
        '''if (self.__tempo_corrido.days and self.__tempo_corrido) <= 0:
            return None
        else:'''
        
        __total_preco = self.__tempo_locado * TAXA  # preço total do excedente
        __total_preco = "%.2f"%(__total_preco) # formatando para duas casas decimais apos virgula
        __total_preco = str(__total_preco.replace('.',',')) #troca ponto por virgula pra formatar em moeda BR
        print('modulo data')
        return __total_preco

    @staticmethod
    def cobranca_excedente(dias, hora, minuto, id_armario):
        __conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        calculo_minuto = 0
        __minuto = minuto
        classe_armario = pd.read_sql("select classe from tb_armario where id_armario = %s"% id_armario, __conn)
        classe = str(classe_armario['classe'][0])
        if __minuto <= 15 and minuto > 5:
            calculo_minuto = (1/4) 
        elif __minuto > 15 and minuto <= 30:
            calculo_minuto = (2/4) 
        elif __minuto > 30 and minuto <= 45:
            calculo_minuto = (3/4) 
        if classe == "A":
            valor_total = ((dias * TAXA_DIARIA_A) + (hora * TAXA_HORA_A) + calculo_minuto * TAXA_HORA_A)
        elif classe == "B":
            valor_total = ((dias * TAXA_DIARIA_B) + (hora * TAXA_HORA_B) + calculo_minuto * TAXA_HORA_B)
        elif classe == "C":
            valor_total = ((dias * TAXA_DIARIA_C) + (hora * TAXA_HORA_C) + calculo_minuto * TAXA_HORA_c)
        elif classe == "D":
            valor_total = ((dias * TAXA_DIARIA_D) + (hora * TAXA_HORA_D) + calculo_minuto * TAXA_HORA_D)
        
        #valor_total = ((dias *24 * 15) + (hora * TAXA) + calculo_minuto * TAXA)
        message = "tempo excedido cobrança de R$ : %s"% valor_total
        
        print('22222222222 tempo 222222222222')
        print(valor_total)
        
        __excedente = float(valor_total)
        #total = __excedente * taxa
        total = "%.2f"%valor_total
        print ('$$$$$$$ total $$$$ %s' % total)
        return (total )
    
    def finalizar(self,senha):
        taxa = 15
        result = ''
        id_armario = ''
        
        hj = datetime.datetime.now()
        hj = datetime.datetime(hj.year, hj.month, hj.day, hj.hour, hj.minute, hj.second)
        #hj = hj + datetime.timedelta(minutes=+10)
        hj = pd.to_datetime(hj)
        
        self.__senha = senha
        
        print('senha e nome finalizar', self.__senha)
        self.__id_user = self.select_user(self.__senha)
        if self.__id_user == 'senha incorreta, tente novamente':
            return 'senha incorreta, tente novamente'
        
        else:
            self.__locacao = self.get_locacao(self.__senha)
            if (self.__locacao['tempo_locado'][0]) >= hj:
                
                tempo_total = hj - self.__locacao['tempo_locado'][0]
                dias_passados = tempo_total.days
                minutos_passados = tempo_total.seconds / 60
                calculo_hora = tempo_total // 3600
                calculo_minuto = 0
                if minutos_passados <= 15 and minutos_passados > 5:
                    calculo_minuto = (1/4) 
                elif minutos_passados > 15 and minutos_passados <= 30:
                    calculo_minuto = (2/4) 
                elif minutos_passados > 15 and minutos_passados <= 30:
                    calculo_minuto = (3/4) 
                valor_total = ((dias_passados * 24 * 60) * 50)
                valor_total = valor_total + (calculo_minuto * taxa )
                valor_total = valor_total + calculo_hora * 15
                result = self.cobranca_excedente(dias_passados, calculo_hora, calculo_minuto)#(valor_total,hj) 
                
            
            
                self.__c.execute("DELETE FROM tb_locacao WHERE senha = '%s'" % (self.__senha,))
                self.__c.execute("UPDATE tb_armario set estado = 'LIVRE' WHERE id_armario = '%s'" % (self.__locacao[0][0],))
                self.__conn.commit()
                self.__conn.close()
                return "armario liberado"
                port = self.select_port(self.__locacao[0][0])
                self.port.exec_port(port[0], "abre")
                      
            else:
                query_data_locacao = "select data_locacao from tb_locacao where senha = '%s'"%self.__senha
                query_data_limite = "select tempo_locado from tb_locacao where senha = '%s'"%self.__senha
                self.__c.execute("select dayname(data_locacao) from tb_locacao where senha = '%s'"%self.__senha)
                query_dia_semana_locacao = self.__c.fetchone()
                self.__c.execute("select dayname(tempo_locado) from tb_locacao where senha = '%s'"%self.__senha)
                query_dia_semana_locado = self.__c.fetchone()
                df_data_locacao = pd.read_sql(query_data_locacao, self.__conn)
                data_locacao = str(pd.to_datetime(df_data_locacao.head().values[0][0]))#data em que foi feita a locacao
                df_data_limite = pd.read_sql(query_data_limite, self.__conn)
                data_limite = str(pd.to_datetime(df_data_limite.head().values[0][0])) #data e hora final da locacao
                mes_locacao = data_locacao[5:7] # mes da locacao
                dia_locacao = data_locacao[8:10] #dia da locacao
                hora_locacao = data_locacao[11:16]
                mes_locado = data_limite[5:7]
                dia_locado = data_limite[8:10]
                hora_locado = data_limite[11:16]
                #dia_da_semana_locacao = pd.to_datetime(df_data_locacao.head().values[0][0]).day_name
                #dia_da_semana_locado = pd.to_datetime(df_data_limite.head().values[0][0]).day_name
            
                data_locacao = dia_locacao + "/" + mes_locacao
                tempo_locado = dia_locado + "/" + mes_locado
                tempo = hj - self.__locacao['tempo_locado'][0]
                __dia_extra = tempo.days
                __hora_extra = tempo.seconds//3600 #hj.hour - self.__locacao[0][2].hour
                minuto = tempo.seconds/3600        
                __minuto_extra = (tempo.seconds%3600)//60 #hj.minute - self.__locacao[0][2].minute
                
                tempo = (tempo.days * 24 * 60) + ( tempo.seconds / 60 )
                print('-------> %s'%tempo)
                result = self.cobranca_excedente(__dia_extra, __hora_extra, __minuto_extra)
                dados_locacao = {
                                "total": result,
                                "data_locacao": data_locacao, 
                                "tempo_locado": tempo_locado, 
                                "dia_locacao":query_dia_semana_locacao[0], 
                                "dia_limite": query_dia_semana_locado[0], 
                                "hora_locacao":hora_locacao, 
                                "hora_locado":hora_locado, 
                                "dia_extra": __dia_extra, 
                                "hora_extra":__hora_extra, 
                                "minuto_extra":__minuto_extra 
                                }
                return dados_locacao
    def send_email(self, nome, email, senha, compartimento, data_locacao, hora_inicio_locacao, data_limite,  hora_fim_locacao, language):
        __server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        __server.login("marcospaulo.silvaviana@gmail.com", "m1cr0@t805i")
        __nome = string.capwords(nome)
        if language == "pt_BR":
            __message = " Este e-mail foi enviado de forma automática , não responda diretamente a este e-mail!\n\n Obrigado por utilizar nossos serviços %s, abaixo encontra-se os seus dados de acesso para liberação do compartimento:\n\
                COMPARTIMENTO:  %s \n SENHA: %s\n DATA LOCAÇÃO: %s %s \n DATA LIMITE: %s %s\n "%(__nome, compartimento, senha, data_locacao, hora_inicio_locacao, data_limite, hora_fim_locacao)
        elif language == "en_US":
            __message = "This email was sent automatically, please do not reply directly to this email! Thanks for using our services %s, below is your compartment release access details:\n \
                COMPARTMENT: %s \n PASSWORD: %s \n DATE RENT: %s %s \n DEADLINE: %s %s \n"%(__nome, compartimento, senha, data_locacao, hora_inicio_locacao, data_limite, hora_fim_locacao)

        __mail_from = "marcospaulo.silvaviana@gmail.com"
        __mail_to = email.lower()
        __server.sendmail(__mail_from, __mail_to, __message.encode("utf8"))
        __server.quit()


        

    
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
        __conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        __cursor = __conn.cursor()
        print('senha data', senha)
        result = ''
        id_armario = ''
        taxa = 15
        hj = datetime.datetime.now()
        hj = datetime.datetime(hj.year, hj.month, hj.day, hj.hour, hj.minute, hj.second)
        
        
        self.__senha = senha
        self.__id_user = self.select_user(self.__senha)
        if self.__id_user == 'senha incorreta, tente novamente':
            return 'senha incorreta, tente novamente'
        
        else:
            self.__locacao = self.get_locacao(self.__senha)
            
            print('********** dados locacao **************')
            print(self.__locacao['tempo_locado'][0])
            if (self.__locacao['tempo_locado'][0]) >= hj:
                              
                #self.__c.execute("SELECT id_armario FROM tb_locacao WHERE senha = '%s'" % (self.__senha,))
                #self.__conn.commit()
                #self.__conn.close()
                return "armario liberado"
                port = self.select_port(loca_armario[0][0])
                self.port.exec_port(port, "abre")
            else:
                query_data_locacao = "select data_locacao from tb_locacao where senha = '%s'"%self.__senha
                query_data_limite = "select tempo_locado from tb_locacao where senha = '%s'"%self.__senha
                __cursor.execute("select dayname(data_locacao) from tb_locacao where senha = '%s'"%self.__senha)
                query_dia_semana_locacao = __cursor.fetchone()
                __cursor.execute("select dayname(tempo_locado) from tb_locacao where senha = '%s'"%self.__senha)
                query_dia_semana_locado = __cursor.fetchone()
                df_data_locacao = pd.read_sql(query_data_locacao, __conn)
                data_locacao = str(pd.to_datetime(df_data_locacao.head().values[0][0]))#data em que foi feita a locacao
                df_data_limite = pd.read_sql(query_data_limite, __conn)
                data_limite = str(pd.to_datetime(df_data_limite.head().values[0][0])) #data e hora final da locacao
                mes_locacao = data_locacao[5:7] # mes da locacao
                dia_locacao = data_locacao[8:10] #dia da locacao
                hora_locacao = data_locacao[11:16]
                mes_locado = data_limite[5:7]
                dia_locado = data_limite[8:10]
                hora_locado = data_limite[11:16]
                #dia_da_semana_locacao = pd.to_datetime(df_data_locacao.head().values[0][0]).day_name
                #dia_da_semana_locado = pd.to_datetime(df_data_limite.head().values[0][0]).day_name
               
                data_locacao = dia_locacao + "/" + mes_locacao
                tempo_locado = dia_locado + "/" + mes_locado
                tempo = hj - self.__locacao['tempo_locado'][0]
                __dia_extra = tempo.days
                __hora_extra = tempo.seconds//3600 #hj.hour - self.__locacao[0][2].hour
                minuto = tempo.seconds/3600        
                __minuto_extra = (tempo.seconds%3600)//60 #hj.minute - self.__locacao[0][2].minute
                
                tempo = (tempo.days * 24 * 60) + ( tempo.seconds / 60 )
                print('-------> %s'%tempo)
                result = self.cobranca_excedente(__dia_extra, __hora_extra, __minuto_extra, self.__locacao['id_armario'][0])
                dados_locacao = {
                                 "total": result,
                                 "data_locacao": data_locacao, 
                                 "tempo_locado": tempo_locado, 
                                 "dia_locacao":query_dia_semana_locacao[0], 
                                 "dia_limite": query_dia_semana_locado[0], 
                                 "hora_locacao":hora_locacao, 
                                 "hora_locado":hora_locado, 
                                 "dia_extra": __dia_extra, 
                                 "hora_extra":__hora_extra, 
                                 "minuto_extra":__minuto_extra 
                                 }
                return dados_locacao#result, data_locacao, tempo_locado, query_dia_semana_locacao, query_dia_semana_locado, hora_locacao, hora_locado, __dia_extra, __hora_extra, __minuto_extra)
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
    

    def pagamento(self, total, senha):
        codigo = "paguei"
        print("informe o codigo")
        entrada = "paguei"
        self.__locacao = self.get_locacao(senha)
        if codigo==entrada:
            self.__c.execute("DELETE FROM tb_locacao WHERE senha = '%s'" % (senha,))
            self.__c.execute("UPDATE tb_armario set estado = 'LIVRE' WHERE id_armario = '%s'" % (self.__locacao['id_armario'][0],))
            self.__conn.commit()
            self.__conn.close()
            return ("lk4thHG34=GKss0xndhe")
        else:
            return ("houve um problema com o pagamento")
    
    def pagamento_locacao(self, total):
        codigo = "paguei"
        print("informe o codigo")
        entrada = "paguei"
        if codigo==entrada:
            return ("lk4thHG34=GKss0xndhe")
        else:
            return ("houve um problema com o pagamento")
    





if __name__ == "__main__":
    Banco()
