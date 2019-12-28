import os , sys
from interops_test import *
from Enums import *

from ctypes import *
from CustomObjects import *

class Venda:
    def __init__(self):
        #valor = args
        
        self.pgWeb = PGWebLibrary()
        # INICIALIZA A BIBLIOTECA 
        self.pgWeb.PW_iInit()
        
        #MANDADATORY PARAMS
        self.PWINFO_AUTNAME =  "COOLBAGSAFE-RENTLOCKER" # 21
        self.PWINFO_AUTVER = "1.0" #22
        self.PWINFO_AUTDEV = "COOLBAG-SAFE GUARDA BAGAGENS AUTOMATIZADO LTDA" # 23
        self.PWINFO_AUTCAP = "4" #36
        self.PWINFO_AUTHSYST = "REDE"
        #PARAMS DEFAULT PARAMS
        self.PWINFO_CURRENCY = "986"
        self.PWINFO_CURREXP = "2" 
        self.venda()
    def PW_iExecGetData(self, vstParam, iNumParam):
        i = j = iKey = iRet = ''
        szAux = c_buffer(1024) 
        szDspMsg = c_buffer(128)
        szMsgPinPad = c_buffer(34)
        ulEvent= c_int32(0)
        if vstParam[0].szMsgPrevia != None and vstParam[0].szMsgPrevia == True:
            print(vstParam[0].szMsgPrevia)
        

        #PERCORRE TODOS OS DADOS ENQUANTO HOUVER PARA CAPTURA
        while iRet != E_PWRET.PWRET_OK.value or iRet == E_PWRET.PWRET_NOTHING.value or iRet == E_PWRET.PWRET_DISPLAY.value:
            for i in range(0, iNumParam):
                print("vstParam[i].wIdentificador", vstParam[i].wIdentificador)
                if vstParam[i].wIdentificador == E_PWINFO.PWINFO_CARDTYPE.value:
                    ret = vstParam[i].ulTipoEntradaCartao
                    print("ret ulTipoEntradaCartao", vstParam[i].ulTipoEntradaCartao) 
                    ret = self.pgWeb.PW_iPPGetCard(i)
                    print("ret getcard", ret)
                elif vstParam[i].bTipoDeDado == E_PWDAT.PWDAT_MENU.value:
                    if vstParam[i].bNumOpcoesMenu == 1:
                        ret = self.pgWeb.PW_iAddParam(vstParam[i].wIdentificador, str(vstParam[i].vszValorMenu[0]))
                        print(ret, ret)
                    elif vstParam[i].bNumOpcoesMenu >= 2:
                        num = vstParam[i].bNumOpcoesMenu
                        x = 0
                        print("vstParam[i].bNumOpcoesMenu", vstParam[i].bNumOpcoesMenu)
                        for j in range(0,vstParam[i].bNumOpcoesMenu):
                            
                            ret = self.pgWeb.PW_iAddParam(vstParam[i].wIdentificador, str(vstParam[i].vszValorMenu[j]))
                            print("add param menu",ret)
                           


                sleep(3)



    def venda(self):
        self.szDspMsg = create_string_buffer(100000)
        vstParam_11 = (PW_GetData * 11)
        vstParam = vstParam_11()
        iNumParam = 10
        ulEvent = c_byte(0)
        # INICIA UMA NOVATRANSACAO
        self.pgWeb.PW_iNewTransac(0x21)
        self.pgWeb.PW_iAddParam(21, self.PWINFO_AUTNAME)
        self.pgWeb.PW_iAddParam(22, self.PWINFO_AUTVER)
        self.pgWeb.PW_iAddParam(23, self.PWINFO_AUTDEV)
        self.pgWeb.PW_iAddParam(36, self.PWINFO_AUTCAP)
        self.pgWeb.PW_iAddParam(0x26, self.PWINFO_CURRENCY) 
        self.pgWeb.PW_iAddParam(0x27, self.PWINFO_CURREXP)
        self.pgWeb.PW_iAddParam(53, self.PWINFO_AUTHSYST)
        self.pgWeb.PW_iAddParam(41,"1")
        wait = ''
        getCard = ''
        while wait == '':
            self.pgWeb.PW_iPPDisplay("INSERIR, PASSAR OU APROXIMAR O CARTÃO")
            
            wait = self.pgWeb.PW_iPPWaitEvent(POINTER(c_byte(ulEvent)))
            print("byref ulevent",byref(ulEvent))
            getCard = self.pgWeb.PW_iPPEventLoop(self.szDspMsg, sizeof(self.szDspMsg))
            print("getCard", getCard)
            print("wait", wait)
        
        ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
        getCard = self.pgWeb.PW_iPPEventLoop(self.szDspMsg, sizeof(self.szDspMsg))
        print("getCard", wait, getCard)
        print("ulEvent", ulEvent)
        if ret == -2497:
            ret = self.PW_iExecGetData(vstParam, iNumParam)

        

        """while wait != 0:
            self.pgWeb.PW_iPPDisplay("INSERIR, PASSAR OU APROXIMAR O CARTÃO")
            getCard = self.pgWeb.PW_iPPEventLoop(self.szDspMsg, sizeof(self.szDspMsg))
            print("getCard", wait, getCard)
            wait = self.pgWeb.PW_iPPWaitEvent(15)
            print("wait", wait)"""
            
            
                
        

if __name__ == "__main__":
    Venda()
