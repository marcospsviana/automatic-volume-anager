import sys, os
import mysql.connector as mdb


class DataAccessObjectsNuvem(object):
    def __init__(self):
        super(DataAccessObjectsBase, self).__init__()
        self.__host = "mysql.coolbagsafe.kinghost.net"
        self.__user = "coolbagsaf_add1"
        self.__database = "coolbagsafe"
        self.__passwd = "m1cr0@t805i"
    

        self.__conn = mdb.connect(host = self.__host, user = self.__user, passwd = self.__passwd, database = self.__database)
        self.__cursor = self.__conn.cursor(buffered=True)

        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS `coolbagsafe`.`tb_armario` ( `id_armario` VARCHAR(15) NOT NULL,
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
                ENGINE = InnoDB CHARACTER SET utf8 COLLATE utf8_general_ci;
                '''
                                )
        self.__cursor.execute(''' CREATE TABLE IF NOT EXISTS `coolbagsafe`.`tb_usuario` (
                                    `id_usuario` VARCHAR(15)  NOT NULL,
                                    `nome` VARCHAR(50) NULL DEFAULT '',
                                    `email` VARCHAR(80) NOT NULL,
                                    `telefone` TEXT NOT NULL,
                                    PRIMARY KEY (`id_usuario`)
                                    )
                                    ENGINE = InnoDB CHARACTER SET utf8 COLLATE utf8_general_ci;''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS `coolbagsafe`.`tb_locacao` (
                        `id_locacao` VARCHAR(15) NOT NULL,
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
                        ) ENGINE = InnoDB CHARACTER SET utf8 COLLATE utf8_general_ci;

                        ''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS `tb_locacao_persistence` (
                        `id_locacao_persistence` VARCHAR(15) NOT NULL,
                        `data_locacao` datetime NOT NULL,
                        `tempo_locado` datetime NOT NULL,
                        `tempo_corrido` time DEFAULT '00:00:00',
                        `id_armario` int(10) NOT NULL DEFAULT '0',
                        `id_usuario` int(10) NOT NULL DEFAULT '0',
                        `valor_locacao` double NOT NULL DEFAULT '0',
                        KEY `id_locacao_persistence` (`id_locacao_persistence`),
                        KEY `FK__tb_armario` (`id_armario`),
                        KEY `FK__tb_usuario` (`id_usuario`),
                        CONSTRAINT `FK_PERSISTENCE__tb_armario` FOREIGN KEY (`id_armario`) REFERENCES `tb_armario` (`id_armario`) ON DELETE CASCADE ON UPDATE CASCADE,
                        CONSTRAINT `FK_PERSISTENCE__tb_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `tb_usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
                        ) ENGINE = InnoDB CHARACTER SET utf8 COLLATE utf8_general_ci;''')

        self.__conn.close()

    
    def db_passwd(self):
        return self.__passwd


    def db_user(self):
        return self.__user


    def db_host(self):
        return self.__host
    
    def db_database(self):
        return self.__database

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
        self.__cursor.execute(
            "SELECT * from tb_usuario where email= '%s' OR telefone= '%s'" % (__email, __telefone))
        self.select = self.__cursor.fetchall()

        if self.select == [] or self.select == None:
            consulta = ''

            self.__cursor.execute("INSERT INTO tb_usuario (id_usuario, nome, email, telefone) values (null,'%s','%s','%s')" % (
                __nome, __email,  __telefone))
            self.__conn.commit()
            self.__cursor.execute("SELECT id_usuario from tb_usuario where email='%s' AND telefone='%s'" % (
                __email, __telefone,))
            consulta = self.__cursor.fetchall()
            print("-----CONSULTA ID USUARIO-----")
            print(consulta)
            return consulta

        elif self.select[0][2] != __email and self.select[0][3] == __telefone:
                self.__cursor.execute("UPDATE tb_usuario SET email = '%s' WHERE id_usuario = %s" % (
                    __email, self.select[0][0]))
                self.__conn.commit()

                return self.select[0][0]  # id_usuario
        elif self.select[0][2] == __email and self.select[0][3] != __telefone:
                self.__cursor.execute("UPDATE tb_usuario SET telefone = '%s' WHERE id_usuario = %s" % (
                    __telefone, self.select[0][0]))
                self.__conn.commit()
                return self.select[0][0]
        else:
            return self.select[0][0] 

    def select_armario(self, id_armario):
        classe_armario = pd.read_sql(
            "select classe from tb_armario where id_armario = %s" % id_armario, self.__conn)
        print(classe_armario)
        


    def insert_locacao(__data_locacao, __data_limite, __senha, loca_armario, dados_locatario, __total):
        self.__cursor.execute("INSERT INTO tb_locacao(id_locacao, data_locacao,tempo_locado,tempo_corrido,senha,id_armario,id_usuario, valor_locacao) VALUES(null, '%s','%s',null,'%s',%s,%s,%s)" % (__data_locacao, __data_limite, __senha, loca_armario, dados_locatario, __total))
            
        self.__cursor.execute("UPDATE tb_armario SET estado = 'OCUPADO' where id_armario = %s" % (loca_armario))

        self.__conn.commit()
        self.__cursor.execute("INSERT INTO tb_locacao_persistence(id_locacao_persistence, data_locacao,tempo_locado,tempo_corrido,id_armario,id_usuario, valor_locacao) VALUES(null, '%s','%s',null,'%s',%s,%s,%s)" % (self.__data_locacao, self.__data_limite, loca_armario[0], self.dados_locatario, self.__total))
            
        self.__conn.commit()
    
    def cadastrar_armario(self, classe, terminal, coluna, nivel, porta, compartimento):

        #self.__c = self.__conn.cursor(buffered=True)
        self.__classe = classe
        self.__local = 'home'
        self.__terminal = terminal
        self.__coluna = coluna
        self.__nivel = nivel
        self.__porta = porta
        self.__compartimento = compartimento
        self.__cursor.execute("select porta, compartimento  from tb_armario where porta='%s' and compartimento = '%s' and estado='LIVRE'" % (
            self.__porta, self.__compartimento))
        select_porta = self.__cursor.fetchall()
        print("select_porta", select_porta)
        if select_porta == None or select_porta == [] or select_porta == "":

            self.__compartimento = compartimento
            self.__cursor.execute("INSERT INTO tb_armario ( id_armario, classe, terminal, local, estado, nivel, porta, compartimento )" +
                             "VALUES (0,%s,%s,%s, 'LIVRE', %s, %s, %s)", (self.__classe, self.__terminal, self.__coluna, self.__nivel, self.__porta, self.__compartimento))
            result = self.__cursor.fetchone()
            self.__conn.commit()
            self.__conn.close()
            return (self.__classe, self.__coluna, self.__nivel, self.__terminal, "cadastrado com sucesso")
        else:
            return "porta ou compartimento já utilizada confira a porta exata para o cadastro e evite problemas!"
        
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
    
    def finalizar(self, senha, id_armario):
        self.__c.execute(
            "DELETE FROM tb_locacao WHERE senha = '%s'" % (__senha,))
        self.__c.execute(
            "UPDATE tb_armario set estado = 'LIVRE' WHERE id_armario = '%s'" % (id_armario,))
        self.__conn.commit()
