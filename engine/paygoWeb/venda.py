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
        #self.PWINFO_AUTCAP = "15" #36
        #self.PWINFO_AUTHSYST = "CIELO"
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
        szDspMsg = c_buffer(128)
        szAux = create_string_buffer(10000)
        wait = ''
        retEventLoop = ''
        """self.pgWeb.PW_iPPDisplay("APROXIME, INSIRA OU\r PASSE O CARTAO")
        retEventLoop = self.pgWeb.PW_iPPEventLoop(self.szDspMsg, sizeof(self.szDspMsg))
            
        wait = self.pgWeb.PW_iPPWaitEvent(15)

        while retEventLoop == '' and retEventLoop != 0:
            
            retEventLoop = self.pgWeb.PW_iPPEventLoop(self.szDspMsg, sizeof(self.szDspMsg))
            print("retEventLoop", retEventLoop)
            print("wait", wait)
            return retEventLoop"""
        
       

            
        ret = ''    
        # INICIA UMA NOVA TRANSACAO
        self.pgWeb.PW_iNewTransac(0x21)
        self.pgWeb.PW_iAddParam(21, self.PWINFO_AUTNAME)
        self.pgWeb.PW_iAddParam(22, self.PWINFO_AUTVER)
        self.pgWeb.PW_iAddParam(23, self.PWINFO_AUTDEV)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTCAP.value, "28")
        self.pgWeb.PW_iAddParam(0x26, self.PWINFO_CURRENCY) 
        self.pgWeb.PW_iAddParam(0x27, self.PWINFO_CURREXP)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTHSYST.value, "CIELO")
        self.pgWeb.PW_iAddParam(0x29,"1")
        self.pgWeb.PW_iAddParam(59, "1")
        self.pgWeb.PW_iAddParam(0x25, "1200")
        self.pgWeb.PW_iAddParam(0x1F21, "1") #PWINFO_PAYMNTMODE 1 SOMENTE CARTAO
        #self.pgWeb.PW_iAddParam(0xF4, "0")
        #self.pgWeb.PW_iAddParam(0, "28") #PWINFO_CARDENTMODE = 192
        self.pgWeb.PW_iAddParam(77, "00")
        self.pgWeb.PW_iAddParam(78, "00")
        #self.pgWeb.PW_iAddParam(0xF6, "314159")
        
        
        
        ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
        
        while ret == E_PWRET.PWRET_MOREDATA.value or ret != E_PWRET.PWRET_OK.value or ret == E_PWRET.PWRET_NOTHING.value:
            #ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
            ret = self.pgWeb.PW_iExecGetData(vstParam, iNumParam)
            print("ret exectransac venda", ret)
            
            if ret == 0:
                ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
                
                if ret == 0:
                    PWINFO_REQNUM = PWINFO_AUTLOCREF = PWINFO_AUTEXTREF = PWINFO_VIRTMERCH = PWINFO_AUTHSYST = ''
                    
                    for i in range(iNumParam):
                        if vstParam[i].wIdentificador == E_PWINFO.PWINFO_REQNUM.value:
                            self.pgWeb.PW_iGetResult(
                                vstParam[i].wIdentificador, szAux, sizeof(szAux))
                            PWINFO_REQNUM = szAux.value
                            print("PWINFO_REQNUM", PWINFO_REQNUM)
                        elif vstParam[i].wIdentificador == E_PWINFO.PWINFO_AUTLOCREF.value:
                            self.pgWeb.PW_iGetResult(
                                vstParam[i].wIdentificador, szAux, sizeof(szAux))
                            PWINFO_AUTLOCREF = szAux.value
                            print("PWINFO_AUTLOCREF", PWINFO_AUTLOCREF)
                        elif vstParam[i].wIdentificador == E_PWINFO.PWINFO_AUTEXTREF.value:
                            self.pgWeb.PW_iGetResult(
                                vstParam[i].wIdentificador, szAux, sizeof(szAux))
                            PWINFO_AUTEXTREF = szAux.value
                            print("PWINFO_AUTEXTREF", PWINFO_AUTEXTREF)
                        elif vstParam[i].wIdentificador == E_PWINFO.PWINFO_VIRTMERCH.value:
                            self.pgWeb.PW_iGetResult(
                                vstParam[i].wIdentificador, szAux, sizeof(szAux))
                            PWINFO_VIRTMERCH = szAux.value
                            print("PWINFO_VIRTMERCH", PWINFO_VIRTMERCH)
                        elif vstParam[i].wIdentificador == E_PWINFO.PWINFO_AUTHSYST.value:
                            self.pgWeb.PW_iGetResult(
                                vstParam[i].wIdentificador, szAux, sizeof(szAux))
                            PWINFO_AUTHSYST = szAux.value
                            print("PWINFO_AUTHSYST", PWINFO_AUTHSYST)
                        elif vstParam[i].wIdentificador == E_PWINFO.PWINFO_RCPTMERCH.value:
                            print("result transacao nota")
                            self.pgWeb.PW_iGetResult(
                                vstParam[i].wIdentificador, szAux, sizeof(szAux))
                            COMPROVANTE = szAux.value
                            f = open('comprovantes/COMPROVANTE Nº %s:%s-%s-%s %s:%s:%s.txt'%(PWINFO_REQNUM, data.day, data.month, data.year, data.hour, data.minute, data.second),'w')
                            f.write(COMPROVANTE)
                            f.close()
                        elif vstParam[i].wIdentificador == E_PWINFO.PWINFO_RESULTMSG.value:
                            print("result transacao mal sucedida")
                            COMPROVANTE = self.pgWeb.PW_iGetResult(
                                vstParam[i].wIdentificador, szAux, sizeof(szAux))
                            f = open('comprovantes/COMPROVANTE MALSUCEDIDO Nº %s:%s-%s-%s %s:%s:%s.txt'%(PWINFO_REQNUM, data.day, data.month, data.year, data.hour, data.minute, data.second),'w')
                            f.write(COMPROVANTE)
                            f.close()
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
