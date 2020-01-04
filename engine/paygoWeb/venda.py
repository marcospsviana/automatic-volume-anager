import os , sys
#from Interops import *
from Interops import *
from Enums import *

from ctypes import *
from CustomObjects import *

class Venda:
    def __init__(self):
        
        self.szDspMsg = create_string_buffer(100000)
        
        self.pgWeb = PGWebLibrary()
        # INICIALIZA A BIBLIOTECA 
        self.pgWeb.PW_iInit()
        
        #MANDADATORY PARAMS
        self.PWINFO_AUTNAME =  "COOLBAGSAFE-RENTLOCKER" # 21
        self.PWINFO_AUTVER = "1.0" #22
        self.PWINFO_AUTDEV = "COOLBAG-SAFE GUARDA BAGAGENS AUTOMATIZADO LTDA" # 23
        self.PWINFO_AUTCAP = "4" #36
        self.PWINFO_AUTHSYST = "CIELO"
        #PARAMS DEFAULT PARAMS
        self.PWINFO_CURRENCY = "986"
        self.PWINFO_CURREXP = "2" 
        #self.PWINFO_CARDTYPE = "3" # DEBITO E CREDITO
        self.venda()
    



    def venda(self):
        iRet = ''
        vstParam_11 = (PW_GetData * 11)
        vstParam = vstParam_11()
        iNumParam = 10
        ulEvent = 0
        szAux = create_string_buffer(10000)
        # INICIA UMA NOVA TRANSACAO
        self.pgWeb.PW_iNewTransac(0x21)
        self.pgWeb.PW_iAddParam(21, self.PWINFO_AUTNAME)
        self.pgWeb.PW_iAddParam(22, self.PWINFO_AUTVER)
        self.pgWeb.PW_iAddParam(23, self.PWINFO_AUTDEV)
        self.pgWeb.PW_iAddParam(36, self.PWINFO_AUTCAP)
        self.pgWeb.PW_iAddParam(0x26, self.PWINFO_CURRENCY) 
        self.pgWeb.PW_iAddParam(0x27, self.PWINFO_CURREXP)
        self.pgWeb.PW_iAddParam(53, self.PWINFO_AUTHSYST)
        #self.pgWeb.PW_iAddParam(0x29,"1")
        self.pgWeb.PW_iAddParam(59, "1")
        self.pgWeb.PW_iAddParam(0x25, "1200")
        self.pgWeb.PW_iAddParam(0x1F21, "1") #PWINFO_PAYMNTMODE 1 SOMENTE CARTAO
        #self.pgWeb.PW_iAddParam(0xF4, "0")
        #self.pgWeb.PW_iAddParam(0, "28") #PWINFO_CARDENTMODE = 192
        self.pgWeb.PW_iAddParam(77, "00")
        self.pgWeb.PW_iAddParam(78, "00")
        
        wait = ''
        retEventLoop = ''
        self.pgWeb.PW_iPPDisplay("APROXIME, INSIRA OU\r PASSE O CARTAO")
            
        wait = self.pgWeb.PW_iPPWaitEvent(15)
        while retEventLoop == '' and retEventLoop != 0:
            
            retEventLoop = self.pgWeb.PW_iPPEventLoop(self.szDspMsg, sizeof(self.szDspMsg))
            print("retEventLoop", retEventLoop)
            print("wait", wait)

            
        ret = ''    
        
        
        ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
        
        while ret == -2497 or ret != E_PWRET.PWRET_OK.value or ret == E_PWRET.PWRET_NOTHING.value:
            
            ret = self.pgWeb.PW_iExecGetData(vstParam, iNumParam)
            print("ret exectransac venda", ret)
            if ret == 0:
                ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
                if ret == 0:
                    PWINFO_REQNUM = PWINFO_AUTLOCREF = PWINFO_AUTEXTREF = PWINFO_VIRTMERCH = PWINFO_AUTHSYST = ''
                    
                    for i in range(iNumParam):
                        if vstParam[i].wIdentificador == E_PWINFO.PWINFO_REQNUM.value:
                            PWINFO_REQNUM = self.pgWeb.PW_iGetResult(vstParam[i].wIdentificador, szAux, sizeof(szAux))
                        elif vstParam[i].wIdentificador == E_PWINFO.PWINFO_AUTLOCREF.value:
                            PWINFO_AUTLOCREF = self.pgWeb.PW_iGetResult(vstParam[i].wIdentificador, szAux, sizeof(szAux))
                        elif vstParam[i].wIdentificador == E_PWINFO.PWINFO_AUTEXTREF.value:
                            PWINFO_AUTEXTREF = self.pgWeb.PW_iGetResult(vstParam[i].wIdentificador, szAux, sizeof(szAux))
                        elif vstParam[i].wIdentificador == E_PWINFO.PWINFO_VIRTMERCH.value:
                            PWINFO_VIRTMERCH = self.pgWeb.PW_iGetResult(vstParam[i].wIdentificador, szAux, sizeof(szAux))
                        elif vstParam[i].wIdentificador == E_PWINFO.PWINFO_AUTHSYST.value:
                            PWINFO_AUTHSYST = self.pgWeb.PW_iGetResult(vstParam[i].wIdentificador, szAux, sizeof(szAux))
                    iRet = self.pgWeb.PW_iConfirmation(
                                                    E_PWCNF.PWCNF_CNF_AUTO.value, 
                                                    PWINFO_REQNUM, 
                                                    PWINFO_AUTLOCREF,
                                                    PWINFO_AUTEXTREF,
                                                    PWINFO_VIRTMERCH,
                                                    PWINFO_AUTHSYST
                                                    )
                    return iRet
            
                print(" ret exectransac venda", ret)



        

       
            
            
                
        

if __name__ == "__main__":
    Venda()
