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
#from .portas import Portas
from .TransacsAndOps import TransacsOps as transops


class DataAccessObjectsManager(object):
    def __init__(self):

        self.data = ''
        self.porta = ''
        #self.port = Portas()
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
            user="coolbaguser", password="m1cr0@t805i", database="coolbag")
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

        __nome = str(nome).lower()
        __email = str(email).lower()
        __telefone = str(telefone)
        self.__c.execute(
            "SELECT * from tb_usuario where email= '%s' OR telefone= '%s'" % (__email, __telefone))
        self.select = self.__c.fetchall()

        if self.select == [] or self.select == None:
            consulta = ''

            self.__c.execute("INSERT INTO tb_usuario (id_usuario, nome, email, telefone) values (null,'%s','%s','%s')" % (
                __nome, __email,  __telefone))
            self.__conn.commit()
            self.__c.execute("SELECT id_usuario from tb_usuario where email='%s' AND telefone='%s'" % (
                __email, __telefone,))
            consulta = self.__c.fetchall()
            print("-----CONSULTA ID USUARIO-----")
            print(consulta)
            return consulta

        elif self.select[0][2] != __email and self.select[0][3] == __telefone:
                self.__c.execute("UPDATE tb_usuario SET email = '%s' WHERE id_usuario = %s" % (
                    __email, self.select[0][0]))
                self.__conn.commit()

                return self.select[0][0]  # id_usuario
        elif self.select[0][2] == __email and self.select[0][3] != __telefone:
                self.__c.execute("UPDATE tb_usuario SET telefone = '%s' WHERE id_usuario = %s" % (
                    __telefone, self.select[0][0]))
                self.__conn.commit()
                return self.select[0][0]
        else:
            return self.select[0][0]

        self.__conn.close()

    def locar_armario(self, nome, email, telefone, dia, hora, minuto, armario, language, total):
        #self.port = Portas()
        port = ''
        dia = dia
        dia = dia.replace(".0", "")
        self.__dia = int(dia)
        self.__hora = int(hora.replace(".0", ""))
        minuto = minuto
        print("minuto---*", minuto)
        minuto = int(minuto.replace(".0", ""))
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

        self.dados_locatario = self.create_user(
            __nome, __email, __telefone)
        print("dados locatario data.py locacao===>", self.dados_locatario)
        # seleciona um armario com a classe indicada e recebe seu id
        loca_armario = self.localisa_armario(self.__armario)

        print('======= loca ramario =====')
        print(loca_armario)
        # self.__c.execute("SET FOREIGN_KEY_CHECKS = 0;")
        # se houver armário livre segue com cadastro de locação
        #retorno = None
        retorno = self.pagamento_locacao()
        #data = datetime.datetime.now()
        #diretorio = os.getcwd()
        #print("diretorio ---->", diretorio)
        #f = open('%s/engine/paygoWeb/comprovantes/retornotransacao.json'%(diretorio), 'r')
        #resultado_transacao = json.load(f)
        #f.close()
        #retorno_transacao = open('%s/engine/paygoWeb/comprovantes/retornotransacao.json'%(diretorio), 'w+')
        #retorno_transacao.write('\n{  \n')
        #retorno_transacao.write('     "DATA" : "%s %s %s %s %s",\n'%(data.day, data.month, data.year, data.hour, data.minute))
        #retorno_transacao.write('     "PWINFO_RESULTMSG" : "SEM TRANSACAO"')
        #retorno_transacao.write('\n}  \n')
        #retorno_transacao.close()
        

        resultado_transacao = transops.retorno_transacao()
        print("resultado_transacao", resultado_transacao)
        if 'aprovada' in resultado_transacao["PWINFO_RESULTMSG"].lower():
            __senha = self.__get_passwd()
            # senha_encode = __senha.encode(encoding='utf-8', errors='restrict')
            # self.__hash_senha = hashlib.sha3_512(senha_encode).hexdigest()
            print("==== id_armario, id_usuario ======")
            # print(loca_armario[0], self.dados_locatario[0])
            self.__c.execute("INSERT INTO tb_locacao(id_locacao, data_locacao,tempo_locado,tempo_corrido,senha,id_armario,id_usuario) VALUES(null, '%s','%s',null,'%s',%s,%s)" % (
                self.__data_locacao, self.__data_limite, __senha, loca_armario[0], self.dados_locatario))

            self.__c.execute(
                "UPDATE tb_armario SET estado = 'OCUPADO' where id_armario = %s" % (loca_armario[0]))

            self.__conn.commit()

            # self.__c.execute("select data_locacao, tempo_locado, senha from tb_locacao where id_armario= %s" %(loca_armario[0]))
            # query_select = "select senha from tb_locacao where id_armario= %s" %(loca_armario[0])
            # data_and_passwd = pd.read_sql(query_select, self.__conn)
            compartimento_query = "select compartimento from tb_armario where id_armario = %s" % (
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
            self.send_email(__nome, __email, __senha,
                            compartimento[0], data_locacao, hora_locacao, tempo_locado,  hora_locada, language)

            # query_select = self.__c.fetchall()

            print("result locacao", __senha)

            port = self.select_port(loca_armario[0])
            print("porta selecionada", port[0][0])

            # HABILILAR NO RASPBERRY PI
            #self.port.exec_port(str(port[0][0]), "abre")

            locacao_json = {
                "message": "locacao concluida com sucesso",
                "data_locacao": data_locacao,
                "hora_locacao": hora_locacao,
                "data_locada": tempo_locado,
                "hora_locada": hora_locada,
                "senha": __senha,
                "compartimento": compartimento[0]
            }
            return (locacao_json["message"], locacao_json["data_locacao"], locacao_json["hora_locacao"], locacao_json["data_locada"], locacao_json["hora_locada"], locacao_json["senha"], locacao_json["compartimento"])
            # return ("locacao concluida com sucesso", data_locacao, hora_locacao, tempo_locado, hora_locada, __senha, compartimento)
        else:
            locacao_json = {
                "message": resultado_transacao["PWINFO_RESULTMSG"]
            }
            return locacao_json["message"]
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
        __conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        __c = __conn.cursor(buffered=True)
        # senha_encode = senha.encode(encoding='utf-8', errors='restrict')
        # senha_encode = hashlib.sha3_512(senha_encode).hexdigest()
        __password = senha  # _encode#.encode('utf-8')

        print("nome ou mail select user", __password)
        query = ''
        __c.execute(
            "SELECT id_usuario FROM tb_locacao where senha = '" + __password + "'")
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

    def __send_passwd(self, passwd):
        pass  # self.passwd = passwd

    @staticmethod
    def get_locacao(senha):
        __conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        __c = __conn.cursor(buffered=True)
        result = ''
        # pass_encoded = senha.encode(encoding='utf-8', errors='strict')
        __senha = senha  # hashlib.sha3_512(pass_encoded).hexdigest()
        print('---senha---', __senha)
        # __senha = __senha.decode('utf-8')
        # print('*** id usuario *** ', __id_user[0])
        # print(__senha)
        # __c.execute("SELECT id_armario, id_locacao, tempo_locado, data_locacao from tb_locacao where senha = '%s' AND id_usuario = %s" %(__senha,__id_user[0]))
        dados = pd.read_sql(
            "SELECT id_armario, id_locacao, tempo_locado, data_locacao from tb_locacao where senha = '%s'" % (__senha), __conn)
        # for reg in __c.next_proc_resultset():
        # __result = __c.fetchall()
        # print("888888 ---- result")
        # print(__result)
        print("dados get_locacao", dados)

        __conn.close()
        return (dados)

    def liberar_armario(self, id_armario):
        #self.port = Portas()
        self.__id = id_armario[0][0]
        print("self id armario em liberar armario", self.__id)
        port = self.select_port(self.__id)
        #self.port.exec_port(port, "abre")
        return "armario liberado"

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
        self.__c.execute("select porta, compartimento  from tb_armario where porta='%s' and compartimento = '%s' and estado='LIVRE'" % (
            self.__porta, self.__compartimento))
        select_porta = self.__c.fetchone()
        print("select_porta", select_porta)
        if select_porta == None or select_porta == [] or select_porta == "":

            self.__compartimento = compartimento
            self.__c.execute("INSERT INTO tb_armario ( id_armario, classe, terminal, local, estado, nivel, porta, compartimento )" +
                             "VALUES (0,%s,%s,%s, 'LIVRE', %s, %s, %s)", (self.__classe, self.__terminal, self.__coluna, self.__nivel, self.__porta, self.__compartimento))
            result = self.__c.fetchone()
            self.__conn.commit()
            self.__conn.close()
            return (self.__classe, self.__coluna, self.__nivel, self.__terminal, "cadastrado com sucesso")
        else:
            return "porta ou compartimento já utilizada confira a porta exada para o cadastro e evite problemas!"

    def resgatar_bagagem(self, senha):
        ''' seleciona a locacao conforme a senha fornecida retornando todos os dados:
        id_locacao , id_usuario, id_armario: type int
        data_limite : type datetime
        libera armario após ser confirmado e verificar que não haja saldo devedor
        saldo devedor calculo: data atual datetime - tempo_locado datetime

        if finalizar == True:
            pass'''

        # __email = email
        # __telefone = telefone
        # pass_encoded = senha.encode(encoding='utf-8', errors='strict')
        __senha = senha  # hashlib.sha3_512(pass_encoded).hexdigest()
        # __senha = __senha.encode('utf-8')

        self.__c.execute(
            "SELECT * FROM tb_locacao where senha = '%s'" % (__senha))
        self.__result = self.__c.fetchall()
        print('resgatar_bagagem result---->', self.__result)
        print(self.__result[0])
        return self.__result[0]
        # envia a data limite para calculo de tempo excedente
        self.__cobranca = self.__cobranca(self.result[0][2])
        if self.__cobranca == None:
            self.liberar_armario(senha)  # __senha)
        else:
            return ('tempo excedente', self.__cobranca)

    @classmethod
    def cobranca(self, total, data_futura):
        """ compara duas datas retornando a diferença de tempo entre as duas
            parametros: data_atual tipo datetime, tempo_locado tipo datetime
            retorno: diferença tipo datetime.timedelta convertido em minutos e calculado o preço conforme
            taxa por minuto cobrado"""

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
        return __total_preco

    @staticmethod
    def cobranca_excedente(dias, hora, minuto, id_armario):
        __conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        calculo_minuto = 0
        __minuto = minuto
        classe_armario = pd.read_sql(
            "select classe from tb_armario where id_armario = %s" % id_armario, __conn)
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
                           (hora * TAXA_HORA_C) + calculo_minuto * TAXA_HORA_c)
        elif classe == "D":
            valor_total = ((dias * (TAXA_HORA_D * 24)) +
                           (hora * TAXA_HORA_D) + calculo_minuto * TAXA_HORA_D)

        # valor_total = ((dias *24 * 15) + (hora * TAXA) + calculo_minuto * TAXA)
        message = "tempo excedido cobrança de R$ : %s" % valor_total

        print('22222222222 tempo 222222222222')
        print(valor_total)

        __excedente = float(valor_total)
        # total = __excedente * taxa
        total = "%.2f" % valor_total
        print('$$$$$$$ total $$$$ %s' % total)
        return (total)

    def finalizar(self, senha):
        #self.port = Portas()
        taxa = 15
        result = ''
        id_armario = ''

        hj = datetime.datetime.now()
        hj = datetime.datetime(hj.year, hj.month, hj.day,
                               hj.hour, hj.minute, hj.second)
        # hj = hj + datetime.timedelta(minutes=+10)
        hj = pd.to_datetime(hj)
        # senha = senha.encode(encoding='utf-8', errors='strict')
        __senha = senha  # hashlib.sha3_512(senha).hexdigest()
        # __senha = __senha.encode('utf-8')

        print('senha e nome finalizar', __senha)
        self.__id_user = self.select_user(senha)  # __senha)
        if self.__id_user == 'senha incorreta, tente novamente':
            return 'senha incorreta, tente novamente'

        else:
            self.__locacao = self.get_locacao(senha)  # __senha)
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
                valor_total = int((dias_passados * 24 * 60) * 50)
                valor_total = int(valor_total + (calculo_minuto * taxa))
                valor_total = int(valor_total + calculo_hora * 15)
                result = self.cobranca_excedente(
                    dias_passados, calculo_hora, calculo_minuto, id_armario)  # (valor_total,hj)
                porta = self.select_port(id_armario)
                #self.port.exec_port(porta[0][0], "abre")

                self.__c.execute(
                    "DELETE FROM tb_locacao WHERE senha = '%s'" % (__senha,))
                self.__c.execute(
                    "UPDATE tb_armario set estado = 'LIVRE' WHERE id_armario = '%s'" % (id_armario,))
                self.__conn.commit()

                self.__conn.close()
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

    def send_email(self, nome, email, senha, compartimento, data_locacao, hora_inicio_locacao, data_limite,  hora_fim_locacao, language):
        # __server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        from smtplib import SMTP
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        RECIBO = ''
        diretorio = os.getcwd()
        comprovante_pagamento = open('%s/engine/paygoWeb/comprovantes/COMPROVANTE CLIENTE EMAIL.txt'%(diretorio),'r')
        for l in comprovante_pagamento:
            RECIBO += l + '<br>'
        comprovante_pagamento.close()
        
    
        msg = MIMEMultipart()
        __nome = string.capwords(nome)
        css= """<style type='text/css' >
            .flex-box {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: flex-center;
            }
            .body{

            background: #FDCF03;
            }

            .message{
                position: absolute;
            }
            .pai{
                
                position: relative;
                text-align: center;
                margin-left: 40%;
                width: 300px;
                height: 500px;
                background: #ffffff;
                margin-bottom: 10px;
            }
            .filho{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
            }

            </style>"""
        if language == "pt_BR":
            __message = """<html><head> %s </head> 
            <body class='body'> 
            <div class='message'>
              <strong>Este e-mail foi enviado de forma automática ,não responda diretamente a este e-mail!</strong><br><br>
                    Obrigado por utilizar nossos serviços<b> %s</b>, abaixo encontra-se os seus dados de acesso para liberação do compartimento:<br><br>
                <p>COMPARTIMENTO: <b> %s  </b>
                <p>SENHA:<b> %s</b>
                <p>DATA LOCAÇÃO:<b> %s %s  </b>
                <p>DATA LIMITE:<b> %s %s</b>
            </div>
        <div class='flex-box pai'>
             <div class='filho'>%s</div>
        </div>
        </body></html>""" % (css, __nome, compartimento, senha, data_locacao, hora_inicio_locacao, data_limite, hora_fim_locacao, RECIBO)

        elif language == "en_US":
            __message = """<html><head> %s </head>
            <body class='body'> <div class='message'><strong>
        This email was sent automatically,please do not reply directly to this email! </strong><br><br>
        Thanks for using our services <b>%s</b>, below is your compartment release access details:<br><br>
        <p>COMPARTMENT: <b> %s  </b>
        <p>PASSWORD: <b> %s  </b>
        <p>DATE RENT: <b> %s %s  </b>
        <p>DEADLINE:  <b> %s %s </b><br>
        </div>
        <div class='flex-box pai'>
             <div class='filho'>%s</div>
        </div>
        
        </body></html>""" % (css, __nome, compartimento, senha, data_locacao, hora_inicio_locacao, data_limite, hora_fim_locacao, RECIBO)

       
        body = MIMEText(__message, 'html')
                    

       
        msg['Subject'] = 'CoolBag-SafeLocker - Credentials Access'
        msg.attach(body)

        msg['From'] = 'marcospaulo.silvaviana@gmail.com'
        msg['To'] = email
        password = "m1cr0@t805i"
        __server = SMTP('smtp.gmail.com:587')
        __server.starttls()
        __server.ehlo()
        __server.login("marcospaulo.silvaviana@gmail.com", "m1cr0@t805i")

        __server.sendmail( msg['From'], msg['To'].split(","), msg.as_string())

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

        __conn.close()
        return result

    def seleciona_classe(self, classe):
        self.classe = classe
        print('classe recebida data', self.classe)
        __conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        __c = __conn.cursor(buffered=True)
        __classes = []
        result = ''
        __c.execute("select classe from tb_armario where estado = 'LIVRE' and classe = '%s'" % self.classe)
        result = __c.fetchall()
        print('result data classe', result)

        __conn.close()
        return result

    @classmethod
    def abrir_armario(self, senha):
        #self.port = Portas()
        __conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        __cursor = __conn.cursor(buffered=True)
        print('senha em data', senha)
        result = ''
        port = ''
        
        taxa = 15
        hj = datetime.datetime.now()
        hj = datetime.datetime(hj.year, hj.month, hj.day,
                               hj.hour, hj.minute, hj.second)
        #__cursor.execute("SELECT senha FROM tb_locacao WHERE id_armario = %s"%(id_armario))

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
                __cursor.execute("SELECT id_armario FROM tb_locacao WHERE senha = '%s'" % (__senha,))
                # self.__conn.commit()
                # self.__conn.close()
                id_armario = __cursor.fetchall()

                porta = self.select_port(id_armario[0][0])
                print("abrir armario data.py porta", str(porta[0][0]))
                # self.port.exec_port(porta[0][0], "abre")
                #self.port.exec_port(porta[0][0], "abre")
                return "armario liberado"
            else:
                query_data_locacao = "select data_locacao from tb_locacao where senha = '%s'" % __senha
                query_data_limite = "select tempo_locado from tb_locacao where senha = '%s'" % __senha
                __cursor.execute("select dayname(data_locacao) from tb_locacao where senha = '%s'" % __senha)
                query_dia_semana_locacao = __cursor.fetchone()
                __cursor.execute("select dayname(tempo_locado) from tb_locacao where senha = '%s'" % __senha)
                query_dia_semana_locado = __cursor.fetchone()
                df_data_locacao = pd.read_sql(query_data_locacao, __conn)
                # data em que foi feita a locacao
                data_locacao = str(pd.to_datetime(df_data_locacao.head().values[0][0]))
                df_data_limite = pd.read_sql(query_data_limite, __conn)
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
        __conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        __c = __conn.cursor(buffered=True)
        __senha = senha
        # __nome = nome
        # __id_user = self.select_user(__nome)
        # __locacao = self.get_locacao(__senha, __id_user[0])
        # __senha = senha.encode(encoding='utf-8', errors='strict')
        # print('senha encode', senha)
        __senha = senha  # hashlib.sha3_512(senha).hexdigest()
        __c.execute("DELETE FROM tb_locacao WHERE senha = '%s'" % (__senha))
        id_armario = __c.execute(
            "SELECT id_armario FROM tb_locacao WHERE senha = '%s'" % (__senha,))
        print("finaliza_pagamento id armario", id_armario)
        self.__c.execute(
            "UPDATE tb_armario set estado = 'LIVRE' WHERE id_armario = '%s'" % (id_armario,))
        __conn.commit()

        __conn.close()
        return "locacao finalizada com sucesso"

    def pagamento(self, total, senha):
        
        #__port = Portas()
        subprocess.run("docker start paygoweb", shell=True)
        #subprocess("docker exec paygoweb cd paygoWeb")
        subprocess.run('docker exec paygoweb /bin/bash -c "cd paygoWeb/ && python3 venda.py"', shell=True)
        
        sleep(0.3)
        #print("informe o codigo")
        
        
        
        __senha = senha
        self.__locacao = self.get_locacao(senha)
        print('self.__locacao id_armario', self.__locacao["id_armario"][0])
        # __senha_encode = senha.encode(encoding='utf-8', errors='strict')
        self.__c.execute("select id_armario from tb_locacao where senha='%s'" % (__senha))
        result_id_armario = self.__c.fetchall()
        # print("curosr select id_armario data.py", self.__c.fetchone())
        subprocess.run("docker stop paygoweb", shell=True)
        #diretorio = os.getcwd()
        #with open('%s/engine/paygoWeb/comprovantes/retornotransacao.json'%(diretorio), 'r') as f:
        #    resultado_transacao = json.load(f)
        #sleep(0.2)
        #retorno_transacao = open('%s/engine/paygoWeb/comprovantes/retornotransacao.json'%(diretorio), 'w+')
        #retorno_transacao.write('\n{  \n')
        #retorno_transacao.write('     "DATA" : "%s %s %s %s %s",\n'%(data.day, data.month, data.year, data.hour, data.minute))
        #retorno_transacao.write('     "PWINFO_RESULTMSG" : "SEM TRANSACAO"')
        #retorno_transacao.write('\n}  \n')
        #retorno_transacao.close()
        #comp = transops.retorno_transacao()
        resultado_transacao = transops.retorno_transacao()
        print("resultado_transacaok", resultado_transacao)
        if 'aprovada' in resultado_transacao["PWINFO_RESULTMSG"].lower():
            self.__c.execute(
                "DELETE FROM tb_locacao WHERE senha = '%s'" % (__senha,))
            self.__c.execute("UPDATE tb_armario set estado = 'LIVRE' WHERE id_armario = %s" % (
                result_id_armario[0]))
            self.__conn.commit()
            self.__conn.close()
            #self.port = self.select_port(result_id_armario)
            
            #self.port.exec_port(__porta[0][0], "abre")
            return (resultado_transacao["PWINFO_RESULTMSG"])
        else:
            return (resultado_transacao["PWINFO_RESULTMSG"])

    def pagamento_locacao(self):
        p = None
        subprocess.run("docker start paygoweb", shell=True)
        #subprocess("docker exec paygoweb cd paygoWeb")
        
        p = subprocess.run('docker exec paygoweb /bin/bash -c "cd paygoWeb/ && python3 venda.py"', shell=True)
        #cmd = ['docker', 'exec', 'paygoweb', 'bash', '-c', 'cd paygoWeb && python3 venda.py']
        #p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #print(p)
        #subprocess('docker exec paygoweb bash -c "cd paygoWeb && python3 venda.py"')
        while p == None:
            print("processando...")
            sleep(0.2)
        subprocess.run("docker stop paygoweb", shell=True)
        #print("informe o codigo")
        
        #subprocess.run('docker exec paygoweb bash -c cd paygoWeb', shell=True)
        return True

    @classmethod
    def select_port(self, armario):
        __armario = []
        __conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        __c = __conn.cursor(buffered=True)
        __armario = armario
        print("__ARMARIO EM SELECT_port ", __armario)
        __c.execute(
            "select porta from tb_armario where id_armario='%s'" % (__armario))
        retorno_porta = __c.fetchall()
        __conn.close()
        return retorno_porta

    @classmethod
    def fechar_armario(self, id_armario):
        import serial
        self.serial = serial.Serial("/dev/ttyS0", 9600)
        porta = Portas()
        __id_armario = id_armario
        print("id armario em fechar armario data.py", __id_armario)
        __porta = self.select_port(__id_armario[0][0])
        print("porta select porta id_armario", __porta)
        porta.exec_port(str(__porta[0][0]), "fecha")
        #comando = str(__porta[0][0]) + ":fecha"
        #result = self.serial.write(b'%s' % comando.encode('utf-8'))
        #print(result)
        return "fechado"

    """"@classmethod
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
        __conn = mdb.connect(
            user='coolbaguser', password='m1cr0@t805i', database='coolbag')
        __c = __conn.cursor(buffered=True)
        __c.execute("select id_armario from tb_locacao where senha = '%s'" % senha)
        result = __c.fetchall()
        return result


if __name__ == "__main__":
    Banco()
