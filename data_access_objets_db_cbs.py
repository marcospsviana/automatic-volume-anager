import sys, os
import mysql.connector as mdb
import subprocess



class DataAccessObjectsBase(object):
    def __init__(self):
        #super(DataAccessObjectsBase, self).__init__()
        self.__host = "localhost"
        self.__user = "root"
        self.__database = "coolbag"
        self.__passwd = "microat8051"
    

        self.__conn = mdb.connect(host = self.__host, user = self.__user, passwd = self.__passwd, database = self.__database)
        self.__cursor = self.__conn.cursor(buffered=True)

        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS `tb_armario` (
                `id_armario` NVARCHAR(30) NOT NULL,
                `classe` TINYTEXT NOT NULL,
                `local` TINYTEXT NOT NULL,
                `terminal` VARCHAR(50) NOT NULL,
                `estado` TINYTEXT NULL DEFAULT '',
                `nivel` TINYTEXT NULL DEFAULT '',
                `numeracao` TINYTEXT NULL DEFAULT NULL,
                `porta` TINYTEXT NULL DEFAULT NULL,
                `compartimento` TINYTEXT NULL DEFAULT NULL,
                PRIMARY KEY (`id_armario`)
                )
                ENGINE = InnoDB CHARACTER SET utf8 COLLATE utf8_general_ci;
                '''
                                )
        self.__cursor.execute(''' CREATE TABLE IF NOT EXISTS `tb_usuario` (
                                    `id_usuario` NVARCHAR(30)  NOT NULL,
                                    `nome` VARCHAR(50) NULL DEFAULT NULL,
                                    `email` VARCHAR(80) NOT NULL,
                                    `telefone` TEXT NOT NULL,
                                    PRIMARY KEY (`id_usuario`)
                                    )
                                    ENGINE = InnoDB CHARACTER SET utf8 COLLATE utf8_general_ci;''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS `tb_locacao` (
                        `id_locacao` NVARCHAR(30) NOT NULL,
                        `data_locacao` datetime NOT NULL,
                        `tempo_locado` datetime NOT NULL,
                        `tempo_corrido` time DEFAULT '00:00:00',
                        `senha` tinytext COLLATE utf8mb4_unicode_ci NOT NULL,
                        `id_armario` NVARCHAR(30) NOT NULL,
                        `id_usuario` NVARCHAR(30) NOT NULL,
                        KEY `id_locacao` (`id_locacao`),
                        KEY `FK__tb_armario` (`id_armario`),
                        KEY `FK__tb_usuario` (`id_usuario`),
                        CONSTRAINT `FK__tb_armario` FOREIGN KEY (`id_armario`) REFERENCES `tb_armario` (`id_armario`) ON DELETE CASCADE ON UPDATE CASCADE,
                        CONSTRAINT `FK__tb_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `tb_usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
                        ) ENGINE = InnoDB CHARACTER SET utf8 COLLATE utf8_general_ci;

                        ''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS `tb_locacao_persistence` (
                        `id_locacao_persistence` NVARCHAR(30) NOT NULL,
                        `data_locacao` datetime NOT NULL,
                        `tempo_locado` datetime NOT NULL,
                        `tempo_corrido` time DEFAULT '00:00:00',
                        `id_armario` NVARCHAR(30) NOT NULL,
                        `id_usuario` NVARCHAR(30) NOT NULL,
                        `valor_locacao` double NOT NULL DEFAULT '0',
                        `classe` tinytext DEFAULT '',
                        KEY `id_locacao_persistence` (`id_locacao_persistence`),
                        KEY `FK_PERSISTENCE__tb_armario` (`id_armario`),
                        KEY `FK_PERSISTENCE__tb_usuario` (`id_usuario`),
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

            self.__cursor.execute("INSERT INTO tb_usuario (id_usuario, nome, email, telefone) values ('%s','%s','%s','%s')" % (
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
    
    @classmethod
    def docker_run(self):
        subprocess.run('docker exec paygoweb /bin/bash -c "cd /opt/paygoWeb/ && python3 venda.py"', shell=True)
    
    

