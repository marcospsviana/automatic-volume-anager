import sys, os
import mysql.connector as mdb


class DataAccessObjectsNuvem(object):
    def __init__(self):
        super(DataAccessObjectsBase, self).__init__()
        self.__host = "mysql.coolbagsafe.kinghost.net"
        self.__user = "coolbagsaf_add1"
        self.__database = "coolbagsafe"
        self.__passwd = "m1cr0@t805i"
    

        self.__CONN = mdb.connect(host = self.__host, user = self.__user, passwd = self.__passwd, database = self.__database)
        self.__cursor = self.__CONN.cursor(buffered=True)

        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS`tb_armario` (
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
        self.__cursor.execute(''' CREATE TABLE IF NOT EXISTS `tb_usuario` (
                                    `id_usuario` INT(10)  AUTO_INCREMENT,
                                    `nome` VARCHAR(50) NULL DEFAULT NULL,
                                    `email` VARCHAR(80) NOT NULL,
                                    `telefone` TEXT NOT NULL,
                                    PRIMARY KEY (`id_usuario`)
                                    )
                                    ENGINE=InnoDB;''')
        self.__cursor.execute('''CREATE TABLE IF NOT EXISTS `tb_locacao` (
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
        self.__CONN.close()

    
    def db_passwd(self):
        return self.__passwd


    def db_user(self):
        return self.__user


    def db_host(self):
        return self.__host
    
    def db_database(self):
        return self.__database
