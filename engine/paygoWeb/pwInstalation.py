import datetime
import json
import os
import sys
from ctypes import *

from CustomObjects import *
from Enums import *
from Interops import *


class PgwInstall:
    def __init__(self):
        self.pgWeb = PGWebLibrary()
        self.pgWeb.PW_iInit()

        self.pgWeb = PGWebLibrary()
        # INICIALIZA A BIBLIOTECA
        self.pgWeb.PW_iInit()
        # EXECUTA A FUNÇÃO VENDA

        self.install()

    def install(self):

        iRet = ''
        vstParam_11 = PW_GetData * 11
        vstParam = vstParam_11()
        iNumParam = 10
        ulEvent = 0
        szDspMsg = c_buffer(128)
        szAux = create_string_buffer(10000)
        wait = ''
        retEventLoop = ''
        ret = ''
        ret2 = ''

        self.pgWeb.PW_iNewTransac(0x01)
        self.pgWeb.PW_iAddParam(0x11, '62547')   # self.PWINFO_POSID
        self.pgWeb.PW_iAddParam(
            0x15, 'COOLBAGSAFE-RENTLOCKER'
        )   # self.PWINFO_AUTNAME
        self.pgWeb.PW_iAddParam(0x16, '1.0')   # self.PWINFO_AUTVER)
        self.pgWeb.PW_iAddParam(
            0x17, 'COOLBAG-SAFE GUARDA BAGAGENS AUTOMATIZADO'
        )   # self.PWINFO_AUTDEV)
        self.pgWeb.PW_iAddParam(0x24, '28')   # self.PWINFO_AUTCAP)
        self.pgWeb.PW_iAddParam(
            0x1B, 'app.tpgw.ntk.com.br:17502'
        )   # self.PWINFO_DESTTCPIP
        self.pgWeb.PW_iAddParam(
            0x1C, '35223093000106'
        )   # self.PWINFO_MERCHCNPJCPF)
        self.pgWeb.PW_iAddParam(0xF6, '314159')   # self.PWINFO_AUTHTECHUSER)
        self.pgWeb.PW_iAddParam(0x7F01, '1')   # self.PWINFO_USINGPINPAD)
        self.pgWeb.PW_iAddParam(0x7F02, '0')   # self.PWINFO_PPCOMMPORT)

        ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)

        while ret == -2497 or ret == E_PWRET.PWRET_NOTHING.value:
            # ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
            ret = self.pgWeb.PW_iExecGetData(vstParam, iNumParam)
            print('ret exectransac venda', ret)

            if ret == E_PWRET.PWRET_CANCEL.value:
                print('E_PWRET.PWRET_CANCEL')
                self.pgWeb.PW_iPPAbort()
                retEventLoop = self.pgWeb.PW_iPPEventLoop(
                    self.szDspMsg, sizeof(self.szDspMsg)
                )
                print('retEventLoop', retEventLoop)
                return retEventLoop
            elif ret == E_PWRET.PWRET_HOSTTIMEOUT.value:
                self.pgWeb.PW_iPPAbort()
                retEventLoop = self.pgWeb.PW_iPPEventLoop(
                    self.szDspMsg, sizeof(self.szDspMsg)
                )
                print('retEventLoop', retEventLoop)
                return retEventLoop
            elif ret == E_PWRET.PWRET_REQPARAM.value:
                print('PWRET_REQPARAM', E_PWRET.PWRET_REQPARAM.value)
                self.pgWeb.PW_iPPAbort()
                retEventLoop = self.pgWeb.PW_iPPEventLoop(
                    self.szDspMsg, sizeof(self.szDspMsg)
                )
                print('retEventLoop', retEventLoop)
                return retEventLoop
            elif ret == E_PWRET.PWRET_FROMHOSTPENDTRN.value:
                print(
                    'PWRET_FROMHOSTPENDTRN',
                    E_PWRET.PWRET_FROMHOSTPENDTRN.value,
                )
                self.confirmPendTransaction(
                    transactionStatus=1, transactionResponse=ret
                )
                retEventLoop = self.pgWeb.PW_iPPEventLoop(
                    self.szDspMsg, sizeof(self.szDspMsg)
                )
                print('retEventLoop', retEventLoop)
                return retEventLoop
            ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
            print('efetuando a transacao...')
            print('ret ---->', ret)


if __name__ == '__main__':
    PgwInstall()
