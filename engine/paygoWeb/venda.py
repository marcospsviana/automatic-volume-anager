import os , sys

from Interops import *
from Enums import *
import datetime
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
        ret = '' 
        ret2 = '' 
          
        # INICIA UMA NOVA TRANSACAO
        self.pgWeb.PW_iNewTransac(E_PWOPER.PWOPER_SALE.value)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTNAME.value, self.PWINFO_AUTNAME)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTVER.value, self.PWINFO_AUTVER)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTDEV.value, self.PWINFO_AUTDEV)
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTCAP.value, "28")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_CURRENCY.value, "986") # MOEDA: REAL
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_CURREXP.value, "2") 
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_AUTHSYST.value, "CIELO")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_CARDTYPE.value,"2") # 1 - CREDITO 2 - DEBITO
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_FINTYPE.value, "1") # 1 A VISTA
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_TOTAMNT.value, "2050")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_PAYMNTMODE.value, "1") # 1 SOMENTE CARTAO
        #self.pgWeb.PW_iAddParam(0, "28") #PWINFO_CARDENTMODE = 192
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_BOARDINGTAX.value, "00")
        self.pgWeb.PW_iAddParam(E_PWINFO.PWINFO_TIPAMOUNT.value, "00")
        
        
        
        
        ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
        
        while ret == -2497 or ret == E_PWRET.PWRET_NOTHING.value:
            #ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
            ret = self.pgWeb.PW_iExecGetData(vstParam, iNumParam)
            print("ret exectransac venda", ret)
            
            
            if ret == E_PWRET.PWRET_CANCEL.value:
                print("E_PWRET.PWRET_CANCEL")
                self.pgWeb.PW_iPPAbort()
                retEventLoop = self.pgWeb.PW_iPPEventLoop(
                    self.szDspMsg, sizeof(self.szDspMsg))
                print("retEventLoop", retEventLoop)
                return retEventLoop
            elif ret == E_PWRET.PWRET_HOSTTIMEOUT.value:
                self.pgWeb.PW_iPPAbort()
                retEventLoop = self.pgWeb.PW_iPPEventLoop(
                    self.szDspMsg, sizeof(self.szDspMsg))
                print("retEventLoop", retEventLoop)
                return retEventLoop
            elif ret == E_PWRET.PWRET_REQPARAM.value:
                print("PWRET_REQPARAM", E_PWRET.PWRET_REQPARAM.value)
                self.pgWeb.PW_iPPAbort()
                retEventLoop = self.pgWeb.PW_iPPEventLoop(
                    self.szDspMsg, sizeof(self.szDspMsg))
                print("retEventLoop", retEventLoop)
                return retEventLoop
            elif ret == E_PWRET.PWRET_FROMHOSTPENDTRN.value:
                print("PWRET_FROMHOSTPENDTRN", E_PWRET.PWRET_FROMHOSTPENDTRN.value)
                self.confirmPendTransaction(transactionStatus=1, transactionResponse=ret)
                retEventLoop = self.pgWeb.PW_iPPEventLoop(
                    self.szDspMsg, sizeof(self.szDspMsg))
                print("retEventLoop", retEventLoop)
                return retEventLoop
            ret = self.pgWeb.PW_iExecTransac(vstParam, iNumParam)
            print("efetuando a transacao...")
            print("ret ---->", ret)
        

        
        PWINFO_REQNUM = PWINFO_AUTLOCREF = PWINFO_AUTEXTREF = PWINFO_VIRTMERCH = PWINFO_AUTHSYST = ''
        data = datetime.datetime.now()
        self.pgWeb.PW_iGetResult(
                    E_PWINFO.PWINFO_REQNUM.value, szAux, sizeof(szAux))
        PWINFO_REQNUM = szAux.value.decode('utf-8')
        print("PWINFO_REQNUM", PWINFO_REQNUM)
        sleep(0.3)
        self.pgWeb.PW_iGetResult(
                    E_PWINFO.PWINFO_AUTLOCREF.value, szAux, sizeof(szAux))
        PWINFO_AUTLOCREF = szAux.value.decode('utf-8')
        print("PWINFO_AUTLOCREF", PWINFO_AUTLOCREF)
        sleep(0.3)
        self.pgWeb.PW_iGetResult(
                    E_PWINFO.PWINFO_AUTEXTREF.value, szAux, sizeof(szAux))
        PWINFO_AUTEXTREF = szAux.value.decode('utf-8')
        print("PWINFO_AUTEXTREF", PWINFO_AUTEXTREF)
        if PWINFO_AUTEXTREF == None or PWINFO_AUTEXTREF == '':
            PWINFO_AUTEXTREF = '0'
        sleep(0.3)
        self.pgWeb.PW_iGetResult(
                    E_PWINFO.PWINFO_VIRTMERCH.value, szAux, sizeof(szAux))
        PWINFO_VIRTMERCH = szAux.value.decode('utf-8')
        print("PWINFO_VIRTMERCH", PWINFO_VIRTMERCH)
        sleep(0.3)
        self.pgWeb.PW_iGetResult(
                    E_PWINFO.PWINFO_AUTHSYST.value, szAux, sizeof(szAux))
        PWINFO_AUTHSYST = szAux.value.decode('utf-8')
        print("PWINFO_AUTHSYST", PWINFO_AUTHSYST)
        sleep(0.3)
        self.pgWeb.PW_iGetResult(
            E_PWINFO.PWINFO_RCPTMERCH.value, szAux, sizeof(szAux))
        print("PWINFO_RCPTMERCH", E_PWINFO.PWINFO_RCPTMERCH.value)
        COMPROVANTE = szAux.value.decode('utf-8')
        print("result transacao nota")
        f = open('comprovantes/COMPROVANTE N. %s:%s-%s-%s %s:%s:%s.txt'%(PWINFO_REQNUM, data.day, data.month, data.year, data.hour, data.minute, data.second),'w+')
        f.write(COMPROVANTE)
        f.close()

        sleep(0.3)
            
        iRet = self.pgWeb.PW_iConfirmation(
            E_PWCNF.PWCNF_CNF_AUTO.value,
            PWINFO_REQNUM,
            PWINFO_AUTLOCREF,
            PWINFO_AUTEXTREF,
            PWINFO_VIRTMERCH,
            PWINFO_AUTHSYST
        )
        print("iRet PW_iConfirmation", iRet)
        return iRet
    
            
                
        

if __name__ == "__main__":
    Venda()