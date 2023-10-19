#!/usr/bin/env python3
import json
import os
import sys

import mysql.connector as mdb
import pandas as pd


class DataAccessObjectsNuvem(object):
    def __init__(self):
        self.__host = 'mysql.coolbagsafe.kinghost.net'
        self.__user = 'coolbagsaf_add1'
        self.__database = 'coolbagsafe'
        self.__passwd = 'm1cr0@t805i'
        self.diretorio = os.getcwd()

        self.__conn = mdb.connect(
            host=self.__host,
            user=self.__user,
            password=self.__passwd,
            database=self.__database,
        )
        self.__cursor = self.__conn.cursor(buffered=True)

        self.__cursor.execute(
            """CREATE TABLE IF NOT EXISTS `tb_armario` (
                `id_armario` NVARCHAR(30) NOT NULL,
                `classe` TINYTEXT NOT NULL ,
                `local` TINYTEXT NOT NULL,
                `terminal` VARCHAR(50) NOT NULL ,
                `estado` TINYTEXT NULL DEFAULT '' ,
                `nivel` TINYTEXT NULL DEFAULT '' ,
                `numeracao` TINYTEXT NULL DEFAULT NULL ,
                `porta` TINYTEXT NULL DEFAULT NULL ,
                `compartimento` TINYTEXT NULL DEFAULT NULL,
                PRIMARY KEY (`id_armario`)
                )
                ENGINE = InnoDB CHARACTER SET utf8 COLLATE utf8_general_ci;
                """
        )
        self.__cursor.execute(
            """ CREATE TABLE IF NOT EXISTS `tb_usuario` (
                                    `id_usuario` NVARCHAR(30)  NOT NULL,
                                    `nome` VARCHAR(50) NULL DEFAULT NULL,
                                    `email` VARCHAR(80) NOT NULL,
                                    `telefone` TEXT NOT NULL,
                                    PRIMARY KEY (`id_usuario`)
                                    )
                                    ENGINE = InnoDB CHARACTER SET utf8 COLLATE utf8_general_ci;"""
        )
        self.__cursor.execute(
            """CREATE TABLE IF NOT EXISTS `tb_locacao` (
                        `id_locacao` NVARCHAR(30) NOT NULL,
                        `data_locacao` datetime NOT NULL,
                        `tempo_locado` datetime NOT NULL,
                        `tempo_corrido` time DEFAULT '00:00:00',
                        `senha` tinytext COLLATE utf8mb4_unicode_ci NOT NULL,
                        `id_armario` NVARCHAR(30) NOT NULL,
                        `id_usuario` NVARCHAR(30) NOT NULL,
                        KEY `id_armario` (`id_armario`),
                        KEY `FK__tb_armario` (`id_armario`),
                        KEY `FK__tb_usuario` (`id_usuario`),
                        CONSTRAINT `FK__tb_armario` FOREIGN KEY (`id_armario`) REFERENCES `tb_armario` (`id_armario`) ON DELETE CASCADE ON UPDATE CASCADE,
                        CONSTRAINT `FK__tb_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `tb_usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
                        ) ENGINE = InnoDB CHARACTER SET utf8 COLLATE utf8_general_ci;

                        """
        )
        self.__cursor.execute(
            """CREATE TABLE IF NOT EXISTS `tb_locacao_persistence` (
                        `id_armario_persistence` NVARCHAR(30) NOT NULL,
                        `data_locacao` datetime NOT NULL,
                        `tempo_locado` datetime NOT NULL,
                        `tempo_corrido` time DEFAULT '00:00:00',
                        `id_armario` NVARCHAR(30) NOT NULL,
                        `id_usuario` NVARCHAR(30) NOT NULL,
                        `valor_locacao` double NOT NULL DEFAULT '0',
                        `classe` tinytext DEFAULT '',
                        KEY `id_armario_persistence` (`id_armario_persistence`),
                        KEY `FK_PERSISTENCE__tb_armario` (`id_armario`),
                        KEY `FK_PERSISTENCE__tb_usuario` (`id_usuario`),
                        CONSTRAINT `FK_PERSISTENCE__tb_armario` FOREIGN KEY (`id_armario`) REFERENCES `tb_armario` (`id_armario`) ON DELETE CASCADE ON UPDATE CASCADE,
                        CONSTRAINT `FK_PERSISTENCE__tb_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `tb_usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
                        ) ENGINE = InnoDB CHARACTER SET utf8 COLLATE utf8_general_ci;"""
        )

    # self.__conn.close()

    def dbn_passwd(self):
        return self.__passwd

    def dbn_user(self):
        return self.__user

    def dbn_host(self):
        return self.__host

    def dbn_database(self):
        return self.__database

    def create_user(self, id_user, nome, email, telefone):
        """verifica se existe um usuario já cadastrado atraves de busa pelo email
        ou telefone, caso haja , compara o email obtido do banco com o fornecido e o telefone
        obtido com o fornecido , havendo discrepancia ele atualiza o registro. Caso não haver
        registro algum é feito um novo registro.
        Dados: str: nome
        str: telefone
        str: email
        return: id_usuario"""

        # f = open(self.diretorio + "/create_user.json", "+w")
        # create_json = json.load(f).decoder("utf-8")

        __id_user = id_user
        __nome = nome
        __email = email
        __telefone = telefone

        consulta = ''

        self.__cursor.execute(
            "INSERT INTO tb_usuario (id_usuario, nome, email, telefone) values ('%s','%s','%s','%s')"
            % (__id_user, __nome, __email, __telefone)
        )
        self.__conn.commit()
        self.__cursor.execute(
            "SELECT id_usuario from tb_usuario where email='%s' AND telefone='%s'"
            % (
                __email,
                __telefone,
            )
        )
        consulta = self.__cursor.fetchall()
        print('-----CONSULTA ID USUARIO DAO NUVEM-----')
        print(consulta)
        # f.write("")
        # f.close()
        self.__conn.close()

    def select_armario(self, id_armario):
        classe_armario = pd.read_sql(
            'select classe from tb_armario where id_armario = %s' % id_armario,
            self.__conn,
        )
        print(classe_armario)

    def insert_locacao(
        self,
        id_locacao,
        __data_locacao,
        __data_limite,
        __senha,
        loca_armario,
        dados_locatario,
        __total,
    ):
        self.__cursor.execute(
            "INSERT INTO tb_locacao(id_locacao, data_locacao,tempo_locado,tempo_corrido,senha,id_armario,id_usuario) VALUES('%s', '%s','%s',null,'%s','%s','%s')"
            % (
                id_locacao,
                __data_locacao,
                __data_limite,
                __senha,
                loca_armario,
                dados_locatario,
            )
        )

        self.__cursor.execute(
            "UPDATE tb_armario SET estado = 'OCUPADO' where id_armario = '%s'"
            % (loca_armario)
        )

        self.__conn.commit()
        self.__cursor.execute(
            "INSERT INTO tb_locacao_persistence(id_locacao_persistence, data_locacao,tempo_locado,tempo_corrido,id_armario,id_usuario, valor_locacao) VALUES('%s', '%s','%s',null,'%s','%s','%s')"
            % (
                id_locacao,
                __data_locacao,
                __data_limite,
                loca_armario,
                dados_locatario,
                __total,
            )
        )

        self.__conn.commit()

    def cadastrar_armario(
        self, id_armario, classe, terminal, coluna, nivel, porta, compartimento
    ):

        # self.__c = self.__conn.cursor(buffered=True)
        self.__id_armario = id_armario
        self.__classe = classe
        self.__local = 'home'
        self.__terminal = terminal
        self.__coluna = coluna
        self.__nivel = nivel
        self.__porta = porta
        self.__compartimento = compartimento
        self.__cursor.execute(
            "select porta, compartimento  from tb_armario where porta='%s' and compartimento = '%s' and estado='LIVRE'"
            % (self.__porta, self.__compartimento)
        )
        select_porta = self.__cursor.fetchall()
        print('select_porta', select_porta)
        if select_porta == None or select_porta == [] or select_porta == '':

            self.__compartimento = compartimento
            self.__cursor.execute(
                'INSERT INTO tb_armario ( id_armario, classe, terminal, local, estado, nivel, porta, compartimento )'
                + "VALUES ('%s','%s','%s','%s', 'LIVRE', '%s', '%s', '%s')",
                (
                    self.__id_armario,
                    self.__classe,
                    self.__terminal,
                    self.__coluna,
                    self.__nivel,
                    self.__porta,
                    self.__compartimento,
                ),
            )
            result = self.__cursor.fetchone()
            self.__conn.commit()
            self.__conn.close()
            DAON.cadastrar_armario(
                id_armario,
                classe,
                terminal,
                coluna,
                nivel,
                porta,
                compartimento,
            )
            return (
                self.__classe,
                self.__coluna,
                self.__nivel,
                self.__terminal,
                'cadastrado com sucesso',
            )
        else:
            return 'porta ou compartimento já utilizada confira a porta exata para o cadastro e evite problemas!'

    def remover_armario(self, id_armario):

        self.__id = id_armario
        self.__c.execute(
            "SELECT estado  from tb_armario where id_armario = '%s'"
            % (self.__id)
        )
        result = self.__c.fetchall()
        if result == 'LIVRE':
            self.__c.execute(
                "DELETE FROM tb_armario where id_armario = '%s' " % (self.__id)
            )
        else:
            return 'não é possível remover armario, verifique se o mesmo não está em uso'

    @staticmethod
    def finalizar(valor_locacao, senha, id_armario):
        __host = 'mysql.coolbagsafe.kinghost.net'
        __user = 'coolbagsaf_add1'
        __database = 'coolbagsafe'
        __passwd = 'm1cr0@t805i'
        __conn = mdb.connect(
            host=__host, user=__user, password=__passwd, database=__database
        )
        __cursor = __conn.cursor(buffered=True)
        __cursor.execute(
            "DELETE FROM tb_locacao WHERE senha = '%s'" % (senha,)
        )

        __cursor.execute(
            "UPDATE tb_armario set estado = 'LIVRE' WHERE id_armario = '%s'"
            % (id_armario,)
        )

        __cursor.execute(
            "UPDATE tb_locacao_persistence set valor_locacao = '%s' WHERE id_armario = '%s'"
            % (
                valor_locacao,
                id_armario,
            )
        )
        __conn.commit()

        __conn.close()
