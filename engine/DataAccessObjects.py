from coolbagsafe_system.data_access_objets_db_cbs import DataAccessObjectsBase as DAO
from coolbagsafe_system.data_access_objets_db_nuvem import DataAccessObjectsNuvem as DAON
from coolbagsafe_system.portas import Portas
from coolbagsafe_system.taxas import *
from .TransacsAndOps import TransacsOps
import sys, os
import asyncio
import mysql.connector as mdb
import datetime
from datetime import date, timedelta, time
import time
from time import sleep
import subprocess
import random
import string
from random import choice, sample
import pandas as pd
import smtplib
import json
import sqlite3
TAXA_HORA_A = 0     
TAXA_HORA_B = 0
TAXA_HORA_C = 0
TAXA_HORA_D = 0
TAXA_DIARIA_A = 0
TAXA_DIARIA_B = 0
TAXA_DIARIA_C = 0
TAXA_DIARIA_D = 0


class DataAccessObjectsManager(object):
    def __init__(self):
        global TAXA_HORA_A
        global TAXA_HORA_B
        global TAXA_HORA_C
        global TAXA_HORA_D
        global TAXA_DIARIA_A
        global TAXA_DIARIA_B
        global TAXA_DIARIA_C
        global TAXA_DIARIA_D
        global TAXA_MINUTO_A 
        global TAXA_MINUTO_B 
        global TAXA_MINUTO_C 
        global TAXA_MINUTO_D
        self.data_dao = ''

        self.data = ''
        self.porta = ''
        self.port = Portas()
        
        TAXA_DIARIA_A = TaxAndRates.TAXA_DIARIA_A.value
        TAXA_DIARIA_B = TaxAndRates.TAXA_DIARIA_B.value
        TAXA_DIARIA_C = TaxAndRates.TAXA_DIARIA_C.value
        TAXA_DIARIA_D = TaxAndRates.TAXA_DIARIA_D.value
        TAXA_HORA_A = TaxAndRates.TAXA_HORA_A.value
        TAXA_HORA_B = TaxAndRates.TAXA_HORA_B.value
        TAXA_HORA_C = TaxAndRates.TAXA_HORA_C.value
        TAXA_HORA_D = TaxAndRates.TAXA_HORA_D.value
        TAXA_MINUTO_A = TaxAndRates.TAXA_MINUTO_A.value
        TAXA_MINUTO_B = TaxAndRates.TAXA_MINUTO_B.value
        TAXA_MINUTO_C = TaxAndRates.TAXA_MINUTO_C.value
        TAXA_MINUTO_D = TaxAndRates.TAXA_MINUTO_D.value

        
        """self.ddao = DAON()
        self.conexao = mdb.connect(host=self.ddao.dbn_host(), user=self.ddao.dbn_user(), password=self.ddao.dbn_passwd(), database=self.ddao.dbn_database())
        self.dbn_cursor = self.conexao.cursor(buffered=True)"""
        self.data_dao = DAO()

        self.__conn = mdb.connect(host=self.data_dao.db_host(), user=self.data_dao.db_user(), password=self.data_dao.db_passwd(), database=self.data_dao.db_database())
        #self.__c = self.__conn.cursor(buffered=True)
        self.__c = self.__conn.cursor(buffered=True)
        #self.ddao = DAON()
        #self.__conn_nuvem = mdb.connect(host=self.ddao.db_host(), user=self.ddao.db_user(), password=self.ddao.db_passwd(), database=self.ddao.db_database())
        #self.__c = self.__conn.cursor(buffered=True)
        #self.dbn_cursor = self.__conn_nuvem.cursor(buffered=True)


    def create_user(self, nome, email, telefone):
        """ verifica se existe um usuario já cadastrado atraves de busa pelo email
        ou telefone, caso haja , compara o email obtido do banco com o fornecido e o telefone
        obtido com o fornecido , havendo discrepancia ele atualiza o registro. Caso não haver
        registro algum é feito um novo registro.
        Dados: str: nome
        str: telefone
        str: email
        return: id_usuario  """
        

        __nome = str(nome).lower()
        __email = str(email).lower()
        __telefone = str(telefone)
        
        __telefone = __telefone.replace("(","")
        __telefone = __telefone.replace(")","")
        __telefone = __telefone.replace("+","")
        __telefone = __telefone.replace(" ","")

        print("__telefone", __telefone)
        query_select_user = "SELECT * from tb_usuario where email= '%s' OR telefone= '%s'" % (__email, __telefone)
        #self.__c.execute("SELECT * from tb_usuario where email= '%s' OR telefone= '%s'" % (__email, __telefone))
        self.select = pd.read_sql(query_select_user, self.__conn)#self.__c.fetchall()
        print("self.select em create user", self.select)
        

        if self.select.empty:
            consulta = ''
            alfanum = string.digits + string.ascii_letters

            lista_user = 'CBS_USER'
            for i in range(0,15):
                lista_user += random.choice(alfanum)
            print(lista_user)
            
            
            from coolbagsafe_system.data_access_objets_db_nuvem import DataAccessObjectsNuvem as DAON 
            dao =DAON() 
            dao.create_user(lista_user, __nome, __email,  __telefone)
            

            self.__c.execute("INSERT INTO tb_usuario (id_usuario, nome, email, telefone) values ('%s','%s','%s','%s')" % (
               lista_user, __nome, __email,  __telefone))
            self.__conn.commit()
            #self.__c.execute("SELECT id_usuario from tb_usuario where email='%s' AND telefone='%s'" % (
               # __email, __telefone,))
            #consulta = self.__c.fetchall()
            print("-----CONSULTA ID USUARIO-----")
            print(lista_user)
            
            
            #subprocess.run('docker stop ubuntu', shell=True)
            return lista_user

            """elif self.select[0][2] != __email and self.select[0][3] == __telefone:
                self.__c.execute("UPDATE tb_usuario SET email = '%s', telefone = '%s', nome = '%s' WHERE id_usuario = '%s'" % (
                    __email, __telefone, __nome,  self.select[0][0]))
                self.__conn.commit()
                

                return self.select[0][0]  # id_usuario
            elif self.select[0][2] == __email and self.select[0][3] != __telefone:
                self.__c.execute("UPDATE tb_usuario SET telefone = '%s' WHERE id_usuario = '%s'" % (
                    __telefone, self.select[0][0]))
                self.__conn.commit()
                return self.select[0][0]
            elif self.select[0][2] == __email and self.select[0][3] == __telefone:
                self.__c.execute("UPDATE tb_usuario SET telefone = '%s' WHERE id_usuario = '%s'" % (
                    __telefone, self.select[0][0]))
                self.__conn.commit()
                return self.select[0][0]"""
        elif not self.select.empty:
            self.__c.execute("UPDATE tb_usuario SET email = '%s', telefone = '%s', nome = '%s' WHERE id_usuario = '%s'" % (
                    __email, __telefone, __nome,  self.select['id_usuario']))
            self.__conn.commit()
            return self.select['id_usuario'][0]
        else:
            return self.select['id_usuario'][0]#[0]

        self.__conn.close()

    def locar_armario(self, nome, email, telefone, dia, hora, minuto, armario, language, total):
        port = ''
        dia = dia
        #dia = dia.replace(".0", "")
        self.__dia = int(dia)
        self.__hora = int(hora) #.replace(".0", ""))
        minuto = minuto
        print("minuto---*", minuto)
        #minuto = int(minuto.replace(".0", ""))
        self.__total = total
        self.__minuto = minuto
        self.__armario = str(armario)
        __nome = str(nome)
        __email = str(email)
        __telefone = str(telefone)
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

        __senha = ''

        self.dados_locatario = self.create_user(__nome, __email, __telefone)
        #self.ddao.create_user(__nome, __email,  __telefone)
        print("dados locatario data.py locacao===>", self.dados_locatario)
        # seleciona um armario com a classe indicada e recebe seu id
        loca_armario = self.localisa_armario(self.__armario)

        print('======= loca ramario =====')
        print(loca_armario[0])
        retorno = self.pagamento_locacao()
            

        resultado_transacao = TransacsOps.retorno_transacao()
        print("resultado_transacao", resultado_transacao["PWINFO_RESULTMSG"])
        print("testando o valor booleano")
        print('autorizada' or 'aprovada' in str(resultado_transacao["PWINFO_RESULTMSG"].lower()))
        if 'autorizada' in (resultado_transacao["PWINFO_RESULTMSG"].lower()).split():
            __senha = self.__get_passwd()
            print("self.__data_locacao", self.__data_locacao)
            print("self.__data_limite",self.__data_limite)
            print("__senha", __senha)
            print("loca_armario[0]", loca_armario[0])
            print("self.dados_locatario", self.dados_locatario)
            print("self.__total",self.__total)
            alfanum = string.digits + string.ascii_letters
            lista = 'CBS_LOCACAO'
            for i in range(0,15):
                lista += random.choice(alfanum)
            print(lista)
            

            self.__c.execute("INSERT INTO tb_locacao(id_locacao, data_locacao,tempo_locado,tempo_corrido,senha,id_armario,id_usuario) VALUES('%s', '%s','%s',null,'%s','%s','%s','%s')" % (lista, self.__data_locacao, self.__data_limite, __senha, loca_armario[0], self.dados_locatario))
            

            self.__c.execute("UPDATE tb_armario SET estado = 'OCUPADO' where id_armario = '%s'" % (loca_armario[0]))

            self.__conn.commit()
            dao = DAON()
            dao.insert_locacao(lista, self.__data_locacao, self.__data_limite, __senha, loca_armario[0], self.dados_locatario, self.__total)

            lista_persist = 'CBS_LOCPERSIST'
            for i in range(0,15):
                lista_persist += random.choice(alfanum)
            print(lista_persist)

            self.__c.execute("INSERT INTO tb_locacao_persistence(id_locacao_persistence, data_locacao,tempo_locado,tempo_corrido,id_armario,id_usuario, valor_locacao) VALUES('%s', '%s','%s',null,'%s','%s','%s','%s', '%s')" % (lista_persist, self.__data_locacao, self.__data_limite, loca_armario[0], self.dados_locatario, self.__total, self.__armario))
            
            self.__conn.commit()

            compartimento_query = "select compartimento from tb_armario where id_armario = '%s'" % (loca_armario[0])
            compartimento_select = pd.read_sql(compartimento_query, self.__conn)
            self.__data_locacao = str(self.__data_locacao)
            self.__data_limite = str(self.__data_limite)
            mes_locacao = str(self.__data_locacao[5:7])
            dia_locacao = str(self.__data_locacao[8:10])
            mes_locado = str(self.__data_limite[5:7])
            dia_locado = str(self.__data_limite[8:10])
            # senha = data_and_passwd.head().values[0]
            # senha =
            compartimento = compartimento_select.head().values[0]
            hora_locacao = str(self.__data_locacao[11:16])
            hora_locada = str(self.__data_limite[11:16])
            data_locacao = dia_locacao + "/" + mes_locacao
            tempo_locado = dia_locado + "/" + mes_locado
            TransacsOps.send_email(__nome, __email, __senha,
                            compartimento[0], data_locacao, hora_locacao, tempo_locado,  hora_locada, language)
            #try:
            TransacsOps.send_sms(__nome, __senha, compartimento[0], data_locacao, hora_locacao, tempo_locado,  hora_locada, __telefone)
            #except Exception:
            #    print(Exception.value)

            # query_select = self.__c.fetchall()

            print("result locacao", __senha)

            port = self.select_port(loca_armario[0])
            print("porta selecionada", port)

            # HABILILAR NO RASPBERRY PI
            self.port.exec_port(str(port), "abre", "ocupado")
            


            locacao_json = {
                "message": "locacao concluida com sucesso",
                "data_locacao": data_locacao,
                "hora_locacao": hora_locacao,
                "data_locada": tempo_locado,
                "hora_locada": hora_locada,
                "senha": __senha,
                "compartimento": compartimento[0], 
                
            }
            
            return locacao_json
            
        elif 'aprovada' in (resultado_transacao["PWINFO_RESULTMSG"].lower()).split():
            __senha = self.__get_passwd()
            print("self.__data_locacao", self.__data_locacao)
            print("self.__data_limite",self.__data_limite)
            print("__senha", __senha)
            print("loca_armario[0]", loca_armario[0])
            print("self.dados_locatario", self.dados_locatario)
            print("self.__total",self.__total)
            print("type self.__total", type(self.__total))
            self.__total = self.__total.replace(',', '.')
            self.__total = self.__total.replace('R$', '')
            alfanum = string.digits + string.ascii_letters
            lista = 'CBS_LOCACAO'
            for i in range(0,15):
                lista += random.choice(alfanum)
            print(lista)
            

            self.__c.execute("INSERT INTO tb_locacao(id_locacao, data_locacao,tempo_locado,tempo_corrido,senha,id_armario,id_usuario) VALUES('%s', '%s','%s',null,'%s','%s','%s')" % (lista, self.__data_locacao, self.__data_limite, __senha, loca_armario[0], self.dados_locatario))
            

            self.__c.execute("UPDATE tb_armario SET estado = 'OCUPADO' where id_armario = '%s'" % (loca_armario[0]))

            self.__conn.commit()
            lista_persist = 'CBS_LOCPERSIST'
            for i in range(0,15):
                lista_persist += random.choice(alfanum)
            print(lista)

            self.__c.execute("INSERT INTO tb_locacao_persistence(id_locacao_persistence, data_locacao,tempo_locado,tempo_corrido,id_armario,id_usuario, valor_locacao) VALUES('%s', '%s','%s',null,'%s','%s','%s', '%s')" % (lista_persist, self.__data_locacao, self.__data_limite, loca_armario[0], self.dados_locatario, self.__total, self.__armario))
            
            self.__conn.commit()
            dao = DAON()
            dao.insert_locacao(lista, self.__data_locacao, self.__data_limite, __senha, loca_armario[0], self.dados_locatario, self.__total)

            compartimento_query = "select compartimento from tb_armario where id_armario = '%s'" % (
                loca_armario[0])
            compartimento_select = pd.read_sql(
                compartimento_query, self.__conn)
            self.__data_locacao = str(self.__data_locacao)
            self.__data_limite = str(self.__data_limite)
            mes_locacao = str(self.__data_locacao[5:7])
            dia_locacao = str(self.__data_locacao[8:10])
            mes_locado = str(self.__data_limite[5:7])
            dia_locado = str(self.__data_limite[8:10])
            # senha = data_and_passwd.head().values[0]
            # senha =
            compartimento = compartimento_select.head().values[0]
            hora_locacao = str(self.__data_locacao[11:16])
            hora_locada = str(self.__data_limite[11:16])
            data_locacao = dia_locacao + "/" + mes_locacao
            tempo_locado = dia_locado + "/" + mes_locado
            TransacsOps.send_email(__nome, __email, __senha,
                            compartimento[0], data_locacao, hora_locacao, tempo_locado,  hora_locada, language)
            #try:
            TransacsOps.send_sms(__nome, __senha, compartimento[0], data_locacao, hora_locacao, tempo_locado,  hora_locada, __telefone)
            #except Exception:
            #    print(Exception)
            # query_select = self.__c.fetchall()

            print("result locacao", __senha)

            port = self.select_port(loca_armario[0])
            print("porta selecionada", port)

            # HABILILAR NO RASPBERRY PI
            self.port.exec_port(str(port), "abre", "ocupado")
            


            locacao_json = {
                "message": "locacao concluida com sucesso",
                "data_locacao": data_locacao,
                "hora_locacao": hora_locacao,
                "data_locada": tempo_locado,
                "hora_locada": hora_locada,
                "senha": __senha,
                "compartimento": compartimento[0]
            }
            #self.ddao.insert_locacao(self.__data_locacao, self.__data_limite, __senha, loca_armario[0], self.dados_locatario, self.__total)
            return locacao_json    
            
        else:
            print("falhou")
            locacao_json_failure = {"message": resultado_transacao["PWINFO_RESULTMSG"]}
            return locacao_json_failure
        self.__conn.close()

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
    def select_user(senha):
        data_dao = DAO()
        __conn = mdb.connect(host=data_dao.db_host(), user=data_dao.db_user(), password=data_dao.db_passwd(), database=data_dao.db_database())
        __c = __conn.cursor(buffered=True)
        
        # senha_encode = senha.encode(encoding='utf-8', errors='restrict')
        # senha_encode = hashlib.sha3_512(senha_encode).hexdigest()
        __password = senha  # _encode#.encode('utf-8')

        print("nome ou mail select user", __password)
        query = "SELECT id_usuario FROM tb_locacao where senha = '" + __password + "'"
        id_user = pd.read_sql(query, __conn)
        #query = __c.fetchall()
        
        if id_user.empty:
            return 'senha incorreta, tente novamente'
        else:
            print("##### id usuario ----")
            print(id_user['id_usuario'][0])
            return id_user['id_usuario'][0]
        __conn.close()

    def __get_passwd(self):
        """ gera a senha automaticamente com combinação aleatória de 2 letras e 2 numeros
        sem ordem predefinida , a ordem dos dígitos também serão aleatórios """
        __password = []
        self.__pass2 = ''
        __alfabet = list(string.ascii_uppercase)
        __num = list(range(1,10))
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
                # pass_encoded = __password.encode(encoding='utf-8', errors='strict')
                if __password in comparativo:
                    __password = ""
                else:
                    __passwd = sample(__password, len(__password))
                    print('===========senha=======')
                    print(__passwd)
                    print('======fimsenha=========')
                    for i in __passwd:
                        self.__pass2 += str(i)

            print(self.__pass2)

        return self.__pass2

  
    @staticmethod
    def get_locacao(senha):
        data_dao = DAO()
        __conn = mdb.connect(host=data_dao.db_host(), user=data_dao.db_user(), password=data_dao.db_passwd(), database=data_dao.db_database())
        __c = __conn.cursor(buffered=True)
        result = ''
        # pass_encoded = senha.encode(encoding='utf-8', errors='strict')
        __senha = senha  # hashlib.sha3_512(pass_encoded).hexdigest()
        print('---senha---', __senha)
        # __senha = __senha.decode('utf-8')
        # print('*** id usuario *** ', __id_user[0])
        # print(__senha)
        # __c.execute("SELECT id_armario, id_locacao, tempo_locado, data_locacao from tb_locacao where senha = '%s' AND id_usuario = '%s'" %(__senha,__id_user[0]))
        dados = pd.read_sql(
            "SELECT * from tb_locacao where senha = '%s'" % (__senha), __conn)
        # for reg in __c.next_proc_resultset():
        # __result = __c.fetchall()
        # print("888888 ---- result")
        # print(__result)
        if dados.empty:
            dados = "senha incorreta, tente novamente"
        print("dados get_locacao", dados)

        __conn.close()
        return (dados)

    def liberar_armario(self, id_armario):
        self.__id = id_armario[0][0]
        print("self id armario em liberar armario", self.__id)
        port = self.select_port(self.__id)
        self.port.exec_port(port[0][0], "abre", "livre")
        return "armario liberado"

    def remover_armario(self, id_armario):

        self.__id = id_armario
        self.__c.execute(
            "SELECT estado  from tb_armario where id_armario = '%s'" % (self.__id))
        result = self.__c.fetchall()
        if result == 'LIVRE':
            self.__c.execute(
                "DELETE FROM tb_armario where id_armario = '%s' " % (self.__id))
        else:
            return "não é possível remover armario, verifique se o mesmo não está em uso"

    def cadastrar_armario(self, classe, terminal, coluna, nivel, porta, compartimento):

        alfanum = string.digits + string.ascii_letters
        self.__classe = classe
        self.__local = 'home'
        self.__terminal = terminal
        self.__coluna = coluna
        self.__nivel = nivel
        self.__porta = porta
        self.__compartimento = compartimento
        self.__c.execute("select porta, compartimento  from tb_armario where porta='%s' and compartimento = '%s' and estado='LIVRE'" % (
            self.__porta, self.__compartimento))
        select_porta = self.__c.fetchall()
        print("select_porta", select_porta)
        if select_porta == None or select_porta == [] or select_porta == "":
            lista_armario = 'CBS_ARMARIO'
            for i in range(0,15):
                lista_armario += random.choice(alfanum)
            print(lista_armario)

            self.__compartimento = compartimento
            self.__c.execute("INSERT INTO tb_armario ( id_armario, classe, terminal, local, estado, nivel, porta, compartimento )" +
                             "VALUES ('%s','%s','%s','%s', 'LIVRE', '%s', '%s', '%s')", (lista_armario, self.__classe, self.__terminal, self.__coluna, self.__nivel, self.__porta, self.__compartimento))
            result = self.__c.fetchone()
            self.__conn.commit()
            self.__conn.close()
            #self.ddao(self.__classe, self.__terminal, self.__coluna, self.__nivel, self.__porta, self.__compartimento)
            return (self.__classe, self.__coluna, self.__nivel, self.__terminal, "cadastrado com sucesso")
        else:
            return "porta ou compartimento já utilizada confira a porta exata para o cadastro e evite problemas!"


    """@classmethod
    def cobranca(cls, self, total, data_futura):
        compara duas datas retornando a diferença de tempo entre as duas
            parametros: data_atual tipo datetime, tempo_locado tipo datetime
            retorno: diferença tipo datetime.timedelta convertido em minutos e calculado o preço conforme
            taxa por minuto cobrado

        self.__data_atual = data_futura
        # self.__data_futura = data_futura
        self.__tempo_locado = total
        # self.__tempo_corrido = self.__data_futura - self.__data_atual
        '''if (self.__tempo_corrido.days and self.__tempo_corrido) <= 0:
            return None
        else:'''

        __total_preco = self.__tempo_locado * TAXA  # preço total do excedente
        # formatando para duas casas decimais apos virgula
        __total_preco = "%.2f" % (__total_preco)
        # troca ponto por virgula pra formatar em moeda BR
        __total_preco = str(__total_preco.replace('.', ','))
        print('modulo data')
        return __total_preco"""

    @staticmethod
    def cobranca_excedente(dias, hora, minuto, id_armario):
        data_dao = DAO()
        __conn = mdb.connect(host=data_dao.db_host(), user=data_dao.db_user(), password=data_dao.db_passwd(), database=data_dao.db_database())
        calculo_minuto = 0
        __minuto = minuto
        classe_armario = pd.read_sql(
            "select classe from tb_armario where id_armario = '%s'" % id_armario, __conn)
        classe = str(classe_armario['classe'][0])
        if __minuto <= 5:
            valor_total = 0
        if __minuto <= 15 and minuto > 5:
            calculo_minuto = (1/4)
        elif __minuto > 15 and minuto <= 30:
            calculo_minuto = (2/4)
        elif __minuto > 30 and minuto <= 45:
            calculo_minuto = (3/4)
        if classe == "A":
            valor_total = ((dias * (TAXA_HORA_A * 24)) +
                           (hora * TAXA_HORA_A) + calculo_minuto * TAXA_HORA_A)
        elif classe == "B":
            valor_total = ((dias * (TAXA_HORA_B * 24)) +
                           (hora * TAXA_HORA_B) + calculo_minuto * TAXA_HORA_B)
        elif classe == "C":
            valor_total = ((dias * (TAXA_HORA_C *24)) +
                           (hora * TAXA_HORA_C) + calculo_minuto * TAXA_HORA_C)
        elif classe == "D":
            valor_total = ((dias * (TAXA_HORA_D * 24)) +
                           (hora * TAXA_HORA_D) + calculo_minuto * TAXA_HORA_D)

        # valor_total = ((dias *24 * 15) + (hora * TAXA) + calculo_minuto * TAXA)
        message = "tempo excedido cobrança de R$ : '%s'" % valor_total

        print('22222222222 tempo 222222222222')
        print(valor_total)

        __excedente = float(valor_total)
        # total = __excedente * taxa
        total = "%.2f" % valor_total
        print('$$$$$$$ total $$$$ %s' % total)
        return (total)

    def finalizar(self, senha):
       
        result = ''
        id_armario = ''
        

        hj = datetime.datetime.now()
        hj = datetime.datetime(hj.year, hj.month, hj.day,
                               hj.hour, hj.minute, hj.second)
        
        hj = pd.to_datetime(hj)
        
        __senha = senha  
        self.__id_user = self.select_user(__senha)
        if self.__id_user == 'senha incorreta, tente novamente':
            return 'senha incorreta, tente novamente'
        self.__locacao = self.get_locacao(senha)
        classe_armario = pd.read_sql(
            "select classe from tb_armario where id_armario = '%s'" % self.__locacao["id_armario"][0], self.__conn)
        classe = str(classe_armario['classe'][0])
        if classe == "A":
            taxa_minuto = TAXA_MINUTO_A
            taxa_dia = TAXA_DIARIA_A
            taxa_hora = TAXA_HORA_A
        elif classe == "B":
            taxa_minuto = TAXA_MINUTO_B
            taxa_dia = TAXA_DIARIA_B
            taxa_hora = TAXA_HORA_B
        elif classe == "C":
            taxa_minuto = TAXA_MINUTO_C
            taxa_dia = TAXA_DIARIA_C
            taxa_hora = TAXA_HORA_C
        elif classe == "D":
            taxa_minuto = TAXA_MINUTO_D
            taxa_dia = TAXA_DIARIA_D
            taxa_hora = TAXA_HORA_D

        print('senha e nome finalizar', __senha)
        self.__id_user = self.select_user(senha)  # __senha)
        
        if self.__id_user == 'senha incorreta, tente novamente':
            return 'senha incorreta, tente novamente'

        else:
            
            if (self.__locacao['tempo_locado'][0]) > hj:

                tempo_total = hj - self.__locacao['tempo_locado'][0]
                dias_passados = tempo_total.days
                minutos_passados = tempo_total.seconds / 60
                calculo_hora = tempo_total.seconds // 3600
                calculo_minuto = 0
                if minutos_passados <= 15 and minutos_passados > 5:
                    calculo_minuto = (1/4)
                elif minutos_passados > 15 and minutos_passados <= 30:
                    calculo_minuto = (2/4)
                elif minutos_passados > 15 and minutos_passados <= 30:
                    calculo_minuto = (3/4)
                id_armario = self.__locacao['id_armario'][0]
                print(" ID ARMARIO", id_armario)
                valor_total = int((dias_passados) * taxa_dia)
                valor_total = int(valor_total + (calculo_minuto * taxa_minuto))
                valor_total = int(valor_total + calculo_hora * taxa_hora)
                result = self.cobranca_excedente(
                    dias_passados, calculo_hora, calculo_minuto, id_armario)  # (valor_total,hj)
                porta = self.select_port(id_armario)
                self.port.exec_port(porta, "abre", "livre")
                self.__c.execute("SELECT valor_locacao from tb_locacao_persistence where id_usuario = '%s'"%(self.__id_user))
                valor_locacao_persist = self.__c.fetchone()
                print("valor_locacao_persist --->", valor_locacao_persist)
                """if valor_locacao_persist != None:
                    valor_locacao_persist = valor_locacao_persist + result
                    self.__c.execute(
                    "UPDATE tb_locacao_persistence set valor_locacao = '%s' WHERE id_armario = '%s'" % (valor_locacao, id_armario,))"""

                self.__c.execute(
                    "DELETE FROM tb_locacao WHERE senha = '%s'" % (__senha,))
                self.__c.execute(
                    "UPDATE tb_armario set estado = 'LIVRE' WHERE id_armario = '%s'" % (id_armario,))
                
                self.__conn.commit()
                
                self.__conn.close()
                dao = DAON()
                dao.finalizar(valor_locacao_persist, __senha, id_armario)
                return "armario liberado"

            else:
                query_data_locacao = "select data_locacao from tb_locacao where senha = '%s'" % __senha
                query_data_limite = "select tempo_locado from tb_locacao where senha = '%s'" % __senha
                self.__c.execute(
                    "select dayname(data_locacao) from tb_locacao where senha = '%s'" % __senha)
                query_dia_semana_locacao = self.__c.fetchone()
                self.__c.execute(
                    "select dayname(tempo_locado) from tb_locacao where senha = '%s'" % __senha)
                query_dia_semana_locado = self.__c.fetchone()
                df_data_locacao = pd.read_sql(query_data_locacao, self.__conn)
                # data em que foi feita a locacao
                data_locacao = str(pd.to_datetime(
                    df_data_locacao.head().values[0][0]))
                df_data_limite = pd.read_sql(query_data_limite, self.__conn)
                # data e hora final da locacao
                data_limite = str(pd.to_datetime(
                    df_data_limite.head().values[0][0]))
                mes_locacao = data_locacao[5:7]  # mes da locacao
                dia_locacao = data_locacao[8:10]  # dia da locacao
                hora_locacao = data_locacao[11:16]
                mes_locado = data_limite[5:7]
                dia_locado = data_limite[8:10]
                hora_locado = data_limite[11:16]
                # dia_da_semana_locacao = pd.to_datetime(df_data_locacao.head().values[0][0]).day_name
                # dia_da_semana_locado = pd.to_datetime(df_data_limite.head().values[0][0]).day_name

                data_locacao = dia_locacao + "/" + mes_locacao
                tempo_locado = dia_locado + "/" + mes_locado
                tempo = hj - self.__locacao['tempo_locado'][0]
                __dia_extra = tempo.days
                # hj.hour - self.__locacao[0][2].hour
                __hora_extra = tempo.seconds//3600
                minuto = tempo.seconds/3600
                # hj.minute - self.__locacao[0][2].minute
                __minuto_extra = (tempo.seconds % 3600)//60

                tempo = (tempo.days * 24 * 60) + (tempo.seconds / 60)
                print('-------> %s' % tempo)
                __id_armario = self.__locacao["id_armario"][0]
                result = self.cobranca_excedente(
                    __dia_extra, __hora_extra, __minuto_extra, __id_armario)
                dados_locacao = {
                    "total": result,
                    "data_locacao": data_locacao,
                    "tempo_locado": tempo_locado,
                    "dia_locacao": query_dia_semana_locacao[0],
                    "dia_limite": query_dia_semana_locado[0],
                    "hora_locacao": hora_locacao,
                    "hora_locado": hora_locado,
                    "dia_extra": __dia_extra,
                    "hora_extra": __hora_extra,
                    "minuto_extra": __minuto_extra
                }
                return dados_locacao


    @staticmethod
    def listar_classes_armarios():
        data_dao = DAO()
        __conn = mdb.connect(host=data_dao.db_host(), user=data_dao.db_user(), password=data_dao.db_passwd(), database=data_dao.db_database())
        __c = __conn.cursor(buffered=True)
        __classes = []
        result = ''
        __c.execute("SELECT classe FROM tb_armario WHERE estado = 'LIVRE'")
        result = __c.fetchall()
        print('result listar classes data', result)

        __conn.close()
        return result

    def seleciona_classe(self, classe):
        self.classe = classe
        print('classe recebida data', self.classe)
        """__conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        __c = __conn.cursor(buffered=True)"""
        #__conn = data_dao.db_conn_string
        #__c = __conn.cursor(buffered=True)
        result = ''
        self.__c.execute("select classe from tb_armario where estado = 'LIVRE' and classe = '%s'" % self.classe)
        result = __c.fetchall()
        print('result data classe', result)

        self.__conn.close()
        return result

    @classmethod
    def abrir_armario(self, senha):
        data_dao = DAO()
        self.port = Portas()
        self.__conn = mdb.connect(host=data_dao.db_host(), user=data_dao.db_user(), password=data_dao.db_passwd(), database=data_dao.db_database())
        self.__c = self.__conn.cursor(buffered=True)
        print('senha em data', senha)
        result = ''
        port = ''
        
        taxa = 15
        hj = datetime.datetime.now()
        hj = datetime.datetime(hj.year, hj.month, hj.day,
                               hj.hour, hj.minute, hj.second)
        #__cursor.execute("SELECT senha FROM tb_locacao WHERE id_armario = '%s'"%(id_armario))

        # __senha = senha.encode(encoding='utf-8', errors='strict')
        # print('senha encode', senha)
        #__senha = __cursor.fetchall()
        __senha = senha  #__senha[0][0]
        # print(__senha)
        self.__id_user = self.select_user(__senha)  # __senha)
        if self.__id_user == 'senha incorreta, tente novamente':
            return 'senha incorreta, tente novamente'

        else:
            self.__locacao = self.get_locacao(__senha)  # __senha)

            print('********** dados locacao **************')
            print(self.__locacao['tempo_locado'][0])
            if (self.__locacao['tempo_locado'][0]) >= hj:
                #import threading
                porta_armario = pd.read_sql("SELECT id_armario FROM tb_locacao WHERE senha = '%s'" % (__senha,), self.__conn)
                # self.__conn.commit()
                # self.__conn.close()
                #id_armario = __cursor.fetchall()

                porta = self.select_port(porta_armario["id_armario"][0])#id_armario[0][0])
                print("abrir armario data.py porta", str(porta))
                self.port.exec_port(porta, "abre", "ocupado")
                return "armario liberado"
            else:
                query_data_locacao = "select data_locacao from tb_locacao where senha = '%s'" % __senha
                query_data_limite = "select tempo_locado from tb_locacao where senha = '%s'" % __senha
                self.__c.execute("select dayname(data_locacao) from tb_locacao where senha = '%s'" % __senha)
                query_dia_semana_locacao = self.__c.fetchone()
                self.__c.execute("select dayname(tempo_locado) from tb_locacao where senha = '%s'" % __senha)
                query_dia_semana_locado = self.__c.fetchone()
                df_data_locacao = pd.read_sql(query_data_locacao, self.__conn)
                # data em que foi feita a locacao
                data_locacao = str(pd.to_datetime(df_data_locacao.head().values[0][0]))
                df_data_limite = pd.read_sql(query_data_limite, self.__conn)
                # data e hora final da locacao
                data_limite = str(pd.to_datetime(df_data_limite.head().values[0][0]))
                mes_locacao = data_locacao[5:7]  # mes da locacao
                dia_locacao = data_locacao[8:10]  # dia da locacao
                hora_locacao = data_locacao[11:16]
                mes_locado = data_limite[5:7]
                dia_locado = data_limite[8:10]
                hora_locado = data_limite[11:16]
                # dia_da_semana_locacao = pd.to_datetime(df_data_locacao.head().values[0][0]).day_name
                # dia_da_semana_locado = pd.to_datetime(df_data_limite.head().values[0][0]).day_name

                data_locacao = dia_locacao + "/" + mes_locacao
                tempo_locado = dia_locado + "/" + mes_locado
                tempo = hj - self.__locacao['tempo_locado'][0]
                __dia_extra = tempo.days
                # hj.hour - self.__locacao[0][2].hour
                __hora_extra = tempo.seconds//3600
                minuto = tempo.seconds/3600
                __minuto_extra = (tempo.seconds %3600)//60  # hj.minute - self.__locacao[0][2].minute

                tempo = (tempo.days * 24 * 60) + (tempo.seconds / 60)
                print('-------> %s' % tempo)
                result = self.cobranca_excedente(
                    __dia_extra, __hora_extra, __minuto_extra, self.__locacao['id_armario'][0])
                dados_locacao = {
                    "total": result,
                    "data_locacao": data_locacao,
                                 "tempo_locado": tempo_locado,
                                 "dia_locacao": query_dia_semana_locacao[0],
                                 "dia_limite": query_dia_semana_locado[0],
                                 "hora_locacao": hora_locacao,
                                 "hora_locado": hora_locado,
                                 "dia_extra": __dia_extra,
                                 "hora_extra": __hora_extra,
                                 "minuto_extra": __minuto_extra
                }
                return dados_locacao  # result, data_locacao, tempo_locado, query_dia_semana_locacao, query_dia_semana_locado, hora_locacao, hora_locado, __dia_extra, __hora_extra, __minuto_extra)

    def finalizar_pagamento(self, senha):
        
        __senha = senha
        # __nome = nome
        # __id_user = self.select_user(__nome)
        # __locacao = self.get_locacao(__senha, __id_user[0])
        # __senha = senha.encode(encoding='utf-8', errors='strict')
        # print('senha encode', senha)
        __senha = senha  # hashlib.sha3_512(senha).hexdigest()
        self.__c.execute("DELETE FROM tb_locacao WHERE senha = '%s'" % (__senha))
        id_armario = self.__c.execute(
            "SELECT id_armario FROM tb_locacao WHERE senha = '%s'" % (__senha,))
        print("finaliza_pagamento id armario", id_armario)
        self.__c.execute(
            "UPDATE tb_armario set estado = 'LIVRE' WHERE id_armario = '%s'" % (id_armario,))
        self.__conn.commit()

        self.__conn.close()
        return "locacao finalizada com sucesso"

    def pagamento(self, total, senha):
        subprocess.run("docker start paygo", shell=True)
        #subprocess.run('docker exec paygo /bin/bash -c "cd paygo/ && python3 venda.py"', shell=True)
        sleep(0.3)
        DAO.docker_run()
        
        __senha = senha
        self.__locacao = self.get_locacao(senha)
        print('self.__locacao id_armario', self.__locacao["id_armario"][0])
        # __senha_encode = senha.encode(encoding='utf-8', errors='strict')
        #self.__c.execute("select id_armario from tb_locacao where senha='%s'" % (__senha))
        subprocess.run("docker stop paygo", shell=True)
        
        resultado_transacao = TransacsOps.retorno_transacao()
        print("resultado_transacaok", resultado_transacao)
        if 'autorizada' in resultado_transacao["PWINFO_RESULTMSG"].lower():
            self.__c.execute(
                "DELETE FROM tb_locacao WHERE senha = '%s'" % (__senha,))
            self.__c.execute("UPDATE tb_armario set estado = 'LIVRE' WHERE id_armario = '%s'" % (self.__locacao["id_armario"][0]))
            self.__conn.commit()
            self.__conn.close()
            statment = "UPDATE tb_armario set estado = 'LIVRE' WHERE id_armario = '%s'" % (self.__locacao["id_armario"][0])
            subprocess.run('docker start mariadb_king', shell=True)
            DAO.docker_statment(statment)
            sleep(1)
            subprocess.run('docker stop mariadb_king', shell=True)
            __porta = self.select_port(self.__locacao["id_armario"][0])
            print("porta em pagamento", __porta)
            
            # LIBERAR NO RASPBERRY
            self.port.exec_port(__porta, "abre", "livre")
            #self.ddao.finalizar(__senha, id_armario)
            return ("pagamento ok")
        elif 'aprovada' in resultado_transacao["PWINFO_RESULTMSG"].lower():
            self.__c.execute(
                "DELETE FROM tb_locacao WHERE senha = '%s'" % (__senha,))
            self.__c.execute("UPDATE tb_armario set estado = 'LIVRE' WHERE id_armario = '%s'" % (self.__locacao["id_armario"][0]))
            self.__conn.commit()
            self.__conn.close()
            __porta = self.select_port(self.__locacao["id_armario"][0])
            print("porta em pagamento", __porta)
            
            # LIBERAR NO RASPBERRY
            self.port.exec_port(__porta, "abre", "livre")
            self.ddao.finalizar(__senha, id_armario)
            return ("pagamento ok")
        else:
            return (resultado_transacao["PWINFO_RESULTMSG"])

    def pagamento_locacao(self):
        p = None
        subprocess.run("docker start paygo", shell=True)
        #subprocess("docker exec paygo cd paygo")
        DAO.docker_run()
        
        sleep(2)
        subprocess.run("docker stop paygo", shell=True)
        #print("informe o codigo")
        
        #subprocess.run('docker exec paygo bash -c cd paygo', shell=True)
        return True

    @classmethod
    def select_port(self, armario):
        data_dao = DAO()
        __armario = []
        self.__conn = mdb.connect(host=data_dao.db_host(), user=data_dao.db_user(), password=data_dao.db_passwd(), database=data_dao.db_database())
        
        #armario = pd.read_sql()
        __armario = armario
        print("__ARMARIO EM SELECT_port ", __armario)
        retorno_porta = pd.read_sql("select porta from tb_armario where id_armario='%s'" % (__armario), self.__conn)
        #retorno_porta = __c.fetchall()
        print("retorno_porta", retorno_porta["porta"][0])
        self.__conn.close()
        return retorno_porta["porta"][0]

    #USO INTERNO APENAS PARA TESTES
    @classmethod
    def fechar_armario(self, id_armario):
        import serial
        self.serial = serial.Serial("/dev/ttyS0", 9600)
        #porta = Portas()
        __id_armario = id_armario
        print("id armario em fechar armario data.py", __id_armario)
        __porta = self.select_port(__id_armario[0][0])
        print("porta select porta id_armario", __porta)
        #porta.exec_port(str(__porta[0][0]), "fecha")
        return "fechado"

    """@classmethod
    def abrir_armario(self, id_armario):
        #porta = Portas()
        __id_armario = id_armario
        print("id armario em abrir armario data.py", __id_armario)
        __porta = self.select_port(__id_armario[0][0])
        print("porta select porta id_armario", __porta)
        #porta.exec_port(__porta[0][0], "abre")

        return "armario liberado"""

    @classmethod
    def localiza_id_armario(self, senha):
        data_dao = DAO()
        self.__conn = mdb.connect(host=data_dao.db_host(), user=data_dao.db_user(), password=data_dao.db_passwd(), database=data_dao.db_database())
        
        self.__c = self.__conn.cursor(buffered=True)
        self.__c.execute("select id_armario from tb_locacao where senha = '%s'" % senha)
        result = self.__c.fetchall()
        return result


if __name__ == "__main__":
    DataAccessObjectsManager()
